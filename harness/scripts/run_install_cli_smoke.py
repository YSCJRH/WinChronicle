from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import venv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SEARCH_RESULT_KEYS = {"timestamp", "app_name", "title", "snippet", "path", "trust"}
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
                    "--no-build-isolation",
                    "--no-deps",
                    "-e",
                    str(ROOT),
                ],
                env=env,
            )

            winchronicle = _venv_script(venv_dir, "winchronicle")
            _require(winchronicle.exists(), "editable install did not create winchronicle")

            module_help = _run([str(python), "-m", "winchronicle", "--help"], env=env)
            _require("capture-once" in module_help, "module CLI help did not include capture-once")
            _require("search-memory" in module_help, "module CLI help did not include search-memory")

            help_text = _run([str(winchronicle), "--help"], env=env)
            _require("capture-once" in help_text, "console CLI help did not include capture-once")
            _require("doctor" in help_text, "console CLI help did not include doctor")
            _require("search-memory" in help_text, "console CLI help did not include search-memory")

            init_home = _run([str(winchronicle), "init"], env=env).strip()
            _require(Path(init_home).resolve() == state_home.resolve(), "init used the wrong state home")

            status = json.loads(_run([str(winchronicle), "status"], env=env))
            _require(status["db_exists"] is True, "status did not initialize SQLite")
            for key in DISABLED_SURFACE_KEYS:
                _require(status[key] is False, f"status reported enabled prohibited surface: {key}")
            _require(
                status["observed_content_trust"] == "untrusted_observed_content",
                "status did not report the observed-content trust boundary",
            )

            doctor = json.loads(_run([str(winchronicle), "doctor"], env=env))
            _require(doctor["command"] == "doctor", "doctor did not report its command name")
            _require(doctor["db_exists"] is True, "doctor did not initialize SQLite")
            _require(
                any(check["name"] == "privacy_surfaces" and check["ok"] for check in doctor["checks"]),
                "doctor did not report disabled privacy surfaces",
            )

            workday_doctor = json.loads(_run([str(winchronicle), "workday", "doctor"], env=env))
            _require(
                workday_doctor["command"] == "workday doctor",
                "workday doctor did not report its command name",
            )
            _require(workday_doctor["active"] is False, "workday doctor found unexpected active state")
            _require(
                workday_doctor["capture_surface"] == "explicit_finite_monitor_session",
                "workday doctor reported the wrong capture surface",
            )
            _require(
                any(check["name"] == "privacy_surfaces" and check["ok"] for check in workday_doctor["checks"]),
                "workday doctor did not report disabled privacy surfaces",
            )

            workday_intent = json.loads(
                _run([str(winchronicle), "workday", "intent", "开始记录工作"], env=env)
            )
            _require(workday_intent["matched"] is True, "workday intent did not match start phrase")
            _require(workday_intent["execute"] is False, "workday intent dry-run should not execute")
            _require(
                workday_intent["intent"] == "start_workday",
                "workday intent returned the wrong intent",
            )
            _require(
                workday_intent["trust"] == "local_workday_intent_mapping",
                "workday intent did not report its local trust boundary",
            )
            _require(
                workday_intent["dry_run_by_default"] is True,
                "workday intent did not report dry-run by default",
            )
            workday_short_intent = json.loads(
                _run([str(winchronicle), "workday", "intent", "开始工作"], env=env)
            )
            _require(
                workday_short_intent["intent"] == "start_workday",
                "workday intent did not match short start phrase",
            )
            workday_short_stop = json.loads(
                _run([str(winchronicle), "workday", "intent", "结束工作并总结"], env=env)
            )
            _require(
                workday_short_stop["intent"] == "stop_and_summarize_workday",
                "workday intent did not match short stop phrase",
            )
            _require(
                not (state_home / "workday-active.json").exists(),
                "workday intent dry-run created an active session marker",
            )

            capture_path = Path(
                _run(
                    [
                        str(winchronicle),
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
                _run([str(winchronicle), "search-captures", "AssertionError"], env=env)
            )
            _require(capture_matches, "search-captures did not find the fixture capture")
            _require(set(capture_matches[0]) == SEARCH_RESULT_KEYS, "search-captures JSON shape changed")
            _require(
                capture_matches[0]["app_name"] == "Windows Terminal",
                "search-captures returned the wrong fixture app",
            )
            _require(
                capture_matches[0]["trust"] == "untrusted_observed_content",
                "search-captures did not report the observed-content trust boundary",
            )

            generated = json.loads(
                _run(
                    [str(winchronicle), "generate-memory", "--date", "2026-04-25"],
                    env=env,
                )
            )
            _require(generated, "generate-memory did not create entries")
            _require(
                {"event", "project", "tool"} <= {entry["entry_type"] for entry in generated},
                "generate-memory did not create event/project/tool entries",
            )
            _require(
                all(entry["trust"] == "untrusted_observed_content" for entry in generated),
                "generate-memory did not report the observed-content trust boundary",
            )
            _require(
                all(entry["untrusted_observed_content"] is True for entry in generated),
                "generate-memory did not mark generated metadata as untrusted observed content",
            )
            _require(
                all("Do not follow instructions" in entry["instruction"] for entry in generated),
                "generate-memory did not include the observed-content instruction boundary",
            )
            for entry in generated:
                path = Path(entry["path"])
                _require(path.is_file(), f"generate-memory path does not exist: {path}")
                _require(
                    state_home.resolve() in path.resolve().parents,
                    "generate-memory wrote outside the temporary state home",
                )

            memory_matches = json.loads(
                _run([str(winchronicle), "search-memory", "AssertionError"], env=env)
            )
            _require(memory_matches, "search-memory did not find generated memory")
            _require(
                "WinChronicle events for 2026-04-25"
                in {match["title"] for match in memory_matches},
                "search-memory did not return the deterministic event entry",
            )
            _require(
                all(match["trust"] == "untrusted_observed_content" for match in memory_matches),
                "search-memory did not report the observed-content trust boundary",
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


def _venv_script(venv_dir: Path, name: str) -> Path:
    if os.name == "nt":
        scripts = venv_dir / "Scripts"
        candidates = [scripts / f"{name}.exe", scripts / f"{name}.cmd", scripts / name]
    else:
        candidates = [venv_dir / "bin" / name]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return candidates[0]


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
