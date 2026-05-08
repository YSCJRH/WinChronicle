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
V015_RELEASE = ROOT / "docs" / "release-v0.1.5.md"
V016_RELEASE = ROOT / "docs" / "release-v0.1.6.md"
V017_RELEASE = ROOT / "docs" / "release-v0.1.7.md"
V018_RELEASE = ROOT / "docs" / "release-v0.1.8.md"
V019_RELEASE = ROOT / "docs" / "release-v0.1.9.md"


def test_release_checklist_requires_compatibility_evidence():
    text = CHECKLIST.read_text(encoding="utf-8")
    normalized = _normalized(text)

    for phrase in (
        "## Compatibility Evidence",
        "`pyproject.toml`, `winchronicle.__version__`, and MCP `serverInfo.version`",
        "exact read-only MCP tool list",
        "Phase 6 screenshot/OCR work remains specification-only",
        "product targeted capture flags are exposed",
        "v0.1.9 release-readiness record",
        "v0.1.8 maintenance release record",
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
        "v0.1.9 release-readiness record",
        "v0.1.8 maintenance release record",
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


def test_v015_release_record_is_published_and_compatible():
    text = V015_RELEASE.read_text(encoding="utf-8")
    normalized = _normalized(text)

    for phrase in (
        "Publication status: published maintenance release.",
        "Release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.5",
        "Final tag target | `89f0c1d5e6c094ed36c0ecf75e18bb7afcd5aaf4`",
        "Candidate PR | https://github.com/YSCJRH/WinChronicle/pull/71",
        "Candidate PR Windows Harness | Passed, run `25544005112`",
        "Candidate post-merge `main` Windows Harness | Passed, run `25544114712`",
        "Final pre-publication `main` Windows Harness | Passed, run `25544832155`",
        "Previous stable release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.4",
        "P1 post-merge `main` Windows Harness | Passed, run `25542239210`",
        "P2 post-merge `main` Windows Harness | Passed, run `25542706517`",
        "P3 post-merge `main` Windows Harness | Passed, run `25543079012`",
        "`python -m pytest -q` | Pass | `102 passed",
        "must report `0.1.5`",
        "exact read-only MCP tool list remains unchanged",
        "Phase 6 remains specification-only",
        "no new capture surfaces",
        "no helper/watcher product behavior changes",
        "no screenshot capture code",
        "no OCR engine integration",
        "Publication approval: completed by the active thread goal directing stage completion, remote push, and publication.",
        "Deterministic gates: local P4 validation, PR Windows Harness, post-merge `main` Windows Harness, and GitHub release publication passed.",
        "P2 decision only because product UIA helper behavior",
    ):
        assert phrase in normalized

    for tool_name in TOOL_NAMES:
        assert f"`{tool_name}`" in text


def test_v016_release_record_is_published_and_compatible():
    text = V016_RELEASE.read_text(encoding="utf-8")
    normalized = _normalized(text)

    for phrase in (
        "Publication status: published maintenance release.",
        "Release | `v0.1.6`",
        "Stage | Published maintenance release",
        "Base `main` SHA before S4 readiness | `4a8222f24423c565b64c065da3b151ee5e246b99`",
        "Candidate PR | https://github.com/YSCJRH/WinChronicle/pull/79",
        "Candidate PR Windows Harness | Passed, run `25551243900`",
        "Candidate post-merge `main` Windows Harness | Passed, run `25551362920`",
        "Release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.6",
        "Final tag target | `914cf361ac5864fa31d393d125d14e45eeba96bc`",
        "Previous stable release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.5",
        "`v0.1.5` tag target | `89f0c1d5e6c094ed36c0ecf75e18bb7afcd5aaf4`",
        "S0 PR Windows Harness | Passed, run `25546758389`",
        "S1 PR Windows Harness | Passed, run `25547398940`",
        "S2 PR Windows Harness | Passed, run `25548402922`",
        "S3 PR Windows Harness | Passed, run `25549622445`",
        "S3 post-merge `main` Windows Harness | Passed, run `25549851891`",
        "`python -m pytest -q` | Pass | `106 passed",
        "must report `0.1.6`",
        "exact read-only MCP tool list remains unchanged",
        "Phase 6 remains specification-only",
        "no new capture surfaces",
        "no helper/watcher product behavior changes",
        "no screenshot capture code",
        "no OCR engine integration",
        "explicitly accepts inherited `v0.1.0` Notepad",
        "Deterministic gates: local S4 validation, PR Windows Harness, post-merge `main` Windows Harness, and GitHub release publication passed.",
        "Publication approval: completed by the active thread goal directing stage completion, remote push, and publication.",
        "follow-up release candidate instead of retagging `v0.1.6`",
    ):
        assert phrase in normalized

    for tool_name in TOOL_NAMES:
        assert f"`{tool_name}`" in text


def test_v017_release_record_is_ready_and_compatible():
    text = V017_RELEASE.read_text(encoding="utf-8")
    normalized = _normalized(text)

    for phrase in (
        "Publication status: published maintenance release.",
        "Release | `v0.1.7`",
        "Stage | Published maintenance release",
        "Base `main` SHA before T4 readiness | `6d1d8f94c56636c23daafcb4ceae24053ff226aa`",
        "Candidate PR | https://github.com/YSCJRH/WinChronicle/pull/85",
        "Candidate PR Windows Harness | Passed, run `25556058760`",
        "Candidate post-merge `main` Windows Harness | Passed, run `25556207363`",
        "Release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.7",
        "Final tag target | `0b5969509754f78b218f823d0e6bb7a0ea61392b`",
        "Previous stable release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.6",
        "`v0.1.6` tag target | `914cf361ac5864fa31d393d125d14e45eeba96bc`",
        "T0 PR Windows Harness | Passed, run `25553025094`",
        "T1 PR Windows Harness | Passed, run `25553940230`",
        "T2 PR Windows Harness | Passed, run `25554431580`",
        "T3 PR Windows Harness | Passed, run `25555063537`",
        "T3 post-merge `main` Windows Harness | Passed, run `25555180274`",
        "must report `0.1.7`",
        "`python -m pytest -q` | Pass | `108 passed",
        "exact read-only MCP tool list remains unchanged",
        "Phase 6 remains specification-only",
        "no new capture surfaces",
        "no helper/watcher product behavior changes",
        "no screenshot capture code",
        "no OCR engine integration",
        "explicitly accepts inherited `v0.1.0` Notepad",
        "Fallback path: follow-up release candidate if any product or contract change",
        "Publication approval: completed by the active thread goal",
        "Deterministic gates: local T4 validation, PR Windows Harness, post-merge `main` Windows Harness, and GitHub release publication passed.",
        "Release URL: https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.7.",
    ):
        assert phrase in normalized

    for tool_name in TOOL_NAMES:
        assert f"`{tool_name}`" in text


def test_v018_release_record_is_ready_and_compatible():
    text = V018_RELEASE.read_text(encoding="utf-8")
    normalized = _normalized(text)

    for phrase in (
        "Publication status: published maintenance release.",
        "Release | `v0.1.8`",
        "Stage | Published maintenance release",
        "Base `main` SHA before U4 readiness | `8a25ec8abf2f91a912aaffd807ae4a4897847578`",
        "Candidate PR | https://github.com/YSCJRH/WinChronicle/pull/91",
        "Candidate PR Windows Harness | Passed, run `25561704868`",
        "Candidate post-merge `main` Windows Harness | Passed, run `25561832883`",
        "Release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.8",
        "Final tag target | `1ea1e378aedb0a509d202fd32bc69704dbe903d4`",
        "Previous stable release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.7",
        "`v0.1.7` tag target | `0b5969509754f78b218f823d0e6bb7a0ea61392b`",
        "v0.1.7 publication reconciliation PR | https://github.com/YSCJRH/WinChronicle/pull/86",
        "U0 PR Windows Harness | Passed, run `25557993996`",
        "U1 PR Windows Harness | Passed, run `25558809159`",
        "U2 PR Windows Harness | Passed, run `25559501788`",
        "U3 PR Windows Harness | Passed, run `25560353073`",
        "U3 post-merge `main` Windows Harness | Passed, run `25560483461`",
        "must report `0.1.8`",
        "exact read-only MCP tool list remains unchanged",
        "Phase 6 remains specification-only",
        "no new capture surfaces",
        "no helper/watcher product behavior changes",
        "no screenshot capture code",
        "no OCR engine integration",
        "explicitly accepts inherited `v0.1.0` Notepad",
        "`python -m pytest -q` | Pass | `111 passed",
        "Fallback path: follow-up release candidate if any product or contract change",
        "Publication approval: completed by the active thread goal",
        "Deterministic gates: local U4 validation, PR Windows Harness, post-merge `main` Windows Harness, and GitHub release publication passed.",
        "Release URL: https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.8.",
        "Final tag target: `1ea1e378aedb0a509d202fd32bc69704dbe903d4`.",
    ):
        assert phrase in normalized

    for tool_name in TOOL_NAMES:
        assert f"`{tool_name}`" in text


def test_v019_release_readiness_record_is_ready_and_compatible():
    text = V019_RELEASE.read_text(encoding="utf-8")
    normalized = _normalized(text)

    for phrase in (
        "Publication status: release-readiness candidate",
        "Release | `v0.1.9`",
        "Stage | Release-readiness candidate",
        "Base `main` SHA before W4 readiness | `36d430c478e65ad107125b7e87ed4ec18ac18709`",
        "Previous stable release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.8",
        "`v0.1.8` tag target | `1ea1e378aedb0a509d202fd32bc69704dbe903d4`",
        "W0 PR Windows Harness | Passed, run `25562785206`",
        "W1 PR Windows Harness | Passed, run `25563462333`",
        "W2 PR Windows Harness | Passed, run `25564182547`",
        "W3 PR Windows Harness | Passed, run `25564810377`",
        "W3 post-merge `main` Windows Harness | Passed, run `25564926634`",
        "must report `0.1.9`",
        "exact read-only MCP tool list remains unchanged",
        "Phase 6 remains specification-only",
        "no new capture surfaces",
        "no helper/watcher product behavior changes",
        "no screenshot capture code",
        "no OCR engine integration",
        "explicitly accepts inherited `v0.1.0` Notepad",
        "`python -m pytest -q` | Pass | `113 passed",
        "Fallback path: release candidate if any product or contract change",
        "Publication approval: authorized by the active thread goal",
        "Deterministic gates: local W4 validation passed",
    ):
        assert phrase in normalized

    for tool_name in TOOL_NAMES:
        assert f"`{tool_name}`" in text


def _normalized(text: str) -> str:
    return " ".join(text.split())
