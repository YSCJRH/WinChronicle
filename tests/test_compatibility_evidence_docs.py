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
POST_V0116_PLAN = ROOT / "docs" / "next-round-plan-post-v0.1.16.md"
PUBLIC_METADATA_V0116 = ROOT / "docs" / "public-metadata-audit-post-v0.1.16.md"
HELPER_WATCHER_V0116 = ROOT / "docs" / "helper-watcher-diagnostics-sweep-post-v0.1.16.md"
MCP_MEMORY_V0116 = ROOT / "docs" / "mcp-memory-contract-sweep-post-v0.1.16.md"


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
        "v0.1.16 final release record",
        "v0.1.16-rc.0 release candidate record",
        "v0.1.16 final-release plan",
        "Post-v0.1.16 maintenance plan",
        "Public metadata audit after v0.1.16",
        "Helper and watcher diagnostics sweep after v0.1.16",
        "MCP and memory contract sweep after v0.1.16",
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
        "v0.1.16 final release record",
        "v0.1.16-rc.0 release candidate record",
        "v0.1.16 final-release plan",
        "Post-v0.1.16 maintenance plan",
        "Public metadata audit after v0.1.16",
        "Helper and watcher diagnostics sweep after v0.1.16",
        "MCP and memory contract sweep after v0.1.16",
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


def test_post_v0116_plan_is_active_without_expanding_scope():
    text = POST_V0116_PLAN.read_text(encoding="utf-8")
    normalized = _normalized(text)

    for phrase in (
        "`v0.1.16` is published at https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.16",
        "tag targets `255f2a01cddde330d756a87359c4d3a8be4b11a2`",
        "published at `2026-05-09T09:31:17Z`",
        "Current stage: AF3 - MCP And Memory Contract Review.",
        "Stage status: AF3 review in progress; AF2 completion reconciliation is complete.",
        "AF2 completion PR #153 merged as",
        "`3f819b9c2fa9aaaffc2e23ad72c8142c94cd8a15`",
        "PR Windows Harness run `25599243227` passed",
        "post-merge `main` Windows Harness run `25599306888` passed",
        "docs/mcp-memory-contract-sweep-post-v0.1.16.md",
        "`generate-memory` manifest trust-boundary fix",
        "literal standalone MCP smoke tool-list guardrail",
        "expanded forbidden MCP stdio call evidence",
        "invalid embedded helper payloads",
        "`watch --events` validation diagnostic leak",
        "Next atomic task: land this AF3 review",
        "Stage AF0 - Post-v0.1.16 Baseline Cursor",
        "Stage AF1 - Public Metadata And Evidence Freshness Follow-up",
        "Stage AF2 - Helper And Watcher Preview Diagnostics Review",
        "Stage AF3 - MCP And Memory Contract Review",
        "Stage AF4 - Compatibility Guardrail Sweep",
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
    ):
        assert phrase in normalized

    for tool_name in TOOL_NAMES:
        assert f"`{tool_name}`" in text


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


def test_helper_watcher_diagnostics_sweep_post_v016_is_docs_only_and_scoped():
    text = HELPER_WATCHER_V0116.read_text(encoding="utf-8")
    normalized = _normalized(text)

    for phrase in (
        "Helper And Watcher Diagnostics Sweep After v0.1.16",
        "published `v0.1.16` final release",
        "AF1 completion reconciliation",
        "adds a narrow content-free CLI diagnostic fix",
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


def _normalized(text: str) -> str:
    return " ".join(text.split())
