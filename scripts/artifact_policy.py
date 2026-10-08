"""Canonical installed artifact guard and repository-tool path allocation."""
from __future__ import annotations

import os
import stat
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_MARKER = '<!-- tigerkit:artifact-paths -->'
NO_ARTIFACT_SKILLS = frozenset(("tk-adhd", "tk-grill", "tk-ask-repo", "tk-review"))
ARTIFACT_BLOCK = """<!-- tigerkit:artifact-paths -->
## Artifact Paths

Create artifacts only when this skill's task authorizes them. Before any artifact write, temporary checkout/transport, or ignore setup, read [artifact paths](references/artifact-paths.md) and apply its Git exclusion, safe-path, and ownership checks. Default repository-owned output to `.tigerkit/`; honor explicit final destinations. Conversation-only work skips this reference and performs no file or ignore setup. Artifact handling grants no unrelated mutation or publication authority.
"""
NO_ARTIFACT_BLOCK = """<!-- tigerkit:artifact-paths -->
## Artifact Paths

This skill creates no artifacts. Do not create temporary files, write reports, or edit ignore rules for this invocation; return the result in the conversation.
"""
USER_INPUT_REFERENCE = '''
## User-editable temporary input

Apply this branch only when the task requires the user to supply values through a newly created temporary file. Use a UTF-8 `input.json` containing a pretty-printed plain JSON object with double-quoted, task-specific keys; initialize missing text values to `""` and prefill only confirmed non-secret defaults. Include only fields needed for the pending step. For a single token, create:

```json
{
  "token": ""
}
```

Use the same object shape for one or several fields. Keep field meanings, required types and editing instructions outside the file; do not use JSON-LD, comments, trailing commas, instructional placeholder values or a zero-byte/raw-text file. This rule does not convert existing user files, final documents, code/config files, machine transport, or conversational questions into JSON and grants no new write authority.

Put ordinary input in `.tigerkit/tmp/<skill>/<run-id>/input.json`. If any field is secret, keep the entire object in `.tigerkit/secret-input/<skill>-<run-id>/input.json` with directory `0700` and file `0600`. Apply the exclusion, nonsymlink and ownership checks above; create exclusively and never overwrite an unrelated existing file. Require a regular file with one hard link, inside the safe run-owned directory. Reuse an existing run-owned pending file without resetting entered values. Never prefill secrets or expose their contents in chat, commands, logs, receipts or parser errors.

Show both repository-relative and absolute paths, the secret-free initial template, and which fields the user must fill and save. Offer a host-appropriate clipboard-to-field command only when useful; it must JSON-serialize the clipboard value into the named field while preserving other fields, never overwrite the object with raw clipboard text or place values in arguments/history. Do not automatically launch an editor, opener, GUI, terminal UI or change focus. Open the shown path only on explicit user request.

Record the initial file metadata privately, then use bounded metadata-change polling. File existence, non-zero size or modification alone is not completion: the seeded template is already non-empty. After a change, a trusted local reader may parse without returning contents, validate the exact requested keys/types and nonblank required text fields, and report only `Pending | Ready | Unsafe`. Reject duplicate or unexpected keys. An unchanged template, missing/blank field, malformed or partly saved JSON stays `Pending`; preserve the user's bytes and wait for the next change. Explain only the missing field name or syntax requirement, never raw values or parser excerpts. Before use, recheck safe path, ownership and secret permissions and reparse the current file; validate and consume the same snapshot. Unsafe replacement stops the file branch as `Blocked | Unverifiable`.

When ready, resume the exact authorized pending step without a separate completion message. Renew bounded waits while the task remains active; if the host cannot wait, preserve the same run-owned path and explain resumption. On resumption, privately validate the existing run-owned file once before waiting for another change. Pass only validated fields to the approved consumer, never the JSON wrapper as a credential. Delete secret input and its run directory immediately after consumption on success, failure or exception and verify no residue; ordinary input follows its run-owned temporary lifecycle. Preserve the existing host-native hidden-input option when safer.
'''
ARTIFACT_REFERENCE = """# Artifact Paths

Default repository-owned output to `.tigerkit/`: transient files in `tmp/<skill>/<run-id>/`, verification evidence in `evidence/<skill>/<run-id>/`, explanations in `explanations/`, lessons in `study/<topic>/`, and retrospectives in `retro/`. Preserve existing owner-specific paths and explicit user-selected final destinations. Create artifacts only when the active task calls for them. Before writing, verify the repository root, no tracked `.tigerkit` paths, and safe nonsymlink destinations. From the repository root, run `git ls-files -- .tigerkit .tigerkit/` to check tracking, then `git check-ignore -q -- .tigerkit/` to check effective exclusion. Exit 0 means leave ignore files unchanged, including when exclusion comes from `core.excludesFile` (such as configured `~/.gitignore`), the default global ignore file, or `.git/info/exclude`; a missing repository `.gitignore` or missing literal entry is not evidence of missing coverage. Only exit 1 permits creating the root `.gitignore` or appending `/.tigerkit/`, preserving existing bytes and line endings, then rerunning the same check before writing. Any other exit status or command failure blocks the file branch without an ignore edit. Use `git check-ignore -v -- .tigerkit/` only to diagnose the source; a printed negated pattern is not proof of exclusion. This narrow ignore setup is part of an authorized artifact write even for a read-only task; it grants no other source/config/index/commit/publication authority. Existing effective ignore rules need no edit. Do not untrack files or follow a symlinked/nonregular `.gitignore`; if unsafe, unwritable, still unignored, or no repository is identified, stop only the file branch as `Blocked | Unverifiable`, without an OS-temp fallback. Briefly report an ignore edit; never stage or commit it solely for setup. Atomic replacement may use a run-owned sibling temporary file on the destination filesystem; clean it after success. External tool caches and isolated test fixtures retain their tool-owned lifecycle.
"""


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



def artifact_block(name: str) -> str:
    return NO_ARTIFACT_BLOCK if name in NO_ARTIFACT_SKILLS else ARTIFACT_BLOCK


def artifact_reference(name: str) -> str:
    return ARTIFACT_REFERENCE + USER_INPUT_REFERENCE


def sync_artifact_guards(root: Path = ROOT) -> None:
    for path in sorted((root / 'skills').glob('tk-*/SKILL.md')):
        text = path.read_text(encoding='utf-8')
        start = text.find(ARTIFACT_MARKER)
        if start >= 0:
            end = text.find('<!-- tigerkit:', start + len(ARTIFACT_MARKER))
            end = len(text) if end < 0 else end
            text = text[:start] + artifact_block(path.parent.name) + '\n' + text[end:]
        else:
            text = text.rstrip() + '\n\n' + artifact_block(path.parent.name)
        path.write_text(text, encoding='utf-8')
        if path.parent.name not in NO_ARTIFACT_SKILLS:
            reference = path.parent / 'references/artifact-paths.md'
            reference.parent.mkdir(exist_ok=True)
            reference.write_text(artifact_reference(path.parent.name), encoding='utf-8')


def validate_artifact_guards(root: Path = ROOT) -> list[str]:
    errors = []
    for path in sorted((root / 'skills').glob('tk-*/SKILL.md')):
        text = path.read_text(encoding='utf-8')
        if text.count(artifact_block(path.parent.name)) != 1 or text.count(ARTIFACT_MARKER) != 1:
            errors.append(f'{path.relative_to(root)}: artifact guard must match exactly once')
        reference = path.parent / 'references/artifact-paths.md'
        if path.parent.name not in NO_ARTIFACT_SKILLS:
            if not reference.is_file() or reference.read_text(encoding='utf-8') != artifact_reference(path.parent.name):
                errors.append(f'{reference.relative_to(root)}: artifact reference must match canonical checks')
        elif reference.exists():
            errors.append(f'{reference.relative_to(root)}: non-writing skill must not carry a writer reference')
    return errors
