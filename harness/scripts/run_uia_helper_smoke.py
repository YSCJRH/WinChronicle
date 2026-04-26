from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="run_uia_helper_smoke.py",
        description="Run a temporary capture-frontmost smoke without printing observed content.",
    )
    parser.add_argument("--helper", required=True, help="Path or command for win-uia-helper.")
    parser.add_argument(
        "--helper-arg",
        action="append",
        default=[],
        help="Extra argument passed to the helper command before capture-frontmost.",
    )
    parser.add_argument("--depth", type=int, default=2)
    parser.add_argument(
        "--delay-seconds",
        type=float,
        default=0,
        help="Wait before capture so a human can focus the target app.",
    )
    parser.add_argument("--expect-app", help="Substring expected in app/process/window metadata.")
    parser.add_argument("--expect-text", help="Substring expected in visible or focused text.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.delay_seconds < 0:
        print("FAIL: delay-seconds must be non-negative")
        return 1

    with tempfile.TemporaryDirectory(prefix="winchronicle-uia-smoke-") as temp_dir:
        env = os.environ.copy()
        env["WINCHRONICLE_HOME"] = str(Path(temp_dir) / "state")
        command = [
            sys.executable,
            "-m",
            "winchronicle",
            "capture-frontmost",
            "--helper",
            args.helper,
            "--depth",
            str(args.depth),
        ]
        for helper_arg in args.helper_arg:
            command.extend(["--helper-arg", helper_arg])

        if args.delay_seconds:
            time.sleep(args.delay_seconds)

        completed = subprocess.run(
            command,
            cwd=ROOT,
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        if completed.returncode:
            print("FAIL: capture-frontmost command failed")
            return completed.returncode

        output = completed.stdout.strip()
        if output.startswith("SKIPPED:"):
            if args.expect_app or args.expect_text:
                print("FAIL: capture skipped before expected content could be checked")
                return 1
            print("PASS: capture skipped")
            return 0

        capture_path = Path(output)
        if not capture_path.exists():
            print("FAIL: capture path was not written")
            return 1

        privacy = subprocess.run(
            [sys.executable, "-m", "winchronicle", "privacy-check", str(capture_path)],
            cwd=ROOT,
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        if privacy.returncode:
            print("FAIL: privacy-check failed")
            return privacy.returncode

        capture = json.loads(capture_path.read_text(encoding="utf-8"))
        if args.expect_app and args.expect_app.lower() not in _metadata_text(capture).lower():
            print("FAIL: expected app metadata was not found")
            return 1
        if args.expect_text and args.expect_text.lower() not in _observed_text(capture).lower():
            print("FAIL: expected observed text was not found")
            return 1

    print("PASS: UIA helper smoke passed")
    return 0


def _metadata_text(capture: dict[str, object]) -> str:
    window = capture.get("window_meta", {})
    if not isinstance(window, dict):
        return ""
    values = [
        window.get("app_name"),
        window.get("process_name"),
        window.get("title"),
    ]
    return " ".join(str(value or "") for value in values)


def _observed_text(capture: dict[str, object]) -> str:
    focused = capture.get("focused_element", {})
    values: list[object | None] = [capture.get("visible_text")]
    if isinstance(focused, dict):
        values.extend([focused.get("text"), focused.get("value")])
    return " ".join(str(value or "") for value in values)


if __name__ == "__main__":
    raise SystemExit(main())
