from pathlib import Path

from winchronicle.mcp.server import TOOL_NAMES


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "mcp-client-setup.md"
EXPECTED_CODEX_TOOL_ORDER = [
    "privacy_status",
    "current_context",
    "recent_activity",
    "search_memory",
    "search_captures",
    "read_recent_capture",
]


def test_mcp_client_setup_documents_codex_dry_run_config_shape():
    text = DOC.read_text(encoding="utf-8")

    for expected in (
        "## Codex App And Codex CLI",
        "winchronicle codex install --dry-run",
        "[mcp_servers.winchronicle]",
        'command = "winchronicle"',
        'args = ["mcp-stdio"]',
        "startup_timeout_sec = 20",
        "tool_timeout_sec = 30",
        "enabled = true",
        "enabled_tools = [",
        "does not edit `config.toml`",
        "does not read or write secrets",
    ):
        assert expected in text

    for tool_name in EXPECTED_CODEX_TOOL_ORDER:
        assert f'"{tool_name}"' in text
    assert set(EXPECTED_CODEX_TOOL_ORDER) == set(TOOL_NAMES)


def test_mcp_client_setup_keeps_codex_example_read_only():
    text = DOC.read_text(encoding="utf-8")
    codex_section = text.split("## Codex App And Codex CLI", 1)[1].split(
        "## Read-Only Boundary",
        1,
    )[0]

    for forbidden in (
        '"click"',
        '"type"',
        '"press_key"',
        '"keyboard"',
        '"clipboard"',
        '"screenshot"',
        '"ocr"',
        '"audio"',
        '"network_upload"',
        '"cloud_upload"',
        '"desktop_control"',
        '"write_memory"',
        '"read_file"',
    ):
        assert forbidden not in codex_section
