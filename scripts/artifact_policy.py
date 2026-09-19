"""Canonical installed artifact guard and repository-tool path allocation."""
from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_MARKER = '<!-- tigerkit:artifact-paths -->'
ARTIFACT_BLOCK = '''<!-- tigerkit:artifact-paths -->
## Artifact Paths

Default repository-owned output to `.tigerkit/`: transient files in `tmp/<skill>/<run-id>/`, verification evidence in `evidence/<skill>/<run-id>/`, explanations in `explanations/`, and lessons in `study/<topic>/`. Preserve existing owner-specific paths and explicit user-selected final destinations. This policy grants no new write authority or mandatory artifact. Before using `.tigerkit/`, verify the repository root, no tracked files under it, and effective Git ignore coverage. Reject symlink escapes; preserve unrelated existing files. If unsafe or no repository is identified, stop the file branch as `Blocked | Unverifiable`, without editing ignore rules or falling back to OS temp. Atomic replacement may use a run-owned sibling temporary file on the destination filesystem; clean it after success. External tool caches and isolated test fixtures retain their tool-owned lifecycle.
'''


def checked_artifact_root(root: Path = ROOT) -> Path:
    root = root.resolve()
    top = subprocess.run(['git', 'rev-parse', '--show-toplevel'], cwd=root, text=True, capture_output=True, check=True)
    if Path(top.stdout.strip()).resolve() != root:
        raise ValueError('artifact root must be the repository root')
    target = root / '.tigerkit'
    if target.is_symlink() or target.resolve() != target:
        raise ValueError('artifact path must not escape through a symlink')
    tracked = subprocess.run(['git', 'ls-files', '--', '.tigerkit/'], cwd=root, text=True, capture_output=True, check=True)
    ignored = subprocess.run(['git', 'check-ignore', '-q', '--', '.tigerkit/'], cwd=root)
    if tracked.stdout.strip() or ignored.returncode != 0:
        raise ValueError('.tigerkit must be untracked and effectively ignored')
    return target


def artifact_directory(relative: str, root: Path = ROOT) -> Path:
    base = checked_artifact_root(root)
    target = base / relative
    if not target.resolve().is_relative_to(base) or any(p.is_symlink() for p in [target, *target.parents] if p.is_relative_to(base)):
        raise ValueError('artifact path escapes .tigerkit')
    target.mkdir(parents=True, exist_ok=True)
    return target


def scratch_directory(owner: str, root: Path = ROOT):
    return tempfile.TemporaryDirectory(prefix='run-', dir=artifact_directory(f'tmp/{owner}', root))


def output_directory(value: str | None, owner: str, root: Path = ROOT) -> Path:
    if value is None:
        base = artifact_directory(f'evidence/{owner}', root)
        return Path(tempfile.mkdtemp(prefix='run-', dir=base))
    target = Path(value).absolute()
    # Explicit final paths are allowed; repository-local ones must remain ignored artifacts.
    if target.is_relative_to(root.resolve()):
        base = checked_artifact_root(root)
        if not target.is_relative_to(base):
            raise ValueError('--output must be outside the repository or under ignored .tigerkit/')
        target = artifact_directory(str(target.relative_to(base)), root)
    if target.is_symlink() or target.resolve() != target:
        raise ValueError('output must not traverse a symlink')
    if target.exists() and any(target.iterdir()):
        raise ValueError('output directory must be new or empty; preserve existing results')
    target.mkdir(parents=True, exist_ok=True)
    return target


def validate_artifact_guards(root: Path = ROOT) -> list[str]:
    errors = []
    for path in sorted((root / 'skills').glob('tk-*/SKILL.md')):
        text = path.read_text(encoding='utf-8')
        if text.count(ARTIFACT_BLOCK) != 1 or text.count(ARTIFACT_MARKER) != 1:
            errors.append(f'{path.relative_to(root)}: artifact guard must match exactly once')
    return errors
