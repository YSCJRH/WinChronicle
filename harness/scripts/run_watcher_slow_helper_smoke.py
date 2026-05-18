from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_WATCHER_DLL = (
    ROOT
    / "resources"
    / "win-uia-watcher"
    / "bin"
    / "Debug"
    / "net8.0-windows"
    / "win-uia-watcher.dll"
)
OBSERVED_CANARY = "SLOW_HELPER_OBSERVED_CONTENT_MUST_NOT_ECHO"


def main() -> int:
    if not DEFAULT_WATCHER_DLL.exists():
        print("FAIL: watcher DLL does not exist; run dotnet build first")
        return 1

    with tempfile.TemporaryDirectory(prefix="winchronicle-slow-helper-smoke-") as temp_dir:
        fake_helper = _write_slow_helper(Path(temp_dir))
        started = time.monotonic()
        completed = subprocess.run(
            [
                "dotnet",
                str(DEFAULT_WATCHER_DLL),
                "watch",
                "--duration-ms",
                "1200",
                "--heartbeat-ms",
                "250",
                "--helper-timeout-ms",
                "250",
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
            timeout=5,
        )
        elapsed = time.monotonic() - started

    if completed.returncode:
        print("FAIL: watcher command failed")
        return completed.returncode
    if elapsed >= 3:
        print(f"FAIL: slow helper delayed watcher exit ({elapsed:.2f}s)")
        return 1
    if OBSERVED_CANARY in completed.stdout:
        print("FAIL: slow helper observed content leaked")
        return 1

    events = [json.loads(line) for line in completed.stdout.splitlines() if line.strip()]
    if not events:
        print("FAIL: watcher produced no heartbeat after slow helper timeout")
        return 1
    if any(event.get("event_type") != "heartbeat" for event in events):
        print("FAIL: slow helper unexpectedly produced capture output")
        return 1

    print("PASS: watcher slow-helper smoke passed")
    return 0


def _write_slow_helper(temp: Path) -> Path:
    fake_helper = temp / "slow_helper.py"
    fake_helper.write_text(
        "import time\n"
        "time.sleep(10)\n"
        f"print({OBSERVED_CANARY!r})\n",
        encoding="utf-8",
    )
    return fake_helper


if __name__ == "__main__":
    raise SystemExit(main())
