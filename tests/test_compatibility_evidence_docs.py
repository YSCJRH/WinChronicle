from pathlib import Path

from winchronicle.mcp.server import TOOL_NAMES


ROOT = Path(__file__).resolve().parents[1]
CHECKLIST = ROOT / "docs" / "release-checklist.md"
EVIDENCE = ROOT / "docs" / "release-evidence.md"
MCP_SCORECARD = ROOT / "harness" / "scorecards" / "mcp-quality.md"
PHASE6_SCORECARD = ROOT / "harness" / "scorecards" / "phase6-privacy-enrichment.md"


def test_release_checklist_requires_compatibility_evidence():
    text = CHECKLIST.read_text(encoding="utf-8")
    normalized = _normalized(text)

    for phrase in (
        "## Compatibility Evidence",
        "`pyproject.toml`, `winchronicle.__version__`, and MCP `serverInfo.version`",
        "exact read-only MCP tool list",
        "Phase 6 screenshot/OCR work remains specification-only",
        "product targeted capture flags are exposed",
    ):
        assert phrase in normalized

    for tool_name in TOOL_NAMES:
        assert f"`{tool_name}`" in text


def test_release_evidence_requires_mcp_and_phase6_compatibility_records():
    text = EVIDENCE.read_text(encoding="utf-8")
    normalized = _normalized(text)

    for phrase in (
        "## Compatibility Evidence",
        "version identity check passed",
        "MCP tool list remains exactly",
        "Phase 6 remains specification-only",
        "no screenshot capture code",
        "OCR engine integration",
    ):
        assert phrase in normalized

    for tool_name in TOOL_NAMES:
        assert f"`{tool_name}`" in text


def test_scorecards_remain_the_evidence_oracles_for_mcp_and_phase6():
    mcp = MCP_SCORECARD.read_text(encoding="utf-8")
    phase6 = PHASE6_SCORECARD.read_text(encoding="utf-8")

    assert "tool list is an exact compatibility contract" in mcp
    assert "does not authorize implementing" in phase6
    assert "No screenshot capture code, OCR engine integration" in phase6


def _normalized(text: str) -> str:
    return " ".join(text.split())
