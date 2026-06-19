import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "windows-harness.yml"
CONTRIBUTING = ROOT / "CONTRIBUTING.md"
HARNESS_README = ROOT / "harness" / "README.md"
INSTALL_CLI_SMOKE = ROOT / "harness" / "scripts" / "run_install_cli_smoke.py"
RUN_HARNESS = ROOT / "harness" / "scripts" / "run_harness.py"


def _load_script(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_windows_harness_uses_current_windows_runner_without_gate_drift():
    text = WORKFLOW.read_text(encoding="utf-8")

    assert 'FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: "true"' in text
    assert "runs-on: windows-2025-vs2026" in text
    assert "runs-on: windows-latest" not in text
    assert "uses: actions/checkout@v6" in text
    assert "uses: actions/setup-python@v6" in text
    assert "uses: actions/setup-dotnet@v5" in text
    assert text.count("timeout-minutes:") >= 6

    expected_steps = (
        "Check out repository",
        "Set up Python",
        "Set up .NET",
        "Install Python package",
        "Run unit tests",
        "Build UIA helper",
        "Build UIA watcher",
        "Run deterministic harness",
        "Check whitespace",
    )
    positions = [text.index(f"- name: {step}") for step in expected_steps]

    assert positions == sorted(positions)
    assert 'run: python -m pytest -q' in text
    assert (
        "run: dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo"
        in text
    )
    assert (
        "run: dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo"
        in text
    )
    assert "run: python harness/scripts/run_harness.py" in text
    assert "run: git diff --check" in text
    for command in (
        'python -m pip install -e ".[dev]"',
        "python -m pytest -q",
        "dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo",
        "dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo",
        "python harness/scripts/run_harness.py",
        "git diff --check",
    ):
        command_index = text.index(f"run: {command}")
        next_step_index = text.find("\n      - name:", command_index + 1)
        step_text = text[command_index:] if next_step_index == -1 else text[command_index:next_step_index]
        assert "timeout-minutes:" in step_text


def test_contributing_documents_harness_timeout_policy():
    text = CONTRIBUTING.read_text(encoding="utf-8")
    normalized = " ".join(text.split())

    assert "### Harness Timeout Policy" in text
    assert "900 seconds per subprocess" in normalized
    assert "WINCHRONICLE_HARNESS_COMMAND_TIMEOUT_SECONDS" in text
    assert "300 seconds per subprocess" in normalized
    assert "WINCHRONICLE_INSTALL_CLI_SMOKE_COMMAND_TIMEOUT_SECONDS" in text
    assert "timeout-minutes" in text
    assert "do not print partial stdout or stderr" in normalized
    assert "observed content" in normalized
    assert "does not authorize new capture surfaces" in normalized
    assert "screenshots, OCR, clipboard capture, cloud upload" in normalized


def test_harness_readme_documents_timeout_defaults_and_ci_budget():
    text = HARNESS_README.read_text(encoding="utf-8")
    normalized = " ".join(text.split())

    assert "## Harness Timeouts" in text
    assert "900 seconds per subprocess" in normalized
    assert "WINCHRONICLE_HARNESS_COMMAND_TIMEOUT_SECONDS" in text
    assert "300 seconds per subprocess" in normalized
    assert "WINCHRONICLE_INSTALL_CLI_SMOKE_COMMAND_TIMEOUT_SECONDS" in text
    assert "30-minute outer timeout" in normalized
    assert "do not print partial stdout or stderr" in normalized
    assert "observed content" in normalized
    assert "does not expand capture surfaces" in normalized
    assert "static release-evidence validator" in normalized
    assert "manual-smoke freshness validator" in normalized
    assert "does not call GitHub" in normalized
    assert "python harness/scripts/run_harness.py --list-commands" in normalized
    assert "python harness/scripts/run_harness.py --list-commands --format json" in normalized
    assert "does not create harness state, start subprocesses, or read observed content" in normalized


def test_install_cli_smoke_covers_workday_intent_dry_run():
    text = INSTALL_CLI_SMOKE.read_text(encoding="utf-8")

    assert '"workday", "intent", "开始记录工作"' in text
    assert '"dry_run_by_default"' in text
    assert '"local_workday_intent_mapping"' in text
    assert '"workday-active.json"' in text


def test_install_cli_smoke_covers_codex_text_format_entrypoints():
    text = INSTALL_CLI_SMOKE.read_text(encoding="utf-8")

    assert '"codex", "setup", "--dry-run", "--format", "text"' in text
    assert '"codex", "plugin", "--dry-run", "--format", "text"' in text
    assert '"codex", "daily", "--dry-run", "--format", "text"' in text
    assert '"WinChronicle Codex setup dry-run"' in text
    assert '"WinChronicle Codex plugin dry-run"' in text
    assert '"WinChronicle Codex daily dry-run"' in text
    assert '"Fast path for Codex App:"' in text
    assert '"In a Codex App thread, say:"' in text
    assert '"开始记录工作"' in text
    assert '"Safety boundary:"' in text
    assert '"Disabled surfaces remain off:"' in text
    assert '"First prompt to try: 开始记录工作"' in text


def test_run_harness_times_out_subprocess_with_diagnostic(monkeypatch, capsys):
    run_harness = _load_script(RUN_HARNESS)

    def timeout_run(command, *_args, **kwargs):
        assert kwargs["timeout"] == 7
        raise subprocess.TimeoutExpired(
            command,
            timeout=7,
            output="SECRET_CANARY partial stdout\n",
            stderr="SECRET_CANARY partial stderr\n",
        )

    monkeypatch.setattr(run_harness.subprocess, "run", timeout_run)

    assert run_harness._run(["slow-command"], env={}, timeout_seconds=7) == 1

    output = capsys.readouterr().out
    assert "SECRET_CANARY" not in output
    assert "Command timed out after 7s: slow-command" in output


def test_run_harness_includes_static_release_validators(monkeypatch):
    run_harness = _load_script(RUN_HARNESS)
    commands = []

    def record_run(command, _env):
        commands.append(command)
        return 0

    monkeypatch.setattr(run_harness, "_run", record_run)

    assert run_harness.main() == 0

    assert [
        sys.executable,
        "harness/scripts/check_release_evidence.py",
        "docs/release-v0.2.0.md",
    ] in commands
    assert [
        sys.executable,
        "harness/scripts/check_manual_smoke_freshness.py",
        "--project",
        "pyproject.toml",
        "--ledger",
        "docs/manual-smoke-evidence-ledger.md",
        "--guide",
        "docs/release-evidence.md",
        "--checklist",
        "docs/release-checklist.md",
    ] in commands


def test_run_harness_lists_commands_without_running(monkeypatch, capsys):
    run_harness = _load_script(RUN_HARNESS)

    def fail_run(*_args, **_kwargs):
        raise AssertionError("--list-commands must not run harness commands")

    monkeypatch.setattr(run_harness, "_run", fail_run)

    assert run_harness.main(["--list-commands"]) == 0

    output = capsys.readouterr().out
    assert "WinChronicle harness command plan" in output
    assert "No commands were run." in output
    assert "1. " in output
    assert "python.exe -m pytest -q" in output or "python -m pytest -q" in output
    assert "harness/scripts/check_release_evidence.py docs/release-v0.2.0.md" in output
    assert "harness/scripts/check_manual_smoke_freshness.py" in output
    assert "dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo" in output
    assert "harness/scripts/run_install_cli_smoke.py" in output
    assert "-m winchronicle privacy-check harness/fixtures/privacy/secrets_visible_text.json" in output
    assert "-m winchronicle watch --events harness/fixtures/watcher/notepad_burst.jsonl" in output
    assert output.index("-m pytest -q") < output.index("harness/scripts/check_release_evidence.py")
    assert output.index("harness/scripts/run_install_cli_smoke.py") < output.index(
        "-m winchronicle init"
    )


def test_run_harness_lists_commands_as_json_without_running(monkeypatch, capsys):
    run_harness = _load_script(RUN_HARNESS)

    def fail_run(*_args, **_kwargs):
        raise AssertionError("--list-commands --format json must not run harness commands")

    monkeypatch.setattr(run_harness, "_run", fail_run)

    assert run_harness.main(["--list-commands", "--format", "json"]) == 0

    output = capsys.readouterr().out
    plan = json.loads(output)

    assert plan["schema"] == "winchronicle.harness.command_plan.v1"
    assert plan["execution"] == "not_run"
    assert plan["privacy"] == {
        "creates_harness_state": False,
        "starts_subprocesses": False,
        "reads_observed_content": False,
    }
    assert plan["command_count"] == len(run_harness._harness_commands())
    assert plan["commands"][0] == {
        "index": 1,
        "argv": [sys.executable, "-m", "pytest", "-q"],
        "display": run_harness._display_command([sys.executable, "-m", "pytest", "-q"]),
    }
    assert plan["commands"] == [
        {
            "index": index,
            "argv": command,
            "display": run_harness._display_command(command),
        }
        for index, command in enumerate(run_harness._harness_commands(), start=1)
    ]


def test_run_harness_rejects_format_without_list_commands(monkeypatch, capsys):
    run_harness = _load_script(RUN_HARNESS)

    def fail_run(*_args, **_kwargs):
        raise AssertionError("--format without --list-commands must not run the harness")

    monkeypatch.setattr(run_harness, "_run", fail_run)

    with pytest.raises(SystemExit) as exc_info:
        run_harness.main(["--format", "json"])

    assert exc_info.value.code == 2
    assert "--format is only valid with --list-commands" in capsys.readouterr().err


def test_run_harness_command_plan_matches_executed_commands(monkeypatch):
    run_harness = _load_script(RUN_HARNESS)
    commands = []

    def record_run(command, _env):
        commands.append(command)
        return 0

    monkeypatch.setattr(run_harness, "_run", record_run)

    assert run_harness.main() == 0

    assert commands == run_harness._harness_commands()


def test_run_harness_uses_default_and_env_timeout(monkeypatch):
    run_harness = _load_script(RUN_HARNESS)
    seen_timeouts = []

    def ok_run(_command, *_args, **kwargs):
        seen_timeouts.append(kwargs["timeout"])
        return subprocess.CompletedProcess(_command, 0, stdout="")

    monkeypatch.setattr(run_harness.subprocess, "run", ok_run)
    monkeypatch.delenv(run_harness.COMMAND_TIMEOUT_ENV, raising=False)
    assert run_harness._run(["default-timeout"], env={}) == 0
    monkeypatch.setenv(run_harness.COMMAND_TIMEOUT_ENV, "13")
    assert run_harness._run(["env-timeout"], env={}) == 0
    monkeypatch.setenv(run_harness.COMMAND_TIMEOUT_ENV, "0")
    assert run_harness._run(["invalid-timeout"], env={}) == 0

    assert seen_timeouts == [
        run_harness.DEFAULT_COMMAND_TIMEOUT_SECONDS,
        13,
        run_harness.DEFAULT_COMMAND_TIMEOUT_SECONDS,
    ]


def test_install_cli_smoke_times_out_subprocess_with_smoke_failure(monkeypatch, capsys):
    install_smoke = _load_script(INSTALL_CLI_SMOKE)

    def timeout_run(command, *_args, **kwargs):
        assert kwargs["timeout"] == 11
        raise subprocess.TimeoutExpired(
            command,
            timeout=11,
            output="SECRET_CANARY partial install\n",
            stderr="SECRET_CANARY partial stderr\n",
        )

    monkeypatch.setattr(install_smoke.subprocess, "run", timeout_run)

    with pytest.raises(
        install_smoke.SmokeFailure,
        match="command timed out after 11s: slow install",
    ):
        install_smoke._run(["slow", "install"], env={}, timeout_seconds=11)

    assert "SECRET_CANARY" not in capsys.readouterr().out


def test_install_cli_smoke_uses_default_and_env_timeout(monkeypatch):
    install_smoke = _load_script(INSTALL_CLI_SMOKE)
    seen_timeouts = []

    def ok_run(_command, *_args, **kwargs):
        seen_timeouts.append(kwargs["timeout"])
        return subprocess.CompletedProcess(_command, 0, stdout="")

    monkeypatch.setattr(install_smoke.subprocess, "run", ok_run)
    monkeypatch.delenv(install_smoke.COMMAND_TIMEOUT_ENV, raising=False)
    install_smoke._run(["default-timeout"], env={})
    monkeypatch.setenv(install_smoke.COMMAND_TIMEOUT_ENV, "17")
    install_smoke._run(["env-timeout"], env={})
    monkeypatch.setenv(install_smoke.COMMAND_TIMEOUT_ENV, "not-an-int")
    install_smoke._run(["invalid-timeout"], env={})

    assert seen_timeouts == [
        install_smoke.DEFAULT_COMMAND_TIMEOUT_SECONDS,
        17,
        install_smoke.DEFAULT_COMMAND_TIMEOUT_SECONDS,
    ]
