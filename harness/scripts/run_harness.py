from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="winchronicle-harness-") as temp_dir:
        env = os.environ.copy()
        env["WINCHRONICLE_HOME"] = str(Path(temp_dir) / "state")

        commands = [
            [sys.executable, "-m", "pytest", "-q"],
            [sys.executable, "-m", "winchronicle", "init"],
            [sys.executable, "-m", "winchronicle", "status"],
            [
                sys.executable,
                "-m",
                "winchronicle",
                "capture-once",
                "--fixture",
                "harness/fixtures/uia/terminal_error.json",
            ],
            [
                sys.executable,
                "-m",
                "winchronicle",
                "privacy-check",
                "harness/fixtures/privacy/secrets_visible_text.json",
            ],
            [sys.executable, "-m", "winchronicle", "search-captures", "AssertionError"],
        ]

        for command in commands:
            if _run(command, env) != 0:
                return 1

    print("WinChronicle harness passed.")
    return 0


def _run(command: list[str], env: dict[str, str]) -> int:
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
        print(f"Command failed with exit code {completed.returncode}: {display}")
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
