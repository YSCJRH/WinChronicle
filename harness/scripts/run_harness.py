from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


SEARCH_FIXTURES = [
    ("harness/fixtures/uia/terminal_error.json", "AssertionError"),
    ("harness/fixtures/uia/vscode_editor.json", "written_json"),
    ("harness/fixtures/uia/edge_browser.json", "OpenChronicle"),
]


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="winchronicle-harness-") as temp_dir:
        env = os.environ.copy()
        env["WINCHRONICLE_HOME"] = str(Path(temp_dir) / "state")

        commands = [
            [sys.executable, "-m", "pytest", "-q"],
            [
                "dotnet",
                "build",
                "resources/win-uia-helper/WinChronicle.UiaHelper.csproj",
                "--nologo",
            ],
            [
                "dotnet",
                "build",
                "resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj",
                "--nologo",
            ],
            [sys.executable, "harness/scripts/run_watcher_smoke.py"],
            [sys.executable, "harness/scripts/run_mcp_smoke.py"],
            [sys.executable, "-m", "winchronicle", "init"],
            [sys.executable, "-m", "winchronicle", "status"],
            [
                sys.executable,
                "-m",
                "winchronicle",
                "privacy-check",
                "harness/fixtures/privacy/secrets_visible_text.json",
            ],
        ]

        for command in commands:
            if _run(command, env) != 0:
                return 1

        for fixture, query in SEARCH_FIXTURES:
            if (
                _run(
                    [
                        sys.executable,
                        "-m",
                        "winchronicle",
                        "capture-once",
                        "--fixture",
                        fixture,
                    ],
                    env,
                )
                != 0
            ):
                return 1
            if _run([sys.executable, "-m", "winchronicle", "search-captures", query], env) != 0:
                return 1

        memory_commands = [
            [sys.executable, "-m", "winchronicle", "generate-memory", "--date", "2026-04-25"],
            [sys.executable, "-m", "winchronicle", "search-memory", "AssertionError"],
            [sys.executable, "-m", "winchronicle", "search-memory", "written_json"],
            [sys.executable, "-m", "winchronicle", "search-memory", "OpenChronicle"],
        ]
        for command in memory_commands:
            if _run(command, env) != 0:
                return 1

        watch_commands = [
            [
                sys.executable,
                "-m",
                "winchronicle",
                "watch",
                "--events",
                "harness/fixtures/watcher/notepad_burst.jsonl",
            ],
            [
                sys.executable,
                "-m",
                "winchronicle",
                "search-captures",
                "deterministic capture",
            ],
            [
                sys.executable,
                "-m",
                "winchronicle",
                "watch",
                "--watcher",
                "dotnet",
                "--watcher-arg",
                "resources/win-uia-watcher/bin/Debug/net8.0-windows/win-uia-watcher.dll",
                "--helper",
                sys.executable,
                "--helper-arg",
                "harness/scripts/fake_uia_helper.py",
                "--duration",
                "1",
                "--heartbeat-ms",
                "250",
                "--capture-on-start",
            ],
        ]
        for command in watch_commands:
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
