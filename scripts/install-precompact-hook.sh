#!/usr/bin/env bash
set -euo pipefail

TARGET_SETTINGS_JSON="${1:-$HOME/.claude/settings.json}"
PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-}"

if [ -z "$PLUGIN_ROOT" ]; then
  if [ -d "$(pwd)/hooks" ] && [ -f "$(pwd)/hooks/precompact-handoff.py" ]; then
    PLUGIN_ROOT="$(pwd)"
  else
    PLUGIN_ROOT="$(python3 - <<'PY'
import json, subprocess
result = subprocess.run(['claude', 'plugin', 'list', '--json'], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
if result.returncode != 0:
    raise SystemExit(result.stderr.strip() or 'claude plugin list --json failed')
items = json.loads(result.stdout)
for item in items:
    if item.get('id') == 'tk' or item.get('name') == 'tk' or item.get('id') == 'tk@tiger-kit':
        path = item.get('installPath')
        if path:
            print(path)
            raise SystemExit(0)
raise SystemExit('could not resolve installed TigerKit plugin root')
PY
)"
  fi
fi

HOOK_COMMAND="python3 \"$PLUGIN_ROOT/hooks/precompact-handoff.py\""
mkdir -p "$(dirname "$TARGET_SETTINGS_JSON")"

python3 - "$TARGET_SETTINGS_JSON" "$HOOK_COMMAND" <<'PY'
import json, sys
from pathlib import Path

path = Path(sys.argv[1]).expanduser()
command = sys.argv[2]
if path.exists():
    data = json.loads(path.read_text(encoding='utf-8'))
else:
    data = {}
if not isinstance(data, dict):
    raise SystemExit('settings.json must contain a top-level object')

hooks = data.setdefault('hooks', {})
if not isinstance(hooks, dict):
    raise SystemExit('settings.json hooks must be an object')
entries = hooks.setdefault('PreCompact', [])
if not isinstance(entries, list):
    raise SystemExit('settings.json hooks.PreCompact must be a list')

for entry in entries:
    if not isinstance(entry, dict):
        continue
    for hook in entry.get('hooks', []):
        if isinstance(hook, dict) and hook.get('command') == command:
            path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
            print(str(path))
            raise SystemExit(0)

entries.append({
    'matcher': '',
    'hooks': [
        {
            'type': 'command',
            'command': command,
            'timeout': 10,
            'async': True,
        }
    ],
})
path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(str(path))
PY

echo "Installed TigerKit PreCompact hook into $TARGET_SETTINGS_JSON"
echo "Hook command: $HOOK_COMMAND"
