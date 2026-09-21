"""Canonical installed artifact guard and repository-tool path allocation."""
from __future__ import annotations

import os
import stat
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_MARKER = '<!-- tigerkit:artifact-paths -->'
ARTIFACT_BLOCK = '''<!-- tigerkit:artifact-paths -->
## Artifact Paths

Default repository-owned output to `.tigerkit/`: transient files in `tmp/<skill>/<run-id>/`, verification evidence in `evidence/<skill>/<run-id>/`, explanations in `explanations/`, and lessons in `study/<topic>/`. Preserve existing owner-specific paths and explicit user-selected final destinations. Create artifacts only when the active task calls for them. Before writing, verify the repository root, no tracked `.tigerkit` paths, and safe nonsymlink destinations. From the repository root, run `git ls-files -- .tigerkit .tigerkit/` to check tracking, then `git check-ignore -q -- .tigerkit/` to check effective exclusion. Exit 0 means leave ignore files unchanged, including when exclusion comes from `core.excludesFile` (such as configured `~/.gitignore`), the default global ignore file, or `.git/info/exclude`; a missing repository `.gitignore` or missing literal entry is not evidence of missing coverage. Only exit 1 permits creating the root `.gitignore` or appending `/.tigerkit/`, preserving existing bytes and line endings, then rerunning the same check before writing. Any other exit status or command failure blocks the file branch without an ignore edit. Use `git check-ignore -v -- .tigerkit/` only to diagnose the source; a printed negated pattern is not proof of exclusion. This narrow ignore setup is part of an authorized artifact write even for a read-only task; it grants no other source/config/index/commit/publication authority. Existing effective ignore rules need no edit. Do not untrack files or follow a symlinked/nonregular `.gitignore`; if unsafe, unwritable, still unignored, or no repository is identified, stop only the file branch as `Blocked | Unverifiable`, without an OS-temp fallback. Briefly report an ignore edit; never stage or commit it solely for setup. Atomic replacement may use a run-owned sibling temporary file on the destination filesystem; clean it after success. External tool caches and isolated test fixtures retain their tool-owned lifecycle.
'''


def checked_artifact_root(root: Path = ROOT) -> Path:
    root = root.resolve()
    top = subprocess.run(['git', 'rev-parse', '--show-toplevel'], cwd=root, text=True, capture_output=True, check=True)
    if Path(top.stdout.strip()).resolve() != root:
        raise ValueError('artifact root must be the repository root')
    target = root / '.tigerkit'
    if target.is_symlink() or target.resolve() != target:
        raise ValueError('artifact path must not escape through a symlink')
    if target.exists() and not target.is_dir():
        raise ValueError('artifact root must be a directory')
    tracked = subprocess.run(['git', 'ls-files', '--', '.tigerkit', '.tigerkit/'], cwd=root, text=True, capture_output=True, check=True)
    if tracked.stdout.strip():
        raise ValueError('.tigerkit must be untracked')
    ignored = subprocess.run(['git', 'check-ignore', '-q', '--', '.tigerkit/'], cwd=root, capture_output=True)
    if ignored.returncode == 1:
        ignore = root / '.gitignore'
        if ignore.is_symlink() or (ignore.exists() and not ignore.is_file()):
            raise ValueError('.gitignore must be a regular nonsymlink file')
        try:
            fd = os.open(ignore, os.O_RDWR | os.O_CREAT | os.O_APPEND | getattr(os, 'O_NOFOLLOW', 0), 0o666)
            with os.fdopen(fd, 'a+b') as stream:
                info = os.fstat(stream.fileno())
                if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
                    raise ValueError('.gitignore must be an unshared regular file')
                stream.seek(0)
                content = stream.read()
                newline = b'\r\n' if b'\r\n' in content else b'\n'
                separator = b'' if not content or content.endswith(b'\n') else newline
                stream.write(separator + b'/.tigerkit/' + newline)
        except OSError as exc:
            raise ValueError('cannot initialize .gitignore for .tigerkit') from exc
        ignored = subprocess.run(['git', 'check-ignore', '-q', '--', '.tigerkit/'], cwd=root, capture_output=True)
    if ignored.returncode != 0:
        raise ValueError('.tigerkit must be effectively ignored before writing')
    return target


def artifact_directory(relative: str, root: Path = ROOT) -> Path:
    base = root.resolve() / '.tigerkit'
    target = base / relative
    if not target.resolve().is_relative_to(base) or any(p.is_symlink() for p in [target, *target.parents] if p.is_relative_to(base)):
        raise ValueError('artifact path escapes .tigerkit')
    checked_artifact_root(root)
    target.mkdir(parents=True, exist_ok=True)
    return target


def scratch_directory(owner: str, root: Path = ROOT):
    return tempfile.TemporaryDirectory(prefix='run-', dir=artifact_directory(f'tmp/{owner}', root))


def output_directory(value: str | None, owner: str, root: Path = ROOT) -> Path:
    if value is None:
        base = artifact_directory(f'evidence/{owner}', root)
        return Path(tempfile.mkdtemp(prefix='run-', dir=base))
    target = Path(value).absolute()
    if target.is_symlink() or target.resolve() != target:
        raise ValueError('output must not traverse a symlink')
    if target.exists() and (not target.is_dir() or any(target.iterdir())):
        raise ValueError('output directory must be new or empty; preserve existing results')
    # Validate the requested destination before the optional ignore-file mutation.
    if target.is_relative_to(root.resolve()):
        base = root.resolve() / '.tigerkit'
        if not target.is_relative_to(base):
            raise ValueError('--output must be outside the repository or under ignored .tigerkit/')
        target = artifact_directory(str(target.relative_to(base)), root)
    target.mkdir(parents=True, exist_ok=True)
    return target



def validate_artifact_guards(root: Path = ROOT) -> list[str]:
    errors = []
    for path in sorted((root / 'skills').glob('tk-*/SKILL.md')):
        text = path.read_text(encoding='utf-8')
        if text.count(ARTIFACT_BLOCK) != 1 or text.count(ARTIFACT_MARKER) != 1:
            errors.append(f'{path.relative_to(root)}: artifact guard must match exactly once')
    return errors
