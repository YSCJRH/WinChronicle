import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "windows-harness.yml"
CONTRIBUTING = ROOT / "CONTRIBUTING.md"
HARNESS_FIRST_TASK_TEMPLATE = ROOT / ".github" / "ISSUE_TEMPLATE" / "harness_first_task.yml"
PULL_REQUEST_TEMPLATE = ROOT / ".github" / "pull_request_template.md"
HARNESS_README = ROOT / "harness" / "README.md"
HARNESS_COMMAND_PLAN_SCHEMA = ROOT / "harness" / "specs" / "harness-command-plan.schema.json"
INSTALL_CLI_SMOKE = ROOT / "harness" / "scripts" / "run_install_cli_smoke.py"
RUN_HARNESS = ROOT / "harness" / "scripts" / "run_harness.py"
CONTRACT_COVERAGE_DOCUMENTATION_SECTION = "Command Plan Contract Coverage"
CONTRACT_COVERAGE_JSON_PLAN_COMMAND = (
    "python harness/scripts/run_harness.py --list-commands --format json"
)
CONTRACT_COVERAGE_INTEGRITY_TEST_NODE = (
    "tests/test_windows_harness_workflow.py::"
    "test_run_harness_json_contract_coverage_integrity_runs_all_gates"
)
CONTRACT_COVERAGE_INTEGRITY_TEST_COMMAND = (
    f"python -m pytest {CONTRACT_COVERAGE_INTEGRITY_TEST_NODE} -q"
)
CONTRACT_COVERAGE_ENTRY_MAINTENANCE_RULE = (
    "New `contract_coverage` entries must update the README navigation, "
    "the Current coverage examples table, the JSON command plan, and at "
    "least one focused pytest node in the same change."
)


def _load_script(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _normalize_pytest_node_id(node_id: str) -> str:
    return node_id.strip().replace("\\", "/")


def _assert_contract_coverage_pytest_nodes_exist(node_ids: list[str]) -> None:
    assert node_ids, "contract_coverage pytest nodes are required"
    completed = subprocess.run(
        [sys.executable, "-m", "pytest", "--collect-only", "-q", *node_ids],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=60,
    )
    output = completed.stdout or ""
    collected = {
        _normalize_pytest_node_id(line)
        for line in output.splitlines()
        if "::" in line and line.strip().startswith("tests")
    }
    missing = [
        node_id
        for node_id in node_ids
        if _normalize_pytest_node_id(node_id) not in collected
    ]
    if completed.returncode != 0 or missing:
        missing_text = "\n".join(missing) if missing else "(pytest collection failed)"
        raise AssertionError(
            "Missing contract_coverage pytest nodes:\n"
            f"{missing_text}\n\npytest output:\n{output}"
        )


def _contract_coverage_artifact_paths(entry: dict[str, object]) -> list[str]:
    paths = []
    spec = entry.get("spec")
    if isinstance(spec, str):
        paths.append(spec)
    fixtures = entry.get("fixtures")
    if isinstance(fixtures, list):
        paths.extend(path for path in fixtures if isinstance(path, str))
    return paths


def _assert_contract_coverage_artifact_paths_exist(
    coverage_entries: list[dict[str, object]]
) -> None:
    assert coverage_entries, "contract_coverage artifact paths are required"
    missing = []
    unsafe = []
    for entry in coverage_entries:
        entry_id = str(entry.get("id", "<unknown>"))
        for path_text in _contract_coverage_artifact_paths(entry):
            path = Path(path_text)
            if path.is_absolute() or ".." in path.parts:
                unsafe.append(f"{entry_id}: {path_text}")
                continue
            if not (ROOT / path).is_file():
                missing.append(f"{entry_id}: {path_text}")

    if missing or unsafe:
        details = []
        if missing:
            details.append("missing:\n" + "\n".join(missing))
        if unsafe:
            details.append("unsafe:\n" + "\n".join(unsafe))
        raise AssertionError(
            "Invalid contract_coverage artifact paths:\n" + "\n\n".join(details)
        )


# Keep command-plan coverage checks together so new contract_coverage entries
# pass through schema, pytest-node, and artifact-path gates.
def _assert_command_plan_contract_coverage_integrity(plan: dict[str, object]) -> None:
    schema = json.loads(HARNESS_COMMAND_PLAN_SCHEMA.read_text(encoding="utf-8"))
    Draft202012Validator(schema).validate(plan)

    commands = plan["commands"]
    command_count = plan["command_count"]
    coverage = plan["contract_coverage"]
    assert isinstance(commands, list)
    assert isinstance(command_count, int)
    assert isinstance(coverage, list)
    assert command_count == len(commands)
    assert len({item["id"] for item in coverage}) == len(coverage)

    node_ids = []
    for item in coverage:
        assert 1 <= item["command_index"] <= command_count
        assert commands[item["command_index"] - 1]["index"] == item["command_index"]
        assert item["tests"]
        assert all("::" in test_id for test_id in item["tests"])
        assert item["privacy_boundary"]
        node_ids.extend(item["tests"])

    _assert_contract_coverage_pytest_nodes_exist(node_ids)
    _assert_contract_coverage_artifact_paths_exist(coverage)


def _assert_contract_coverage_validation_prompt(surface: str, text: str) -> None:
    normalized = " ".join(text.split())

    assert "`contract_coverage`" in text, surface
    assert CONTRACT_COVERAGE_DOCUMENTATION_SECTION in text, surface
    assert "schema, pytest-node, and artifact-path gates" in normalized, surface
    if surface == "CONTRIBUTING.md":
        assert CONTRACT_COVERAGE_JSON_PLAN_COMMAND in text, surface
        assert CONTRACT_COVERAGE_INTEGRITY_TEST_COMMAND in text, surface
        assert CONTRACT_COVERAGE_INTEGRITY_TEST_NODE in text, surface
    else:
        assert "CONTRIBUTING.md" in text, surface
        assert "instead of copying its commands here" in text, surface


def _assert_contract_coverage_entry_maintenance_rule(surface: str, text: str) -> None:
    normalized = " ".join(text.split())

    assert CONTRACT_COVERAGE_ENTRY_MAINTENANCE_RULE in normalized, surface


def _markdown_section(text: str, heading: str) -> str:
    marker = f"## {heading}"
    start = text.index(marker)
    next_heading = text.find("\n## ", start + len(marker))
    return text[start:] if next_heading == -1 else text[start:next_heading]


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


def test_contributing_documents_command_plan_contract_coverage_gate():
    text = CONTRIBUTING.read_text(encoding="utf-8")
    normalized = " ".join(text.split())

    _assert_contract_coverage_validation_prompt("CONTRIBUTING.md", text)
    assert f"### {CONTRACT_COVERAGE_DOCUMENTATION_SECTION}" in text
    assert "harness/specs/harness-command-plan.schema.json" in text
    assert (
        "When adding a coverage entry, update its `spec`, `fixtures`, `tests`, "
        "and `privacy_boundary` anchors together."
        in normalized
    )
    _assert_contract_coverage_entry_maintenance_rule("CONTRIBUTING.md", text)


def test_contributing_documents_contract_coverage_entry_examples():
    text = CONTRIBUTING.read_text(encoding="utf-8")
    section_start = text.index(f"### {CONTRACT_COVERAGE_DOCUMENTATION_SECTION}")
    section_end = text.index(
        "Run the standard deterministic validation set", section_start
    )
    section = text[section_start:section_end]
    run_harness = _load_script(RUN_HARNESS)

    assert "Current coverage examples" in section
    assert "| Entry id | Contract artifacts | Focused tests | Privacy boundary |" in section
    assert "pytest node ids" in section

    for entry in run_harness.CONTRACT_COVERAGE:
        assert f"`{entry['id']}`" in section
        assert f"command {entry['command_index']}" in section
        if "spec" in entry:
            assert entry["spec"] in section
        fixtures = entry.get("fixtures", [])
        if fixtures:
            for fixture in fixtures:
                assert fixture in section
        else:
            assert "no fixtures" in section

    assert "not_read_by_dry_run" in section
    assert "read_only_mcp_expected" in section
    assert "metadata_only_available" in section


def test_contributing_documents_contract_coverage_privacy_boundary_keys():
    text = CONTRIBUTING.read_text(encoding="utf-8")
    section_start = text.index(f"### {CONTRACT_COVERAGE_DOCUMENTATION_SECTION}")
    section_end = text.index(
        "Run the standard deterministic validation set", section_start
    )
    section = text[section_start:section_end]
    run_harness = _load_script(RUN_HARNESS)

    for entry in run_harness.CONTRACT_COVERAGE:
        for key in entry["privacy_boundary"]:
            assert f"`{key}`" in section, f"{entry['id']} missing {key}"


def test_harness_first_task_template_prompts_contract_coverage_validation():
    text = HARNESS_FIRST_TASK_TEMPLATE.read_text(encoding="utf-8")

    _assert_contract_coverage_validation_prompt(
        ".github/ISSUE_TEMPLATE/harness_first_task.yml", text
    )
    assert "If this adds or changes `contract_coverage`" in text
    _assert_contract_coverage_entry_maintenance_rule(
        ".github/ISSUE_TEMPLATE/harness_first_task.yml", text
    )


def test_pull_request_template_prompts_contract_coverage_validation():
    text = PULL_REQUEST_TEMPLATE.read_text(encoding="utf-8")

    _assert_contract_coverage_validation_prompt(
        ".github/pull_request_template.md", text
    )
    assert "If this changes `contract_coverage`" in text
    _assert_contract_coverage_entry_maintenance_rule(
        ".github/pull_request_template.md", text
    )


def test_contract_coverage_validation_prompts_share_contributing_command_set():
    surfaces = {
        "CONTRIBUTING.md": CONTRIBUTING.read_text(encoding="utf-8"),
        ".github/ISSUE_TEMPLATE/harness_first_task.yml": (
            HARNESS_FIRST_TASK_TEMPLATE.read_text(encoding="utf-8")
        ),
        ".github/pull_request_template.md": (
            PULL_REQUEST_TEMPLATE.read_text(encoding="utf-8")
        ),
    }

    for surface, text in surfaces.items():
        _assert_contract_coverage_validation_prompt(surface, text)


def test_contract_coverage_templates_reference_contributing_without_command_copies():
    template_surfaces = {
        ".github/ISSUE_TEMPLATE/harness_first_task.yml": (
            HARNESS_FIRST_TASK_TEMPLATE.read_text(encoding="utf-8")
        ),
        ".github/pull_request_template.md": (
            PULL_REQUEST_TEMPLATE.read_text(encoding="utf-8")
        ),
    }

    for surface, text in template_surfaces.items():
        assert "CONTRIBUTING.md" in text, surface
        assert CONTRACT_COVERAGE_DOCUMENTATION_SECTION in text, surface
        assert CONTRACT_COVERAGE_JSON_PLAN_COMMAND not in text, surface
        assert CONTRACT_COVERAGE_INTEGRITY_TEST_COMMAND not in text, surface


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
    assert "release-state validator" in normalized
    assert "manual-smoke freshness validator" in normalized
    assert "does not call GitHub" in normalized
    assert "python harness/scripts/run_harness.py --list-commands" in normalized
    assert "python harness/scripts/run_harness.py --list-commands --format json" in normalized
    assert "does not create harness state, start subprocesses, or read observed content" in normalized


def test_harness_readme_documents_workday_dry_run_text_fixture_contracts():
    text = HARNESS_README.read_text(encoding="utf-8")
    normalized = " ".join(text.split())

    assert "## Workday Dry-Run Text Fixtures" in text
    assert "harness/specs/workday-dry-run-text-contract.schema.json" in text
    for fixture in (
        "plugin_dry_run_text_contract.json",
        "setup_dry_run_text_contract.json",
        "daily_dry_run_text_contract.json",
    ):
        assert fixture in text
    for key in (
        "`command`",
        "`expected_contains`",
        "`forbidden_substrings`",
        "`ordered_pairs`",
    ):
        assert key in text
    assert "`Reads desktop: no`" in text
    assert "`reads desktop: no`" in text
    assert "desktop: yes" in normalized
    assert "`contract_coverage`" in text
    assert "`workday_dry_run_text_contracts`" in text
    assert "python -m pytest tests\\test_cli.py::test_workday_dry_run_text_contract_fixtures_match_schema" in text


def test_harness_readme_documents_workday_stop_summary_fixture_contract():
    text = HARNESS_README.read_text(encoding="utf-8")
    normalized = " ".join(text.split())

    assert "## Workday Stop Summary Fixture" in text
    assert "stop_human_summary_contract.json" in text
    assert "harness/specs/workday-stop-summary-contract.schema.json" in text
    assert "`human_summary_forbidden_markers`" in text
    assert "`technical_summary_required_markers`" in text
    assert "default human Workday summary" in normalized
    assert "explicit technical Workday summary" in normalized
    assert "does not add a capture source" in normalized
    assert "`contract_coverage`" in text
    assert "`workday_stop_summary_contract`" in text
    assert "python -m pytest tests\\test_workday.py::test_workday_stop_summary_contract_fixture_matches_schema" in text
    assert (
        "tests/test_windows_harness_workflow.py::"
        "test_run_harness_json_plan_declares_workday_stop_summary_contract_coverage"
        in text
    )


def test_harness_readme_documents_mcp_contract_coverage_metadata():
    text = HARNESS_README.read_text(encoding="utf-8")
    normalized = " ".join(text.split())

    assert "## MCP Contract Coverage Metadata" in text
    assert "`mcp_read_only_metadata_contracts`" in text
    assert "harness/specs/mcp-tool-result.schema.json" in text
    assert "tests/test_compatibility_contracts.py::test_mcp_result_schema_tool_enum_matches_exact_read_only_contract" in text
    assert "tests/test_mcp_tools.py::test_mcp_tool_results_include_evidence_policy_matrix" in text
    assert "tests/test_mcp_tools.py::test_mcp_metadata_only_mode_omits_observed_text_without_tool_list_change" in text
    for phrase in (
        "read-only MCP",
        "metadata-only",
        "local_winchronicle_state",
        "coverage_quality_not_permission",
        "external sharing requires user approval",
    ):
        assert phrase in normalized


def test_harness_readme_documents_command_plan_schema():
    text = HARNESS_README.read_text(encoding="utf-8")
    normalized = " ".join(text.split())

    assert "harness/specs/harness-command-plan.schema.json" in text
    assert "`contract_coverage`" in text
    for key in ("`id`", "`command_index`", "`tests`", "`privacy_boundary`"):
        assert key in text
    assert "metadata consumers can audit" in normalized
    assert "CONTRIBUTING.md" in text
    assert "Current coverage examples" in text
    assert (
        "Use `CONTRIBUTING.md` for the entry-level `spec`, `fixtures`, `tests`, "
        "and `privacy_boundary` anchors"
        in normalized
    )
    assert "Treat the JSON command plan as source of truth" in text


def test_harness_readme_documents_command_plan_pytest_node_collection():
    text = HARNESS_README.read_text(encoding="utf-8")
    normalized = " ".join(text.split())

    assert "pytest --collect-only" in text
    assert "every pytest node listed in `contract_coverage.tests`" in normalized
    assert "renamed or deleted checks" in normalized


def test_harness_readme_documents_command_plan_artifact_path_checks():
    text = HARNESS_README.read_text(encoding="utf-8")
    normalized = " ".join(text.split())

    assert "every `spec` and `fixtures` path" in normalized
    assert "repo-relative file" in normalized
    assert "moved or deleted schema and fixture artifacts" in normalized


def test_harness_readme_summarizes_command_plan_coverage_integrity():
    text = HARNESS_README.read_text(encoding="utf-8")
    section = _markdown_section(text, "Command Plan Coverage Integrity")
    normalized = " ".join(section.split())

    assert "harness/specs/harness-command-plan.schema.json" in section
    assert "schema shape" in normalized
    assert "`pytest --collect-only`" in section
    assert "pytest node" in normalized
    assert "repo-relative artifact paths" in normalized
    assert "`execution` remains `not_run`" in section
    assert "`creates_harness_state`" in section
    assert "`starts_subprocesses`" in section
    assert "`reads_observed_content`" in section


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


def test_install_cli_smoke_covers_codex_dry_run_read_desktop_boundary():
    text = INSTALL_CLI_SMOKE.read_text(encoding="utf-8")

    assert 'plugin_dry_run["reads_desktop"] is False' in text
    assert '"codex plugin dry-run should not read desktop"' in text
    assert 'setup_dry_run["reads_desktop"] is False' in text
    assert '"codex setup dry-run should not read desktop"' in text
    assert 'daily_dry_run["reads_desktop"] is False' in text
    assert '"codex daily dry-run should not read desktop"' in text


def test_install_cli_smoke_covers_codex_text_read_desktop_boundary():
    text = INSTALL_CLI_SMOKE.read_text(encoding="utf-8")

    assert '"Reads desktop: no" in plugin_text' in text
    assert '"codex plugin text dry-run did not report the read-desktop boundary"' in text
    assert '"reads desktop: no" in setup_text' in text
    assert '"codex setup text dry-run did not report the read-desktop boundary"' in text
    assert '"Reads desktop: no" in daily_text' in text
    assert '"codex daily text dry-run did not report the read-desktop boundary"' in text


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
        "harness/scripts/check_release_evidence.py",
        "--project",
        "pyproject.toml",
        "--require-release-state",
        "docs/release-evidence.md",
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
    assert (
        "harness/scripts/check_release_evidence.py --project pyproject.toml "
        "--require-release-state docs/release-evidence.md"
    ) in output
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


def test_run_harness_json_command_plan_matches_schema_without_running(
    monkeypatch, capsys
):
    run_harness = _load_script(RUN_HARNESS)

    def fail_run(*_args, **_kwargs):
        raise AssertionError("--list-commands --format json must not run harness commands")

    monkeypatch.setattr(run_harness, "_run", fail_run)

    assert run_harness.main(["--list-commands", "--format", "json"]) == 0

    plan = json.loads(capsys.readouterr().out)
    _assert_command_plan_contract_coverage_integrity(plan)


def test_run_harness_json_contract_coverage_integrity_runs_all_gates(
    monkeypatch, capsys
):
    run_harness = _load_script(RUN_HARNESS)

    def fail_run(*_args, **_kwargs):
        raise AssertionError("--list-commands --format json must not run harness commands")

    monkeypatch.setattr(run_harness, "_run", fail_run)

    assert run_harness.main(["--list-commands", "--format", "json"]) == 0

    plan = json.loads(capsys.readouterr().out)
    _assert_command_plan_contract_coverage_integrity(plan)


def test_contract_coverage_pytest_node_validator_rejects_missing_node():
    with pytest.raises(AssertionError, match="contract_coverage pytest nodes"):
        _assert_contract_coverage_pytest_nodes_exist(
            ["tests/test_windows_harness_workflow.py::missing_contract_coverage_node"]
        )


def test_run_harness_json_contract_coverage_tests_reference_existing_pytest_nodes(
    monkeypatch, capsys
):
    run_harness = _load_script(RUN_HARNESS)

    def fail_run(*_args, **_kwargs):
        raise AssertionError("--list-commands --format json must not run harness commands")

    monkeypatch.setattr(run_harness, "_run", fail_run)

    assert run_harness.main(["--list-commands", "--format", "json"]) == 0

    plan = json.loads(capsys.readouterr().out)
    node_ids = [
        test_id
        for item in plan["contract_coverage"]
        for test_id in item["tests"]
    ]
    _assert_contract_coverage_pytest_nodes_exist(node_ids)


def test_contract_coverage_artifact_path_validator_rejects_missing_paths():
    with pytest.raises(AssertionError, match="contract_coverage artifact paths"):
        _assert_contract_coverage_artifact_paths_exist(
            [
                {
                    "id": "missing_artifacts",
                    "spec": "harness/specs/missing-contract.schema.json",
                    "fixtures": ["harness/fixtures/workday/missing-contract.json"],
                }
            ]
        )


def test_run_harness_json_contract_coverage_artifact_paths_exist(
    monkeypatch, capsys
):
    run_harness = _load_script(RUN_HARNESS)

    def fail_run(*_args, **_kwargs):
        raise AssertionError("--list-commands --format json must not run harness commands")

    monkeypatch.setattr(run_harness, "_run", fail_run)

    assert run_harness.main(["--list-commands", "--format", "json"]) == 0

    plan = json.loads(capsys.readouterr().out)
    _assert_contract_coverage_artifact_paths_exist(plan["contract_coverage"])


def test_run_harness_json_plan_declares_workday_dry_run_contract_coverage(
    monkeypatch, capsys
):
    run_harness = _load_script(RUN_HARNESS)

    def fail_run(*_args, **_kwargs):
        raise AssertionError("--list-commands --format json must not run harness commands")

    monkeypatch.setattr(run_harness, "_run", fail_run)

    assert run_harness.main(["--list-commands", "--format", "json"]) == 0

    plan = json.loads(capsys.readouterr().out)
    coverage = {
        item["id"]: item
        for item in plan["contract_coverage"]
    }
    workday = coverage["workday_dry_run_text_contracts"]

    assert workday == {
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
    }
    assert plan["commands"][workday["command_index"] - 1]["argv"] == [
        sys.executable,
        "-m",
        "pytest",
        "-q",
    ]


def test_run_harness_json_plan_declares_workday_stop_summary_contract_coverage(
    monkeypatch, capsys
):
    run_harness = _load_script(RUN_HARNESS)

    def fail_run(*_args, **_kwargs):
        raise AssertionError("--list-commands --format json must not run harness commands")

    monkeypatch.setattr(run_harness, "_run", fail_run)

    assert run_harness.main(["--list-commands", "--format", "json"]) == 0

    plan = json.loads(capsys.readouterr().out)
    coverage = {
        item["id"]: item
        for item in plan["contract_coverage"]
    }
    stop_summary = coverage["workday_stop_summary_contract"]

    assert stop_summary == {
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
    }
    assert plan["commands"][stop_summary["command_index"] - 1]["argv"] == [
        sys.executable,
        "-m",
        "pytest",
        "-q",
    ]


def test_run_harness_json_plan_declares_mcp_read_only_metadata_contract_coverage(
    monkeypatch, capsys
):
    run_harness = _load_script(RUN_HARNESS)

    def fail_run(*_args, **_kwargs):
        raise AssertionError("--list-commands --format json must not run harness commands")

    monkeypatch.setattr(run_harness, "_run", fail_run)

    assert run_harness.main(["--list-commands", "--format", "json"]) == 0

    plan = json.loads(capsys.readouterr().out)
    coverage = {
        item["id"]: item
        for item in plan["contract_coverage"]
    }
    mcp = coverage["mcp_read_only_metadata_contracts"]

    assert mcp == {
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
    }
    assert plan["commands"][mcp["command_index"] - 1]["argv"] == [
        sys.executable,
        "-m",
        "pytest",
        "-q",
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
