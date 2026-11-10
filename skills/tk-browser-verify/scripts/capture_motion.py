#!/usr/bin/env python3
"""Capture a bounded approved scenario on an already run-owned Playwright CLI page."""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import math
import os
from pathlib import Path
import re
import signal
import stat
import subprocess
import sys

# Only the public CLI transports this payload. No browser launch, attach or Node imports.
CODE = r"""async (page) => {
 const scenario = (__SCENARIO__);
 const frames = [], acknowledgements = [], errors = [];
 const cleanup = {stopped:false,listenerRemoved:false,detached:false};
 let session, attempted=false, timer, bytes=0, rejected, scenarioResult, start, end, scenarioSettled=false;
 const failed = new Promise((_,reject)=>{rejected=reject;});
 const abort = message => rejected(new Error(message));
 const clock = async () => {
  const before = await session.send('Runtime.evaluate',{expression:'Date.now()/1000',returnByValue:true});
  const metrics = await session.send('Performance.getMetrics');
  const after = await session.send('Runtime.evaluate',{expression:'({epoch_s:Date.now()/1000,time_origin_ms:performance.timeOrigin,url:location.href})',returnByValue:true});
  const value = metrics.metrics.find(m=>m.name==='Timestamp');
  if (!value) throw new Error('Performance Timestamp unavailable');
  return {epoch_before_s:before.result.value,monotonic_s:value.value,...after.result.value};
 };
 const listener = event => {
  const index=frames.length;
  if (index>=__MAX_FRAMES__ || bytes+event.data.length>__MAX_BYTES__) {
   abort('capture budget exceeded');
  } else {
   frames.push({index,data:event.data,metadata:event.metadata,sessionId:event.sessionId});
   bytes+=event.data.length;
  }
  acknowledgements.push(session.send('Page.screencastFrameAck',{sessionId:event.sessionId})
   .then(()=>({index,sessionId:event.sessionId,ok:true}))
   .catch(e=>{errors.push('ack: '+String(e));abort('frame acknowledgement failed');return {index,ok:false};}));
 };
 try {
  session=await page.context().newCDPSession(page);
  await session.send('Performance.enable');
  start=await clock();
  session.on('Page.screencastFrame',listener);attempted=true;
  await session.send('Page.startScreencast',{format:'png',everyNthFrame:1});
  timer=setTimeout(()=>abort('scenario deadline exceeded'),__TIMEOUT_MS__);
  const value=await Promise.race([Promise.resolve().then(()=>scenario(page))
   .finally(()=>{scenarioSettled=true;}),failed]);
  const encoded=JSON.stringify(value===undefined?null:value);
  if(encoded.length>16384)throw new Error('scenario result exceeds 16KiB');
  scenarioResult=JSON.parse(encoded);
 } catch(e) {errors.push(String(e));}
 finally {
  clearTimeout(timer);
  if(session){
   try{end=await clock();}catch(e){errors.push('end clock: '+String(e));}
   if(attempted){try{await session.send('Page.stopScreencast');cleanup.stopped=true;}catch(e){errors.push('stop: '+String(e));}}
   session.removeListener('Page.screencastFrame',listener);cleanup.listenerRemoved=true;
   await Promise.all(acknowledgements);
   try{await session.send('Performance.disable');}catch(e){errors.push('metrics cleanup: '+String(e));}
   try{await session.detach();cleanup.detached=true;}catch(e){errors.push('detach: '+String(e));}
  }
 }
 return {start,end,frames,acknowledgements:await Promise.all(acknowledgements),errors,cleanup,scenarioResult,scenario_settled:scenarioSettled};
}
"""


def plain(path: Path, directory: bool = False) -> Path:
    absolute = path.absolute()
    if absolute != absolute.resolve() or any(p.is_symlink() for p in (absolute, *absolute.parents)):
        raise ValueError("path must not contain symlinks")
    info = absolute.stat()
    if not (stat.S_ISDIR(info.st_mode) if directory else stat.S_ISREG(info.st_mode) and info.st_nlink == 1):
        raise ValueError("expected an ordinary directory or single-link file")
    return absolute


def git(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True, check=True)


def write(path: Path, value: bytes) -> None:
    with path.open("xb") as stream:
        os.chmod(path, 0o600)
        stream.write(value)


def number(value: object) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError("missing or non-finite frame clock")
    return float(value)


def assemble(payload: dict, root: Path) -> dict:
    if payload["errors"] or not all(payload["cleanup"].values()) or payload.get("scenario_settled") is not True:
        raise ValueError("capture failed; inspect capture.json; no evidence manifest created")
    frames = payload["frames"]
    if not frames or len(payload["acknowledgements"]) != len(frames):
        raise ValueError("missing frames or acknowledgements")
    if not all(ack["ok"] and ack["index"] == i and ack["sessionId"] == frames[i]["sessionId"]
               for i, ack in enumerate(payload["acknowledgements"])):
        raise ValueError("frame acknowledgement mismatch")
    monotonic = all("monotonicTimestamp" in row["metadata"] for row in frames)
    field = "monotonicTimestamp" if monotonic else "timestamp"
    clock_field = "monotonic_s" if monotonic else "epoch_s"
    end = number(payload["end"][clock_field])
    times = [number(row["metadata"][field]) for row in frames]
    epochs = [number(row["metadata"]["timestamp"]) for row in frames]
    if any(b < a for a, b in zip(times, times[1:])) or any(b < a for a, b in zip(epochs, epochs[1:])):
        raise ValueError("original frame clock regressed; do not sort away discontinuities")
    if monotonic and any(abs((epochs[i]-epochs[i-1])-(times[i]-times[i-1])) > 0.05
                         for i in range(1, len(frames))):
        raise ValueError("frame wall/monotonic clock discontinuity")
    # Independently sampled wall/monotonic intervals detect large clock discontinuities.
    a, b = payload["start"], payload["end"]
    if abs((number(b["epoch_s"])-number(a["epoch_s"])) -
           (number(b["monotonic_s"])-number(a["monotonic_s"]))) > 0.05:
        raise ValueError("capture clock discontinuity")
    eligible = [(i, row) for i, row in enumerate(frames) if times[i] <= end]
    if not eligible:
        raise ValueError("no frame before capture end")
    first = times[eligible[0][0]]
    end_ms = round((end-first)*1000)
    selected = {}
    for i, row in eligible:
        selected[round((times[i]-first)*1000)] = (i, row)
    if end_ms <= max(selected):
        raise ValueError("capture end must follow the final frame")
    result = []
    for timestamp, (i, row) in sorted(selected.items()):
        image = base64.b64decode(row.pop("data"), validate=True)
        if not image.startswith(b"\x89PNG\r\n\x1a\n"):
            raise ValueError("frame is not PNG")
        path = root / f"frame-{i:05d}.png"
        write(path, image)
        row.update(path=str(path), sha256=hashlib.sha256(image).hexdigest(), bytes=len(image))
        result.append({"path": str(path), "timestamp_ms": timestamp})
    payload.update(timestamp_field=field, end_clock_field=clock_field,
                   rounded_collision_count=len(eligible)-len(selected),
                   excluded_after_end=len(frames)-len(eligible),
                   limitation="CDP has no compositor frame sequence: upstream frame loss is not measurable")
    return {"mode": "evidence", "frames": result, "end_ms": end_ms}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cli", required=True, type=Path)
    parser.add_argument("--session", required=True, help="existing non-default run-owned named session")
    parser.add_argument("--scenario", required=True, type=Path, help="approved async (page) => ... expression")
    parser.add_argument("--output-dir", required=True, type=Path, help="new directory in ignored repository evidence")
    parser.add_argument("--timeout-ms", type=int, default=15000)
    parser.add_argument("--max-frames", type=int, default=600)
    parser.add_argument("--max-base64-bytes", type=int, default=32*1024*1024)
    parser.add_argument("--keep-session-on-failure", action="store_true",
                        help="Keep an owned session only when scenario settlement and recorder cleanup are proven")
    args = parser.parse_args()
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,79}", args.session) or args.session == "default":
        raise ValueError("require an explicit non-default run-owned session")
    if not (100 <= args.timeout_ms <= 60000 and 1 <= args.max_frames <= 3600
            and 1024 <= args.max_base64_bytes <= 128*1024*1024):
        raise ValueError("capture limits outside supported bounds")
    cli = args.cli.absolute()  # Official node_modules/.bin links are allowed for this explicit executable.
    if not cli.is_file() or not os.access(cli, os.X_OK):
        raise ValueError("installed CLI executable required")
    scenario_path = plain(args.scenario)
    if scenario_path.stat().st_size > 65536:
        raise ValueError("scenario exceeds 64KiB")
    scenario = scenario_path.read_text(encoding="utf-8").strip()
    target = args.output_dir.absolute()
    parent = plain(target.parent, directory=True)
    repository = Path(git(parent, "rev-parse", "--show-toplevel").stdout.strip()).resolve()
    relative = target.relative_to(repository).parts
    if len(relative) < 4 or relative[:2] != (".tigerkit", "evidence"):
        raise ValueError("output must be inside repository .tigerkit/evidence/<owner>/<run>")
    if git(repository, "ls-files", "--", ".tigerkit/").stdout:
        raise ValueError("tracked .tigerkit files are not allowed")
    git(repository, "check-ignore", "-q", "--", ".tigerkit/")
    listing = subprocess.run([str(cli), "list", "--json"], cwd=repository,
                             capture_output=True, text=True, check=True, timeout=10)
    matches = [row for row in json.loads(listing.stdout)["browsers"] if row.get("name") == args.session]
    if len(matches) != 1 or any(matches[0].get(key) != value for key, value in
                              {"status":"open", "headed":False, "attached":False,
                               "persistent":False, "compatible":True}.items()):
        raise ValueError("existing isolated headless CLI session not established; helper never opens one")
    target.mkdir(mode=0o700)  # Exclusive: never reuse/overwrite another run.
    write(target / "capture.session.json", json.dumps(matches[0], indent=2).encode())
    code = CODE.replace("__SCENARIO__", scenario).replace("__MAX_FRAMES__", str(args.max_frames))
    code = code.replace("__MAX_BYTES__", str(args.max_base64_bytes)).replace("__TIMEOUT_MS__", str(args.timeout_ms))
    code_path = target / "capture.run-code.js"
    write(code_path, code.encode())
    interrupted = []
    def defer(signum, _frame):
        interrupted.append(signum)  # Let the bounded remote finally finish; do not orphan a recording.
    old = {sig: signal.signal(sig, defer) for sig in (signal.SIGINT, signal.SIGTERM)}
    command = [str(cli), f"-s={args.session}", "--raw", "run-code", f"--filename={code_path}"]
    succeeded = False
    safe_to_keep = False
    try:
        try:
            completed = subprocess.run(command, cwd=repository, capture_output=True, timeout=args.timeout_ms/1000+30)
        except subprocess.TimeoutExpired as error:
            write(target / "capture.stdout.json", error.stdout or b"")
            write(target / "capture.invocation.json", json.dumps({"command":command, "exit":None,
                  "timeout":True, "signals":interrupted}).encode())
            raise
        write(target / "capture.stdout.json", completed.stdout)
        write(target / "capture.invocation.json", json.dumps({"command": command, "exit": completed.returncode,
              "stderr": completed.stderr.decode(errors="replace"), "signals": interrupted}).encode())
        if completed.returncode or len(completed.stdout) > args.max_base64_bytes + 4*1024*1024:
            raise ValueError("CLI failed or exceeded payload bound")
        payload = json.loads(completed.stdout)
        safe_to_keep = (payload.get("scenario_settled") is True
                        and all(payload.get("cleanup", {}).get(k) is True
                                for k in ("stopped", "listenerRemoved", "detached")))
        write(target / "capture.json", json.dumps(payload).encode())
        if interrupted:
            print(json.dumps({"status":"interrupted", "cleanup":payload.get("cleanup"), "output_dir":str(target)}))
            return 128 + interrupted[0]
        manifest = assemble(payload, target)
        write(target / "capture.metadata.json", json.dumps(payload, indent=2).encode())
        write(target / "capture.manifest.json", json.dumps(manifest, indent=2).encode())
        print(json.dumps({"manifest":str(target / "capture.manifest.json"), "frame_count":len(manifest["frames"]),
                          "end_ms":manifest["end_ms"], "timestamp_field":payload["timestamp_field"],
                          "cleanup":payload["cleanup"]}))
        succeeded = True
        return 0
    finally:
        try:
            if not succeeded and args.keep_session_on_failure and safe_to_keep:
                write(target / "capture.session-kept.json", json.dumps(
                    {"session": args.session, "scenario_settled": True,
                     "recorder_cleanup": "complete", "next_required": "retry only this scene or close the owned session"}).encode())
            if not succeeded and not (args.keep_session_on_failure and safe_to_keep):
                # Recorder finally cannot cancel a racing scenario Promise. Closing only this
                # explicitly owned session revokes its page/context before any later run.
                close_command = [str(cli), f"-s={args.session}", "close"]
                try:
                    closed = subprocess.run(close_command, cwd=repository, capture_output=True, timeout=15)
                    receipt = {"command":close_command, "exit":closed.returncode,
                               "stdout":closed.stdout.decode(errors="replace"),
                               "stderr":closed.stderr.decode(errors="replace")}
                except (OSError, subprocess.SubprocessError) as error:
                    receipt = {"command":close_command, "exit":None, "error":str(error)}
                write(target / "capture.session-close.json", json.dumps(receipt).encode())
        finally:
            for sig, handler in old.items():
                signal.signal(sig, handler)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, KeyError, subprocess.SubprocessError) as error:
        print(json.dumps({"error":str(error), "next_required":"inspect preserved capture; close only the owned named session"}), file=sys.stderr)
        sys.exit(1)
