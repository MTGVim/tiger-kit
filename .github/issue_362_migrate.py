from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

ROOT = Path.cwd()


def rewrite(path: str, old: str, new: str, *, required: bool = True) -> None:
    target = ROOT / path
    text = target.read_text(encoding="utf-8")
    if required and old not in text:
        raise RuntimeError(f"missing expected text in {path}: {old[:120]!r}")
    target.write_text(text.replace(old, new), encoding="utf-8")


def replace_regex(path: str, pattern: str, replacement: str) -> None:
    target = ROOT / path
    text = target.read_text(encoding="utf-8")
    updated, count = re.subn(pattern, replacement, text, flags=re.MULTILINE)
    if count == 0:
        raise RuntimeError(f"pattern did not match in {path}: {pattern}")
    target.write_text(updated, encoding="utf-8")


# 1. Physically separate authoring evals from runtime skill packages.
evals_root = ROOT / "evals" / "skills"
evals_root.mkdir(parents=True, exist_ok=True)
skill_names: list[str] = []
for skill_dir in sorted((ROOT / "skills").glob("tk-*")):
    if not (skill_dir / "SKILL.md").is_file():
        continue
    name = skill_dir.name
    skill_names.append(name)
    source = skill_dir / "evals"
    destination = evals_root / name
    if not source.is_dir():
        raise RuntimeError(f"missing source eval directory: {source}")
    if destination.exists():
        raise RuntimeError(f"destination already exists: {destination}")
    shutil.move(str(source), str(destination))

    behavior_path = destination / "evals.json"
    behavior = json.loads(behavior_path.read_text(encoding="utf-8"))
    for case in behavior.get("evals", []):
        files = case.get("files")
        if isinstance(files, list):
            case["files"] = [
                item.replace("evals/fixtures/", "fixtures/") if isinstance(item, str) else item
                for item in files
            ]

        def migrate_strings(value):
            if isinstance(value, str):
                value = value.replace(
                    f"skills/{name}/evals/fixtures/",
                    f"evals/skills/{name}/fixtures/",
                )
                return value.replace("evals/fixtures/", f"evals/skills/{name}/fixtures/")
            if isinstance(value, list):
                return [migrate_strings(item) for item in value]
            if isinstance(value, dict):
                return {
                    key: (child if key == "files" else migrate_strings(child))
                    for key, child in value.items()
                }
            return value

        migrated = migrate_strings(case)
        case.clear()
        case.update(migrated)
    behavior_path.write_text(
        json.dumps(behavior, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


# 2. Eval execution consumes the repository-only canonical path. The legacy path is
# accepted only when explicitly loading a historical baseline across this migration.
rewrite(
    "scripts/run_skill_evals.py",
    '''def load_eval_contracts(root: Path, selected: set[str] | None) -> dict[str, dict[str, object]]:\n    contracts: dict[str, dict[str, object]] = {}\n''',
    '''def eval_dir_for(\n    root: Path, skill_name: str, *, allow_legacy_skill_local: bool = False\n) -> Path:\n    canonical = root / "evals" / "skills" / skill_name\n    if canonical.is_dir() or not allow_legacy_skill_local:\n        return canonical\n    return root / "skills" / skill_name / "evals"\n\n\ndef load_eval_contracts(\n    root: Path,\n    selected: set[str] | None,\n    *,\n    allow_legacy_skill_local: bool = False,\n) -> dict[str, dict[str, object]]:\n    contracts: dict[str, dict[str, object]] = {}\n''',
)
rewrite(
    "scripts/run_skill_evals.py",
    '''        triggers = json.loads((skill_dir / "evals" / "triggers.json").read_text(encoding="utf-8"))\n        behavior = json.loads((skill_dir / "evals" / "evals.json").read_text(encoding="utf-8"))\n        contracts[skill_dir.name] = {"triggers": triggers, "behavior": behavior}\n''',
    '''        eval_dir = eval_dir_for(\n            root,\n            skill_dir.name,\n            allow_legacy_skill_local=allow_legacy_skill_local,\n        )\n        triggers = json.loads((eval_dir / "triggers.json").read_text(encoding="utf-8"))\n        behavior = json.loads((eval_dir / "evals.json").read_text(encoding="utf-8"))\n        contracts[skill_dir.name] = {"triggers": triggers, "behavior": behavior}\n''',
)
rewrite(
    "scripts/run_skill_evals.py",
    "baseline_contracts = load_eval_contracts(baseline_root, selected)\n            candidate_contracts = load_eval_contracts(candidate_root, selected)",
    "baseline_contracts = load_eval_contracts(\n                baseline_root, selected, allow_legacy_skill_local=True\n            )\n            candidate_contracts = load_eval_contracts(candidate_root, selected)",
)


# 3. Validation resolves contracts from evals/skills and checks distribution separation.
rewrite(
    "scripts/validate_skills.py",
    '"""Validate TigerKit Agent Skills from skill-local canonical contracts."""',
    '"""Validate TigerKit Agent Skills and repository-owned eval contracts."""',
)
rewrite(
    "scripts/validate_skills.py",
    'ROOT = Path(__file__).resolve().parents[1]\n\n\ndef _display_path',
    '''ROOT = Path(__file__).resolve().parents[1]\n\n\ndef eval_dir_for(name: str, root: Path | None = None) -> Path:\n    return (ROOT if root is None else root) / "evals" / "skills" / name\n\n\ndef _display_path''',
)
rewrite(
    "scripts/validate_skills.py",
    '(path.parent.parent / relative).is_file()',
    '(path.parent / relative).is_file()',
)
rewrite(
    "scripts/validate_skills.py",
    '''    for owner, (skill_dir, _, _) in skills.items():\n        try:\n            cases = json.loads((skill_dir / "evals/evals.json").read_text(encoding="utf-8")).get("evals", [])\n        except (OSError, UnicodeError, json.JSONDecodeError, AttributeError):\n            continue\n''',
    '''    for owner, (skill_dir, _, _) in skills.items():\n        eval_path = eval_dir_for(owner) / "evals.json"\n        try:\n            cases = json.loads(eval_path.read_text(encoding="utf-8")).get("evals", [])\n        except (OSError, UnicodeError, json.JSONDecodeError, AttributeError):\n            continue\n''',
)
rewrite(
    "scripts/validate_skills.py",
    'f"{_display_path(skill_dir / \'evals/evals.json\')}: case {case.get(\'id\')} "',
    'f"{_display_path(eval_path)}: case {case.get(\'id\')} "',
)
rewrite(
    "scripts/validate_skills.py",
    '''        trigger_path = skill_dir / "evals/triggers.json"\n        behavior_path = skill_dir / "evals/evals.json"\n''',
    '''        eval_dir = eval_dir_for(name)\n        trigger_path = eval_dir / "triggers.json"\n        behavior_path = eval_dir / "evals.json"\n''',
)
rewrite(
    "scripts/validate_skills.py",
    'directory.name in {"references", "scripts", "agents", "evals"}',
    'directory.name in {"references", "scripts", "agents"}',
)
rewrite(
    "scripts/validate_skills.py",
    '''    obsolete = [\n        "scripts/sync_eval_compat.py",\n''',
    '''    eval_root = ROOT / "evals" / "skills"\n    if not eval_root.is_dir():\n        errors.append("evals/skills: canonical per-skill eval root is missing")\n    else:\n        eval_names = {path.name for path in eval_root.glob("tk-*") if path.is_dir()}\n        missing_evals = sorted(skill_names - eval_names)\n        stale_evals = sorted(eval_names - skill_names)\n        if missing_evals:\n            errors.append("evals/skills: missing contracts for " + ", ".join(missing_evals))\n        if stale_evals:\n            errors.append("evals/skills: stale contracts for " + ", ".join(stale_evals))\n    for name in sorted(skill_names):\n        runtime_evals = SKILLS / name / "evals"\n        if runtime_evals.exists():\n            errors.append(\n                f"{runtime_evals.relative_to(ROOT)}: authoring evals must stay outside runtime skill packages"\n            )\n\n    obsolete = [\n        "scripts/sync_eval_compat.py",\n''',
)
rewrite(
    "scripts/validate_skills.py",
    'print("Validated skill-local trigger/behavior SSOT and catalog routing contracts.")',
    'print("Validated repository-owned trigger/behavior SSOT and catalog routing contracts.")',
)


# 4. Catalog audit uses the same canonical eval directory.
rewrite(
    "scripts/audit_catalog.py",
    '"""Audit the TigerKit catalog from canonical skill-local contracts."""',
    '"""Audit the TigerKit catalog from repository-owned eval contracts."""',
)
rewrite(
    "scripts/audit_catalog.py",
    '''def positive_trigger_count(skill_dir: Path) -> int:\n    value = json.loads((skill_dir / "evals/triggers.json").read_text(encoding="utf-8"))\n''',
    '''def positive_trigger_count(eval_dir: Path) -> int:\n    value = json.loads((eval_dir / "triggers.json").read_text(encoding="utf-8"))\n''',
)
rewrite(
    "scripts/audit_catalog.py",
    '''def behavior_paths(skill_dir: Path) -> set[str]:\n    value = json.loads((skill_dir / "evals/evals.json").read_text(encoding="utf-8"))\n''',
    '''def behavior_paths(eval_dir: Path) -> set[str]:\n    value = json.loads((eval_dir / "evals.json").read_text(encoding="utf-8"))\n''',
)
rewrite(
    "scripts/audit_catalog.py",
    '''        triggers = positive_trigger_count(skill_dir)\n        paths = behavior_paths(skill_dir)\n''',
    '''        eval_dir = validate_skills.eval_dir_for(name)\n        triggers = positive_trigger_count(eval_dir)\n        paths = behavior_paths(eval_dir)\n''',
)


# 5. Release gate scans new paths, normalizes the one-time path migration when comparing
# language baselines, and verifies an actual pinned CLI consumer install.
rewrite(
    "scripts/run_release_gate.py",
    'import subprocess\nfrom pathlib import Path',
    'import subprocess\nimport tempfile\nfrom pathlib import Path',
)
rewrite(
    "scripts/run_release_gate.py",
    'paths.extend(sorted(root.glob("skills/tk-*/evals/*.json")))',
    'paths.extend(sorted(root.glob("evals/skills/tk-*/*.json")))',
)
rewrite(
    "scripts/run_release_gate.py",
    '''def compare_language_regression(\n    baseline: Mapping[str, object], candidate: Mapping[str, object]\n) -> list[str]:\n''',
    '''def _canonical_language_identity(value: str) -> str:\n    return re.sub(\n        r"skills/(tk-[a-z0-9-]+)/evals/(triggers|evals)\\.json",\n        r"evals/skills/\\1/\\2.json",\n        value,\n    )\n\n\ndef compare_language_regression(\n    baseline: Mapping[str, object], candidate: Mapping[str, object]\n) -> list[str]:\n''',
)
rewrite(
    "scripts/run_release_gate.py",
    'str(row.get("fingerprint"))\n        for row in baseline_rows',
    '_canonical_language_identity(str(row.get("fingerprint")))\n        for row in baseline_rows',
)
rewrite(
    "scripts/run_release_gate.py",
    'str(row.get("fingerprint"))\n        for row in candidate_rows',
    '_canonical_language_identity(str(row.get("fingerprint")))\n        for row in candidate_rows',
)
rewrite(
    "scripts/run_release_gate.py",
    'location = str(row.get("location", "")).split(":", 1)[0]',
    'location = _canonical_language_identity(str(row.get("location", ""))).split(":", 1)[0]',
)
rewrite(
    "scripts/run_release_gate.py",
    'baseline_contracts = load_eval_contracts(baseline_root, None)\n        candidate_contracts = load_eval_contracts(candidate_root, None)',
    'baseline_contracts = load_eval_contracts(\n            baseline_root, None, allow_legacy_skill_local=True\n        )\n        candidate_contracts = load_eval_contracts(candidate_root, None)',
)

release_path = ROOT / "scripts/run_release_gate.py"
release_text = release_path.read_text(encoding="utf-8")
marker = "\ndef parse_args() -> argparse.Namespace:\n"
if marker not in release_text:
    raise RuntimeError("release gate insertion marker missing")
consumer_helpers = r'''

def consumer_install_errors(
    source_root: Path, installed_skills: Mapping[str, Path]
) -> list[str]:
    errors: list[str] = []
    expected = {
        source.name: source
        for source in sorted((source_root / "skills").glob("tk-*"))
        if (source / "SKILL.md").is_file()
    }
    missing = sorted(set(expected) - set(installed_skills))
    if missing:
        errors.append("consumer install is missing skills: " + ", ".join(missing))
    for name, source in expected.items():
        installed = installed_skills.get(name)
        if installed is None:
            continue
        if not (installed / "SKILL.md").is_file():
            errors.append(f"{name}: installed package is missing SKILL.md")
            continue
        for optional in ("references", "scripts", "agents"):
            if (source / optional).is_dir() and not (installed / optional).is_dir():
                errors.append(f"{name}: installed package is missing {optional}/")
        if (installed / "evals").exists():
            errors.append(f"{name}: installed package contains authoring evals/")
        leaked = [
            path.relative_to(installed)
            for path in installed.rglob("*")
            if path.is_file() and path.name in {"triggers.json", "evals.json"}
        ]
        if leaked:
            errors.append(
                f"{name}: installed package contains authoring eval files: "
                + ", ".join(str(path) for path in leaked)
            )
    return errors


def run_consumer_install(candidate_root: Path) -> dict[str, object]:
    with tempfile.TemporaryDirectory(prefix="tigerkit-consumer-install-") as directory:
        consumer = Path(directory)
        record = run_checked(
            [
                "npx",
                "--yes",
                "skills@1.5.9",
                "add",
                str(candidate_root.resolve()),
                "--agent",
                "codex",
                "--copy",
                "--yes",
            ],
            cwd=consumer,
        )
        errors: list[str] = []
        if bool(record["passed"]):
            installed_skills: dict[str, Path] = {}
            for skill_file in consumer.rglob("SKILL.md"):
                if "node_modules" in skill_file.parts:
                    continue
                directory_path = skill_file.parent
                if directory_path.name.startswith("tk-"):
                    installed_skills.setdefault(directory_path.name, directory_path)
            errors.extend(consumer_install_errors(candidate_root, installed_skills))
        record["consumer_errors"] = errors
        if errors:
            record["passed"] = False
        return record
'''
release_path.write_text(
    release_text.replace(marker, consumer_helpers + marker), encoding="utf-8"
)
rewrite(
    "scripts/run_release_gate.py",
    '''        for command in commands:\n            static_records.append(run_checked(command, cwd=candidate_root))\n''',
    '''        for command in commands:\n            static_records.append(run_checked(command, cwd=candidate_root))\n        static_records.append(run_consumer_install(candidate_root))\n''',
)


# 6. Focused tests follow the new repository layout and cover the distribution boundary.
audit_test = ROOT / "scripts/test_audit_catalog.py"
text = audit_test.read_text(encoding="utf-8")
text = text.replace(
    '''            skill = Path(directory)\n            (skill / "evals").mkdir()\n            (skill / "evals/triggers.json").write_text(''',
    '''            eval_dir = Path(directory)\n            (eval_dir / "triggers.json").write_text(''',
).replace(
    "audit_catalog.positive_trigger_count(skill)",
    "audit_catalog.positive_trigger_count(eval_dir)",
).replace(
    '''            skill = Path(directory)\n            (skill / "evals").mkdir()\n            (skill / "evals/evals.json").write_text(''',
    '''            eval_dir = Path(directory)\n            (eval_dir / "evals.json").write_text(''',
).replace(
    "audit_catalog.behavior_paths(skill)",
    "audit_catalog.behavior_paths(eval_dir)",
)
audit_test.write_text(text, encoding="utf-8")

validate_test = ROOT / "scripts/test_validate_skills.py"
text = validate_test.read_text(encoding="utf-8")
text = text.replace(
    'skill_dir / "evals/evals.json"',
    'validate_skills.eval_dir_for(name) / "evals.json"',
)
text = text.replace(
    '''            parent = root / "tk-parent"\n            child = root / "tk-child"\n            (parent / "evals").mkdir(parents=True)\n            child.mkdir()\n            (parent / "evals/evals.json").write_text(''',
    '''            parent = root / "tk-parent"\n            child = root / "tk-child"\n            eval_dir = root / "evals/skills/tk-parent"\n            eval_dir.mkdir(parents=True)\n            child.mkdir()\n            (eval_dir / "evals.json").write_text(''',
)
text = text.replace(
    '''            errors = validate_skills.validate_invocation_graph(skills)\n            self.assertTrue(any("cannot invoke user-invoked skill tk-child" in error for error in errors))''',
    '''            with patch.object(validate_skills, "ROOT", root):\n                errors = validate_skills.validate_invocation_graph(skills)\n            self.assertTrue(any("cannot invoke user-invoked skill tk-child" in error for error in errors))''',
)
validate_test.write_text(text, encoding="utf-8")

release_test = ROOT / "scripts/test_run_release_gate.py"
text = release_test.read_text(encoding="utf-8")
text = text.replace(
    'evals = root / "skills/tk-example/evals"',
    'evals = root / "evals/skills/tk-example"',
)
# Keep one old-path baseline and one new-path candidate to prove language path migration
# itself does not become a false regression.
text = text.replace(
    '"fingerprint": "skills/tk-example/evals/evals.json.evals[].prompt|English prose",\n                    "location": "skills/tk-example/evals/evals.json.evals[4].prompt:1",',
    '"fingerprint": "evals/skills/tk-example/evals.json.evals[].prompt|English prose",\n                    "location": "evals/skills/tk-example/evals.json.evals[4].prompt:1",',
)
insertion = r'''
    def test_consumer_install_verification_keeps_runtime_files_and_rejects_evals(self) -> None:
        with tempfile.TemporaryDirectory() as source_directory, tempfile.TemporaryDirectory() as installed_directory:
            source_root = Path(source_directory)
            installed_root = Path(installed_directory)
            source = source_root / "skills/tk-example"
            installed = installed_root / "tk-example"
            for root in (source, installed):
                root.mkdir(parents=True)
                (root / "SKILL.md").write_text("skill\n", encoding="utf-8")
                for optional in ("references", "scripts", "agents"):
                    (root / optional).mkdir()
                    (root / optional / "keep.txt").write_text("keep\n", encoding="utf-8")
            self.assertEqual(
                run_release_gate.consumer_install_errors(
                    source_root, {"tk-example": installed}
                ),
                [],
            )
            (installed / "evals").mkdir()
            (installed / "evals/evals.json").write_text("{}\n", encoding="utf-8")
            errors = run_release_gate.consumer_install_errors(
                source_root, {"tk-example": installed}
            )
            self.assertTrue(any("authoring evals" in error for error in errors))
'''
text = text.replace(
    '\n\nif __name__ == "__main__":\n',
    '\n' + insertion + '\n\nif __name__ == "__main__":\n',
)
release_test.write_text(text, encoding="utf-8")

run_skill_test = ROOT / "scripts/test_run_skill_evals.py"
text = run_skill_test.read_text(encoding="utf-8")
for name in skill_names:
    text = text.replace(
        f'root / "skills/{name}/evals/evals.json"',
        f'root / "evals/skills/{name}/evals.json"',
    )
    text = text.replace(
        f'ROOT / "skills/{name}/evals/evals.json"',
        f'ROOT / "evals/skills/{name}/evals.json"',
    )
run_skill_test.write_text(text, encoding="utf-8")

# Add explicit loader migration coverage.
loader_test = '''\n    def test_eval_loader_requires_canonical_path_unless_legacy_is_explicit(self) -> None:\n        with tempfile.TemporaryDirectory() as directory:\n            root = Path(directory)\n            skill = root / "skills/tk-example"\n            legacy = skill / "evals"\n            legacy.mkdir(parents=True)\n            (skill / "SKILL.md").write_text("skill\\n", encoding="utf-8")\n            (legacy / "triggers.json").write_text(\n                '{"skill":"tk-example","kind":"user-invoked","queries":[]}',\n                encoding="utf-8",\n            )\n            (legacy / "evals.json").write_text(\n                '{"skill_name":"tk-example","evals":[]}', encoding="utf-8"\n            )\n            with self.assertRaises(FileNotFoundError):\n                run_skill_evals.load_eval_contracts(root, {"tk-example"})\n            loaded = run_skill_evals.load_eval_contracts(\n                root, {"tk-example"}, allow_legacy_skill_local=True\n            )\n            self.assertIn("tk-example", loaded)\n'''
if "class " in text and "if __name__" in text:
    text = text.replace('\n\nif __name__ == "__main__":', loader_test + '\n\nif __name__ == "__main__":')
run_skill_test.write_text(text, encoding="utf-8")


# 7. Documentation states the repository-only source of truth.
for path in ("README.md", "AGENTS.md"):
    target = ROOT / path
    text = target.read_text(encoding="utf-8")
    text = text.replace(
        "skills/<skill>/evals/triggers.json", "evals/skills/<skill>/triggers.json"
    ).replace(
        "skills/<skill>/evals/evals.json", "evals/skills/<skill>/evals.json"
    )
    target.write_text(text, encoding="utf-8")

agents = ROOT / "AGENTS.md"
text = agents.read_text(encoding="utf-8")
text = text.replace(
    "- `package-local` `scripts/`는 `executable helper`를, `agents/`와 `evals/`는 실행·검증 `evidence`를 소유합니다.",
    "- `package-local` `scripts/`는 `executable helper`를, `agents/`는 실행 메타데이터를 소유합니다. 검증용 `eval`은 `evals/skills/<skill>/`에서 저장소 전용 증거를 소유합니다.",
)
agents.write_text(text, encoding="utf-8")

migration = ROOT / "MIGRATION.md"
text = migration.read_text(encoding="utf-8").replace(
    "3. `skill-local` `eval` + `evals/catalog-routing.json`",
    "3. `evals/skills/<skill>/`의 저장소 전용 `eval` + `evals/catalog-routing.json`",
)
migration.write_text(text, encoding="utf-8")


# 8. Fail the staging run if canonical path assumptions remain in code/docs.
stale: list[str] = []
for path in [
    ROOT / "README.md",
    ROOT / "AGENTS.md",
    ROOT / "MIGRATION.md",
    *sorted((ROOT / "scripts").glob("*.py")),
]:
    content = path.read_text(encoding="utf-8")
    if 'skill_dir / "evals' in content or "skills/<skill>/evals" in content:
        stale.append(str(path.relative_to(ROOT)))
if stale:
    raise RuntimeError("stale canonical eval path assumptions remain: " + ", ".join(stale))

runtime_eval_dirs = sorted((ROOT / "skills").glob("tk-*/evals"))
if runtime_eval_dirs:
    raise RuntimeError(
        "runtime eval directories remain: "
        + ", ".join(str(path.relative_to(ROOT)) for path in runtime_eval_dirs)
    )
