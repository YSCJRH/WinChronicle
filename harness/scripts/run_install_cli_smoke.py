from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import venv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SEARCH_RESULT_KEYS = {"timestamp", "app_name", "title", "snippet", "path"}


def main() -> int:
    try:
        with tempfile.TemporaryDirectory(prefix="winchronicle-install-cli-") as temp_dir:
            temp = Path(temp_dir)
            venv_dir = temp / "venv"
            state_home = temp / "state"

            print(f"Creating temporary virtual environment: {venv_dir}")
            venv.EnvBuilder(with_pip=True, system_site_packages=True, clear=True).create(venv_dir)
            python = _venv_python(venv_dir)

            env = os.environ.copy()
            env["WINCHRONICLE_HOME"] = str(state_home)
            env.pop("PYTHONPATH", None)

            _run(
                [
                    str(python),
                    "-m",
                    "pip",
                    "install",
                    "--disable-pip-version-check",
                    "--no-deps",
                    "-e",
                    str(ROOT),
                ],
                env=env,
            )

            help_text = _run([str(python), "-m", "winchronicle", "--help"], env=env)
            _require("capture-once" in help_text, "CLI help did not include capture-once")
            _require("search-memory" in help_text, "CLI help did not include search-memory")

            init_home = _run([str(python), "-m", "winchronicle", "init"], env=env).strip()
            _require(Path(init_home).resolve() == state_home.resolve(), "init used the wrong state home")

            status = json.loads(_run([str(python), "-m", "winchronicle", "status"], env=env))
            _require(status["db_exists"] is True, "status did not initialize SQLite")
            for key in (
                "screenshots_enabled",
                "ocr_enabled",
                "audio_enabled",
                "keyboard_capture_enabled",
            ):
                _require(status[key] is False, f"status reported enabled prohibited surface: {key}")

            capture_path = Path(
                _run(
                    [
                        str(python),
                        "-m",
                        "winchronicle",
                        "capture-once",
                        "--fixture",
                        str(ROOT / "harness" / "fixtures" / "uia" / "terminal_error.json"),
                    ],
                    env=env,
                ).strip()
            )
            _require(capture_path.is_file(), "capture-once did not write a capture artifact")
            _require(
                state_home.resolve() in capture_path.resolve().parents,
                "capture-once wrote outside the temporary state home",
            )

            capture_matches = json.loads(
                _run([str(python), "-m", "winchronicle", "search-captures", "AssertionError"], env=env)
            )
            _require(capture_matches, "search-captures did not find the fixture capture")
            _require(set(capture_matches[0]) == SEARCH_RESULT_KEYS, "search-captures JSON shape changed")
            _require(
                capture_matches[0]["app_name"] == "Windows Terminal",
                "search-captures returned the wrong fixture app",
            )

            generated = json.loads(
                _run(
                    [str(python), "-m", "winchronicle", "generate-memory", "--date", "2026-04-25"],
                    env=env,
                )
            )
            _require(generated, "generate-memory did not create entries")
            _require(
                {"event", "project", "tool"} <= {entry["entry_type"] for entry in generated},
                "generate-memory did not create event/project/tool entries",
            )
            for entry in generated:
                path = Path(entry["path"])
                _require(path.is_file(), f"generate-memory path does not exist: {path}")
                _require(
                    state_home.resolve() in path.resolve().parents,
                    "generate-memory wrote outside the temporary state home",
                )

            memory_matches = json.loads(
                _run([str(python), "-m", "winchronicle", "search-memory", "AssertionError"], env=env)
            )
            _require(memory_matches, "search-memory did not find generated memory")
            _require(
                "WinChronicle events for 2026-04-25"
                in {match["title"] for match in memory_matches},
                "search-memory did not return the deterministic event entry",
            )
    except SmokeFailure as exc:
        print(f"FAIL: {exc}")
        return 1

    print("PASS: install and CLI packaging smoke passed")
    return 0


def _venv_python(venv_dir: Path) -> Path:
    if os.name == "nt":
        return venv_dir / "Scripts" / "python.exe"
    return venv_dir / "bin" / "python"


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
    if completed.returncode:
        if completed.stdout:
            print(completed.stdout, end="" if completed.stdout.endswith("\n") else "\n")
        raise SmokeFailure(f"command failed with exit code {completed.returncode}: {display}")
    print("OK")
    return completed.stdout


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise SmokeFailure(message)


class SmokeFailure(RuntimeError):
    pass


if __name__ == "__main__":
    raise SystemExit(main())
