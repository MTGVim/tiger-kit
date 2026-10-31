# Dependency Planner CLI

Requires Python 3.9+. Reading any source or installed `SKILL.md` additionally requires PyYAML
(verified with 6.0.3); missing parser support is a hard stop, never a successful package check.
A bundled-catalog plan for an empty destination needs only the standard library. Before an approved
installation, verify parser availability in the Python environment that will perform the post-install
check. Any environment/package provisioning needs its own applicable approval; this helper never
installs a parser or falls back to regex-based YAML validation.
Execute the installed package's `scripts/skill_dependencies.py`;
repository maintainers may use the public shim `scripts/skill_dependencies.py` at the repository root.
The examples use that repository shim. Replace all example values with verified user choices.

## Read-only Commands

```sh
python3 scripts/skill_dependencies.py validate --root /absolute/trusted/checkout
python3 scripts/skill_dependencies.py validate --root /absolute/trusted/checkout --catalog skills/tk-setup-skills/references/install-catalog.json
python3 scripts/skill_dependencies.py plan --skill tk-review tk-prep --source owner/repository --target /absolute/project --agent codex --scope project
python3 scripts/skill_dependencies.py plan --root /absolute/trusted/checkout --skill tk-review --source /absolute/trusted/checkout --target /absolute/project --agent claude-code --scope project
python3 scripts/skill_dependencies.py check --installed-root /absolute/project/.agents/skills --skill tk-review
```

`plan` defaults to the catalog bundled beside its implementation; `--root` instead validates current
repository declarations. `--catalog <path>` explicitly selects another trusted metadata catalog.
`--skill` takes one or more exact IDs, not globs or paths. Output is deterministic JSON.
`validate` returns exit 1 with `errors` for invalid source declarations; an optional catalog comparison
rejects stale metadata. `check` walks only the selected installed closure and stops for missing dependencies.
CLI usage errors return 2; validation/planning failures return 1 without a traceback. No command falls back
to an installation, source fetch, or config repair. No-argument invocation prints usage without mutation.

The repository API `validate_dependencies(root: Path) -> list[str]` validates source declarations without
requiring a generated catalog. It returns actionable errors for missing/malformed declarations rather than
raising them. Each package owns exactly `dependencies.json` with `{"version":1,"requires":["tk-..."]}`.
Directory basename and the single plain/quoted `name:` frontmatter value in `SKILL.md` must match exactly.
JSON duplicate keys, duplicate edges, unknown IDs, malformed schemas, traversal and symlinks are rejected.
Cycles and shared dependencies are valid; the closure includes each package once in sorted order.

The trusted installed implementation also exports `read_package(base: Path, name: str) -> list[str]`.
It validates one exact package's metadata, declaration and symlink boundaries, returning its direct
requirements; it does not validate the whole installed closure or authorize installation. The gallery
and legacy report helpers load this explicit same-collection file with `runpy.run_path` (no installed
bytecode writes) before using `tk-writing`. They declare the setup package as a direct dependency and
need PyYAML in their executing Python environment. Parser loading remains lazy; empty-target catalog
planning still requires only the standard library. This API is not a code-authenticity attestation.

## Exact Destination and Installer Guidance

Supported pinned `skills@1.7.4` agent IDs are `codex`, `claude-code`, and `hermes-agent`.
Project target means the existing absolute project directory (installer `cwd`), not an arbitrary skill
folder. Their respective project sibling roots are `.agents/skills`, `.claude/skills`, `.hermes/skills`.
For explicit `global` scope, target must be the current absolute HOME; the same relative roots apply.
Global environment overrides (`CODEX_HOME`, `CLAUDE_CONFIG_DIR`, `HERMES_HOME`) are rejected for manual
host-specific guidance, not rewritten. Resolve operating-system directory aliases first; symlinked roots,
package files and destination boundaries are unsupported, including dangling symlinks.
Other agents or arbitrary destinations need fresh installer evidence and manual guidance, not guessed flags.

`plan` inspects only the selected closure at the exact destination. Compatible existing packages appear
in `present`; only `missing` appears in installer `--skill` arguments. Incompatible declarations or unsafe
paths stop the plan. If nothing is missing, `argv` is empty. Existing declarations do not attest content
freshness, source revision or authenticity. Validate those separately before continuing the owning workflow.

Installer argv is an array, with `cwd` and `installed_root` emitted separately. It uses pinned
`npx --yes skills@1.7.4 add SOURCE --skill ID... --agent AGENT --copy`, with `--global` only when explicit.
The early npx `--yes` permits package resolution only; installer `--yes` is deliberately absent so overwrite
prompts are not suppressed. `--copy` avoids using symlinks as the distribution contract. Installer help and
agent paths were checked against locally cached 1.7.4 source/help; do not claim arbitrary versions work.
Npx may fetch code and the installer may fetch source, create lock metadata and install files if a human
later executes it. Planning itself does none of these. Never pass a concatenated string through a shell.
Shell metacharacters in source remain one literal argv entry; option-like/control-text sources are rejected.
Immediately before an approved install, recheck source trust, exact destination, relevant existing content,
and the pinned installer's current behavior. Do not execute a stale plan or override overwrite prompts.

## Maintainer-only Catalog Generation

```sh
python3 scripts/skill_dependencies.py build-catalog --root /absolute/trusted/checkout
python3 scripts/skill_dependencies.py build-catalog --root /absolute/trusted/checkout --output skills/tk-setup-skills/references/install-catalog.json
```

Without `--output`, generation prints metadata only. An explicit output is the sole file-writing command;
its parent must exist and it may not cross a symlink boundary. Regenerate only in an approved source checkout,
never as automatic runtime repair. Validate the generated catalog against the same source declarations.
The catalog contains exact IDs and dependency edges, no copies of skill/reference content and no network URL
or inferred source authority. Choose a trusted source/revision compatible with the bundled catalog explicitly.
