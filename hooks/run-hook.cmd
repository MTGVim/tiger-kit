: << 'CMDBLOCK'
@echo off
REM Cross-platform polyglot wrapper for TigerKit hook scripts.
REM On Windows: cmd.exe runs this batch portion and locates bash.
REM On Unix: sh/bash treats the block above CMDBLOCK as a no-op heredoc.
REM
REM Hook scripts use extensionless filenames so Claude Code's Windows .sh
REM auto-detection does not rewrite the command.
REM
REM Usage: run-hook.cmd <script-name> [args...]

if "%~1"=="" (
    echo run-hook.cmd: missing script name >&2
    exit /b 1
)

set "HOOK_DIR=%~dp0"

if exist "C:\Program Files\Git\bin\bash.exe" (
    "C:\Program Files\Git\bin\bash.exe" "%HOOK_DIR%%~1" %2 %3 %4 %5 %6 %7 %8 %9
    exit /b %ERRORLEVEL%
)
if exist "C:\Program Files (x86)\Git\bin\bash.exe" (
    "C:\Program Files (x86)\Git\bin\bash.exe" "%HOOK_DIR%%~1" %2 %3 %4 %5 %6 %7 %8 %9
    exit /b %ERRORLEVEL%
)

where bash >nul 2>nul
if %ERRORLEVEL% equ 0 (
    bash "%HOOK_DIR%%~1" %2 %3 %4 %5 %6 %7 %8 %9
    exit /b %ERRORLEVEL%
)

REM No bash found: fail open so the plugin commands remain usable.
exit /b 0
CMDBLOCK

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SCRIPT_NAME="${1:-}"
if [ -z "$SCRIPT_NAME" ]; then
  echo "run-hook.cmd: missing script name" >&2
  exit 1
fi
shift
exec bash "${SCRIPT_DIR}/${SCRIPT_NAME}" "$@"
