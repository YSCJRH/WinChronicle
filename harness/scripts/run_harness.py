from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_COMMAND_TIMEOUT_SECONDS = 900
COMMAND_TIMEOUT_ENV = "WINCHRONICLE_HARNESS_COMMAND_TIMEOUT_SECONDS"


SEARCH_FIXTURES = [
    ("harness/fixtures/uia/terminal_error.json", "AssertionError"),
    ("harness/fixtures/uia/vscode_editor.json", "written_json"),
    ("harness/fixtures/uia/edge_browser.json", "OpenChronicle"),
]

CONTRACT_COVERAGE = [
    {
        "id": "workday_dry_run_text_contracts",
        "command_index": 1,
        "spec": "harness/specs/workday-dry-run-text-contract.schema.json",
        "fixtures": [
            "harness/fixtures/workday/plugin_dry_run_text_contract.json",
            "harness/fixtures/workday/setup_dry_run_text_contract.json",
            "harness/fixtures/workday/daily_dry_run_text_contract.json",
        ],
        "tests": [
            "tests/test_cli.py::test_workday_dry_run_text_contract_fixtures_match_schema",
            "tests/test_cli.py::test_codex_plugin_dry_run_text_matches_golden_fixture_contract",
            "tests/test_cli.py::test_codex_setup_dry_run_text_matches_golden_fixture_contract",
            "tests/test_cli.py::test_codex_daily_dry_run_text_matches_golden_fixture_contract",
        ],
        "privacy_boundary": {
            "reads_desktop_expected": False,
            "forbids_desktop_yes_text": True,
            "observed_content": "not_read_by_dry_run",
        },
    },
    {
        "id": "workday_stop_summary_contract",
        "command_index": 1,
        "spec": "harness/specs/workday-stop-summary-contract.schema.json",
        "fixtures": [
            "harness/fixtures/workday/stop_human_summary_contract.json",
        ],
        "tests": [
            "tests/test_workday.py::test_workday_stop_summary_contract_fixture_matches_schema",
            "tests/test_workday.py::test_workday_summary_marker_contract_fixture_defines_human_and_technical_boundaries",
            "tests/test_workday.py::test_workday_stop_text_command_matches_human_summary_golden_fixture",
            "tests/test_workday.py::test_workday_stop_text_command_keeps_source_notice_in_technical_style",
            "tests/test_workday.py::test_workday_summarize_reads_named_session",
        ],
        "privacy_boundary": {
            "summary_level_evidence_only": True,
            "default_human_summary_hides_technical_markers": True,
            "technical_summary_explicit_only": True,
            "raw_observed_text_expected": False,
            "adds_capture_source": False,
        },
    },
    {
        "id": "mcp_read_only_metadata_contracts",
        "command_index": 1,
        "spec": "harness/specs/mcp-tool-result.schema.json",
        "tests": [
            "tests/test_compatibility_contracts.py::test_mcp_result_schema_tool_enum_matches_exact_read_only_contract",
            "tests/test_compatibility_contracts.py::test_mcp_result_schema_requires_external_sharing_limitation",
            "tests/test_compatibility_contracts.py::test_mcp_result_schema_rejects_metadata_only_policy_mismatches",
            "tests/test_compatibility_contracts.py::test_mcp_result_schema_binds_observed_text_omitted_limitation_to_metadata_only",
            "tests/test_mcp_tools.py::test_mcp_tool_results_include_evidence_policy_matrix",
            "tests/test_mcp_tools.py::test_mcp_metadata_only_mode_omits_observed_text_without_tool_list_change",
            "tests/test_mcp_tools.py::test_mcp_metadata_only_redacts_retained_observed_metadata_fields",
        ],
        "tools": [
            "current_context",
            "search_captures",
            "search_memory",
            "read_recent_capture",
            "recent_activity",
            "privacy_status",
        ],
        "privacy_boundary": {
            "read_only_mcp_expected": True,
            "metadata_only_available": True,
            "observed_text_omitted_when_metadata_only": True,
            "provenance": "local_winchronicle_state",
            "confidence_meaning": "coverage_quality_not_permission",
            "external_sharing_requires_user_approval": True,
        },
    },
]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the deterministic WinChronicle harness.")
    parser.add_argument(
        "--list-commands",
        action="store_true",
        help="Print the harness command plan without running commands.",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default=None,
        help="Output format for --list-commands.",
    )
    args = parser.parse_args([] if argv is None else argv)

    commands = _harness_commands()
    if args.list_commands:
        output_format = args.format or "text"
        if output_format == "json":
            _print_command_plan_json(commands)
        else:
            _print_command_plan(commands)
        return 0
    if args.format is not None:
        parser.error("--format is only valid with --list-commands")

    with tempfile.TemporaryDirectory(prefix="winchronicle-harness-") as temp_dir:
        env = os.environ.copy()
        env["WINCHRONICLE_HOME"] = str(Path(temp_dir) / "state")

        for command in commands:
            if _run(command, env) != 0:
                return 1

    print("WinChronicle harness passed.")
    return 0


def _harness_commands() -> list[list[str]]:
    commands = [
        [sys.executable, "-m", "pytest", "-q"],
        [
            sys.executable,
            "harness/scripts/check_release_evidence.py",
            "docs/release-v0.2.0.md",
        ],
        [
            sys.executable,
            "harness/scripts/check_release_evidence.py",
            "--project",
            "pyproject.toml",
            "--require-release-state",
            "docs/release-evidence.md",
        ],
        [
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
        ],
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
        [sys.executable, "harness/scripts/run_quick_demo.py"],
        [sys.executable, "harness/scripts/run_productization_self_eval.py"],
        [sys.executable, "harness/scripts/run_watcher_smoke.py"],
        [sys.executable, "harness/scripts/run_watcher_slow_helper_smoke.py"],
        [sys.executable, "harness/scripts/run_mcp_smoke.py"],
        [sys.executable, "harness/scripts/run_install_cli_smoke.py"],
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

    for fixture, query in SEARCH_FIXTURES:
        commands.append(
            [
                sys.executable,
                "-m",
                "winchronicle",
                "capture-once",
                "--fixture",
                fixture,
            ]
        )
        commands.append([sys.executable, "-m", "winchronicle", "search-captures", query])

    commands.extend(
        [
            [sys.executable, "-m", "winchronicle", "generate-memory", "--date", "2026-04-25"],
            [sys.executable, "-m", "winchronicle", "search-memory", "AssertionError"],
            [sys.executable, "-m", "winchronicle", "search-memory", "written_json"],
            [sys.executable, "-m", "winchronicle", "search-memory", "OpenChronicle"],
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
    )
    return commands


def _print_command_plan(commands: list[list[str]]) -> None:
    print("WinChronicle harness command plan:")
    print("No commands were run.")
    for index, command in enumerate(commands, start=1):
        print(f"{index}. {_display_command(command)}")


def _print_command_plan_json(commands: list[list[str]]) -> None:
    json.dump(_command_plan_payload(commands), sys.stdout, indent=2)
    print()


def _command_plan_payload(commands: list[list[str]]) -> dict[str, object]:
    return {
        "schema": "winchronicle.harness.command_plan.v1",
        "execution": "not_run",
        "privacy": {
            "creates_harness_state": False,
            "starts_subprocesses": False,
            "reads_observed_content": False,
        },
        "command_count": len(commands),
        "contract_coverage": CONTRACT_COVERAGE,
        "commands": [
            {
                "index": index,
                "argv": command,
                "display": _display_command(command),
            }
            for index, command in enumerate(commands, start=1)
        ],
    }


def _run(
    command: list[str],
    env: dict[str, str],
    timeout_seconds: int | None = None,
) -> int:
    display = _display_command(command)
    print(f"\n$ {display}")
    timeout_seconds = timeout_seconds or _command_timeout_seconds()
    try:
        completed = subprocess.run(
            command,
            cwd=ROOT,
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=timeout_seconds,
        )
    except subprocess.TimeoutExpired:
        print(f"Command timed out after {timeout_seconds}s: {display}")
        return 1
    if completed.stdout:
        print(completed.stdout, end="" if completed.stdout.endswith("\n") else "\n")
    if completed.returncode:
        print(f"Command failed with exit code {completed.returncode}: {display}")
    return completed.returncode


def _display_command(command: list[str]) -> str:
    return " ".join(command)


def _command_timeout_seconds() -> int:
    raw = os.environ.get(COMMAND_TIMEOUT_ENV)
    if raw is None:
        return DEFAULT_COMMAND_TIMEOUT_SECONDS
    try:
        value = int(raw)
    except ValueError:
        return DEFAULT_COMMAND_TIMEOUT_SECONDS
    return value if value > 0 else DEFAULT_COMMAND_TIMEOUT_SECONDS


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
