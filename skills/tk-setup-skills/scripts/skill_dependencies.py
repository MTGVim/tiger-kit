#!/usr/bin/env python3
"""Read-only dependency validation. Installation is never executed here."""
import argparse
import json
from pathlib import Path
import re
import sys

ID = re.compile(r'tk-[a-z0-9]+(?:-[a-z0-9]+)*\Z')


class DependencyError(ValueError):
    """Invalid package metadata or unsafe installation boundary."""


def exact_id(value):
    if not isinstance(value, str) or not ID.fullmatch(value) or len(value) > 64:
        raise DependencyError(f'invalid exact skill ID: {value!r}')
    return value


def safe_path(base, path):
    """Reject symlinks at every boundary, including dangling links."""
    base = Path(base).absolute()
    path = Path(path).absolute()
    try:
        path.relative_to(base)
    except ValueError:
        raise DependencyError(f'path escapes root: {path}') from None
    for part in (path, *path.parents):
        if part.is_symlink():
            raise DependencyError(f'symlink boundary is not supported: {part}')
    if not path.resolve().is_relative_to(base.resolve()):
        raise DependencyError(f'path escapes root: {path}')
    return path


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise DependencyError(f'duplicate JSON key: {key}')
        result[key] = value
    return result


def read_json(path):
    try:
        return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=unique_object)
    except (OSError, ValueError) as exc:
        raise DependencyError(f'{path}: {exc}') from None


def declaration(value, label):
    if not isinstance(value, dict) or set(value) != {'version', 'requires'} or type(value['version']) is not int or value['version'] != 1:
        raise DependencyError(f'{label}: expected version 1 and requires only')
    requires = value['requires']
    if not isinstance(requires, list):
        raise DependencyError(f'{label}: requires must be a list')
    for name in requires:
        exact_id(name)
    if len(set(requires)) != len(requires):
        raise DependencyError(f'{label}: duplicate dependency ID')
    return sorted(requires)


def read_package(base, name):
    exact_id(name)
    package = safe_path(base, Path(base) / name)
    skill = safe_path(base, package / 'SKILL.md')
    try:
        text = skill.read_text(encoding='utf-8')
    except OSError as exc:
        raise DependencyError(f'{name}: missing/unreadable SKILL.md: {exc}') from None
    match = re.match(r'\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)', text, re.S)
    if not match:
        raise DependencyError(f'{name}: SKILL.md identity mismatch (missing frontmatter)')
    try:
        import yaml
    except ImportError:
        raise DependencyError(
            'PyYAML is required to validate SKILL.md; provision it only in an approved Python environment'
        ) from None
    class UniqueSafeLoader(yaml.SafeLoader):
        def construct_mapping(self, node, deep=False):
            # Keep explicit keys before SafeLoader expands legal YAML merges.
            pairs = list(node.value) if isinstance(node, yaml.MappingNode) else []
            result = super().construct_mapping(node, deep=deep)
            keys = [self.construct_object(key, deep=deep) for key, _ in pairs
                    if key.tag != 'tag:yaml.org,2002:merge']
            if len(set(keys)) != len(keys):
                raise yaml.YAMLError('duplicate YAML mapping key')
            return result

    try:
        metadata = yaml.load(match[1], Loader=UniqueSafeLoader)
    except yaml.YAMLError:
        # Parser exceptions may include input snippets; do not echo package contents.
        raise DependencyError(f'{name}: SKILL.md identity mismatch (invalid YAML frontmatter)') from None
    if not isinstance(metadata, dict) or metadata.get('name') != name:
        raise DependencyError(f'{name}: SKILL.md identity mismatch (exact name required)')
    description = metadata.get('description')
    if not isinstance(description, str) or not description.strip() or len(description) > 1024:
        raise DependencyError(f'{name}: SKILL.md description must be non-empty and at most 1024 characters')
    for entry in package.rglob('*'):
        if entry.is_symlink():
            raise DependencyError(f'symlink boundary is not supported: {entry}')
    dep = safe_path(base, package / 'dependencies.json')
    return declaration(read_json(dep), dep)


def read_source(root):
    base = safe_path(root, Path(root) / 'skills')
    if not base.is_dir():
        raise DependencyError(f'missing skills directory: {base}')
    graph = {}
    for package in sorted(base.iterdir()):
        if package.name.startswith('tk-'):
            graph[exact_id(package.name)] = read_package(base, package.name)
    if not graph:
        raise DependencyError(f'no skill packages: {base}')
    for name, deps in graph.items():
        for dep in deps:
            if dep not in graph:
                raise DependencyError(f'{name}: unknown dependency ID: {dep}')
    return graph


def validate_dependencies(root: Path) -> list[str]:
    """Return source-declaration errors; no catalog generation required."""
    try:
        read_source(Path(root))
        return []
    except (DependencyError, OSError, UnicodeError, RuntimeError) as exc:
        return [str(exc)]


AGENTS = {'codex': '.agents/skills', 'claude-code': '.claude/skills',
          'hermes-agent': '.hermes/skills'}


def closure(graph, selected):
    pending = list(selected)
    seen = set()
    while pending:
        name = exact_id(pending.pop())
        if name not in graph:
            raise DependencyError(f'unknown skill/dependency ID: {name}')
        if name not in seen:
            seen.add(name)
            pending.extend(graph[name])
    return sorted(seen)


def installation_plan(graph, selected, source, target, agent, scope):
    import os
    if not source or source.startswith('-') or any(c in source for c in '\x00\r\n'):
        raise DependencyError('source must be a nonempty literal, not an option or control text')
    if not target.is_absolute():
        raise DependencyError('target must be an exact absolute directory')
    safe_path(target, target)
    if not target.is_dir():
        raise DependencyError(f'target must already exist: {target}')
    if scope == 'global':
        if target != Path.home():
            raise DependencyError('global target must equal the current HOME; no alternate-home installation')
        if any(os.environ.get(key) for key in ('CLAUDE_CONFIG_DIR', 'HERMES_HOME', 'CODEX_HOME')):
            raise DependencyError('global environment overrides require manual host-specific guidance')
    names = closure(graph, selected)
    installed_root = safe_path(target, target / AGENTS[agent])
    missing = []
    present = []
    for name in names:
        package = safe_path(installed_root, installed_root / name)
        if package.exists():
            if read_package(installed_root, name) != graph[name]:
                raise DependencyError(f'{name}: installed declaration differs from catalog; refuse overwrite')
            present.append(name)
        else:
            missing.append(name)
    argv = ['npx', '--yes', 'skills@1.7.4', 'add', source, '--skill', *missing,
            '--agent', agent, '--copy'] if missing else []
    if argv and scope == 'global':
        argv.append('--global')
    return {'selected': sorted(set(selected)), 'closure': names, 'present': present,
            'missing': missing, 'source': source, 'scope': scope, 'agent': agent,
            'cwd': str(target), 'installed_root': str(installed_root), 'argv': argv,
            'executed': False}


def catalog_value(graph):
    return {'version': 1, 'packages': {name: {'requires': deps}
                                      for name, deps in sorted(graph.items())}}


def read_catalog(path):
    path = safe_path(path.parent, path)
    value = read_json(path)
    if (not isinstance(value, dict) or set(value) != {'version', 'packages'}
            or type(value['version']) is not int or value['version'] != 1
            or not isinstance(value['packages'], dict) or not value['packages']):
        raise DependencyError(f'{path}: invalid installation catalog schema')
    graph = {}
    for name, metadata in value['packages'].items():
        exact_id(name)
        if not isinstance(metadata, dict) or set(metadata) != {'requires'}:
            raise DependencyError(f'{name}: invalid catalog package metadata')
        graph[name] = declaration({'version': 1, **metadata}, name)
    closure(graph, graph)
    return graph


def check_installed(base, selected):
    graph = {}
    pending = list(selected)
    while pending:
        name = exact_id(pending.pop())
        if name not in graph:
            graph[name] = read_package(base, name)
            pending.extend(graph[name])
    return {'closure': sorted(graph), 'errors': []}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    validate = sub.add_parser('validate', help='validate source package declarations')
    validate.add_argument('--root', type=Path, required=True)
    validate.add_argument('--catalog', type=Path, help='also reject a stale generated catalog')
    build = sub.add_parser('build-catalog', help='generate metadata; writes only with explicit --output')
    build.add_argument('--root', type=Path, required=True)
    build.add_argument('--output', type=Path)
    check = sub.add_parser('check', help='check only selected installed dependency closure')
    check.add_argument('--installed-root', type=Path, required=True)
    check.add_argument('--skill', nargs='+', required=True)
    plan = sub.add_parser('plan', help='emit literal installer argv, never execute')
    origin = plan.add_mutually_exclusive_group()
    origin.add_argument('--root', type=Path)
    origin.add_argument('--catalog', type=Path,
                        default=Path(__file__).absolute().parents[1] / 'references/install-catalog.json')
    plan.add_argument('--skill', nargs='+', required=True)
    plan.add_argument('--source', required=True)
    plan.add_argument('--target', type=Path, required=True)
    plan.add_argument('--agent', choices=sorted(AGENTS), required=True)
    plan.add_argument('--scope', choices=['project', 'global'], required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == 'validate':
            errors = validate_dependencies(args.root)
            if not errors and args.catalog and read_catalog(args.catalog) != read_source(args.root):
                errors.append('stale installation catalog: regenerate with build-catalog')
            result = {'errors': errors}
        elif args.command == 'build-catalog':
            result = catalog_value(read_source(args.root))
            if args.output:
                output = safe_path(args.output.parent, args.output)
                output.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n', encoding='utf-8')
            errors = []
        elif args.command == 'check':
            result = check_installed(args.installed_root, args.skill)
            errors = []
        else:
            graph = read_source(args.root) if args.root else read_catalog(args.catalog)
            result = installation_plan(graph, args.skill, args.source,
                                       args.target, args.agent, args.scope)
            errors = []
        print(json.dumps(result, indent=2, sort_keys=True))
        return 1 if errors else 0
    except (DependencyError, OSError, UnicodeError, RuntimeError) as exc:
        print(json.dumps({'errors': [str(exc)], 'guidance':
                          'Stop the affected action. Invoke tk-setup-skills explicitly to plan missing dependencies; '
                          'if unavailable, obtain tk-setup-skills alone from the trusted source. Do not install automatically.'},
                         indent=2), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
