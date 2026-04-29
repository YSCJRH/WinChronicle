import argparse
import json
from pathlib import Path

import pytest

from winchronicle.capture import capture_once_from_fixture
from winchronicle.cli import build_parser, main
from winchronicle.memory import generate_memory_entries
from winchronicle.mcp.server import TOOL_NAMES, privacy_status
from winchronicle.privacy import DISABLED_SURFACE_STATUS, TRUST, privacy_contract_payload


ROOT = Path(__file__).resolve().parents[1]

EXPECTED_CLI_COMMANDS = [
    "capture-frontmost",
    "capture-once",
    "generate-memory",
    "init",
    "mcp-stdio",
    "privacy-check",
    "search-captures",
    "search-memory",
    "status",
    "watch",
]
EXPECTED_MCP_TOOLS = [
    "current_context",
    "search_captures",
    "search_memory",
    "read_recent_capture",
    "recent_activity",
    "privacy_status",
]
EXPECTED_DISABLED_SURFACES = {
    "screenshots_enabled": False,
    "ocr_enabled": False,
    "audio_enabled": False,
    "keyboard_capture_enabled": False,
    "clipboard_capture_enabled": False,
    "network_upload_enabled": False,
    "cloud_upload_enabled": False,
    "llm_calls_enabled": False,
    "desktop_control_enabled": False,
    "product_targeted_capture_enabled": False,
    "mcp_write_tools_enabled": False,
}
EXPECTED_CAPTURE_SEARCH_KEYS = {"timestamp", "app_name", "title", "snippet", "path", "trust"}
EXPECTED_MEMORY_SEARCH_KEYS = {
    "entry_type",
    "title",
    "start_timestamp",
    "end_timestamp",
    "snippet",
    "path",
    "trust",
}
FORBIDDEN_CLI_OPTIONS = (
    "--hwnd",
    "--pid",
    "--window-title",
    "--window-title-regex",
    "--process-name",
    "--screenshot",
    "--ocr",
    "--audio",
    "--keyboard",
    "--clipboard",
    "--control",
)


def test_disabled_privacy_surface_contract_is_literal_and_shared(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("WINCHRONICLE_HOME", str(tmp_path / "state"))

    assert DISABLED_SURFACE_STATUS == EXPECTED_DISABLED_SURFACES

    payload = privacy_contract_payload()
    assert {key: payload[key] for key in EXPECTED_DISABLED_SURFACES} == EXPECTED_DISABLED_SURFACES
    assert payload["observed_content_trust"] == TRUST

    assert main(["status"]) == 0
    cli_status = json.loads(capsys.readouterr().out)
    mcp_status = privacy_status(home=tmp_path / "state")["result"]

    for key, expected in EXPECTED_DISABLED_SURFACES.items():
        assert cli_status[key] is expected
        assert mcp_status[key] is expected
    for key in (
        "observed_content_trust",
        "trust_boundary_instruction",
        "denylisted_apps",
        "redaction_summary",
    ):
        assert cli_status[key] == mcp_status[key]


def test_mcp_result_schema_tool_enum_matches_exact_read_only_contract():
    schema = json.loads(
        (ROOT / "harness" / "specs" / "mcp-tool-result.schema.json").read_text(encoding="utf-8")
    )

    assert TOOL_NAMES == EXPECTED_MCP_TOOLS
    assert schema["properties"]["tool"]["enum"] == EXPECTED_MCP_TOOLS
    assert schema["properties"]["read_only"] == {"const": True}
    assert schema["properties"]["trust"] == {"const": TRUST}


def test_product_cli_surface_contract_has_no_targeted_or_capture_expansion_flags():
    parser = build_parser()
    subcommands = _subcommands(parser)
    help_text = _all_help_text(parser, subcommands)

    assert sorted(subcommands) == EXPECTED_CLI_COMMANDS
    for forbidden in FORBIDDEN_CLI_OPTIONS:
        assert forbidden not in help_text

    for argv in (
        ["capture-frontmost", "--helper", "helper.exe", "--hwnd", "0x1"],
        ["capture-frontmost", "--helper", "helper.exe", "--pid", "1234"],
        ["capture-frontmost", "--helper", "helper.exe", "--window-title", "Notes"],
        ["mcp-stdio", "--write"],
        ["mcp-stdio", "--screenshot"],
    ):
        with pytest.raises(SystemExit):
            parser.parse_args(argv)


def test_cli_search_shapes_preserve_observed_content_trust_boundaries(
    tmp_path, monkeypatch, capsys
):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    for fixture_name in ("terminal_error.json", "vscode_editor.json", "edge_browser.json"):
        capture_once_from_fixture(ROOT / "harness" / "fixtures" / "uia" / fixture_name, home)

    assert main(["search-captures", "AssertionError"]) == 0
    capture_matches = json.loads(capsys.readouterr().out)
    assert capture_matches
    assert set(capture_matches[0]) == EXPECTED_CAPTURE_SEARCH_KEYS
    assert capture_matches[0]["trust"] == TRUST

    generate_memory_entries(home, date="2026-04-25")
    assert main(["search-memory", "OpenChronicle"]) == 0
    memory_matches = json.loads(capsys.readouterr().out)
    assert memory_matches
    assert all(set(match) == EXPECTED_MEMORY_SEARCH_KEYS for match in memory_matches)
    assert all(match["trust"] == TRUST for match in memory_matches)


def _subcommands(parser: argparse.ArgumentParser) -> dict[str, argparse.ArgumentParser]:
    for action in parser._actions:
        if isinstance(action, argparse._SubParsersAction):
            return dict(action.choices)
    raise AssertionError("parser has no subcommands")


def _all_help_text(
    parser: argparse.ArgumentParser,
    subcommands: dict[str, argparse.ArgumentParser],
) -> str:
    parts = [parser.format_help()]
    parts.extend(subparser.format_help() for subparser in subcommands.values())
    return "\n".join(parts)
