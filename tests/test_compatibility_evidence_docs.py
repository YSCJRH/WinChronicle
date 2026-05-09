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
V0110_RELEASE = ROOT / "docs" / "release-v0.1.10.md"
V0111_RELEASE = ROOT / "docs" / "release-v0.1.11.md"
V0112_RELEASE = ROOT / "docs" / "release-v0.1.12.md"
V0113_RELEASE = ROOT / "docs" / "release-v0.1.13.md"
V0114_RELEASE = ROOT / "docs" / "release-v0.1.14.md"
V0115_RELEASE = ROOT / "docs" / "release-v0.1.15.md"
V0116_RC0_RELEASE = ROOT / "docs" / "release-candidate-v0.1.16-rc.0.md"
V0116_FINAL_PLAN = ROOT / "docs" / "next-round-plan-v0.1.16-final-release.md"
V0116_RELEASE = ROOT / "docs" / "release-v0.1.16.md"
V0117_RELEASE = ROOT / "docs" / "release-v0.1.17.md"
POST_V0117_PLAN = ROOT / "docs" / "next-round-plan-post-v0.1.17.md"
PUBLIC_METADATA_V0117 = ROOT / "docs" / "public-metadata-audit-post-v0.1.17.md"
HELPER_WATCHER_V0117 = ROOT / "docs" / "helper-watcher-diagnostics-sweep-post-v0.1.17.md"
MCP_MEMORY_V0117 = ROOT / "docs" / "mcp-memory-contract-sweep-post-v0.1.17.md"
COMPATIBILITY_V0117 = ROOT / "docs" / "compatibility-guardrail-sweep-post-v0.1.17.md"
POST_V0116_PLAN = ROOT / "docs" / "next-round-plan-post-v0.1.16.md"
PUBLIC_METADATA_V0116 = ROOT / "docs" / "public-metadata-audit-post-v0.1.16.md"
HELPER_WATCHER_V0116 = ROOT / "docs" / "helper-watcher-diagnostics-sweep-post-v0.1.16.md"
MCP_MEMORY_V0116 = ROOT / "docs" / "mcp-memory-contract-sweep-post-v0.1.16.md"
COMPATIBILITY_V0116 = ROOT / "docs" / "compatibility-guardrail-sweep-post-v0.1.16.md"
RELEASE_DECISION_V0117 = ROOT / "docs" / "release-readiness-decision-post-v0.1.17.md"
RELEASE_DECISION_V0116 = ROOT / "docs" / "release-readiness-decision-post-v0.1.16.md"


def test_release_checklist_requires_compatibility_evidence():
    text = CHECKLIST.read_text(encoding="utf-8")
    normalized = _normalized(text)

    for phrase in (
        "## Compatibility Evidence",
        "`pyproject.toml`, `winchronicle.__version__`, and MCP `serverInfo.version`",
        "exact read-only MCP tool list",
        "Phase 6 screenshot/OCR work remains specification-only",
        "product targeted capture flags are exposed",
        "v0.1.15 maintenance release record",
        "v0.1.17 maintenance release record",
        "v0.1.16 final release record",
        "v0.1.16-rc.0 release candidate record",
        "v0.1.16 final-release plan",
        "Post-v0.1.17 maintenance plan",
        "Public metadata audit after v0.1.17",
        "Helper and watcher diagnostics sweep after v0.1.17",
        "MCP and memory contract sweep after v0.1.17",
        "Compatibility guardrail sweep after v0.1.17",
        "Release-readiness decision after v0.1.17",
        "Post-v0.1.16 maintenance plan",
        "Public metadata audit after v0.1.16",
        "Helper and watcher diagnostics sweep after v0.1.16",
        "MCP and memory contract sweep after v0.1.16",
        "Compatibility guardrail sweep after v0.1.16",
        "Release-readiness decision after v0.1.16",
        "Post-v0.1.15 maintenance plan",
        "Post-v0.1.14 maintenance plan",
        "Post-v0.1.13 maintenance plan",
        "Post-v0.1.12 maintenance plan",
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
        "v0.1.15 maintenance release record",
        "v0.1.17 maintenance release record",
        "v0.1.16 final release record",
        "v0.1.16-rc.0 release candidate record",
        "v0.1.16 final-release plan",
        "Post-v0.1.17 maintenance plan",
        "Public metadata audit after v0.1.17",
        "Helper and watcher diagnostics sweep after v0.1.17",
        "MCP and memory contract sweep after v0.1.17",
        "Compatibility guardrail sweep after v0.1.17",
        "Release-readiness decision after v0.1.17",
        "Post-v0.1.16 maintenance plan",
        "Public metadata audit after v0.1.16",
        "Helper and watcher diagnostics sweep after v0.1.16",
        "MCP and memory contract sweep after v0.1.16",
        "Compatibility guardrail sweep after v0.1.16",
        "Release-readiness decision after v0.1.16",
        "Post-v0.1.15 maintenance plan",
        "Post-v0.1.14 maintenance plan",
        "Post-v0.1.13 maintenance plan",
        "Post-v0.1.12 maintenance plan",
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


def test_v019_release_record_is_published_and_compatible():
    text = V019_RELEASE.read_text(encoding="utf-8")
    normalized = _normalized(text)

    for phrase in (
        "Publication status: published maintenance release.",
        "Release | `v0.1.9`",
        "Stage | Published maintenance release",
        "Base `main` SHA before W4 readiness | `36d430c478e65ad107125b7e87ed4ec18ac18709`",
        "Candidate PR | https://github.com/YSCJRH/WinChronicle/pull/96",
        "Candidate PR Windows Harness | Passed, run `25565589238`",
        "Candidate post-merge `main` Windows Harness | Passed, run `25565697723`",
        "Release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.9",
        "Final tag target | `d06ab5bc8bea7520bac2719adb457794c72911d3`",
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
        "Fallback path: follow-up release candidate if any product or contract change",
        "Publication approval: completed by the active thread goal",
        "Deterministic gates: local W4 validation, PR Windows Harness, post-merge",
        "Release URL: https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.9.",
        "Final tag target: `d06ab5bc8bea7520bac2719adb457794c72911d3`.",
    ):
        assert phrase in normalized

    for tool_name in TOOL_NAMES:
        assert f"`{tool_name}`" in text


def test_v0110_release_record_is_ready_and_compatible():
    text = V0110_RELEASE.read_text(encoding="utf-8")
    normalized = _normalized(text)

    for phrase in (
        "Publication status: published maintenance release.",
        "Release | `v0.1.10`",
        "Stage | Published maintenance release",
        "Base `main` SHA before X4 readiness | `d13f84d1849b9300cf534cea55c25a3584aeea02`",
        "Candidate PR | https://github.com/YSCJRH/WinChronicle/pull/101",
        "Candidate PR Windows Harness | Passed, run `25569414864`",
        "Candidate post-merge `main` Windows Harness | Passed, run `25569567825`",
        "Release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.10",
        "Final tag target | `28b062a531519d4360911b51dfc083782b6dcbad`",
        "Previous stable release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.9",
        "`v0.1.9` tag target | `d06ab5bc8bea7520bac2719adb457794c72911d3`",
        "X0 PR Windows Harness | Passed, run `25566609049`",
        "X1 PR Windows Harness | Passed, run `25567381942`",
        "X2 PR Windows Harness | Passed, run `25567947799`",
        "X3 PR Windows Harness | Passed, run `25568494398`",
        "X3 post-merge `main` Windows Harness | Passed, run `25568639603`",
        "`python -m pytest -q` | Pass | `115 passed",
        "Local X4 validation",
        "must report `0.1.10`",
        "exact read-only MCP tool list remains unchanged",
        "Phase 6 remains specification-only",
        "no new capture surfaces",
        "no helper/watcher product behavior changes",
        "no screenshot capture code",
        "no OCR engine integration",
        "explicitly accepts inherited `v0.1.0` Notepad",
        "Fallback path: release candidate if any product or contract change",
        "Publication approval: completed by the active thread goal",
        "Deterministic gates: local X4 validation, PR Windows Harness, post-merge",
        "GitHub release publication passed.",
        "Release URL: https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.10.",
        "Final tag target: `28b062a531519d4360911b51dfc083782b6dcbad`.",
    ):
        assert phrase in normalized

    for tool_name in TOOL_NAMES:
        assert f"`{tool_name}`" in text


def test_v0111_release_record_is_published_and_compatible():
    text = V0111_RELEASE.read_text(encoding="utf-8")
    normalized = _normalized(text)

    for phrase in (
        "Publication status: published maintenance release.",
        "Release | `v0.1.11`",
        "Stage | Published maintenance release",
        "Base `main` SHA before Y4 readiness | `b7a6651d829c914fe9d8eeea0896238d0d880249`",
        "Candidate PR | https://github.com/YSCJRH/WinChronicle/pull/106",
        "Candidate PR Windows Harness | Passed, run `25573214374`",
        "Candidate post-merge `main` Windows Harness | Passed, run `25573347339`",
        "Release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.11",
        "Final tag target | `1724b0e47e6f6b915a99842fb971d7f9c503f65a`",
        "Previous stable release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.10",
        "`v0.1.10` tag target | `28b062a531519d4360911b51dfc083782b6dcbad`",
        "Y0 PR Windows Harness | Passed, run `25570444498`",
        "Y1 PR Windows Harness | Passed, run `25571224423`",
        "Y2 PR Windows Harness | Passed, run `25571923026`",
        "Y3 PR Windows Harness | Passed, run `25572434735`",
        "Y3 post-merge `main` Windows Harness | Passed, run `25572553734`",
        "Local Y4 validation",
        "`python -m pytest -q` | Pass | `117 passed",
        "must report `0.1.11`",
        "exact read-only MCP tool list remains unchanged",
        "Phase 6 remains specification-only",
        "no new capture surfaces",
        "no helper/watcher product behavior changes",
        "no screenshot capture code",
        "no OCR engine integration",
        "explicitly accepts inherited `v0.1.0` Notepad",
        "Fallback path: release candidate if any product or contract change",
        "Publication approval: completed by the active thread goal",
        "Deterministic gates: local Y4 validation, PR Windows Harness, post-merge",
        "GitHub release publication passed.",
        "Release URL: https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.11.",
        "Final tag target: `1724b0e47e6f6b915a99842fb971d7f9c503f65a`.",
    ):
        assert phrase in normalized

    for tool_name in TOOL_NAMES:
        assert f"`{tool_name}`" in text


def test_v0112_release_record_is_published_and_compatible():
    text = V0112_RELEASE.read_text(encoding="utf-8")
    normalized = _normalized(text)

    for phrase in (
        "Publication status: published maintenance release.",
        "Release | `v0.1.12`",
        "Stage | Published maintenance release",
        "Base `main` SHA before Z4 readiness | `86be82cb153269bad68fb92806fa7701a1e8579c`",
        "Candidate PR | https://github.com/YSCJRH/WinChronicle/pull/111",
        "Candidate PR Windows Harness | Passed, run `25576751080`",
        "Candidate post-merge `main` Windows Harness | Passed, run `25576867729`",
        "Release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.12",
        "Final tag target | `df16ea301243e2d3a612a5d09bd59f1436723fb4`",
        "Previous stable release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.11",
        "`v0.1.11` tag target | `1724b0e47e6f6b915a99842fb971d7f9c503f65a`",
        "Z0 PR Windows Harness | Passed, run `25573927712`",
        "Z1 PR Windows Harness | Passed, run `25574694437`",
        "Z2 PR Windows Harness | Passed, run `25575316043`",
        "Z3 PR Windows Harness | Passed, run `25575910225`",
        "Z3 post-merge `main` Windows Harness | Passed, run `25576068774`",
        "must report `0.1.12`",
        "exact read-only MCP tool list remains unchanged",
        "Phase 6 remains specification-only",
        "no new capture surfaces",
        "no helper/watcher product behavior changes",
        "no screenshot capture code",
        "no OCR engine integration",
        "explicitly accepts inherited `v0.1.0` Notepad",
        "`python -m pytest -q` | Pass | `119 passed`",
        "Fallback path: release candidate if any product or contract change",
        "Publication approval: completed by the active thread goal",
        "Deterministic gates: local Z4 validation, PR Windows Harness",
        "GitHub release publication passed",
        "Release URL: https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.12.",
        "Final tag target: `df16ea301243e2d3a612a5d09bd59f1436723fb4`.",
    ):
        assert phrase in normalized

    for tool_name in TOOL_NAMES:
        assert f"`{tool_name}`" in text


def test_v0113_release_record_is_ready_and_compatible():
    text = V0113_RELEASE.read_text(encoding="utf-8")
    normalized = _normalized(text)

    for phrase in (
        "Publication status: published maintenance release.",
        "Release | `v0.1.13`",
        "Stage | Published maintenance release",
        "Base `main` SHA before AA5 readiness | `1c9cabec4d27b8c0e4e245d9a27ddcba96ed3a00`",
        "Candidate PR | https://github.com/YSCJRH/WinChronicle/pull/118",
        "Candidate PR Windows Harness | Passed, run `25580778260`",
        "Candidate post-merge `main` Windows Harness | Passed, run `25580877004`",
        "Release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.13",
        "Final tag target | `1070343d9bcfd60c48238835e26b6c32f9060ae7`",
        "Previous stable release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.12",
        "`v0.1.12` tag target | `df16ea301243e2d3a612a5d09bd59f1436723fb4`",
        "AA0 PR Windows Harness | Passed, run `25578139342`",
        "AA1 PR Windows Harness | Passed, run `25578768178`",
        "AA2 PR Windows Harness | Passed, run `25579283981`",
        "AA3 PR Windows Harness | Passed, run `25579782185`",
        "AA4 PR Windows Harness | Passed, run `25580215098`",
        "AA4 post-merge `main` Windows Harness | Passed, run `25580333158`",
        "must report `0.1.13`",
        "`python -m pytest -q` | Pass | `125 passed`",
        "exact read-only MCP tool list remains unchanged",
        "Phase 6 remains specification-only",
        "no new capture surfaces",
        "no helper/watcher product behavior changes",
        "no screenshot capture code",
        "no OCR engine integration",
        "explicitly accepts inherited `v0.1.0` Notepad",
        "Fallback path: release candidate if any product or contract change",
        "Publication approval: completed by the active thread goal",
        "AA5 local validation, PR Windows Harness",
        "GitHub release publication passed",
        "Release URL: https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.13.",
        "Final tag target: `1070343d9bcfd60c48238835e26b6c32f9060ae7`.",
    ):
        assert phrase in normalized

    for tool_name in TOOL_NAMES:
        assert f"`{tool_name}`" in text


def test_v0114_release_record_is_ready_and_compatible():
    text = V0114_RELEASE.read_text(encoding="utf-8")
    normalized = _normalized(text)

    for phrase in (
        "Publication status: published maintenance release.",
        "Release | `v0.1.14`",
        "Stage | Published maintenance release",
        "Base `main` SHA before AB5 readiness | `cd5215e6e6333c7fe00fe47a526ea0d15dcf1bd7`",
        "Candidate PR | https://github.com/YSCJRH/WinChronicle/pull/125",
        "Candidate PR Windows Harness | Passed, run `25585067457`",
        "Candidate post-merge `main` Windows Harness | Passed, run `25585147402`",
        "Release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.14",
        "Final tag target | `e7e339f4e08828b9954599db76b87201dbcb139b`",
        "Previous stable release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.13",
        "`v0.1.13` tag target | `1070343d9bcfd60c48238835e26b6c32f9060ae7`",
        "AB0 PR Windows Harness | Passed, run `25582300531`",
        "AB1 PR Windows Harness | Passed, run `25582831041`",
        "AB2 PR Windows Harness | Passed, run `25583319858`",
        "AB3 PR Windows Harness | Passed, run `25583769517`",
        "AB4 PR Windows Harness | Passed, run `25584341353`",
        "AB4 post-merge `main` Windows Harness | Passed, run `25584426546`",
        "must report `0.1.14`",
        "`python -m pytest -q` | Pass | `131 passed`",
        "exact read-only MCP tool list remains unchanged",
        "Phase 6 remains specification-only",
        "no new capture surfaces",
        "no helper/watcher product behavior changes",
        "no screenshot capture code",
        "no OCR engine integration",
        "explicitly accepts inherited `v0.1.0` Notepad",
        "Fallback path: release candidate if any product or contract change",
        "Publication approval: completed by the active thread goal",
        "Deterministic gates: AB5 local validation, PR Windows Harness, post-merge `main` Windows Harness, and GitHub release publication passed.",
        "Release URL: https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.14.",
        "Final tag target: `e7e339f4e08828b9954599db76b87201dbcb139b`.",
    ):
        assert phrase in normalized

    for tool_name in TOOL_NAMES:
        assert f"`{tool_name}`" in text


def test_v0115_release_record_is_published_and_compatible():
    text = V0115_RELEASE.read_text(encoding="utf-8")
    normalized = _normalized(text)

    for phrase in (
        "Publication status: published maintenance release.",
        "Release | `v0.1.15`",
        "Stage | Published maintenance release",
        "Base `main` SHA before AC5 readiness | `48994134a3d348745f735e2a6fad56ea82495266`",
        "Candidate PR | https://github.com/YSCJRH/WinChronicle/pull/132",
        "Candidate PR Windows Harness | Passed, run `25588833988`",
        "Candidate post-merge `main` Windows Harness | Passed, run `25588898702`",
        "Candidate post-merge `main` SHA | `7a7f065817b9d7f660248916935fd7b66fadbdd6`",
        "Release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.15",
        "Final tag target | `4869ce7b5b0f6ad3ab41c844e4f010640c0c36c2`",
        "Previous stable release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.14",
        "`v0.1.14` tag target | `e7e339f4e08828b9954599db76b87201dbcb139b`",
        "AC0 PR Windows Harness | Passed, run `25586296541`",
        "AC1 PR Windows Harness | Passed, run `25586734181`",
        "AC2 PR Windows Harness | Passed, run `25587197634`",
        "AC3 PR Windows Harness | Passed, run `25587827078`",
        "AC4 PR Windows Harness | Passed, run `25588225151`",
        "AC4 post-merge `main` Windows Harness | Passed, run `25588297846`",
        "must report `0.1.15`",
        "`python -m pytest -q` | Pass | `137 passed`",
        "exact read-only MCP tool list remains unchanged",
        "Phase 6 remains specification-only",
        "no new capture surfaces",
        "no helper/watcher product behavior changes",
        "no screenshot capture code",
        "no OCR engine integration",
        "explicitly accepts inherited `v0.1.0` Notepad",
        "Fallback path: release candidate if any product or contract change",
        "Publication approval: received before publication.",
        "AC5 local validation, PR Windows Harness",
        "GitHub release publication passed.",
        "Release URL: https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.15.",
        "Final tag target: `4869ce7b5b0f6ad3ab41c844e4f010640c0c36c2`.",
    ):
        assert phrase in normalized

    for tool_name in TOOL_NAMES:
        assert f"`{tool_name}`" in text


def test_v0116_rc0_release_candidate_record_is_ready_and_scoped():
    text = V0116_RC0_RELEASE.read_text(encoding="utf-8")
    normalized = _normalized(text)

    for phrase in (
        "Publication status: published prerelease candidate.",
        "Release candidate | `v0.1.16-rc.0`",
        "Stage | AD5 published prerelease candidate",
        "Base `main` SHA before AD5 readiness | `2c7d0b0b24d9a159c084f262cb24ec7ee9873a39`",
        "Candidate PR | https://github.com/YSCJRH/WinChronicle/pull/140",
        "Candidate PR Windows Harness | Passed, run `25596082939`",
        "Candidate post-merge `main` Windows Harness | Passed, run `25596122521`",
        "Candidate post-merge `main` SHA | `bca4b6485f194a46bca7fa6e1e3866b5105479da`",
        "Final pre-publication `main` Windows Harness | Passed, run `25596273094`",
        "Release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.16-rc.0",
        "Published at | 2026-05-09T08:18:01Z",
        "Final tag target | `70caf364f68d8c159eb74bbbc23e7469db22a244`",
        "Publication reconciliation PR | https://github.com/YSCJRH/WinChronicle/pull/142",
        "Publication reconciliation PR Windows Harness | Passed, run `25596387380`",
        "Publication reconciliation post-merge `main` Windows Harness | Passed, run `25596453899`",
        "Previous stable release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.15",
        "`v0.1.15` tag target | `4869ce7b5b0f6ad3ab41c844e4f010640c0c36c2`",
        "AD4 PR Windows Harness | Passed, run `25595449096`",
        "AD4 post-merge `main` Windows Harness | Passed, run `25595513141`",
        "AD2-AD4 included compatible runtime drift fixes",
        "not direct `v0.1.16` final",
        "must report `0.1.16`",
        "exact read-only MCP tool list remains unchanged",
        "Phase 6 remains specification-only",
        "no new capture surfaces",
        "no CLI/MCP JSON shape changes",
        "no screenshot capture code",
        "no OCR engine integration",
        "`python -m pytest -q` | Pass | `149 passed`",
        "`python -c \"import winchronicle; print(winchronicle.__version__)\"` | Pass | printed `0.1.16`",
        "fresh manual UIA smoke passed for Notepad and Edge",
        "VS Code strict marker remains a diagnostic non-blocking failure",
        "watcher preview live smoke passed",
        "follow-up release candidate if any product or contract regression",
        "GitHub prerelease publication passed",
        "publication reconciliation post-merge `main` Windows Harness passed",
        "Release URL: https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.16-rc.0.",
        "Final tag target: `70caf364f68d8c159eb74bbbc23e7469db22a244`.",
    ):
        assert phrase in normalized

    for tool_name in TOOL_NAMES:
        assert f"`{tool_name}`" in text


def test_v0116_final_release_plan_keeps_direct_final_gated_and_scoped():
    text = V0116_FINAL_PLAN.read_text(encoding="utf-8")
    normalized = _normalized(text)

    for phrase in (
        "`v0.1.16-rc.0` is published as a prerelease",
        "prerelease tag targets `70caf364f68d8c159eb74bbbc23e7469db22a244`",
        "Windows Harness run `25596579705` passed",
        "documentation and documentation-test evidence only",
        "No product code, schemas, CLI/MCP JSON shape, helper/watcher behavior, privacy runtime behavior, or capture surfaces changed",
        "This plan was the active final-release cursor after `v0.1.16-rc.0`",
        "completed historical final-release evidence",
        "Direct final release proceeded only after fresh final gates",
        "explicit final manual smoke evidence",
        "Stage status: AE4 complete",
        "`v0.1.16` is published as the latest stable release",
        "Next atomic task: start the post-`v0.1.16` maintenance cursor",
        "If future release-readiness work requires any product or contract change",
        "prepare a new release-candidate path instead",
        "Do not publish or retag `v0.1.16` during AE0",
        "Rerun fresh final manual UIA smoke instead of automatically inheriting",
        "Do not commit raw helper JSON, raw watcher JSONL, screenshots, OCR output",
        "The final tag should target the post-merge `main` SHA",
        "exact read-only MCP tool list",
        "Phase 6 remains privacy spec/scorecard only",
        "product targeted capture flags",
        "gh release view v0.1.16",
        "release not found",
        "git diff --name-status v0.1.16-rc.0..HEAD",
        "PR #144 Windows Harness run `25596958129`",
        "post-AE0 `main` Windows Harness concluded `success`",
        "`python -m pytest -q` - passed; 151 tests passed",
        "`python harness/scripts/run_harness.py` - passed",
        "PR #145 Windows Harness run `25597196866`",
        "post-AE1 `main` Windows Harness concluded `success`",
        "Stage AE2 manual final smoke validation",
        "diagnostic failure, non-blocking; known Monaco/UIA limitation",
        "`captures_written: 3`",
        "PR #146 Windows Harness run `25597418104`",
        "post-AE2 `main` Windows Harness concluded `success`",
        "Added `docs/release-v0.1.16.md`",
        "PR #147 Windows Harness run `25597623991`",
        "post-AE3 `main` Windows Harness concluded `success`",
        "gh release create v0.1.16",
        "published at `2026-05-09T09:31:17Z`",
        "git ls-remote --tags origin v0.1.16",
        "Stage AE4 publication reconciliation:",
        "PR #148 Windows Harness run `25598038285`",
        "post-AE4 `main` Windows Harness concluded `success`",
    ):
        assert phrase in normalized

    for tool_name in TOOL_NAMES:
        assert f"`{tool_name}`" in text


def test_v0116_final_release_record_is_ready_and_scoped():
    text = V0116_RELEASE.read_text(encoding="utf-8")
    normalized = _normalized(text)

    for phrase in (
        "`v0.1.16` final is published.",
        "Publication status: published final release.",
        "Release | `v0.1.16`",
        "Stage | AE3 final release record and publication readiness",
        "Current candidate `main` SHA before this record | `1ea902a8630b9d0b18397af69cfcd84a9ce4d24a`",
        "Release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.16",
        "Published at | 2026-05-09T09:31:17Z",
        "Final tag target | `255f2a01cddde330d756a87359c4d3a8be4b11a2`",
        "Previous prerelease baseline | `v0.1.16-rc.0`",
        "`v0.1.16-rc.0` tag target | `70caf364f68d8c159eb74bbbc23e7469db22a244`",
        "Previous stable release | `v0.1.15`",
        "`v0.1.15` tag target | `4869ce7b5b0f6ad3ab41c844e4f010640c0c36c2`",
        "AE0 PR Windows Harness | Passed, run `25596958129`",
        "AE1 PR Windows Harness | Passed, run `25597196866`",
        "AE2 PR Windows Harness | Passed, run `25597418104`",
        "AE2 post-merge `main` Windows Harness | Passed, run `25597463319`",
        "AE3 PR Windows Harness | Passed, run `25597623991`",
        "AE3 post-merge `main` Windows Harness | Passed, run `25597678444`",
        "AE4 publication reconciliation PR | https://github.com/YSCJRH/WinChronicle/pull/148",
        "AE4 publication reconciliation Windows Harness | Passed, run `25598038285`",
        "AE4 post-publication `main` Windows Harness | Passed, run `25598080136`",
        "AD5 final pre-publication `main` Windows Harness | Passed, run `25596273094`",
        "`python -m pytest -q` | Pass | `151 passed`",
        "Notepad targeted UIA smoke | Pass",
        "Edge targeted UIA smoke | Pass",
        "VS Code metadata smoke | Pass with diagnostic warning",
        "VS Code strict Monaco marker | Diagnostic failure, non-blocking",
        "Real watcher/helper short preview | Pass",
        "`captures_written: 3`, `denylisted_skipped: 0`, `duplicates_skipped: 1`, `heartbeats: 6`",
        "Promotes the published `v0.1.16-rc.0` prerelease contract to `v0.1.16`",
        "must report `0.1.16`",
        "exact read-only MCP tool list remains unchanged",
        "Product CLI exposes no targeted `--hwnd`, `--pid`, `--window-title`",
        "Phase 6 remains specification-only",
        "This final release does not expand the capture surface beyond `v0.1.16-rc.0`",
        "MCP remains read-only",
        "Do not retag or modify `v0.1.16-rc.0`",
        "Fallback path: `v0.1.16-rc.1`",
        "Publication approval: standing user goal authorizes publishing after review",
        "GitHub release publication: passed.",
        "Release URL: https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.16.",
        "Final tag target: `255f2a01cddde330d756a87359c4d3a8be4b11a2`.",
    ):
        assert phrase in normalized

    for tool_name in TOOL_NAMES:
        assert f"`{tool_name}`" in text


def test_v0117_release_record_is_published_and_scoped():
    text = V0117_RELEASE.read_text(encoding="utf-8")
    normalized = _normalized(text)

    for phrase in (
        "`v0.1.17` is published as a compatible maintenance release.",
        "Publication status: published maintenance release.",
        "Release | `v0.1.17`",
        "Stage | AF6 v0.1.17 published maintenance release",
        "Base `main` SHA before this record | `bbf6d3c64d7fef435e66d64d4e3b19d2390c391b`",
        "Candidate branch | `codex/v017-release-readiness`",
        "Candidate PR | https://github.com/YSCJRH/WinChronicle/pull/159",
        "Publication reconciliation branch | `codex/v017-publication-reconciliation`",
        "Release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.17",
        "Published at | `2026-05-09T12:56:45Z`",
        "Final tag target | `5b260edc3bddc48986e52179b2ffd261856a89ac`",
        "Previous stable release | `v0.1.16`",
        "`v0.1.16` tag target | `255f2a01cddde330d756a87359c4d3a8be4b11a2`",
        "AF5 decision PR | https://github.com/YSCJRH/WinChronicle/pull/158",
        "AF5 PR Windows Harness | Passed, run `25600947496`",
        "AF5 post-merge `main` Windows Harness | Passed, run `25600994238`",
        "Candidate PR Windows Harness | Passed, run `25601571665`",
        "Candidate post-merge `main` Windows Harness | Passed, run `25601624151`",
        "`gh release view v0.1.17` before readiness | Pass | release not found",
        "`git ls-remote --tags origin v0.1.17 v0.1.17-rc.0` before readiness | Pass | no remote tags returned",
        "`git tag --list \"v0.1.17*\"` before readiness | Pass | no local tags returned",
        "`gh release create v0.1.17 --target 5b260edc3bddc48986e52179b2ffd261856a89ac` | Pass",
        "`gh release view v0.1.17 --json tagName,name,url,targetCommitish,isDraft,isPrerelease,publishedAt` | Pass",
        "`git ls-remote --tags origin v0.1.17` | Pass | `5b260edc3bddc48986e52179b2ffd261856a89ac`",
        "`python -m pytest -q` | Pass | `167 passed`",
        "`dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` | Pass | 0 warnings, 0 errors",
        "`dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` | Pass | 0 warnings, 0 errors",
        "`python harness/scripts/run_install_cli_smoke.py` | Pass",
        "`python harness/scripts/run_harness.py` | Pass",
        "`git diff --check` | Pass | no whitespace errors",
        "Notepad targeted UIA smoke | Pass",
        "Edge targeted UIA smoke | Pass",
        "VS Code metadata smoke | Pass with diagnostic warning",
        "VS Code strict Monaco marker | Diagnostic failure, non-blocking",
        "Real watcher/helper short preview | Heartbeat-only liveness diagnostic",
        "`captures_written: 0`, `denylisted_skipped: 0`, `duplicates_skipped: 0`, `heartbeats: 9`",
        "Aligns package, runtime, and MCP server version identity to `0.1.17`",
        "`generate-memory` manifest JSON trust fields",
        "must report `0.1.17`",
        "exact read-only MCP tool list remains unchanged",
        "Product CLI exposes no targeted `--hwnd`, `--pid`, `--window-title`",
        "Phase 6 remains specification-only",
        "does not expand the capture surface beyond `v0.1.16`",
        "Do not retag or modify `v0.1.17` or `v0.1.16`",
        "GitHub release publication: passed.",
        "Release URL: https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.17.",
        "Publication approval: standing user goal authorizes publishing after review",
    ):
        assert phrase in normalized

    for tool_name in TOOL_NAMES:
        assert f"`{tool_name}`" in text


def test_post_v0117_plan_is_active_without_expanding_scope():
    text = POST_V0117_PLAN.read_text(encoding="utf-8")
    normalized = _normalized(text)

    for phrase in (
        "`v0.1.17` is published at https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.17",
        "release tag targets `5b260edc3bddc48986e52179b2ffd261856a89ac`",
        "published at `2026-05-09T12:56:45Z`",
        "AF7 publication reconciliation landed on `main` as `110ace3f27d8bb9f1eff2c45449998fd0373a998`",
        "PR #160 Windows Harness run `25601966464` passed",
        "post-merge `main` Windows Harness run `25602018700` passed",
        "Current stage: Phase 6 Residual Schema Coverage Audit.",
        "Stage status: targeted contract gap fixture expansion complete",
        "Last completed evidence: Phase 6 contract gap fixture expansion PR #176 merged as `05811145444af93178b957bd1a3fc11b47f64cfd`",
        "PR Windows Harness run `25608336721` passed",
        "post-gap-fixtures `main` Windows Harness run `25608403951`",
        "verified the post-gap-fixtures `main` Windows Harness concluded `success`",
        "no runtime, helper/watcher, CLI/MCP output, privacy-runtime",
        "Next atomic task: audit residual Phase 6 schema coverage",
        "schema-enforced branches are either promoted to targeted fixtures",
        "Live UIA smoke remains manual and outside default CI",
        "Stage AG0 - Post-v0.1.17 Baseline Cursor",
        "Stage AG1 - Public Metadata And Evidence Freshness Follow-up",
        "Stage AG2 - Helper And Watcher Preview Diagnostics Review",
        "Stage AG3 - MCP And Memory Contract Review",
        "Stage AG4 - Compatibility Guardrail Sweep",
        "Stage AG5 - Release-Readiness Decision",
        "Next Blueprint Lane - Phase 6 Privacy-Enrichment Contract Preflight",
        "`v0.1.17` is the latest published stable release and must not be retagged",
        "`v0.1.16` remains the previous stable release and must not be retagged",
        "Manual UIA smoke for `v0.1.17` was freshly rerun in AF6",
        "Do not retag `v0.1.17`",
        "CLI command set remains unchanged",
        "`generate-memory` manifest JSON includes the compatible AF3 trust-boundary fields",
        "MCP tool list remains unchanged and read-only",
        "Do not implement screenshot capture, OCR, audio recording",
        "keyboard capture, clipboard capture, network upload, LLM calls",
        "desktop control",
        "product targeted capture",
        "Phase 6 remains privacy spec/scorecard only",
        "Stage AG0 initialization:",
        "gh release view v0.1.16",
        "PR #160 merged at `2026-05-09T13:14:04Z`",
        "PR #160 Windows Harness concluded `success`",
        "post-AF7 `main` Windows Harness concluded `success`",
        "Stage AG0 completion:",
        "PR #161 merged at `2026-05-09T13:30:52Z`",
        "PR #161 Windows Harness concluded `success`",
        "post-AG0 `main` Windows Harness concluded `success`",
        "Stage AG1 initialization:",
        "repository is public on `main`, with empty description, homepage, and topics",
        "`v0.1.17` is published, not a draft, not a prerelease",
        "`v0.1.16` remains published as the previous stable release",
        "Stage AG1 completion:",
        "PR #162 merged at `2026-05-09T13:55:16Z`",
        "PR #162 Windows Harness concluded `success`",
        "post-AG1 `main` Windows Harness concluded `success`",
        "Stage AG2 initialization:",
        "Reviewed `docs/uia-helper-quality-matrix.md`, `docs/watcher-preview.md`",
        "Found no new helper/watcher diagnostics drift",
        "Stage AG2 local validation:",
        "passed, 94 tests",
        "passed, 172 tests",
        "stale AG0/AG1 cursor and v0.1.16 helper/watcher typo scan",
        "Stage AG2 completion:",
        "PR #163 merged at `2026-05-09T14:16:40Z`",
        "PR #163 Windows Harness concluded `success`",
        "post-AG2 `main` Windows Harness concluded `success`",
        "Stage AG3 initialization:",
        "Reviewed `docs/mcp-readonly-examples.md`, `docs/deterministic-demo.md`",
        "Found no new MCP/memory contract drift",
        "Stage AG3 local validation:",
        "passed, 93 tests",
        "passed, 175 tests",
        "stale AG2 cursor scan",
        "Stage AG3 completion:",
        "PR #164 merged at `2026-05-09T14:40:08Z`",
        "PR #164 Windows Harness concluded `success`",
        "post-AG3 `main` Windows Harness concluded `success`",
        "Stage AG4 initialization:",
        "Reviewed `tests/test_compatibility_contracts.py`, `tests/test_mcp_tools.py`",
        "Found no new product compatibility drift",
        "Tightened docs/tests evidence for full disabled pass-through flag rejection",
        "Stage AG4 local validation:",
        "passed, 55 tests",
        "passed, 177 tests",
        "Boundary scan for targeted capture",
        "Background install/polling scan",
        "Control/capture dependency scan",
        "stale AG3 cursor scan",
        "Stage AG4 completion:",
        "PR #165 merged at `2026-05-09T15:05:18Z`",
        "PR #165 Windows Harness concluded `success`",
        "post-AG4 `main` Windows Harness concluded `success`",
        "Stage AG5 initialization:",
        "`v0.1.17` remains published, not a draft, not a prerelease",
        "git fetch origin tag v0.1.17",
        "changes since the published `v0.1.17` tag are docs/tests only",
        "confirming no runtime, helper/watcher, or version-metadata diff",
        "Stage AG5 local validation:",
        "passed, 77 tests",
        "passed, 179 tests",
        "stale AG4 cursor scan",
        "python harness/scripts/run_harness.py",
        "Stage AG5 completion:",
        "PR #166 merged at `2026-05-09T15:25:36Z`",
        "PR #166 Windows Harness concluded `success`",
        "post-AG5 `main` Windows Harness concluded `success`",
        "Returned the active cursor to blueprint implementation after AG5",
        "Phase 6 privacy-enrichment contract preflight",
        "Stage AG6 completion:",
        "PR #167 merged at `2026-05-09T15:44:18Z`",
        "PR #167 Windows Harness concluded `success`",
        "post-AG6 `main` Windows Harness concluded `success`",
        "Phase 6 privacy-enrichment contract preflight local validation:",
        "passed, 87 tests",
        "passed, 184 tests",
        "Product-source contract-artifact reference scan",
        "passed with no matches",
        "Phase 6 privacy-enrichment contract preflight completion:",
        "PR #168 merged at `2026-05-09T16:10:11Z`",
        "PR #168 Windows Harness concluded `success`",
        "post-preflight `main` Windows Harness concluded `success`",
        "Phase 6 privacy-enrichment contract preflight reconciliation local validation:",
        "passed, 76 tests",
        "stale preflight-in-progress cursor scan",
        "passed with no files",
        "Phase 6 privacy-enrichment contract preflight reconciliation completion:",
        "PR #169 merged at `2026-05-09T16:25:46Z`",
        "PR #169 Windows Harness concluded `success`",
        "post-reconciliation `main` Windows Harness concluded `success`",
        "Started the Phase 6 committed negative contract fixture expansion",
        "Phase 6 privacy-enrichment contract fixture expansion local validation:",
        "Product-source contract-artifact reference scan",
        "Phase 6 privacy-enrichment contract fixture expansion completion:",
        "PR #170 merged at `2026-05-09T16:44:08Z`",
        "PR #170 Windows Harness concluded `success`",
        "post-fixture-expansion `main` Windows Harness concluded `success`",
        "Selected the remaining negative fixture expansion",
        "Phase 6 privacy-enrichment contract fixture expansion reconciliation local validation:",
        "stale fixture-expansion-in-progress cursor scan",
        "Phase 6 privacy-enrichment contract fixture expansion reconciliation completion:",
        "PR #171 merged at `2026-05-09T16:56:46Z`",
        "PR #171 Windows Harness concluded `success`",
        "post-reconciliation `main` Windows Harness concluded `success`",
        "Started the Phase 6 remaining negative fixture expansion",
        "Phase 6 privacy-enrichment remaining negative fixture local validation:",
        "Phase 6 privacy-enrichment remaining negative fixture completion:",
        "PR #172 merged at `2026-05-09T17:16:13Z`",
        "PR #172 Windows Harness concluded `success`",
        "post-remaining-fixtures `main` Windows Harness concluded `success`",
        "Selected the next Phase 6 step as a contract coverage audit",
        "Started the Phase 6 contract coverage audit",
        "all historical unsafe in-memory variants now map one-to-one to committed invalid fixtures",
        "high-signal schema-enforced branches",
        "Phase 6 privacy-enrichment remaining fixture reconciliation local validation:",
        "stale remaining-fixture-in-progress cursor scan",
        "Phase 6 privacy-enrichment contract coverage audit local validation:",
        "passed, 88 tests",
        "passed, 185 tests",
        "Phase 6 privacy-enrichment contract coverage audit completion:",
        "PR #174 merged at `2026-05-09T17:49:10Z`",
        "PR #174 Windows Harness concluded `success`",
        "post-coverage-audit `main` Windows Harness concluded `success`",
        "Selected the next Phase 6 step as a targeted contract gap fixture expansion",
        "Phase 6 privacy-enrichment coverage audit reconciliation local validation:",
        "Phase 6 privacy-enrichment coverage audit reconciliation completion:",
        "PR #175 merged at `2026-05-09T18:03:25Z`",
        "PR #175 Windows Harness concluded `success`",
        "Started the Phase 6 targeted contract gap fixture expansion",
        "Phase 6 privacy-enrichment contract gap fixture local validation:",
        "passed, 89 tests",
        "passed, 186 tests",
        "Phase 6 privacy-enrichment contract gap fixture completion:",
        "PR #176 merged at `2026-05-09T18:18:56Z`",
        "PR #176 Windows Harness concluded `success`",
        "post-gap-fixtures `main` Windows Harness concluded `success`",
        "Selected the next Phase 6 step as a residual schema coverage audit",
    ):
        assert phrase in normalized

    for tool_name in TOOL_NAMES:
        assert f"`{tool_name}`" in text


def test_post_v0116_plan_is_completed_without_expanding_scope():
    text = POST_V0116_PLAN.read_text(encoding="utf-8")
    normalized = _normalized(text)

    for phrase in (
        "`v0.1.17` is published at https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.17",
        "`v0.1.16` remains the previous stable release",
        "release tag targets `5b260edc3bddc48986e52179b2ffd261856a89ac`",
        "tag targets `255f2a01cddde330d756a87359c4d3a8be4b11a2`",
        "published at `2026-05-09T12:56:45Z`",
        "published at `2026-05-09T09:31:17Z`",
        "post-v0.1.16 maintenance round is complete",
        "active next cursor is now [Post-v0.1.17 maintenance plan]",
        "Current stage: AF7 - v0.1.17 Publication Reconciliation.",
        "Stage status: AF7 complete; this post-v0.1.16 cursor is completed historical context.",
        "docs/release-v0.1.17.md",
        "AF7 publication reconciliation PR #160 merged as",
        "`110ace3f27d8bb9f1eff2c45449998fd0373a998`",
        "PR Windows Harness run `25601966464` passed",
        "post-merge `main` Windows Harness run `25602018700` passed",
        "post-AF7 `main` Windows Harness run `25602018700` concluded `success`",
        "PR #159 merged as",
        "`5b260edc3bddc48986e52179b2ffd261856a89ac`",
        "PR #159, PR Windows Harness run `25601571665`",
        "post-merge Windows Harness run `25601624151`",
        "release created at https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.17",
        "gh release view v0.1.17",
        "git ls-remote --tags origin v0.1.17",
        "Next atomic task: continue the post-v0.1.17 maintenance cursor",
        "next-round-plan-post-v0.1.17.md",
        "AF3 MCP/memory review PR #154 merged as",
        "`f55638cf213b40c07d01f1872a7ff828b3a85d6f`",
        "PR #154 Windows Harness run `25599715499`",
        "post-AF3 `main` Windows Harness concluded `success`",
        "docs/mcp-memory-contract-sweep-post-v0.1.16.md",
        "`generate-memory` manifest JSON omitted observed-content trust metadata",
        "standalone MCP smoke should freeze a literal tool list",
        "full forbidden write/file/network/control term set",
        "invalid embedded helper payloads",
        "`watch --events` validation diagnostic leak",
        "Stage AF0 - Post-v0.1.16 Baseline Cursor",
        "Stage AF1 - Public Metadata And Evidence Freshness Follow-up",
        "Stage AF2 - Helper And Watcher Preview Diagnostics Review",
        "Stage AF3 - MCP And Memory Contract Review",
        "Stage AF4 - Compatibility Guardrail Sweep",
        "Stage AF5 - Release-Readiness Decision",
        "Stage AF6 - v0.1.17 Release Readiness",
        "Stage AF7 - v0.1.17 Publication Reconciliation",
        "manual UIA smoke freshness decision",
        "Do not retag `v0.1.17`",
        "Do not retag `v0.1.16`",
        "CLI command set remains unchanged",
        "`generate-memory` manifest JSON includes the compatible AF3 trust-boundary fields",
        "MCP tool list remains unchanged and read-only",
        "Do not implement screenshot capture, OCR, audio recording",
        "Phase 6 remains privacy spec/scorecard only",
        "gh release view v0.1.16",
        "git rev-parse v0.1.16",
        "git ls-remote --tags origin v0.1.16",
        "Stage AF0 baseline landing:",
        "Stage AF1 initialization:",
        "gh repo view YSCJRH/WinChronicle",
        "repository is public on `main`, with empty description, homepage, and topics",
        "post-AF0 `main` Windows Harness concluded `success`",
        "Stage AF1 local validation:",
        "57 tests passed",
        "155 tests passed",
        "python harness/scripts/run_harness.py",
        "Stage AF1 completion:",
        "PR #150 Windows Harness run `25598506221`",
        "post-AF1 `main` Windows Harness concluded `success`",
        "Stage AF1 completion reconciliation:",
        "PR #151 Windows Harness run `25598644752`",
        "post-AF1-completion `main` Windows Harness concluded `success`",
        "Stage AF2 local validation:",
        "92 tests passed",
        "160 tests passed",
        "python harness/scripts/run_install_cli_smoke.py",
        "Stage AF2 completion:",
        "PR #152 Windows Harness run `25599095958`",
        "post-AF2 `main` Windows Harness concluded `success`",
        "Stage AF2 completion reconciliation:",
        "PR #153 Windows Harness run `25599243227`",
        "post-AF2-completion `main` Windows Harness concluded `success`",
        "Stage AF3 local validation:",
        "80 tests passed",
        "162 tests passed",
        "python harness/scripts/run_mcp_smoke.py",
        "Stage AF3 completion:",
        "PR #154 Windows Harness run `25599715499`",
        "post-AF3 `main` Windows Harness concluded `success`",
        "Stage AF4 local validation:",
        "50 tests passed",
        "113 tests passed",
        "165 tests passed",
        "Boundary scan and control/capture dependency scan reviewed only existing",
        "no new product CLI/MCP targeted capture",
        "Stage AF4 completion:",
        "PR #156 Windows Harness run `25600358015`",
        "PR #156 merged as `20758124f5679be3a733ac0de8ed9c99e1d8777b`",
        "post-AF4 `main` Windows Harness concluded `success`",
        "Stage AF4 completion reconciliation:",
        "PR #157 Windows Harness run `25600542270`",
        "PR #157 merged as `74aeadc2e8fd0917ab02e0f73009f87453b4b1e8`",
        "post-AF4-completion `main` Windows Harness concluded `success`",
        "Stage AF5 release-readiness decision:",
        "`v0.1.16` remains published, not a draft, not a prerelease",
        "git diff --name-status v0.1.16..HEAD",
        "include runtime/output changes in `src/winchronicle/cli.py`, `src/winchronicle/memory.py`, and `src/winchronicle/mcp/server.py`",
        "runtime changes are narrow compatible privacy/trust-boundary hardenings",
        "65 tests passed",
        "166 tests passed",
        "python harness/scripts/run_harness.py",
        "Stage AF5 completion:",
        "PR #158 Windows Harness run `25600947496`",
        "PR #158 merged as `bbf6d3c64d7fef435e66d64d4e3b19d2390c391b`",
        "post-AF5 `main` Windows Harness concluded `success`",
        "Stage AF6 manual smoke:",
        "smoke-uia-notepad.ps1",
        "smoke-uia-edge.ps1",
        "smoke-uia-vscode.ps1",
        "diagnostic failure, non-blocking",
        "heartbeat-only liveness diagnostic",
        "Stage AF6 local deterministic validation:",
        "71 tests passed",
        "167 tests passed",
        "Stage AF6 completion and publication:",
        "PR #159 Windows Harness run `25601571665`",
        "PR #159 merged as `5b260edc3bddc48986e52179b2ffd261856a89ac`",
        "post-AF6 `main` Windows Harness concluded `success`",
        "gh release create v0.1.17",
        "`v0.1.17` is published, not a draft, not a prerelease",
        "Stage AF7 completion:",
        "PR #160 Windows Harness run `25601966464`",
        "PR #160 merged as `110ace3f27d8bb9f1eff2c45449998fd0373a998`",
        "post-AF7 `main` Windows Harness concluded `success`",
    ):
        assert phrase in normalized

    for tool_name in TOOL_NAMES:
        assert f"`{tool_name}`" in text


def test_public_metadata_audit_post_v017_records_manual_gaps_without_scope_expansion():
    text = PUBLIC_METADATA_V0117.read_text(encoding="utf-8")

    for phrase in (
        "Public Metadata Audit After v0.1.17",
        "does not change product behavior, schemas,\nCLI/MCP JSON shape",
        "gh repo view YSCJRH/WinChronicle",
        "Visibility | `PUBLIC`",
        "Default branch | `main`",
        "Description | Empty",
        "Homepage URL | Empty",
        "Repository topics | Empty / not configured",
        "gh release view v0.1.17",
        "Release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.17",
        "Target | `5b260edc3bddc48986e52179b2ffd261856a89ac`",
        "Draft | `false`",
        "Prerelease | `false`",
        "Published at | `2026-05-09T12:56:45Z`",
        "gh release view v0.1.16",
        "Release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.16",
        "Target | `255f2a01cddde330d756a87359c4d3a8be4b11a2`",
        "Run | `25602345201`",
        "Head SHA | `a994ab768deeaf08746bad296c1f8100d6ed22fb`",
        "README.md` starts with \"UIA-first local memory for Windows agents.\"",
        "docs/operator-quickstart.md` links release checklist",
        "active post-v0.1.17 plan",
        "current post-v0.1.17 audit",
        "published `v0.1.17` maintenance release",
        "previous stable `v0.1.16` final release",
        "historical `v0.1.16-rc.0` prerelease evidence",
        "GitHub repository description",
        "GitHub homepage URL",
        "GitHub topics",
        "Social preview image",
        "manual maintainer checklist item",
        "AF6 manual UIA smoke remains fresh for the published `v0.1.17` maintenance\n  release record only",
        "no required product-code change",
        "The next smallest implementation task is AG2",
    ):
        assert phrase in text

    assert "This audit does not authorize screenshots" in text


def test_public_metadata_audit_post_v016_records_manual_gaps_without_scope_expansion():
    text = PUBLIC_METADATA_V0116.read_text(encoding="utf-8")

    for phrase in (
        "Public Metadata Audit After v0.1.16",
        "does not change product behavior, schemas,\nCLI/MCP JSON shape",
        "gh repo view YSCJRH/WinChronicle",
        "Visibility | `PUBLIC`",
        "Default branch | `main`",
        "Description | Empty",
        "Homepage URL | Empty",
        "Repository topics | Empty / not configured",
        "gh release view v0.1.16",
        "Release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.16",
        "Target | `255f2a01cddde330d756a87359c4d3a8be4b11a2`",
        "Draft | `false`",
        "Prerelease | `false`",
        "Published at | `2026-05-09T09:31:17Z`",
        "Run | `25598257646`",
        "Head SHA | `85172956c978fbb6b3355d7e3e75e2ba25fc909a`",
        "README.md` starts with \"UIA-first local memory for Windows agents.\"",
        "docs/operator-quickstart.md` links release checklist",
        "active post-v0.1.16 plan",
        "GitHub repository description",
        "GitHub homepage URL",
        "GitHub topics",
        "Social preview image",
        "manual maintainer checklist item",
        "AE2 manual UIA smoke remains fresh for the published `v0.1.16` final release",
        "no required product-code change",
        "The next smallest implementation task is AF2",
    ):
        assert phrase in text

    assert "This audit does not authorize screenshots" in text


def test_helper_watcher_diagnostics_sweep_post_v017_is_docs_only_and_scoped():
    text = HELPER_WATCHER_V0117.read_text(encoding="utf-8")
    normalized = _normalized(text)

    for phrase in (
        "Helper And Watcher Diagnostics Sweep After v0.1.17",
        "published `v0.1.17` maintenance release",
        "AG1 public metadata audit",
        "does not change schemas, successful CLI/MCP JSON shape",
        "Helper quality matrix",
        "Watcher preview docs",
        "Operator diagnostics",
        "Capture quality scorecard",
        "Deterministic tests",
        "Helper timeout",
        "Helper malformed JSON",
        "Helper empty stdout",
        "Helper nonzero exit",
        "Watcher nonzero exit",
        "Helper failure surfaced by watcher",
        "Malformed watcher JSONL",
        "Invalid embedded helper payload",
        "Watcher timeout",
        "Heartbeat-only run",
        "Duplicate skip",
        "Denylist or lock-screen skip",
        "Raw watcher JSONL persistence",
        "Product targeted-capture pass-through",
        "AG2 found no new helper/watcher diagnostics drift",
        "no observed-content echo",
        "raw watcher JSONL non-persistence",
        "product targeted-capture pass-through rejection",
        "No schema, successful CLI/MCP JSON, helper/watcher capture behavior",
        "Fresh manual UIA smoke remains outside default CI",
        "AF6 manual UIA smoke is fresh for the published `v0.1.17` maintenance release record",
        "The next smallest implementation task is to land this AG2 review",
        "Validation Log",
        "passed, 94 tests",
        "passed, 172 tests",
        "Stale AG0/AG1 cursor and v0.1.16 helper/watcher typo scan",
        "python harness/scripts/run_harness.py",
        "does not authorize screenshot capture",
        "product targeted capture",
        "live UIA smoke in default CI",
    ):
        assert phrase in normalized


def test_helper_watcher_diagnostics_sweep_post_v016_is_docs_only_and_scoped():
    text = HELPER_WATCHER_V0116.read_text(encoding="utf-8")
    normalized = _normalized(text)

    for phrase in (
        "Helper And Watcher Diagnostics Sweep After v0.1.16",
        "published `v0.1.16` final release",
        "AF1 completion reconciliation",
        "added a narrow content-free CLI diagnostic fix",
        "does not change schemas, successful CLI/MCP JSON shape",
        "Helper quality matrix",
        "Watcher preview docs",
        "Operator diagnostics",
        "Capture quality scorecard",
        "Deterministic tests",
        "Helper timeout",
        "Helper malformed JSON",
        "Helper empty stdout",
        "Helper nonzero exit",
        "Watcher nonzero exit",
        "Helper failure surfaced by watcher",
        "Malformed watcher JSONL",
        "Invalid embedded helper payload",
        "Watcher timeout",
        "Heartbeat-only run",
        "Duplicate skip",
        "Denylist or lock-screen skip",
        "Raw watcher JSONL persistence",
        "AF2 found one helper/watcher diagnostics drift",
        "stable content-free diagnostic",
        "added focused deterministic evidence",
        "no capture behavior change is warranted",
        "Harness smoke may use a temporary fake-helper event file outside state",
        "Fresh manual UIA smoke remains outside default CI",
        "The next smallest implementation task is to land this AF2 review",
        "does not authorize screenshot capture",
        "product targeted capture",
        "live UIA smoke in default CI",
    ):
        assert phrase in normalized


def test_mcp_memory_contract_sweep_post_v016_records_trust_boundary_fix():
    text = MCP_MEMORY_V0116.read_text(encoding="utf-8")
    normalized = _normalized(text)

    for phrase in (
        "MCP And Memory Contract Sweep After v0.1.16",
        "published `v0.1.16` final release",
        "AF2 completion reconciliation",
        "compatible trust-boundary guardrail fixes",
        "`generate-memory` manifest JSON now marks observed-derived metadata as untrusted",
        "standalone MCP smoke now uses a literal expected tool list",
        "does not change schemas, MCP tool list, MCP tool schemas",
        "MCP examples",
        "MCP scorecard",
        "Memory scorecard",
        "Deterministic demo",
        "Operator quickstart",
        "Deterministic tests",
        "Exact MCP tool list",
        "Read-only MCP boundary",
        "Observed-content trust boundary",
        "Memory manifest JSON",
        "`trust`, `untrusted_observed_content`, and `instruction`",
        "`desktop_control`, `control_desktop`, `press_key`, `capture_hwnd`",
        "No fresh manual UIA smoke is required to land this AF3 review",
        "future release-readiness record should make a fresh manual-smoke freshness decision",
        "The next smallest implementation task is to land this AF3 review",
        "does not authorize MCP write tools",
        "arbitrary file reads",
        "product targeted capture",
        "live UIA smoke in default CI",
    ):
        assert phrase in normalized


def test_mcp_memory_contract_sweep_post_v017_records_current_review():
    text = MCP_MEMORY_V0117.read_text(encoding="utf-8")
    normalized = _normalized(text)

    for phrase in (
        "MCP And Memory Contract Sweep After v0.1.17",
        "published `v0.1.17` maintenance release",
        "AG2 helper/watcher diagnostics review",
        "found no new drift requiring product code",
        "schema, MCP tool-list, MCP tool-schema",
        "MCP examples",
        "MCP scorecard",
        "Memory scorecard",
        "Deterministic demo",
        "Operator quickstart",
        "Deterministic tests",
        "Exact MCP tool list",
        "Read-only MCP boundary",
        "Observed-content trust boundary",
        "MCP `search_memory` parity",
        "MCP `search_captures` parity",
        "Durable memory Markdown",
        "Memory manifest JSON",
        "Memory FTS",
        "Idempotent memory generation",
        "Secret exclusion",
        "Fixture-only demo",
        "`trust`, `untrusted_observed_content`, and `instruction`",
        "`desktop_control`, `control_desktop`, `press_key`, `capture_hwnd`",
        "No fresh manual UIA smoke is required to land this AG3 review",
        "The next smallest implementation task is to land this AG3 review",
        "Validation Log",
        "passed, 93 tests",
        "passed, 175 tests",
        "stale AG2 cursor scan",
        "python harness/scripts/run_harness.py",
        "does not authorize MCP write tools",
        "arbitrary file reads",
        "product targeted capture",
        "live UIA smoke in default CI",
    ):
        assert phrase in normalized


def test_compatibility_guardrail_sweep_post_v016_records_precision_fixes():
    text = COMPATIBILITY_V0116.read_text(encoding="utf-8")
    normalized = _normalized(text)

    for phrase in (
        "Compatibility Guardrail Sweep After v0.1.16",
        "AF4 compatibility check",
        "documentation and guardrail precision fixes",
        "`generate-memory` manifest JSON now has a frozen trust-boundary shape",
        "does not change schemas, MCP tool schemas",
        "Version identity",
        "Exact read-only MCP tool list",
        "Disabled privacy surfaces",
        "Observed-content trust boundary",
        "Watcher preview limits",
        "Durable memory contract",
        "Phase 6 spec-only status",
        "Product targeted capture absence",
        "current_context",
        "search_captures",
        "search_memory",
        "read_recent_capture",
        "recent_activity",
        "privacy_status",
        'trust = "untrusted_observed_content"',
        "AF4 fixed README ordering and made MCP smoke compare ordered tool names",
        "AF4 fixed quickstart wording to name every disabled targeted flag",
        "50 passed",
        "No new product CLI/MCP targeted capture",
        "No new runtime dependency or implementation path was found",
        "found and fixed four narrow compatibility evidence drifts",
        "preserving the stable CLI command set",
        "The next smallest implementation task is to land this AF4 review",
    ):
        assert phrase in normalized


def test_compatibility_guardrail_sweep_post_v017_records_current_review():
    text = COMPATIBILITY_V0117.read_text(encoding="utf-8")
    normalized = _normalized(text)

    for phrase in (
        "Compatibility Guardrail Sweep After v0.1.17",
        "AG4 compatibility check",
        "found no required schema",
        "Version identity",
        "Exact read-only MCP tool list",
        "Disabled privacy surfaces",
        "Observed-content trust boundary",
        "Watcher preview limits",
        "Durable memory contract",
        "Phase 6 spec-only status",
        "Product targeted capture absence",
        "current_context",
        "search_captures",
        "search_memory",
        "read_recent_capture",
        "recent_activity",
        "privacy_status",
        'trust = "untrusted_observed_content"',
        "tests/test_privacy_check.py",
        "55 passed",
        "177 passed",
        "Stale cursor scan",
        "WinChronicle harness passed",
        "pass-through rejection tests now cover every disabled helper/watcher surface flag",
        "operator diagnostics now names the full disabled product targeted-capture flag set",
        "No new product CLI/MCP targeted capture",
        "Background install/polling scan",
        "No product daemon/service install",
        "No new runtime dependency or implementation path was found",
        "AG4 found no required schema",
        "The next smallest implementation task is to land this AG4 review",
    ):
        assert phrase in normalized

    for boundary in (
        "MCP write tools",
        "arbitrary file read tools",
        "screenshot capture",
        "OCR",
        "audio recording",
        "keyboard capture",
        "clipboard capture",
        "network upload",
        "LLM calls",
        "desktop control",
        "product targeted capture",
        "daemon/service install",
        "polling capture loops",
        "default background capture",
        "live UIA smoke in default CI",
    ):
        assert boundary in normalized


def test_release_readiness_decision_post_v016_starts_v017_readiness():
    text = RELEASE_DECISION_V0116.read_text(encoding="utf-8")
    normalized = _normalized(text)

    for phrase in (
        "Release-Readiness Decision After v0.1.16",
        "AF5 record",
        "start a narrow `v0.1.17` maintenance release-readiness plan",
        "not immediate publication",
        "Do not retag `v0.1.16`",
        "compatible privacy, trust-boundary, diagnostics, documentation",
        "include unreleased runtime/output changes",
        "Is a release-readiness path warranted? | Yes.",
        "Is immediate publication warranted? | No.",
        "Should `v0.1.16` be retagged? | No.",
        "Should the next release-readiness target be `v0.1.17`? | Yes.",
        "Is fresh manual UIA smoke decided here? | No.",
        "Create a narrow `v0.1.17` release-readiness record",
        "`src/winchronicle/cli.py` | `watch --events` handles invalid embedded helper payloads",
        "`src/winchronicle/memory.py` | `generate-memory` manifest JSON now includes `trust`",
        "`src/winchronicle/mcp/server.py` | MCP control-like tool rejection was hardened",
        "Additive CLI JSON trust-boundary change",
        "Latest published release remains",
        "https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.16",
        "`v0.1.16` is not a draft or prerelease",
        "remain `0.1.16` until a release-readiness branch explicitly changes version",
        "AF4 completion merged as `74aeadc2e8fd0917ab02e0f73009f87453b4b1e8`",
        "run `25600584258` concluded `success`",
        "AF5 does not accept or reject that evidence for `v0.1.17`",
        "git diff --name-status v0.1.16..HEAD",
        "runtime changes exist in `src/winchronicle/cli.py`",
        "Result: passed, 65 tests.",
        "Full AF5 validation:",
        "full pytest reported 166 tests",
        "full deterministic harness passed",
        "does not authorize implementation of screenshot capture",
        "privacy-positive guardrails",
        "Land this AF5 release-readiness decision through PR and post-merge Windows Harness validation",
        "create the narrow `v0.1.17` release-readiness record",
    ):
        assert phrase in normalized


def test_release_readiness_decision_post_v017_declines_release_path():
    text = RELEASE_DECISION_V0117.read_text(encoding="utf-8")
    normalized = _normalized(text)

    for phrase in (
        "Release-Readiness Decision After v0.1.17",
        "AG5 record",
        "do not start a new release-readiness or publication path",
        "Do not retag `v0.1.17`",
        "documentation, evidence, deterministic-test, and compatibility guardrail maintenance only",
        "do not change runtime code",
        "Is a release-readiness path warranted? | No.",
        "Is immediate publication warranted? | No.",
        "Should `v0.1.17` be retagged? | No.",
        "Should the next release-readiness target be chosen here? | No.",
        "Is fresh manual UIA smoke decided here? | No.",
        "Start the next blueprint implementation lane",
        "`docs/` | Added AG1 public metadata audit",
        "`tests/` | Hardened documentation and compatibility assertions",
        "`src/winchronicle`, `resources`, `pyproject.toml` | No diff",
        "Latest published release remains",
        "https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.17",
        "`v0.1.17` is not a draft or prerelease",
        "AG4 completion merged as `ac01afc206852a8b2b52126d61aa91d633e4675b`",
        "AG4 PR Windows Harness run `25604208696` concluded `success`",
        "post-merge `main` Windows Harness run `25604269757`",
        "AG5 PR Windows Harness run `25604616542` concluded `success`",
        "AG5 merged as `a55f1024f2f0a131044eb6e288de945ec1dbb5b2` through PR #166",
        "post-merge `main` Windows Harness run `25604682902`",
        "git fetch origin tag v0.1.17",
        "git diff --name-status v0.1.17..HEAD",
        "runtime/resource/version diff commands printed no files",
        "focused docs/version validation reported 77 tests",
        "full pytest reported 179 tests",
        "stale AG4 cursor scan returned no matches",
        "full deterministic harness passed",
        "AG5 PR and post-merge validation:",
        "PR #166 merged at `2026-05-09T15:25:36Z`",
        "PR Windows Harness run `25604616542` concluded `success`",
        "post-AG5 `main` Windows Harness run `25604682902` concluded `success`",
        "AG5 does not authorize implementation of screenshot capture",
        "privacy-neutral guardrails and evidence maintenance",
        "Start the Phase 6 privacy-enrichment contract preflight",
        "Do not implement screenshot capture, OCR, raw screenshot caches",
    ):
        assert phrase in normalized

    for boundary in (
        "OCR",
        "audio recording",
        "keyboard capture",
        "clipboard capture",
        "network/cloud upload",
        "LLM calls",
        "desktop control",
        "product targeted capture",
        "daemon/service install",
        "polling capture loops",
        "default background capture",
        "MCP write tools",
        "arbitrary file read tools",
    ):
        assert boundary in normalized


def _normalized(text: str) -> str:
    return " ".join(text.split())
