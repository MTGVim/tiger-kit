#!/usr/bin/env python3
"""Run one agent-owned development server per Git project, across linked worktrees.

No background service is installed. Each 'start' spawns a bounded, run-owned supervisor
which holds an OS file lock until its server has stopped. OS-specific locks are flock
(POSIX) and msvcrt.locking (Windows); the process container is a POSIX session or a
Windows Job Object. Browser readiness/evidence remains the verifier's responsibility.
"""
from __future__ import annotations

import argparse
import ctypes
import json
import os
from pathlib import Path
import secrets
import signal
import stat
import subprocess
import sys
import threading
import time

if os.name == "nt":
    import msvcrt
else:
    import fcntl

MAX_LOG_BYTES = 512 * 1024
POLL = 0.25
TERMINATE_GRACE = 5
MAX_RUN_SECONDS = 3600


class GuardError(Exception):
    pass


def report(**values: object) -> None:
    print(json.dumps(values, ensure_ascii=False, sort_keys=True), flush=True)


def _private_directory(path: Path) -> None:
    if path.is_symlink():
        raise GuardError("symlinked guard directory")
    if not path.exists():
        path.mkdir(mode=0o700)
    if not path.is_dir():
        raise GuardError("guard directory is not a directory")
    if os.name != "nt":
        st = path.stat()
        if st.st_uid != os.getuid() or stat.S_IMODE(st.st_mode) != 0o700:
            raise GuardError("guard directory must be owned by the current user and mode 0700")


def _file_ok(path: Path) -> None:
    if path.is_symlink():
        raise GuardError("symlinked guard file")
    if path.exists() and not path.is_file():
        raise GuardError("non-regular guard file")


def _atomic(path: Path, payload: dict) -> None:
    _file_ok(path)
    candidate = path.parent / (".state-" + secrets.token_hex(8))
    fd = os.open(candidate, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as file:
            json.dump(payload, file, ensure_ascii=False, sort_keys=True)
            file.flush()
            os.fsync(file.fileno())
        os.replace(candidate, path)
    finally:
        if candidate.exists():
            candidate.unlink()


def _read(path: Path) -> dict:
    if not path.exists() and not path.is_symlink():
        return {}
    _file_ok(path)
    with path.open(encoding="utf-8") as file:
        result = json.load(file)
    if not isinstance(result, dict):
        raise GuardError("invalid run metadata")
    return result


def _paths(repo: str) -> tuple[Path, Path]:
    checkout = Path(repo).resolve(strict=True)
    root = subprocess.run(
        ["git", "-C", str(checkout), "rev-parse", "--show-toplevel"],
        check=True, text=True, capture_output=True,
    ).stdout.strip()
    if not root or checkout != Path(root).resolve():
        raise GuardError("repo must be a worktree root")
    git = subprocess.run(
        ["git", "-C", str(checkout), "rev-parse", "--path-format=absolute", "--git-common-dir"],
        check=True, text=True, capture_output=True,
    ).stdout.strip()
    common = Path(git)
    if not common.is_dir() or common.is_symlink():
        raise GuardError("unverified Git common directory")
    runtime = common / "tigerkit-runtime"
    _private_directory(runtime)
    _private_directory(runtime / "runs")
    return checkout, runtime


def _run_path(runtime: Path, run_id: str) -> Path:
    if not (8 <= len(run_id) <= 64 and all(c in "0123456789abcdef" for c in run_id)):
        raise GuardError("invalid run identifier")
    path = runtime / "runs" / run_id
    if path.is_symlink() or not path.is_dir():
        raise GuardError("run not found or unsafe")
    return path


def _alive(pid: object) -> bool:
    if not isinstance(pid, int) or pid <= 0:
        return False
    if os.name == "nt":
        kernel = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel.OpenProcess.restype = ctypes.c_void_p
        handle = kernel.OpenProcess(0x1000, False, pid)  # PROCESS_QUERY_LIMITED_INFORMATION
        if not handle:
            return False
        code = ctypes.c_ulong()
        try:
            return bool(kernel.GetExitCodeProcess(ctypes.c_void_p(handle), ctypes.byref(code)) and code.value == 259)
        finally:
            kernel.CloseHandle(ctypes.c_void_p(handle))
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True


class ProjectLock:
    def __init__(self, path: Path):
        _file_ok(path)
        self.file = path.open("a+b", buffering=0)
        self.held = False
        # Windows locks a byte range; create it before trying to acquire.
        if self.file.seek(0, 2) == 0:
            self.file.write(b"\0")

    def try_acquire(self) -> bool:
        self.file.seek(0)
        try:
            if os.name == "nt":
                msvcrt.locking(self.file.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                fcntl.flock(self.file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except (OSError, BlockingIOError):
            return False
        self.held = True
        return True

    def close(self) -> None:
        if self.held:
            self.file.seek(0)
            if os.name == "nt":
                msvcrt.locking(self.file.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(self.file.fileno(), fcntl.LOCK_UN)
        self.file.close()


def _windows_job(process: subprocess.Popen) -> int:
    """Assign only the newly launched child to a kill-on-close Job Object."""
    from ctypes import wintypes

    class BasicLimits(ctypes.Structure):
        _fields_ = [
            ("PerProcessUserTimeLimit", ctypes.c_longlong),
            ("PerJobUserTimeLimit", ctypes.c_longlong),
            ("LimitFlags", wintypes.DWORD),
            ("MinimumWorkingSetSize", ctypes.c_size_t),
            ("MaximumWorkingSetSize", ctypes.c_size_t),
            ("ActiveProcessLimit", wintypes.DWORD),
            ("Affinity", ctypes.c_size_t),
            ("PriorityClass", wintypes.DWORD),
            ("SchedulingClass", wintypes.DWORD),
        ]

    class IoCounters(ctypes.Structure):
        _fields_ = [(x, ctypes.c_ulonglong) for x in (
            "ReadOperationCount", "WriteOperationCount", "OtherOperationCount",
            "ReadTransferCount", "WriteTransferCount", "OtherTransferCount",
        )]

    class ExtendedLimits(ctypes.Structure):
        _fields_ = [
            ("BasicLimitInformation", BasicLimits), ("IoInfo", IoCounters),
            ("ProcessMemoryLimit", ctypes.c_size_t), ("JobMemoryLimit", ctypes.c_size_t),
            ("PeakProcessMemoryUsed", ctypes.c_size_t), ("PeakJobMemoryUsed", ctypes.c_size_t),
        ]

    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel.CreateJobObjectW.restype = ctypes.c_void_p
    job = kernel.CreateJobObjectW(None, None)
    if not job:
        raise GuardError("CreateJobObjectW failed")
    limits = ExtendedLimits()
    limits.BasicLimitInformation.LimitFlags = 0x2000  # JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
    try:
        kernel.SetInformationJobObject.argtypes = [
            ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p, wintypes.DWORD,
        ]
        kernel.AssignProcessToJobObject.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
        if not kernel.SetInformationJobObject(job, 9, ctypes.byref(limits), ctypes.sizeof(limits)):
            raise GuardError("SetInformationJobObject failed")
        # The child is run-owned. Assigning an existing user/provider process is forbidden.
        if not kernel.AssignProcessToJobObject(job, ctypes.c_void_p(int(process._handle))):
            raise GuardError("AssignProcessToJobObject failed")
    except BaseException:
        kernel.CloseHandle(ctypes.c_void_p(job))
        raise
    return int(job)


def _stop_child(process: subprocess.Popen, job: int | None) -> bool:
    """Stop only this supervisor's child; do not kill processes based on stale PIDs."""
    if os.name == "nt":
        if job is not None:
            # Closing the last kill-on-close job handle terminates its owned tree.
            ctypes.WinDLL("kernel32", use_last_error=True).CloseHandle(ctypes.c_void_p(job))
        elif process.poll() is None:
            # Assignment may have failed after the child started. Only terminate
            # the direct child and report that descendants are unverified.
            process.terminate()
    else:
        if process.poll() is None:
            os.killpg(process.pid, signal.SIGTERM)
            try:
                process.wait(timeout=TERMINATE_GRACE)
            except subprocess.TimeoutExpired:
                if process.poll() is None:
                    os.killpg(process.pid, signal.SIGKILL)
    try:
        process.wait(timeout=TERMINATE_GRACE)
    except subprocess.TimeoutExpired:
        return False
    return process.poll() is not None


def _log_drain(source, target: Path) -> None:
    fd = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(fd, "wb") as dst:
            count = 0
            while True:
                data = source.read(8192)
                if not data:
                    return
                if count < MAX_LOG_BYTES:
                    clipped = data[:MAX_LOG_BYTES - count]
                    dst.write(clipped)
                    count += len(clipped)
    finally:
        source.close()


def _leftover(runtime: Path, current_id: str) -> bool:
    """Fail closed if an abandoned server PID may still be live; never kill it."""
    for item in (runtime / "runs").iterdir():
        if item.name == current_id or item.is_symlink() or not item.is_dir():
            continue
        state = _read(item / "state.json")
        if state.get("state") in ("starting", "running", "stopping"):
            if not _alive(state.get("supervisor_pid")) and _alive(state.get("server_pid")):
                return True
    return False


def supervise(checkout: Path, runtime: Path, run_id: str, cwd: Path,
              command: list[str], wait_seconds: int, max_seconds: int) -> None:
    run = _run_path(runtime, run_id)
    state_path = run / "state.json"
    metadata = _read(state_path)
    metadata.update(supervisor_pid=os.getpid(), worktree=str(checkout), state="queued")
    _atomic(state_path, metadata)
    lock = ProjectLock(runtime / "devserver.lock")
    child = None
    job = None
    try:
        deadline = time.monotonic() + wait_seconds
        while not lock.try_acquire():
            if (run / "stop.request").exists():
                metadata["state"] = "stopped"
                return
            if time.monotonic() >= deadline:
                metadata["state"] = "timeout"
                return
            time.sleep(POLL)
        if _leftover(runtime, run_id):
            metadata["state"] = "blocked-orphan"
            return
        if (run / "stop.request").exists():
            metadata["state"] = "stopped"
            return
        metadata["state"] = "starting"
        _atomic(state_path, metadata)
        options: dict = {
            "cwd": str(cwd), "stdin": subprocess.DEVNULL,
            "stdout": subprocess.PIPE, "stderr": subprocess.STDOUT,
        }
        if os.name == "nt":
            options["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.CREATE_NO_WINDOW
        else:
            options["start_new_session"] = True
        child = subprocess.Popen(command, **options)
        if os.name == "nt":
            try:
                job = _windows_job(child)
            except BaseException:
                metadata["state"] = "cleanup-unverifiable"
                raise
        assert child.stdout is not None
        drain = threading.Thread(target=_log_drain, args=(child.stdout, run / "server.log"), daemon=True)
        drain.start()
        metadata.update(state="running", server_pid=child.pid)
        _atomic(state_path, metadata)
        expires = time.monotonic() + max_seconds
        while child.poll() is None:
            if (run / "stop.request").exists() or time.monotonic() >= expires:
                metadata["state"] = "stopping"
                break
            time.sleep(POLL)
        else:
            metadata["state"] = "server-exited"
    except BaseException:
        if metadata.get("state") != "cleanup-unverifiable":
            metadata["state"] = "failed"
    finally:
        if child is not None:
            try:
                if not _stop_child(child, job):
                    metadata["state"] = "cleanup-unverifiable"
            except BaseException:
                metadata["state"] = "cleanup-unverifiable"
        if metadata.get("state") == "stopping":
            metadata["state"] = "stopped"
        try:
            _atomic(state_path, metadata)
        finally:
            lock.close()


def _status(run: Path) -> dict:
    metadata = _read(run / "state.json")
    state = metadata.get("state", "unknown")
    if state in ("queued", "starting", "running", "stopping") and not _alive(metadata.get("supervisor_pid")):
        state = "orphaned-or-exited"
    return {
        "status": state,
        "run_id": run.name,
        "supervisor_pid": metadata.get("supervisor_pid"),
        "server_pid": metadata.get("server_pid"),
        "worktree": metadata.get("worktree"),
        "server_ready": None,  # This manager never substitutes for HTTP/app identity readiness.
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("start", "status", "stop", "_supervise"))
    parser.add_argument("--repo", required=True)
    parser.add_argument("--run-id")
    parser.add_argument("--cwd")
    parser.add_argument("--wait-seconds", type=int, default=120)
    parser.add_argument("--max-seconds", type=int, default=900)
    parser.add_argument("--seconds", type=int, default=10)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    try:
        checkout, runtime = _paths(args.repo)
        if args.action == "start":
            if not (0 < args.wait_seconds <= 3600 and 0 < args.max_seconds <= MAX_RUN_SECONDS):
                raise GuardError("invalid bounded runtime")
            if not args.cwd or not args.command:
                raise GuardError("cwd and command are required")
            command = args.command[1:] if args.command[0] == "--" else args.command
            if not command:
                raise GuardError("empty server command")
            cwd = Path(args.cwd).resolve(strict=True)
            try:
                cwd.relative_to(checkout)
            except ValueError as exc:
                raise GuardError("server cwd must belong to invoking worktree") from exc
            run_id = secrets.token_hex(12)
            run = runtime / "runs" / run_id
            run.mkdir(mode=0o700)
            _atomic(run / "state.json", {"state": "queued", "run_id": run_id, "worktree": str(checkout)})
            worker = [
                sys.executable, str(Path(__file__).resolve()), "_supervise",
                "--repo", str(checkout), "--run-id", run_id, "--cwd", str(cwd),
                "--wait-seconds", str(args.wait_seconds),
                "--max-seconds", str(args.max_seconds), "--", *command,
            ]
            flags: dict = {"stdin": subprocess.DEVNULL, "stdout": subprocess.DEVNULL, "stderr": subprocess.DEVNULL}
            if os.name == "nt":
                flags["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.CREATE_NO_WINDOW
            else:
                flags["start_new_session"] = True
            parent = subprocess.Popen(worker, **flags)
            # Run identity is recorded before returning even if the server is waiting for the lock.
            report(status="queued", run_id=run_id, supervisor_pid=parent.pid)
        elif args.action == "_supervise":
            if not args.run_id or not args.cwd or not args.command:
                raise GuardError("missing run identity or command")
            command = args.command[1:] if args.command[0] == "--" else args.command
            supervise(checkout, runtime, args.run_id, Path(args.cwd).resolve(strict=True),
                      command, args.wait_seconds, args.max_seconds)
        else:
            if not args.run_id:
                raise GuardError("run id required")
            run = _run_path(runtime, args.run_id)
            metadata = _status(run)
            if args.action == "stop" and metadata.get("worktree") != str(checkout):
                raise GuardError("cannot stop another worktree's resources")
            if args.action == "stop" and metadata["status"] in ("queued", "starting", "running"):
                marker = run / "stop.request"
                _file_ok(marker)
                fd = os.open(marker, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600) if not marker.exists() else None
                if fd is not None:
                    os.close(fd)
                end = time.monotonic() + min(30, max(1, args.seconds))
                while time.monotonic() < end:
                    metadata = _status(run)
                    if metadata["status"] not in ("queued", "starting", "running", "stopping"):
                        break
                    time.sleep(POLL)
                else:
                    metadata = _status(run)
            report(**metadata)
        return 0
    except (GuardError, OSError, ValueError, subprocess.CalledProcessError, json.JSONDecodeError):
        report(status="blocked")
        return 2


if __name__ == "__main__":
    sys.exit(main())
