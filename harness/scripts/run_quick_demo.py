from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DISABLED_SURFACE_KEYS = (
    "screenshots_enabled",
    "ocr_enabled",
    "audio_enabled",
    "keyboard_capture_enabled",
    "clipboard_capture_enabled",
    "network_upload_enabled",
    "cloud_upload_enabled",
    "llm_calls_enabled",
    "desktop_control_enabled",
    "product_targeted_capture_enabled",
    "mcp_write_tools_enabled",
)


def main() -> int:
    try:
        with tempfile.TemporaryDirectory(prefix="winchronicle-quick-demo-") as temp_dir:
            state_home = Path(temp_dir) / "state"
            env = os.environ.copy()
            env["WINCHRONICLE_HOME"] = str(state_home)

            winchronicle = [sys.executable, "-m", "winchronicle"]
            helper = ROOT / "harness" / "scripts" / "fake_uia_helper.py"
            watcher = (
                ROOT
                / "resources"
                / "win-uia-watcher"
                / "bin"
                / "Debug"
                / "net8.0-windows"
                / "win-uia-watcher.dll"
            )

            _run([*winchronicle, "init"], env=env)

            status = json.loads(_run([*winchronicle, "status"], env=env))
            _require(status["db_exists"] is True, "status did not initialize SQLite")
            _require_disabled_surfaces(status, "status")

            doctor = json.loads(_run([*winchronicle, "doctor"], env=env))
            _require(doctor["command"] == "doctor", "doctor did not report its command")
            _require_disabled_surfaces(doctor, "doctor")
            _require(
                any(check["name"] == "sqlite" and check["ok"] for check in doctor["checks"]),
                "doctor did not report usable SQLite",
            )

            fixture_capture = Path(
                _run(
                    [
                        *winchronicle,
                        "capture-once",
                        "--fixture",
                        str(ROOT / "harness" / "fixtures" / "uia" / "terminal_error.json"),
                    ],
                    env=env,
                ).strip()
            )
            _require(fixture_capture.is_file(), "fixture capture did not write an artifact")
            _require(
                state_home.resolve() in fixture_capture.resolve().parents,
                "fixture capture wrote outside temporary state",
            )

            matches = json.loads(_run([*winchronicle, "search-captures", "AssertionError"], env=env))
            _require(matches and matches[0]["app_name"] == "Windows Terminal", "fixture search failed")

            frontmost_capture = Path(
                _run(
                    [
                        *winchronicle,
                        "capture-frontmost",
                        "--helper",
                        sys.executable,
                        "--helper-arg",
                        str(helper),
                        "--depth",
                        "2",
                    ],
                    env=env,
                ).strip()
            )
            _require(frontmost_capture.is_file(), "fake-helper capture did not write an artifact")
            _require(
                state_home.resolve() in frontmost_capture.resolve().parents,
                "fake-helper capture wrote outside temporary state",
            )

            helper_matches = json.loads(
                _run([*winchronicle, "search-captures", "helper contract"], env=env)
            )
            _require(helper_matches and helper_matches[0]["app_name"] == "Notepad", "fake-helper search failed")

            _require(watcher.exists(), f"watcher DLL is missing; build it first: {watcher}")
            session = json.loads(
                _run(
                    [
                        *winchronicle,
                        "monitor",
                        "--watcher",
                        "dotnet",
                        "--watcher-arg",
                        str(watcher),
                        "--helper",
                        sys.executable,
                        "--helper-arg",
                        str(helper),
                        "--duration",
                        "1",
                        "--heartbeat-ms",
                        "250",
                        "--capture-on-start",
                        "--session-id",
                        "quick-demo",
                    ],
                    env=env,
                )
            )
            _require(session["session_id"] == "quick-demo", "monitor session id changed")
            _require(Path(session["path"]).is_file(), "monitor session JSON was not written")
            _require(Path(session["report_path"]).is_file(), "monitor HTML report was not written")

            summary = json.loads(_run([*winchronicle, "summarize-session", "quick-demo"], env=env))
            _require(summary["session_id"] == "quick-demo", "summarize-session returned the wrong session")

            _run([sys.executable, "harness/scripts/run_mcp_smoke.py"], env=env)
    except DemoFailure as exc:
        print(f"FAIL: {exc}")
        return 1

    print("PASS: quick demo passed")
    return 0


def _run(command: list[str], *, env: dict[str, str]) -> str:
    display = " ".join(command)
    print(f"\n$ {display}")
    completed = subprocess.run(
        command,
        cwd=ROOT,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if completed.stdout:
        print(completed.stdout, end="" if completed.stdout.endswith("\n") else "\n")
    if completed.returncode:
        raise DemoFailure(f"command failed with exit code {completed.returncode}: {display}")
    return completed.stdout


def _require_disabled_surfaces(payload: dict[str, object], source: str) -> None:
    for key in DISABLED_SURFACE_KEYS:
        _require(payload[key] is False, f"{source} reported enabled prohibited surface: {key}")


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise DemoFailure(message)


class DemoFailure(RuntimeError):
    pass


if __name__ == "__main__":
    raise SystemExit(main())
