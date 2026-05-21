from __future__ import annotations

import json
import os
import queue
import re
import signal
import subprocess
import sys
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Sequence

from .paths import ensure_state, state_paths
from .session import monitor_event_lines, read_session


DEFAULT_DURATION_SECONDS = 12 * 60 * 60
MAX_DURATION_SECONDS = 12 * 60 * 60
CAPTURE_SURFACE = "explicit_finite_monitor_session"
ACTIVE_TRUST = "local_workday_session_status"


class WorkdayError(RuntimeError):
    pass


def default_watcher_command() -> list[str]:
    watcher = _repo_root() / "resources" / "win-uia-watcher" / "bin" / "Debug" / "net8.0-windows" / "win-uia-watcher.dll"
    if not watcher.exists():
        raise WorkdayError("default watcher build output is missing; run dotnet build first")
    return ["dotnet", str(watcher)]


def default_helper_command() -> list[str]:
    helper = _repo_root() / "resources" / "win-uia-helper" / "bin" / "Debug" / "net8.0-windows" / "win-uia-helper.dll"
    if not helper.exists():
        raise WorkdayError("default helper build output is missing; run dotnet build first")
    return ["dotnet", str(helper)]


def start_workday(
    *,
    watcher_command: Sequence[str],
    helper_command: Sequence[str] | None = None,
    home: Path | str | None = None,
    session_id: str | None = None,
    duration_seconds: int = DEFAULT_DURATION_SECONDS,
    depth: int = 80,
    debounce_ms: int = 750,
    heartbeat_ms: int = 5000,
    capture_on_start: bool = True,
    exclude_apps: Sequence[str] = (),
) -> dict[str, Any]:
    if duration_seconds < 0 or duration_seconds > MAX_DURATION_SECONDS:
        raise WorkdayError(f"duration must be between 0 and {MAX_DURATION_SECONDS} seconds")
    paths = ensure_state(home)
    active_path = paths["workday_active"]
    existing = _read_json(active_path)
    if existing and _is_process_running(int(existing.get("pid", 0))):
        return {
            "active": True,
            "error": "workday_session_already_active",
            "session_id": existing.get("session_id", ""),
            "pid": existing.get("pid", 0),
            "trust": ACTIVE_TRUST,
            "capture_surface": CAPTURE_SURFACE,
        }
    if existing:
        active_path.unlink(missing_ok=True)

    session = _slug(session_id or f"workday-{_local_timestamp()}")
    stop_file = paths["logs"] / f"{session}.stop"
    result_file = paths["logs"] / f"{session}.workday-result.json"
    stdout_path = paths["logs"] / f"{session}.workday-stdout.json"
    stderr_path = paths["logs"] / f"{session}.workday-stderr.txt"
    for path in (stop_file, result_file):
        path.unlink(missing_ok=True)

    runner_args = [
        sys.executable,
        "-m",
        "winchronicle",
        "workday",
        "run",
        "--session-id",
        session,
        "--stop-file",
        str(stop_file),
        "--result-file",
        str(result_file),
        "--duration",
        str(duration_seconds),
        "--depth",
        str(depth),
        "--debounce-ms",
        str(debounce_ms),
        "--heartbeat-ms",
        str(heartbeat_ms),
    ]
    for part in watcher_command:
        runner_args.extend(["--watcher-arg", str(part)])
    if helper_command:
        for part in helper_command:
            runner_args.extend(["--helper-arg", str(part)])
    if capture_on_start:
        runner_args.append("--capture-on-start")
    for app in exclude_apps:
        runner_args.extend(["--exclude-app", app])

    env = os.environ.copy()
    env["WINCHRONICLE_HOME"] = str(paths["home"])
    stdout_handle = stdout_path.open("w", encoding="utf-8")
    stderr_handle = stderr_path.open("w", encoding="utf-8")
    try:
        process = subprocess.Popen(
            runner_args,
            cwd=_repo_root(),
            env=env,
            stdout=stdout_handle,
            stderr=stderr_handle,
            creationflags=_creation_flags(),
        )
    finally:
        stdout_handle.close()
        stderr_handle.close()

    active = {
        "schema_version": 1,
        "active": True,
        "session_id": session,
        "pid": process.pid,
        "started_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "duration_seconds": duration_seconds,
        "state_home": str(paths["home"]),
        "stop_file": str(stop_file),
        "result_file": str(result_file),
        "stdout_path": str(stdout_path),
        "stderr_path": str(stderr_path),
        "trust": ACTIVE_TRUST,
        "capture_surface": CAPTURE_SURFACE,
        "bounded": True,
    }
    _write_json(active_path, active)
    return active


def run_workday(
    *,
    watcher_command: Sequence[str],
    helper_command: Sequence[str] | None,
    stop_file: Path,
    result_file: Path,
    home: Path | str | None = None,
    session_id: str,
    duration_seconds: int,
    depth: int,
    debounce_ms: int,
    heartbeat_ms: int,
    capture_on_start: bool,
    exclude_apps: Sequence[str],
) -> dict[str, Any]:
    command = _watcher_command(
        watcher_command,
        helper_command,
        depth=depth,
        duration_seconds=duration_seconds,
        debounce_ms=debounce_ms,
        heartbeat_ms=heartbeat_ms,
        capture_on_start=capture_on_start,
    )
    lines: list[str] = []
    stdout_queue: queue.Queue[str] = queue.Queue()
    stderr_queue: queue.Queue[str] = queue.Queue()
    process = subprocess.Popen(
        command,
        cwd=_repo_root(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
        creationflags=_creation_flags(),
    )
    _start_reader(process.stdout, stdout_queue)
    _start_reader(process.stderr, stderr_queue)
    deadline = time.monotonic() + max(0, duration_seconds)
    stop_requested = False

    while process.poll() is None:
        _drain(stdout_queue, lines)
        _drain(stderr_queue, [])
        if stop_file.exists():
            stop_requested = True
            _terminate_process_tree(process.pid)
            break
        if duration_seconds >= 0 and time.monotonic() > deadline + 5:
            _terminate_process_tree(process.pid)
            break
        time.sleep(0.1)

    try:
        process.wait(timeout=10)
    except subprocess.TimeoutExpired:
        _terminate_process_tree(process.pid)
        process.wait(timeout=5)
    _drain(stdout_queue, lines)
    _drain(stderr_queue, [])

    result = monitor_event_lines(
        lines,
        home,
        session_id=session_id,
        mode="workday",
        exclude_apps=exclude_apps,
    )
    payload = {
        "active": False,
        "stopped": stop_requested,
        "summary_available": True,
        "summary": result.session,
        "path": str(result.path),
        "report_path": str(result.report_path),
        "trust": ACTIVE_TRUST,
        "capture_surface": CAPTURE_SURFACE,
    }
    _write_json(result_file, payload)
    return payload


def status_workday(home: Path | str | None = None) -> dict[str, Any]:
    paths = state_paths(home)
    active = _read_json(paths["workday_active"])
    if not active:
        return {"active": False, "trust": ACTIVE_TRUST, "capture_surface": CAPTURE_SURFACE}
    running = _is_process_running(int(active.get("pid", 0)))
    result = _read_json(Path(active.get("result_file", "")))
    return {
        **active,
        "active": running,
        "running": running,
        "summary_available": bool(result and result.get("summary_available")),
    }


def stop_workday(home: Path | str | None = None, *, wait_seconds: int = 30) -> dict[str, Any]:
    paths = state_paths(home)
    active_path = paths["workday_active"]
    active = _read_json(active_path)
    if not active:
        return {
            "active": False,
            "stopped": False,
            "summary_available": False,
            "trust": ACTIVE_TRUST,
            "capture_surface": CAPTURE_SURFACE,
        }

    stop_file = Path(active["stop_file"])
    result_file = Path(active["result_file"])
    stop_file.write_text(datetime.now().astimezone().isoformat(timespec="seconds"), encoding="utf-8")
    pid = int(active.get("pid", 0))
    deadline = time.monotonic() + max(0, wait_seconds)
    result = _read_json(result_file)
    while time.monotonic() < deadline and not result:
        if _is_process_running(pid):
            time.sleep(0.2)
        else:
            time.sleep(0.1)
        result = _read_json(result_file)
    if not result and _is_process_running(pid):
        _terminate_process_tree(pid)
        time.sleep(0.2)
        result = _read_json(result_file)

    active_path.unlink(missing_ok=True)
    if result:
        return {**result, "active": False, "stopped": True}
    try:
        summary = read_session(active["session_id"], paths["home"])
    except Exception:
        summary = None
    return {
        "active": False,
        "stopped": True,
        "summary_available": summary is not None,
        "summary": summary,
        "trust": ACTIVE_TRUST,
        "capture_surface": CAPTURE_SURFACE,
    }


def summarize_workday(identifier: str, home: Path | str | None = None) -> dict[str, Any]:
    paths = state_paths(home)
    return read_session(identifier, paths["home"])


def _watcher_command(
    watcher_command: Sequence[str],
    helper_command: Sequence[str] | None,
    *,
    depth: int,
    duration_seconds: int,
    debounce_ms: int,
    heartbeat_ms: int,
    capture_on_start: bool,
) -> list[str]:
    if not watcher_command:
        raise WorkdayError("watcher command is required")
    command = [str(part) for part in watcher_command]
    command.extend(
        [
            "watch",
            "--depth",
            str(depth),
            "--debounce-ms",
            str(max(0, debounce_ms)),
            "--duration-ms",
            str(max(0, duration_seconds) * 1000),
            "--heartbeat-ms",
            str(max(250, heartbeat_ms)),
        ]
    )
    if helper_command:
        helper_parts = [str(part) for part in helper_command]
        command.extend(["--helper", helper_parts[0]])
        for helper_arg in helper_parts[1:]:
            command.extend(["--helper-arg", helper_arg])
    if capture_on_start:
        command.append("--capture-on-start")
    return command


def _start_reader(pipe: Any, destination: queue.Queue[str]) -> None:
    if pipe is None:
        return

    def read_lines() -> None:
        try:
            for line in pipe:
                destination.put(line)
        except Exception:
            return

    thread = threading.Thread(target=read_lines, daemon=True)
    thread.start()


def _drain(source: queue.Queue[str], destination: list[str]) -> None:
    while True:
        try:
            item = source.get_nowait()
        except queue.Empty:
            return
        destination.append(item)


def _read_json(path: Path) -> dict[str, Any] | None:
    try:
        if not path.exists():
            return None
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _is_process_running(pid: int) -> bool:
    if pid <= 0:
        return False
    if os.name == "nt":
        completed = subprocess.run(
            ["tasklist", "/FI", f"PID eq {pid}", "/FO", "CSV", "/NH"],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            creationflags=_creation_flags(),
        )
        return str(pid).encode("ascii") in completed.stdout
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    return True


def _terminate_process_tree(pid: int) -> None:
    if pid <= 0:
        return
    if os.name == "nt":
        subprocess.run(
            ["taskkill", "/PID", str(pid), "/T", "/F"],
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=_creation_flags(),
        )
        return
    try:
        os.kill(pid, signal.SIGTERM)
    except OSError:
        return


def _creation_flags() -> int:
    return subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _local_timestamp() -> str:
    return datetime.now().astimezone().strftime("%Y%m%d-%H%M%S")


def _slug(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9]+", "-", value).strip("-").lower()
    return slug or "workday"
