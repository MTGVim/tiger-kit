#!/usr/bin/env bash
set -euo pipefail

TARGET_PROJECT="${1:-.}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
TARGET_SKILLS="$TARGET_PROJECT/.claude/skills"

mkdir -p "$TARGET_SKILLS"
cp -R "$REPO_ROOT/skills/gap" "$TARGET_SKILLS/"
cp -R "$REPO_ROOT/skills/gaplan" "$TARGET_SKILLS/"
cp -R "$REPO_ROOT/skills/go" "$TARGET_SKILLS/"
cp -R "$REPO_ROOT/skills/next" "$TARGET_SKILLS/"
cp -R "$REPO_ROOT/skills/plan" "$TARGET_SKILLS/"

echo "Installed tigap skills into: $TARGET_SKILLS"
echo "Standalone commands may be available as: /gap, /gaplan, /go, /next, /plan"
