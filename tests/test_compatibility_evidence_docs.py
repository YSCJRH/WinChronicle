from pathlib import Path

from winchronicle.mcp.server import TOOL_NAMES


ROOT = Path(__file__).resolve().parents[1]
CHECKLIST = ROOT / "docs" / "release-checklist.md"
EVIDENCE = ROOT / "docs" / "release-evidence.md"
MCP_SCORECARD = ROOT / "harness" / "scorecards" / "mcp-quality.md"
PHASE6_SCORECARD = ROOT / "harness" / "scorecards" / "phase6-privacy-enrichment.md"
V012_RELEASE = ROOT / "docs" / "release-v0.1.2.md"
V013_RELEASE = ROOT / "docs" / "release-v0.1.3.md"
V014_RELEASE = ROOT / "docs" / "release-v0.1.4.md"


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


def test_v012_release_record_is_published_and_compatible():
    text = V012_RELEASE.read_text(encoding="utf-8")
    normalized = _normalized(text)

    for phrase in (
        "Publication status: published maintenance release.",
        "Release URL: https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.2.",
        "Final tag target: `8bc8e9adf01e72031e5fb776007d4152a065ccb2`.",
        "must report `0.1.2`",
        "exact read-only MCP tool list remains unchanged",
        "Phase 6 remains specification-only",
        "no new capture surfaces",
        "no helper/watcher behavior changes",
        "no screenshot capture code",
        "no OCR engine integration",
    ):
        assert phrase in normalized

    for tool_name in TOOL_NAMES:
        assert f"`{tool_name}`" in text


def test_v013_release_record_is_published_and_compatible():
    text = V013_RELEASE.read_text(encoding="utf-8")
    normalized = _normalized(text)

    for phrase in (
        "Publication status: published maintenance release.",
        "Release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.3",
        "Final tag target | `0aa5c1b6e1959ef6504e6d70e4aad79a60594926`",
        "Previous stable release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.2",
        "M3 post-merge `main` Windows Harness | Passed, run `25106280110`",
        "M4 post-merge `main` Windows Harness | Passed, run `25193726729`",
        "must report `0.1.3`",
        "exact read-only MCP tool list remains unchanged",
        "Phase 6 remains specification-only",
        "no new capture surfaces",
        "no helper/watcher behavior changes",
        "no screenshot capture code",
        "no OCR engine integration",
        "Publication approval: granted by the user message `approve publication`.",
    ):
        assert phrase in normalized

    for tool_name in TOOL_NAMES:
        assert f"`{tool_name}`" in text


def test_v014_release_record_is_published_and_compatible():
    text = V014_RELEASE.read_text(encoding="utf-8")
    normalized = _normalized(text)

    for phrase in (
        "Publication status: published maintenance release.",
        "Release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.4",
        "Final tag target | `31164abe0a391a4cf4e2bf5741395fe7a8ae8750`",
        "Previous stable release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.3",
        "Candidate PR Windows Harness | Passed, run `25411926176`",
        "Candidate post-merge `main` Windows Harness | Passed, run `25411989748`",
        "P3 completion post-merge `main` Windows Harness | Passed, run `25411231216`",
        "must report `0.1.4`",
        "exact read-only MCP tool list remains unchanged",
        "Phase 6 remains specification-only",
        "no new capture surfaces",
        "no helper/watcher product behavior changes",
        "no screenshot capture code",
        "no OCR engine integration",
        "Publication approval: completed.",
        "Deterministic gates: local P4 validation, PR Windows Harness, post-merge `main` Windows Harness, and GitHub release publication passed.",
        "deterministic watcher smoke was refreshed through P3 local and Windows Harness evidence",
    ):
        assert phrase in normalized

    for tool_name in TOOL_NAMES:
        assert f"`{tool_name}`" in text


def _normalized(text: str) -> str:
    return " ".join(text.split())
