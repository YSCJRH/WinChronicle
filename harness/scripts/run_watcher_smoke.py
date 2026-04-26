from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from winchronicle.schema import validate_watcher_event

DEFAULT_WATCHER_DLL = (
    ROOT
    / "resources"
    / "win-uia-watcher"
    / "bin"
    / "Debug"
    / "net8.0-windows"
    / "win-uia-watcher.dll"
)
DEFAULT_HELPER_FIXTURE = ROOT / "harness" / "fixtures" / "uia-helper" / "notepad_frontmost.json"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="run_watcher_smoke.py",
        description="Run a short WinEvent watcher smoke with a fake helper.",
    )
    parser.add_argument("--watcher-dll", type=Path, default=DEFAULT_WATCHER_DLL)
    parser.add_argument("--fixture", type=Path, default=DEFAULT_HELPER_FIXTURE)
    parser.add_argument("--duration-ms", type=int, default=850)
    parser.add_argument("--heartbeat-ms", type=int, default=250)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if not args.watcher_dll.exists():
        print("FAIL: watcher DLL does not exist; run dotnet build first")
        return 1

    with tempfile.TemporaryDirectory(prefix="winchronicle-watcher-smoke-") as temp_dir:
        temp = Path(temp_dir)
        env = os.environ.copy()
        env["WINCHRONICLE_HOME"] = str(temp / "state")
        fake_helper = _write_fake_helper(temp, args.fixture)
        watcher = _run_watcher(args, fake_helper)
        if watcher.returncode:
            print("FAIL: watcher command failed")
            return watcher.returncode

        event_path = temp / "watcher-events.jsonl"
        event_path.write_text(watcher.stdout, encoding="utf-8")
        events = _load_and_validate_events(event_path)
        if not events:
            print("FAIL: watcher produced no events")
            return 1

        dispatch = subprocess.run(
            [sys.executable, "-m", "winchronicle", "watch", "--events", str(event_path)],
            cwd=ROOT,
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        if dispatch.returncode:
            print("FAIL: watcher fixture dispatch failed")
            return dispatch.returncode

        counts = json.loads(dispatch.stdout)
        if counts["captures_written"] < 1 or counts["heartbeats"] < 1:
            print("FAIL: watcher smoke did not write a capture and heartbeat")
            return 1

        search = subprocess.run(
            [sys.executable, "-m", "winchronicle", "search-captures", "helper contract"],
            cwd=ROOT,
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        if search.returncode:
            print("FAIL: watcher smoke search failed")
            return search.returncode
        results = json.loads(search.stdout)
        if not results or results[0].get("app_name") != "Notepad":
            print("FAIL: watcher smoke capture was not searchable")
            return 1

    print("PASS: watcher smoke passed")
    return 0


def _write_fake_helper(temp: Path, fixture: Path) -> Path:
    fake_helper = temp / "fake_helper.py"
    fake_helper.write_text(
        "from pathlib import Path\n"
        f"print(Path({str(fixture)!r}).read_text(encoding='utf-8'))\n",
        encoding="utf-8",
    )
    return fake_helper


def _run_watcher(args: argparse.Namespace, fake_helper: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            "dotnet",
            str(args.watcher_dll),
            "watch",
            "--duration-ms",
            str(args.duration_ms),
            "--heartbeat-ms",
            str(args.heartbeat_ms),
            "--depth",
            "2",
            "--helper",
            sys.executable,
            "--helper-arg",
            str(fake_helper),
            "--capture-on-start",
        ],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )


def _load_and_validate_events(event_path: Path) -> list[dict[str, object]]:
    events: list[dict[str, object]] = []
    for line in event_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        event = json.loads(line)
        validate_watcher_event(event)
        events.append(event)
    return events


if __name__ == "__main__":
    raise SystemExit(main())
