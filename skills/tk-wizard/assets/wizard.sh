#!/usr/bin/env bash
# Original TigerKit scaffold. Add only evidence-backed, task-specific stages.
set +x
set -euo pipefail
umask 077

REPLY=''
INPUT_ACTION=''
CURRENT_STAGE=''
COMPLETED=0
PENDING=0

wizard_stop() {
  REPLY=''
  printf '\n중단했습니다. 완료 %s, 미완료 %s. 재실행 시 실제 대상을 다시 확인하세요.\n' "$COMPLETED" "$PENDING" >&2
}
trap 'wizard_stop; exit 130' INT
trap 'wizard_stop; exit 143' TERM

wizard_stage() {
  CURRENT_STAGE=$3
  printf '\n[%s/%s] %s\n' "$1" "$2" "$CURRENT_STAGE"
}

# has_current is metadata only; never pass the existing value as an argument.
# Success means a choice was collected, not that the destination was updated.
wizard_input() {
  local kind=$1 label=$2 has_current=$3 optional=$4 action='' value=''
  REPLY=''
  INPUT_ACTION=''
  while :; do
    printf '%s: [r] 입력' "$label"
    if [[ "$has_current" == yes ]]; then printf ', [k 또는 Enter] 기존 값 유지'; fi
    if [[ "$optional" == yes ]]; then printf ', [s] 건너뛰기'; fi
    printf ': '
    if ! IFS= read -r action; then wizard_stop; return 2; fi
    case "$action" in
      k|'')
        if [[ "$has_current" == yes ]]; then INPUT_ACTION=keep; return 0; fi
        ;;
      s)
        if [[ "$optional" == yes ]]; then INPUT_ACTION=skip; return 0; fi
        ;;
      r) break ;;
    esac
    printf '표시된 선택지 중 하나를 입력하세요.\n'
  done
  while :; do
    printf '%s 입력: ' "$label"
    case "$kind" in
      public)
        if ! IFS= read -e -r value; then wizard_stop; return 2; fi
        ;;
      secret)
        if ! IFS= read -r -s value; then printf '\n'; wizard_stop; return 2; fi
        printf '\n'
        ;;
      *) printf '지원하지 않는 입력 종류입니다.\n' >&2; return 2 ;;
    esac
    if [[ -n "$value" ]]; then REPLY=$value; INPUT_ACTION=replace; return 0; fi
    printf '값이 비어 있습니다. 중단하려면 Ctrl-C를 누르세요.\n'
  done
}

# Call only for a verified public URL covered by the user's run instructions.
wizard_open_url() {
  local url=$1
  case "$url" in https://*) ;; *) return 2 ;; esac
  if command -v wslview >/dev/null 2>&1; then
    wslview "$url" >/dev/null 2>&1 && return 0
  elif command -v open >/dev/null 2>&1; then
    open "$url" >/dev/null 2>&1 && return 0
  elif command -v xdg-open >/dev/null 2>&1; then
    xdg-open "$url" >/dev/null 2>&1 && return 0
  fi
  printf '브라우저에서 직접 여세요: %s\n' "$url"
}

# Use immediately before a specifically approved remote/irreversible operation.
wizard_confirm() {
  local answer=''
  printf '%s [yes 입력 시 진행]: ' "$1"
  if ! IFS= read -r answer; then return 2; fi
  [[ "$answer" == yes ]]
}

wizard_done() { COMPLETED=$((COMPLETED + 1)); }
wizard_pending() { PENDING=$((PENDING + 1)); }
wizard_finish() {
  REPLY=''
  printf '\n검증 완료 %s, 미완료 %s.\n' "$COMPLETED" "$PENDING"
  if (( PENDING > 0 )); then return 3; fi
}

wizard_main() {
  # Replace this body with stages, checks and exact approved destinations.
  # No generic dotenv writer or remote mutation is intentionally provided.
  printf '작업별 단계와 검증을 먼저 작성해야 합니다.\n' >&2
  return 2
}

if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
  if [[ ! -t 0 || ! -t 1 ]]; then
    printf '사용자 터미널에서 직접 실행하세요. 파이프 입력은 받지 않습니다.\n' >&2
    exit 2
  fi
  wizard_main "$@"
  exit
fi
