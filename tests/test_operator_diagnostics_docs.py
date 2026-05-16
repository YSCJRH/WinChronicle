from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_operator_diagnostics_covers_stable_failure_modes_without_content_echo():
    diagnostics = (ROOT / "docs" / "operator-diagnostics.md").read_text(encoding="utf-8")

    for expected_signal in (
        "SKIPPED: helper returned no capture",
        "ERROR: helper timed out",
        "ERROR: helper returned invalid JSON",
        "ERROR: helper failed with exit code <code>",
        "ERROR: watcher failed with exit code <code>",
        "ERROR: watcher JSONL line <n> is malformed",
        "ERROR: watcher output could not be captured safely",
        "ERROR: watcher timed out",
        "captures_written: 0",
        "heartbeats > 0",
        "denylisted_skipped > 0",
        "duplicates_skipped > 0",
        "VS Code metadata smoke",
        "Strict Monaco editor marker capture is diagnostic and non-blocking",
    ):
        assert expected_signal in diagnostics

    for content_guard in (
        "Do not paste observed text",
        "Do not save or commit raw watcher JSONL",
        "record the local artifact path only",
        "Do not introduce screenshots",
        "`--window-title-regex`",
        "`--process-name`",
        "Targeted capture remains helper-only harness smoke",
    ):
        assert content_guard in diagnostics


def test_operator_quickstart_links_diagnostics_playbook():
    quickstart = (ROOT / "docs" / "operator-quickstart.md").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    maintenance_index = (ROOT / "docs" / "maintenance-index.md").read_text(encoding="utf-8")

    for expected in (
        "[Operator diagnostics](operator-diagnostics.md)",
        "[Deterministic demo](deterministic-demo.md)",
        "[Roadmap](roadmap.md)",
        "[Known limitations](known-limitations.md)",
        "[v0.1 closure note](goal-closure-v0.1.md)",
        "[Maintenance and release history index](maintenance-index.md)",
        "[Contributing](../CONTRIBUTING.md)",
    ):
        assert expected in quickstart

    for expected in (
        "[Operator quickstart](docs/operator-quickstart.md)",
        "[Roadmap](docs/roadmap.md)",
        "[v0.1 closure note](docs/goal-closure-v0.1.md)",
        "[Known limitations](docs/known-limitations.md)",
        "[Deterministic demo](docs/deterministic-demo.md)",
        "[Read-only MCP examples](docs/mcp-readonly-examples.md)",
        "[Watcher preview](docs/watcher-preview.md)",
        "[Maintenance and release history index](docs/maintenance-index.md)",
        "[Contributing](CONTRIBUTING.md)",
    ):
        assert expected in readme

    for expected in (
        "[Post-v0.1.18 maintenance plan](next-round-plan-post-v0.1.18.md)",
        "[Public metadata audit after v0.1.18](public-metadata-audit-post-v0.1.18.md)",
        "[Helper and watcher diagnostics sweep after v0.1.18](helper-watcher-diagnostics-sweep-post-v0.1.18.md)",
        "[MCP and memory contract sweep after v0.1.18](mcp-memory-contract-sweep-post-v0.1.18.md)",
        "[Compatibility guardrail sweep after v0.1.18](compatibility-guardrail-sweep-post-v0.1.18.md)",
        "[Release-readiness decision after v0.1.18](release-readiness-decision-post-v0.1.18.md)",
        "[Privacy-output release-readiness decision after v0.1.18](privacy-output-release-readiness-decision-post-v0.1.18.md)",
        "[v0.1.18 maintenance release record](release-v0.1.18.md)",
        "[v0.1.16-rc.0 release candidate record](release-candidate-v0.1.16-rc.0.md)",
        "[v0.1.0-rc.0 release record](release-candidate-v0.1.0-rc.0.md)",
    ):
        assert expected in maintenance_index

    assert "## Operator Docs" not in readme
    assert "## Current Maintenance Docs" not in quickstart
    assert "[Post-v0.1.18 maintenance plan](docs/next-round-plan-post-v0.1.18.md)" not in readme
    assert "[Post-v0.1.18 maintenance plan](next-round-plan-post-v0.1.18.md)" not in quickstart

def test_operator_entry_points_distinguish_current_cursor_from_history():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    quickstart = (ROOT / "docs" / "operator-quickstart.md").read_text(encoding="utf-8")
    maintenance_index = (ROOT / "docs" / "maintenance-index.md").read_text(encoding="utf-8")
    closure = (ROOT / "docs" / "goal-closure-v0.1.md").read_text(encoding="utf-8")
    roadmap = (ROOT / "docs" / "roadmap.md").read_text(encoding="utf-8")
    checklist = (ROOT / "docs" / "release-checklist.md").read_text(encoding="utf-8")
    evidence = (ROOT / "docs" / "release-evidence.md").read_text(encoding="utf-8")
    matrix = (ROOT / "docs" / "uia-helper-quality-matrix.md").read_text(encoding="utf-8")

    assert "The current status is a `v0.2` monitor-session baseline" in readme
    assert (
        "Do not continue the historical maintenance loop automatically."
        in " ".join(readme.split())
    )
    assert "Maintenance and release history index" in readme
    assert "The next step is human product review." in closure
    assert (
        "It is not a release-readiness record, publication plan, or new "
        "maintenance cursor."
    ) in " ".join(closure.split())
    assert "Do not create another compatibility sweep" in closure
    assert (
        "The current stable baseline is the `v0.2` monitor-session baseline"
    ) in " ".join(roadmap.split())
    assert "These are options for human review, not an automatically authorized backlog." in roadmap
    assert "Any future runtime behavior, capture-surface expansion, release path" in roadmap

    for forbidden_readme_phrase in (
        "active post-v0.1.18 maintenance plan",
        "completed post-v0.1.18 public metadata audit",
        "completed post-v0.1.17 maintenance plan",
        "older completed maintenance plans",
    ):
        assert forbidden_readme_phrase not in readme

    for historical_doc in (
        "next-round-plan-post-v0.1.18.md",
        "public-metadata-audit-post-v0.1.18.md",
        "helper-watcher-diagnostics-sweep-post-v0.1.18.md",
        "mcp-memory-contract-sweep-post-v0.1.18.md",
        "compatibility-guardrail-sweep-post-v0.1.18.md",
        "release-readiness-decision-post-v0.1.18.md",
        "privacy-output-release-readiness-decision-post-v0.1.18.md",
        "release-v0.1.19.md",
        "release-v0.1.18.md",
        "release-v0.1.17.md",
        "release-v0.1.16.md",
        "release-candidate-v0.1.16-rc.0.md",
        "release-candidate-v0.1.0-beta.0.md",
        "release-candidate-v0.1.0-beta.1.md",
        "release-candidate-v0.1.0-rc.0.md",
        "release-candidate-v0.1.0-rc.1.md",
    ):
        assert historical_doc in maintenance_index

    assert "release-v0.1.15.md" in checklist
    assert "release-v0.1.15.md" in evidence
    assert "release-v0.1.16.md" in checklist
    assert "release-v0.1.16.md" in evidence
    assert "release-v0.1.17.md" in checklist
    assert "release-v0.1.17.md" in evidence
    assert "release-v0.1.18.md" in checklist
    assert "release-v0.1.18.md" in evidence
    assert "release-v0.1.19.md" in checklist
    assert "release-v0.1.19.md" in evidence
    assert "Targeted capture requires both `--harness` and `WINCHRONICLE_HARNESS=1`" in matrix
    assert "product CLI and MCP expose no targeted HWND/PID/title capture" in matrix

def test_post_v014_plan_is_historical_without_expanding_scope():
    plan = (ROOT / "docs" / "next-round-plan-post-v0.1.4.md").read_text(
        encoding="utf-8"
    )

    for expected in (
        "Current stage: G - v0.1.5 Published Baseline Reconciliation.",
        "Stage status: G - v0.1.5 published; baseline reconciliation complete.",
        "Windows Harness run `25432718007` passed on that SHA",
        "`v0.1.5` is published at\nhttps://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.5",
        "pre-publication\n`main` Windows Harness run `25544832155` passed",
        "post-v0.1.5\nbaseline cursor before starting any new implementation work",
        "Phase 6 remains privacy spec/scorecard work only",
        "No screenshot capture, OCR, audio recording, keyboard capture, clipboard",
        "Product CLI still does not expose targeted `--hwnd`, `--pid`, or",
        "MCP remains read-only",
        "Known blockers: none.",
        "Stage P0 - Post-v0.1.4 Baseline Cursor",
        "Stage P1 - Release Evidence And Entry Hygiene",
        "Stage P2 - Manual Smoke Freshness Decision",
        "Stage P4 - v0.1.5 Release Readiness",
    ):
        assert expected in plan


def test_post_v015_plan_is_completed_without_expanding_scope():
    plan = (ROOT / "docs" / "next-round-plan-post-v0.1.5.md").read_text(
        encoding="utf-8"
    )
    normalized = " ".join(plan.split())

    for expected in (
        "Current stage: G - v0.1.6 Published Baseline Reconciliation.",
        "Stage status: G - v0.1.6 published; baseline reconciliation complete.",
        "`v0.1.6` is published at https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.6",
        "targets `914cf361ac5864fa31d393d125d14e45eeba96bc`",
        "S4 PR Windows Harness run `25551243900` passed",
        "post-merge `main` Windows Harness run `25551362920` passed",
        "Publication reconciliation PR #80 passed PR Windows Harness run `25552120656`",
        "merged as `371060498c70a4e1ff4e075b3fd247b704c6d3f7`",
        "Windows Harness run `25552214063` passed",
        "follow the post-v0.1.6 maintenance plan before starting new implementation work",
        "Stage S0 - Post-v0.1.5 Baseline Cursor",
        "Stage S1 - CI Runtime Maintenance Decision",
        "Stage S2 - Release Evidence And Entry Hygiene",
        "Stage S3 - Compatibility Guardrail Sweep",
        "Stage S4 - v0.1.6 Release Readiness",
        "No screenshot capture, OCR, audio recording, keyboard capture, clipboard",
        "Product CLI still does not expose targeted `--hwnd`, `--pid`, or",
        "MCP remains read-only",
        "Known blockers: none.",
        "pins `windows-2025-vs2026`",
        "audited operator-facing docs, scorecards, and tests",
        "source-level Phase 6 absence",
        "post-v0.1.5 path toward `v0.1.6`",
        "aligning version identity to `0.1.6`",
        "release-readiness record explicitly accepts inherited `v0.1.0` manual UIA",
        "This closes the post-v0.1.5 maintenance round.",
    ):
        assert expected in normalized


def test_post_v016_plan_is_completed_without_expanding_scope():
    plan = (ROOT / "docs" / "next-round-plan-post-v0.1.6.md").read_text(
        encoding="utf-8"
    )
    normalized = " ".join(plan.split())

    for expected in (
        "Current stage: G - v0.1.7 Published Baseline Reconciliation.",
        "Stage status: G - v0.1.7 published; baseline reconciliation complete.",
        "`v0.1.7` is published at https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.7",
        "targets `0b5969509754f78b218f823d0e6bb7a0ea61392b`",
        "Previous stable baseline: `v0.1.6` was published",
        "publication reconciliation PR #80 merged as `371060498c70a4e1ff4e075b3fd247b704c6d3f7`",
        "its PR Windows Harness run `25552120656` passed",
        "Windows Harness run `25552214063` passed",
        "PR #81 Windows Harness run `25553025094` - passed",
        "Post-merge `main` Windows Harness run `25553238476` - passed",
        "During T2, merged PR #83 as",
        "PR #83 Windows Harness run `25554431580` - passed",
        "`fb84fb2b2bf47cfe89680c898f3694f543d75c52`",
        "`25554520036`",
        "`25555063537`",
        "`6d1d8f94c56636c23daafcb4ceae24053ff226aa`",
        "`25555180274`",
        "`25556058760`",
        "merged as `0b5969509754f78b218f823d0e6bb7a0ea61392b`",
        "`25556207363`",
        "Stage T0 - Post-v0.1.6 Baseline Cursor",
        "Stage T1 - Evidence Freshness And Entry Hygiene",
        "Stage T2 - CI Runtime And Dependency Maintenance Scan",
        "Stage T3 - Compatibility Guardrail Sweep",
        "Stage T4 - v0.1.7 Release Readiness",
        "No screenshot capture, OCR, audio recording, keyboard capture, clipboard",
        "Product CLI still does not expose targeted `--hwnd`, `--pid`, or",
        "MCP remains read-only",
        "Known blockers: none.",
        "next compatible release target is `v0.1.7`",
        "Manual UIA smoke remains outside default CI",
        "Do not add real UIA smoke to default CI",
        "prepare a release candidate instead",
        "no deprecation or failed-log signal requiring a workflow/runtime change",
        "FORCE_JAVASCRIPT_ACTIONS_TO_NODE24",
        "windows-2025-vs2026",
        "no-action-needed CI runtime scan",
        "no-action-needed compatibility guardrail sweep",
        "exact read-only MCP tools",
        "product targeted capture absence",
        "Phase 6 spec-only status",
        "direct compatible `v0.1.7` path",
        "aligning version identity to `0.1.7`",
        "release-readiness record explicitly accepts inherited `v0.1.0` manual UIA smoke",
        "published `v0.1.7` from `0b5969509754f78b218f823d0e6bb7a0ea61392b`",
        "establish a post-v0.1.7 maintenance plan before starting",
        "gh release create v0.1.7",
    ):
        assert expected in normalized


def test_post_v017_plan_is_active_without_expanding_scope():
    plan = (ROOT / "docs" / "next-round-plan-post-v0.1.7.md").read_text(
        encoding="utf-8"
    )
    normalized = " ".join(plan.split())

    for expected in (
        "Current stage: G - v0.1.8 Published Baseline Reconciliation.",
        "Stage status: G - v0.1.8 published; baseline reconciliation complete.",
        "`v0.1.7` is published at https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.7",
        "targets `0b5969509754f78b218f823d0e6bb7a0ea61392b`",
        "`v0.1.8` is published at https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.8",
        "targets `1ea1e378aedb0a509d202fd32bc69704dbe903d4`",
        "PR #86 merged as `5e310f9c37836c5e6baa1bee7f89f91f701ff6e8`",
        "PR Windows Harness run `25556946503` passed",
        "post-merge `main` Windows Harness run `25557058094` passed",
        "Next atomic task: follow the post-v0.1.8 maintenance plan",
        "PR #87 Windows Harness run `25557993996` - passed",
        "`3ca1d2772c16ac11b7cfef8f4fe8b6fc28cb6636`",
        "Post-merge `main` Windows Harness run `25558154805` - passed",
        "Stage U0 - Post-v0.1.7 Baseline Cursor",
        "Stage U1 - Evidence Freshness And Entry Hygiene",
        "Stage U2 - CI Runtime And Dependency Maintenance Scan",
        "Stage U3 - Compatibility Guardrail Sweep",
        "Stage U4 - v0.1.8 Release Readiness",
        "No screenshot capture, OCR, audio recording, keyboard capture, clipboard",
        "Product CLI still does not expose targeted `--hwnd`, `--pid`, or",
        "MCP remains read-only",
        "Known blockers: none.",
        "next compatible release target is `v0.1.8`",
        "Manual UIA smoke remains outside default CI",
        "Do not add real UIA smoke to default CI",
        "avoids screenshot/OCR dependency drift",
        "prepare a release candidate instead",
        "exact read-only MCP tool list",
        "product targeted capture absence",
        "Phase 6 spec-only status",
        "Recorded PR #86 and post-merge Windows Harness run `25557058094`",
        "During U0, merged PR #87 as",
        "During U1, decided that inherited `v0.1.0` manual UIA smoke remains",
        "During U1, merged PR #88 as",
        "`bf7397711bc4f2f70ca677dc788464d6fa4f03f3`",
        "`25558809159`",
        "`25558922168`",
        "During U2, reviewed the latest `main` Windows Harness run",
        "no deprecation or failed-log signal requiring a workflow/runtime change",
        "no-action-needed CI runtime scan",
        "direct-dependency guard",
        "pyproject.toml` remains limited to deterministic project and dev",
        "During U2, merged PR #89 as",
        "`a6703f500c0140dba7ed4d2bcdf3427050745649`",
        "`25559501788`",
        "`25559686547`",
        "During U3, treated existing tests and scorecards as compatibility oracles",
        "version identity, exact read-only MCP",
        "Phase 6 spec-only and dependency/source absence",
        "no-action-needed compatibility guardrail sweep",
        "During U3, merged PR #90 as",
        "`8a25ec8abf2f91a912aaffd807ae4a4897847578`",
        "`25560353073`",
        "`25560483461`",
        "During U4, chose the direct compatible `v0.1.8` path",
        "During U4, the `v0.1.8` release-readiness record explicitly accepts",
        "aligned version identity to `0.1.8`",
        "During U4, merged PR #91 as",
        "`1ea1e378aedb0a509d202fd32bc69704dbe903d4`",
        "`25561704868`",
        "`25561832883`",
        "published `v0.1.8` from `1ea1e378aedb0a509d202fd32bc69704dbe903d4`",
        "follow the post-v0.1.8 maintenance plan before starting",
        "Stage U4 release-readiness validation:",
        "`python -m pytest -q` - passed with `111 passed`",
        "v0.1.8 publication validation:",
        "gh release create v0.1.8",
        "No fresh manual smoke is required in U1",
        "Do not retag `v0.1.7`",
        "Do not retag `v0.1.8`",
        "release-readiness record explicitly accepts it",
    ):
        assert expected in normalized


def test_post_v018_plan_is_historical_without_expanding_scope():
    plan = (ROOT / "docs" / "next-round-plan-post-v0.1.8.md").read_text(
        encoding="utf-8"
    )
    normalized = " ".join(plan.split())

    for expected in (
        "Current stage: G - v0.1.9 Published Baseline Reconciliation.",
        "Stage status: G - v0.1.9 published; baseline reconciliation complete.",
        "`v0.1.9` is published at https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.9",
        "targets `d06ab5bc8bea7520bac2719adb457794c72911d3`",
        "follow the post-v0.1.9 maintenance plan before starting",
        "The previous `v0.1.8` release is published at https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.8",
        "targets `1ea1e378aedb0a509d202fd32bc69704dbe903d4`",
        "PR #91 merged as `1ea1e378aedb0a509d202fd32bc69704dbe903d4`",
        "PR Windows Harness run `25561704868` passed",
        "post-merge `main` Windows Harness run `25561832883` passed",
        "PR #95 Windows Harness run `25564810377` - passed",
        "During W3, merged PR #95 as",
        "`36d430c478e65ad107125b7e87ed4ec18ac18709`",
        "Post-merge `main` Windows Harness run `25564926634` - passed",
        "Stage W0 - Post-v0.1.8 Baseline Cursor",
        "Stage W1 - Evidence Freshness And Entry Hygiene",
        "Stage W2 - CI Runtime And Dependency Maintenance Scan",
        "Stage W3 - Compatibility Guardrail Sweep",
        "Stage W4 - v0.1.9 Release Readiness",
        "No screenshot capture, OCR, audio recording, keyboard capture, clipboard",
        "Product CLI still does not expose targeted `--hwnd`, `--pid`, or",
        "MCP remains read-only",
        "Known blockers: none.",
        "next compatible release target is `v0.1.9`",
        "Manual UIA smoke remains outside default CI",
        "not expand the capture surface or start Phase 6 implementation",
        "Do not add real UIA smoke to default CI",
        "prepare a release candidate instead",
        "exact read-only MCP tool list",
        "product targeted capture absence",
        "Phase 6 remains spec-only",
        "Recorded PR #91 and post-merge Windows Harness run `25561832883`",
        "During W0, merged PR #92 as",
        "`6d44aad77eedfb2480147ae8c112c3e001da4710`",
        "`25562785206`",
        "`25562905132`",
        "During W1, decided that inherited `v0.1.0` manual UIA smoke remains",
        "No fresh manual smoke is required in W1",
        "During W1, merged PR #93 as",
        "`9c91f262ebb06f0b4fd8b4c38eeb17e8c688ecb9`",
        "`25563462333`",
        "`25563589781`",
        "During W2, reviewed the latest `main` Windows Harness run",
        "no deprecation or failed-log signal requiring a workflow/runtime change",
        "no-action-needed CI runtime scan",
        "direct-dependency guard",
        "pyproject.toml` remains limited to deterministic project and dev",
        "During W2, merged PR #94 as",
        "`f9dff37828abdedb95511aeaf204a1313b75727c`",
        "`25564182547`",
        "`25564339025`",
        "During W3, re-ran the existing compatibility guardrail tests",
        "No compatibility drift requiring product code",
        "no-action-needed compatibility sweep",
        "During W3, merged PR #95 as",
        "`36d430c478e65ad107125b7e87ed4ec18ac18709`",
        "`25564810377`",
        "`25564926634`",
        "During W4, chose the direct compatible `v0.1.9` path",
        "During W4, the `v0.1.9` release-readiness record explicitly accepts inherited",
        "During W4, aligned version identity to `0.1.9`",
        "published `v0.1.9` from `d06ab5bc8bea7520bac2719adb457794c72911d3`",
        "Do not retag `v0.1.8`",
        "Do not retag `v0.1.9`",
        "Stage W0 initialization:",
        "Stage W0 remote validation:",
        "Stage W1 remote validation:",
        "Stage W2 CI/runtime scan validation:",
        "Stage W2 remote validation:",
        "Stage W3 compatibility guardrail validation:",
        "Stage W3 remote validation:",
        "Stage W4 release-readiness validation:",
        "Stage W4 remote validation:",
        "v0.1.9 publication validation:",
        "gh release create v0.1.9",
        "python -m pytest tests/test_version_identity.py tests/test_compatibility_evidence_docs.py",
        "python -m pytest tests/test_operator_diagnostics_docs.py tests/test_compatibility_contracts.py",
        "python harness/scripts/run_harness.py` - passed",
        "FORCE_JAVASCRIPT_ACTIONS_TO_NODE24",
        "windows-2025-vs2026",
        "python -c \"import winchronicle; print(winchronicle.__version__)\"",
    ):
        assert expected in normalized


def test_post_v019_plan_is_historical_without_expanding_scope():
    plan = (ROOT / "docs" / "next-round-plan-post-v0.1.9.md").read_text(
        encoding="utf-8"
    )
    normalized = " ".join(plan.split())

    for expected in (
        "Current stage: G - v0.1.10 Published Baseline Reconciliation.",
        "Stage status: G - v0.1.10 published; baseline reconciliation complete.",
        "`v0.1.10` is published at https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.10",
        "targets `28b062a531519d4360911b51dfc083782b6dcbad`",
        "post-merge `main` Windows Harness run `25569567825` passed",
        "`v0.1.9` is published at https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.9",
        "targets `d06ab5bc8bea7520bac2719adb457794c72911d3`",
        "post-merge `main` Windows Harness run `25565697723` passed",
        "Stage X0 - Post-v0.1.9 Baseline Cursor",
        "Stage X1 - Evidence Freshness And Entry Hygiene",
        "Stage X2 - CI Runtime And Dependency Maintenance Scan",
        "Stage X3 - Compatibility Guardrail Sweep",
        "Stage X4 - v0.1.10 Release Readiness",
        "No screenshot capture, OCR, audio recording, keyboard capture, clipboard",
        "Product CLI still does not expose targeted `--hwnd`, `--pid`, or",
        "MCP remains read-only",
        "Known blockers: none.",
        "next compatible release target is `v0.1.10`",
        "Manual UIA smoke remains outside default CI",
        "not expand the capture surface or start Phase 6 implementation",
        "Do not add real UIA smoke to default CI",
        "prepare a release candidate instead",
        "exact read-only MCP tool list",
        "product targeted capture absence",
        "Phase 6 remains spec-only",
        "Recorded PR #96 and post-merge Windows Harness run `25565697723`",
        "Recorded X0 PR #97 and post-merge Windows Harness run `25566750349`",
        "During X1, accepted inherited `v0.1.0` manual UIA smoke as inherited/stale",
        "During X2, reviewed the latest `main` Windows Harness run `25567503424`",
        "FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: \"true\"",
        "actions/checkout@v6",
        "actions/setup-python@v6",
        "actions/setup-dotnet@v5",
        "depends only on `jsonschema` at runtime",
        "During X3, treated existing compatibility tests and scorecards as the",
        "exact read-only MCP tool names",
        "product targeted capture absence",
        "no product CLI/MCP targeted capture or new capture/control implementation was found",
        "During X4, chose the direct compatible `v0.1.10` path",
        "During X4, the `v0.1.10` release-readiness record explicitly accepts",
        "During X4, merged PR #101 as",
        "`28b062a531519d4360911b51dfc083782b6dcbad`",
        "`25569414864`",
        "`25569567825`",
        "Published `v0.1.10` from `28b062a531519d4360911b51dfc083782b6dcbad`",
        "Do not retag `v0.1.9`",
        "Stage X0 initialization:",
        "Stage X0 remote validation:",
        "Stage X1 remote validation:",
        "Stage X2 CI/runtime and dependency scan:",
        "Stage X2 remote validation:",
        "Stage X3 compatibility guardrail scan:",
        "Stage X3 remote validation:",
        "Stage X4 release-readiness validation:",
        "`python -m pytest -q` - passed, 115 tests.",
        "PR #101 Windows Harness run `25569414864` - passed.",
        "v0.1.10 publication validation:",
        "gh release create v0.1.10",
        "python -c \"import winchronicle; print(winchronicle.__version__)\"",
    ):
        assert expected in normalized


def test_post_v0110_plan_is_historical_without_expanding_scope():
    plan = (ROOT / "docs" / "next-round-plan-post-v0.1.10.md").read_text(
        encoding="utf-8"
    )
    normalized = " ".join(plan.split())

    for expected in (
        "Current stage: G - v0.1.11 Published Baseline Reconciliation.",
        "Stage status: G - v0.1.11 published; baseline reconciliation complete.",
        "`v0.1.10` is published at https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.10",
        "targets `28b062a531519d4360911b51dfc083782b6dcbad`",
        "Windows Harness run `25569567825` passed",
        "`v0.1.11` is published at https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.11",
        "targets `1724b0e47e6f6b915a99842fb971d7f9c503f65a`",
        "Windows Harness run `25573347339` passed",
        "follow the post-v0.1.11 maintenance plan before starting",
        "Stage Y0 - Post-v0.1.10 Baseline Cursor",
        "Stage Y1 - Evidence Freshness And Entry Hygiene",
        "Stage Y2 - CI Runtime And Dependency Maintenance Scan",
        "Stage Y3 - Compatibility Guardrail Sweep",
        "Stage Y4 - v0.1.11 Release Readiness",
        "No screenshot capture, OCR, audio recording, keyboard capture, clipboard",
        "Product CLI still does not expose targeted `--hwnd`, `--pid`, or",
        "MCP remains read-only",
        "Known blockers: none.",
        "next compatible release target is `v0.1.11`",
        "Manual UIA smoke remains outside default CI",
        "Do not add real UIA smoke to default CI",
        "prepare a release candidate instead",
        "exact read-only MCP tool list",
        "product targeted capture absence",
        "Phase 6 remains spec-only",
        "Do not retag `v0.1.10`",
        "Recorded Y0 PR #102 and post-merge Windows Harness run `25570603780`",
        "During Y1, accepted inherited `v0.1.0` manual UIA smoke as inherited/stale",
        "Recorded Y1 PR #103 and post-merge Windows Harness run `25571374301`",
        "During Y2, reviewed the latest `main` Windows Harness run `25571374301`",
        "FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: \"true\"",
        "actions/checkout@v6",
        "actions/setup-python@v6",
        "actions/setup-dotnet@v5",
        "depends only on `jsonschema` at runtime",
        "Recorded Y2 PR #104 and post-merge Windows Harness run `25572048167`",
        "During Y3, treated the existing compatibility tests and scorecards as",
        "exact read-only MCP tools",
        "watcher preview-only behavior",
        "No additional product tests were needed because no drift was found",
        "Recorded Y3 PR #105 and post-merge Windows Harness run `25572553734`",
        "During Y4, chose the direct compatible `v0.1.11` path",
        "During Y4, aligned package, runtime, and MCP server version identity to",
        "During Y4, the `v0.1.11` release-readiness record explicitly accepts",
        "During Y4, merged PR #106 as",
        "`1724b0e47e6f6b915a99842fb971d7f9c503f65a`",
        "`25573214374`",
        "`25573347339`",
        "Published `v0.1.11` from `1724b0e47e6f6b915a99842fb971d7f9c503f65a`",
        "Stage Y0 initialization:",
        "Stage Y0 local validation:",
        "Stage Y0 remote validation:",
        "Stage Y1 evidence freshness validation:",
        "Stage Y2 CI/runtime and dependency scan:",
        "Stage Y3 compatibility guardrail sweep:",
        "`python -m pytest tests/test_compatibility_contracts.py tests/test_mcp_tools.py tests/test_phase6_privacy_scorecard.py tests/test_watcher_events.py tests/test_state_compatibility.py tests/test_memory_pipeline.py -q` - passed, 44 tests.",
        "`python -m pytest tests/test_operator_diagnostics_docs.py tests/test_compatibility_contracts.py tests/test_mcp_tools.py tests/test_phase6_privacy_scorecard.py tests/test_watcher_events.py tests/test_state_compatibility.py tests/test_memory_pipeline.py -q` - passed, 56 tests.",
        "Stage Y4 release-readiness validation:",
        "`python -m pytest tests/test_version_identity.py tests/test_compatibility_evidence_docs.py tests/test_operator_diagnostics_docs.py -q` - passed",
        "`python -m pytest -q` - passed, 117 tests.",
        "PR #106 Windows Harness run `25573214374` - passed.",
        "v0.1.11 publication validation:",
        "gh release create v0.1.11",
        "python -c \"import winchronicle; print(winchronicle.__version__)\"",
    ):
        assert expected in normalized


def test_post_v0111_plan_is_published_reconciled_without_expanding_scope():
    plan = (ROOT / "docs" / "next-round-plan-post-v0.1.11.md").read_text(
        encoding="utf-8"
    )
    normalized = " ".join(plan.split())

    for expected in (
        "Current stage: G - v0.1.12 Published Baseline Reconciliation.",
        "Stage status: G - v0.1.12 published; baseline reconciliation complete.",
        "`v0.1.12` is published at https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.12",
        "targets `df16ea301243e2d3a612a5d09bd59f1436723fb4`",
        "Windows Harness run `25576867729` passed",
        "PR #107 Windows Harness run `25573927712`",
        "`8ca63acf7298564385f2a7ca777ff973aa7cb09b`",
        "Windows Harness run `25574042929` - passed",
        "PR #108 Windows Harness run `25574694437`",
        "`a24ae2435264790ba8c2cac243c996ce3db0ce88`",
        "Windows Harness run `25574855474` - passed",
        "PR #109 Windows Harness run `25575316043`",
        "`6ac84e7ff62a4d5bd11ac4a9ffec85cbf51a3991`",
        "Windows Harness run `25575439821` - passed",
        "PR #110 Windows Harness run `25575910225`",
        "`86be82cb153269bad68fb92806fa7701a1e8579c`",
        "post-merge Windows Harness run `25576068774` as",
        "Stage Z0 - Post-v0.1.11 Baseline Cursor",
        "Stage Z1 - Evidence Freshness And Entry Hygiene",
        "Stage Z2 - CI Runtime And Dependency Maintenance Scan",
        "Stage Z3 - Compatibility Guardrail Sweep",
        "Stage Z4 - v0.1.12 Release Readiness",
        "No screenshot capture, OCR, audio recording, keyboard capture, clipboard",
        "Product CLI still does not expose targeted `--hwnd`, `--pid`, or",
        "MCP remains read-only",
        "Known blockers: none.",
        "next compatible release target is `v0.1.12`",
        "Manual UIA smoke remains outside default CI",
        "Do not add real UIA smoke to default CI",
        "prepare a release candidate instead",
        "exact read-only MCP tool list",
        "product targeted capture absence",
        "Phase 6 remains spec-only",
        "Do not retag `v0.1.11`",
        "Recorded Z0 PR #107 and post-merge Windows Harness run `25574042929`",
        "During Z1, accepted inherited `v0.1.0` manual UIA smoke as inherited/stale",
        "Z4 explicitly accepted inherited evidence before `v0.1.12` publication",
        "Recorded Z1 PR #108 and post-merge Windows Harness run `25574855474`",
        "During Z2, reviewed the latest `main` Windows Harness run `25574855474`",
        "FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: \"true\"",
        "actions/checkout@v6",
        "actions/setup-python@v6",
        "actions/setup-dotnet@v5",
        "No screenshot/OCR/audio/keyboard/clipboard/network/LLM dependency drift was found",
        "Recorded Z2 PR #109 and post-merge Windows Harness run `25575439821`",
        "During Z3, treated the existing compatibility tests and scorecards as the compatibility oracles",
        "exact read-only MCP tools",
        "watcher preview-only behavior",
        "product targeted capture absence",
        "No additional product tests or code changes were needed",
        "Recorded Z3 PR #110 and post-merge Windows Harness run `25576068774`",
        "During Z4, chose the direct compatible `v0.1.12` path",
        "aligned package, runtime, and MCP server version identity to `0.1.12`",
        "the `v0.1.12` release-readiness record explicitly accepts",
        "Published `v0.1.12` from `df16ea301243e2d3a612a5d09bd59f1436723fb4`",
        "Stage Z0 initialization:",
        "Stage Z0 local validation:",
        "Stage Z0 remote validation:",
        "Stage Z1 evidence freshness validation:",
        "Stage Z1 remote validation:",
        "Stage Z2 CI/runtime and dependency scan:",
        "Stage Z2 remote validation:",
        "Stage Z3 compatibility guardrail sweep:",
        "current_context`, `search_captures`, `search_memory`, `read_recent_capture`, `recent_activity`, and `privacy_status`",
        "product targeted capture remained disabled",
        "Stage Z3 remote validation:",
        "Stage Z4 release-readiness validation:",
        "Stage Z4 remote validation:",
        "PR #111 Windows Harness run `25576751080` - passed.",
        "Post-merge `main` Windows Harness run `25576867729` - passed",
        "v0.1.12 publication validation:",
        "gh release create v0.1.12",
        "gh release view v0.1.12",
        "git rev-parse v0.1.12",
        "python -c \"import winchronicle; print(winchronicle.__version__)\"",
    ):
        assert expected in normalized


def test_post_v012_plan_is_active_without_expanding_scope():
    plan = (ROOT / "docs" / "next-round-plan-post-v0.1.12.md").read_text(
        encoding="utf-8"
    )
    normalized = " ".join(plan.split())

    for expected in (
        "Current stage: G - v0.1.13 Published Baseline Reconciliation.",
        "Stage status: G - `v0.1.13` published; baseline reconciliation complete.",
        "`v0.1.12` is published at https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.12",
        "targets `df16ea301243e2d3a612a5d09bd59f1436723fb4`",
        "Windows Harness run `25577701036` passed",
        "Published `v0.1.13` from `1070343d9bcfd60c48238835e26b6c32f9060ae7`",
        "post-merge `main` Windows Harness run `25580877004` passed",
        "publication reconciliation PR #119 passed PR Windows Harness run `25581510176`",
        "merged as `f4781a91f2120f3eca5088b87bf9034be752274f`",
        "Windows Harness run `25581662790` passed",
        "follow the post-v0.1.13 maintenance plan before starting new implementation work",
        "`3164d185e5d203b504bd78432032fa13003983f8`",
        "Recorded AA4 PR #117 and post-merge Windows Harness run `25580333158`",
        "`1c9cabec4d27b8c0e4e245d9a27ddcba96ed3a00`",
        "Post-merge `main` Windows Harness run `25580333158` - passed",
        "Stage AA0 - Post-v0.1.12 Baseline Cursor",
        "Stage AA1 - Blueprint Gap And Public Surface Audit",
        "Stage AA2 - Deterministic Demo And Operator Experience Refresh",
        "Stage AA3 - Issue, Roadmap, And Contribution Hygiene",
        "Stage AA4 - Compatibility Guardrail Sweep",
        "Stage AA5 - v0.1.13 Release Readiness",
        "next compatible release target is `v0.1.13`",
        "Phase 6 stays at spec/scorecard level",
        "MCP tool list remains unchanged and read-only",
        "Product CLI still does not expose targeted `--hwnd`, `--pid`",
        "Do not implement screenshot capture, OCR, audio recording",
        "Stage AA0 initialization:",
        "gh release view v0.1.12",
        "git rev-parse v0.1.12",
        "gh run view 25577701036",
        "Stage AA0 local validation:",
        "Stage AA0 remote validation:",
        "PR #113 Windows Harness run `25578139342` - passed.",
        "Post-merge `main` Windows Harness run `25578252392` - passed",
        "Stage AA1 blueprint gap audit validation:",
        "reviewed CLI evidence",
        "reviewed MCP evidence",
        "reviewed workflow/docs/harness surfaces",
        "Stage AA1 remote validation:",
        "PR #114 Windows Harness run `25578768178` - passed.",
        "Post-merge `main` Windows Harness run `25578855299` - passed",
        "Stage AA2 deterministic demo validation:",
        "First `python -m pytest tests/test_operator_diagnostics_docs.py tests/test_version_identity.py -q` attempt failed",
        "python -m pytest tests/test_operator_diagnostics_docs.py tests/test_version_identity.py -q` - passed, 17 tests.",
        "python -m pytest -q` - passed, 122 tests.",
        "python harness/scripts/run_install_cli_smoke.py` - passed.",
        "python harness/scripts/run_harness.py` - passed.",
        "git diff --check` - passed.",
        "Stage AA2 remote validation:",
        "PR #115 Windows Harness run `25579283981` - passed.",
        "Post-merge `main` Windows Harness run `25579389224` - passed",
        "Stage AA3 issue/roadmap/contribution validation:",
        "First `python -m pytest tests/test_operator_diagnostics_docs.py tests/test_version_identity.py -q` attempt failed",
        "python -m pytest tests/test_operator_diagnostics_docs.py tests/test_version_identity.py -q` - passed, 18 tests.",
        "python -m pytest -q` - passed, 123 tests.",
        "python harness/scripts/run_install_cli_smoke.py` - passed.",
        "python harness/scripts/run_harness.py` - passed.",
        "git diff --check` - passed.",
        "Stage AA3 remote validation:",
        "PR #116 Windows Harness run `25579782185` - passed.",
        "Post-merge `main` Windows Harness run `25579869673` - passed",
        "Stage AA4 compatibility guardrail sweep:",
        "python -m pytest tests/test_compatibility_contracts.py tests/test_mcp_tools.py",
        "passed, 45 tests.",
        "matches are existing disabled-surface contracts, sentinels, docs, tests",
        "historical plan evidence, privacy-policy canary text, deterministic fixture/golden content",
        "python -m pytest tests/test_operator_diagnostics_docs.py tests/test_version_identity.py -q` - passed, 19 tests.",
        "python -m pytest -q` - passed, 124 tests.",
        "python harness/scripts/run_install_cli_smoke.py` - passed.",
        "python harness/scripts/run_harness.py` - passed.",
        "git diff --check` - passed.",
        "Stage AA4 remote validation:",
        "PR #117 Windows Harness run `25580215098` - passed.",
        "Post-merge `main` Windows Harness run `25580333158` - passed",
        "Stage AA5 release-readiness validation:",
        "python -m pytest tests/test_version_identity.py tests/test_compatibility_evidence_docs.py tests/test_operator_diagnostics_docs.py -q` - passed, 34 tests.",
        "python -m pytest -q` - passed, 125 tests.",
        "python harness/scripts/run_install_cli_smoke.py` - passed.",
        "python harness/scripts/run_harness.py` - passed.",
        "git diff --check` - passed.",
        "Stage AA5 remote validation:",
        "PR #118 Windows Harness run `25580778260` - passed.",
        "Post-merge `main` Windows Harness run `25580877004` - passed",
        "v0.1.13 publication validation:",
        "gh release create v0.1.13",
        "gh release view v0.1.13",
        "git fetch --tags origin; git rev-parse v0.1.13",
        "printed `0.1.13`",
        "v0.1.13 publication reconciliation local validation:",
        "v0.1.13 publication reconciliation remote validation:",
        "PR #119 Windows Harness run `25581510176` - passed.",
        "PR #119 merged as `f4781a91f2120f3eca5088b87bf9034be752274f`.",
        "Post-merge `main` Windows Harness run `25581662790` - passed",
        "This closes the post-v0.1.12 maintenance round.",
    ):
        assert expected in normalized


def test_post_v013_plan_is_active_without_expanding_scope():
    plan = (ROOT / "docs" / "next-round-plan-post-v0.1.13.md").read_text(
        encoding="utf-8"
    )
    normalized = " ".join(plan.split())

    for expected in (
        "`v0.1.13` is published at https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.13",
        "targets `1070343d9bcfd60c48238835e26b6c32f9060ae7`",
        "publication reconciliation on `main` is `f4781a91f2120f3eca5088b87bf9034be752274f`",
        "Windows Harness run `25581662790` passed",
        "reports `0.1.13`",
        "Current stage: G - v0.1.14 Published Baseline Reconciliation.",
        "Stage status: G - `v0.1.14` published; baseline reconciliation is in progress on `main`.",
        "publication reconciliation PR #119 merged as `f4781a91f2120f3eca5088b87bf9034be752274f`",
        "AB0 PR #120 merged as `6a78e4aa1d084cb425351f9e514cb40e6d76f7c0`",
        "AB1 PR #121 merged as `1f557faf9ef2460cc456ea6966495b5f175ad809`",
        "AB2 PR #122 merged as `9cdb6f80b0665915dd403101911c14293d60946f`",
        "AB3 PR #123 merged as `13f1a33ca6bcbc2cc8d5863ac0be9e48d0ccb204`",
        "AB4 PR #124 merged as `cd5215e6e6333c7fe00fe47a526ea0d15dcf1bd7`",
        "PR #124 passed Windows Harness run `25584341353`",
        "post-merge `main` Windows Harness run `25584426546` passed",
        "Stage AB0 - Post-v0.1.13 Baseline Cursor",
        "Stage AB1 - Public Metadata And Evidence Freshness Audit",
        "Stage AB2 - Helper And Watcher Preview Diagnostics Evidence",
        "Stage AB3 - MCP And Memory Operator Contract Sweep",
        "Stage AB4 - Compatibility Guardrail Sweep",
        "Stage AB5 - v0.1.14 Release Readiness",
        "next compatible release target is `v0.1.14`",
        "Phase 6 stays at spec/scorecard level",
        "MCP tool list remains unchanged and read-only",
        "Product CLI still does not expose targeted `--hwnd`, `--pid`",
        "Do not implement screenshot capture, OCR, audio recording",
        "Keep real UIA smoke manual and outside default CI",
        "trust = \"untrusted_observed_content\"",
        "Stage AB0 initialization:",
        "gh release view v0.1.13",
        "git rev-parse v0.1.13",
        "gh run view 25581662790",
        "printed `0.1.13`",
        "Stage AB0 local validation:",
        "python -m pytest -q` - passed, 126 tests.",
        "python harness/scripts/run_harness.py` - passed.",
        "Stage AB0 remote validation:",
        "PR #120 Windows Harness run `25582300531` - passed.",
        "PR #120 merged as `6a78e4aa1d084cb425351f9e514cb40e6d76f7c0`.",
        "Post-merge `main` Windows Harness run `25582374884` - passed.",
        "Stage AB1 initialization:",
        "gh repo view YSCJRH/WinChronicle",
        "description, homepage, and topics are empty or not configured",
        "gh release view v0.1.13",
        "Stage AB1 local validation:",
        "passed, 36 tests.",
        "python -m pytest -q` - passed, 127 tests.",
        "python harness/scripts/run_install_cli_smoke.py` - passed.",
        "Stage AB1 remote validation:",
        "PR #121 Windows Harness run `25582831041` - passed.",
        "PR #121 merged as `1f557faf9ef2460cc456ea6966495b5f175ad809`.",
        "Post-merge `main` Windows Harness run `25582935956` - passed.",
        "Stage AB2 initialization:",
        "Reviewed `docs/uia-helper-quality-matrix.md`, `docs/watcher-preview.md`, `docs/operator-diagnostics.md`",
        "deterministic helper/watcher diagnostics coverage is present",
        "Stage AB2 local validation:",
        "passed, 37 tests.",
        "python -m pytest -q` - passed, 128 tests.",
        "Stage AB2 remote validation:",
        "PR #122 Windows Harness run `25583319858` - passed.",
        "PR #122 merged as `9cdb6f80b0665915dd403101911c14293d60946f`.",
        "Post-merge `main` Windows Harness run `25583397242` - passed.",
        "Stage AB3 initialization:",
        "Reviewed `docs/mcp-readonly-examples.md`, `docs/deterministic-demo.md`, `harness/scorecards/mcp-quality.md`",
        "deterministic MCP/memory trust-boundary and exact-tool coverage is present",
        "Stage AB3 local validation:",
        "passed, 38 tests.",
        "python -m pytest -q` - passed, 129 tests.",
        "Stage AB3 remote validation:",
        "PR #123 Windows Harness run `25583769517` - passed.",
        "PR #123 merged as `13f1a33ca6bcbc2cc8d5863ac0be9e48d0ccb204`.",
        "Post-merge `main` Windows Harness run `25583884127` - passed.",
        "Stage AB4 initialization:",
        "passed, 45 tests.",
        "existing disabled-surface contracts, sentinels, documentation, scorecards",
        "local MCP smoke request variable name",
        "Stage AB4 local validation:",
        "passed, 39 tests.",
        "python -m pytest -q` - passed, 130 tests.",
        "Stage AB4 remote validation:",
        "PR #124 Windows Harness run `25584341353` - passed.",
        "PR #124 merged as `cd5215e6e6333c7fe00fe47a526ea0d15dcf1bd7`.",
        "Post-merge `main` Windows Harness run `25584426546` - passed.",
        "Stage AB5 initialization:",
        "git rev-parse HEAD` - passed and printed `cd5215e6e6333c7fe00fe47a526ea0d15dcf1bd7`.",
        "gh release view v0.1.14",
        "confirmed release not found before AB5 readiness",
        "Stage AB5 local validation:",
        "passed, 40 tests.",
        "python -m pytest -q` - passed, 131 tests.",
        "python harness/scripts/run_install_cli_smoke.py` - passed.",
        "python harness/scripts/run_harness.py` - passed.",
        "git diff --check` - passed.",
        "Stage AB5 remote validation:",
        "PR #125 Windows Harness run `25585067457` - passed.",
        "PR #125 merged as `e7e339f4e08828b9954599db76b87201dbcb139b`.",
        "Post-merge `main` Windows Harness run `25585147402` - passed.",
        "v0.1.14 publication validation:",
        "gh release create v0.1.14",
        "gh release view v0.1.14",
        "published at `2026-05-08T23:52:43Z`",
        "git rev-parse v0.1.14",
        "printed `0.1.14`",
        "v0.1.14 publication reconciliation local validation:",
        "passed, 40 tests.",
        "python -m pytest -q` - passed, 131 tests.",
        "python harness/scripts/run_install_cli_smoke.py` - passed.",
        "python harness/scripts/run_harness.py` - passed.",
        "Pending v0.1.14 publication reconciliation PR Windows Harness.",
        "Pending v0.1.14 publication reconciliation post-merge `main` Windows Harness.",
    ):
        assert expected in normalized


def test_post_v014_plan_is_active_without_expanding_scope():
    plan = (ROOT / "docs" / "next-round-plan-post-v0.1.14.md").read_text(
        encoding="utf-8"
    )
    normalized = " ".join(plan.split())

    for expected in (
        "`v0.1.14` is published at https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.14",
        "targets `e7e339f4e08828b9954599db76b87201dbcb139b`",
        "post-publication reconciliation on `main` is `2627e17dd215d3b7233d237ca5f094eacaff2983`",
        "Windows Harness run `25585707220` passed",
        "reports `0.1.14`",
        "Current stage: G - v0.1.15 Published Baseline Reconciliation.",
        "Stage status: G - `v0.1.15` published; baseline reconciliation is in progress on `main`.",
        "publication reconciliation PR #126 merged as `2627e17dd215d3b7233d237ca5f094eacaff2983`",
        "AC4 PR #131 merged as `48994134a3d348745f735e2a6fad56ea82495266`",
        "AC5 PR #132 merged as `7a7f065817b9d7f660248916935fd7b66fadbdd6`",
        "AC5 evidence PR #133 merged as `4869ce7b5b0f6ad3ab41c844e4f010640c0c36c2`",
        "`v0.1.15` was published at https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.15",
        "Stage AC0 - Post-v0.1.14 Baseline Cursor",
        "Stage AC1 - Public Metadata And Evidence Freshness Follow-up",
        "Stage AC2 - Helper And Watcher Preview Diagnostics Review",
        "Stage AC3 - MCP And Memory Contract Review",
        "Stage AC4 - Compatibility Guardrail Sweep",
        "Stage AC5 - v0.1.15 Release Readiness",
        "next compatible release target is `v0.1.15`",
        "Phase 6 stays at spec/scorecard level",
        "MCP tool list remains unchanged and read-only",
        "Product CLI still does not expose targeted `--hwnd`, `--pid`",
        "Do not implement screenshot capture, OCR, audio recording",
        "Keep real UIA smoke manual and outside default CI",
        "trust = \"untrusted_observed_content\"",
        "Stage AC0 initialization:",
        "gh release view v0.1.14",
        "git rev-parse v0.1.14",
        "gh run view 25585707220",
        "printed `0.1.14`",
        "Stage AC0 local validation:",
        "python -m pytest tests/test_version_identity.py tests/test_compatibility_evidence_docs.py tests/test_operator_diagnostics_docs.py -q` - passed, 41 tests.",
        "python -m pytest -q` - passed, 132 tests.",
        "dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - passed.",
        "dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - passed.",
        "python harness/scripts/run_install_cli_smoke.py` - passed.",
        "python harness/scripts/run_harness.py` - passed.",
        "git diff --check` - passed.",
        "Stage AC0 remote validation:",
        "PR #127 Windows Harness run `25586296541` - passed.",
        "PR #127 merged as `42ce9658b0189d37f2e7c80e1b57205ca13cb23e`.",
        "Post-merge `main` Windows Harness run `25586359016` - passed.",
        "Stage AC1 initialization:",
        "gh repo view YSCJRH/WinChronicle",
        "description and homepage are empty",
        "topics are empty or not configured",
        "gh release view v0.1.14",
        "Stage AC1 local validation:",
        "python -m pytest tests/test_version_identity.py tests/test_compatibility_evidence_docs.py tests/test_operator_diagnostics_docs.py -q` - passed, 42 tests.",
        "python -m pytest -q` - passed, 133 tests.",
        "dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - passed.",
        "dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - passed.",
        "python harness/scripts/run_install_cli_smoke.py` - passed.",
        "python harness/scripts/run_harness.py` - passed.",
        "git diff --check` - passed.",
        "Stage AC1 remote validation:",
        "PR #128 Windows Harness run `25586734181` - passed.",
        "PR #128 merged as `157b9e195c5de85588c0df24130bbf99f10c4111`.",
        "Post-merge `main` Windows Harness run `25586802404` - passed.",
        "Stage AC2 initialization:",
        "Reviewed `docs/uia-helper-quality-matrix.md`, `docs/watcher-preview.md`, `docs/operator-diagnostics.md`",
        "deterministic helper/watcher diagnostics coverage is present",
        "Stage AC2 local validation:",
        "python -m pytest tests/test_version_identity.py tests/test_compatibility_evidence_docs.py tests/test_operator_diagnostics_docs.py -q` - passed, 43 tests.",
        "python -m pytest -q` - passed, 134 tests.",
        "dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - passed.",
        "dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - passed.",
        "python harness/scripts/run_install_cli_smoke.py` - passed.",
        "python harness/scripts/run_harness.py` - passed.",
        "git diff --check` - passed.",
        "Stage AC2 remote validation:",
        "PR #129 Windows Harness run `25587197634` - passed.",
        "PR #129 merged as `7d65cbbb4778f5cf253191c2d3da1e21c54b7b58`.",
        "Post-merge `main` Windows Harness run `25587281619` - passed.",
        "Stage AC3 initialization:",
        "Reviewed `docs/mcp-readonly-examples.md`, `harness/scorecards/mcp-quality.md`",
        "deterministic MCP/memory trust-boundary and exact-tool coverage is present",
        "Stage AC3 local validation:",
        "python -m pytest tests/test_version_identity.py tests/test_compatibility_evidence_docs.py tests/test_operator_diagnostics_docs.py -q` - passed, 44 tests.",
        "python -m pytest -q` - passed, 135 tests.",
        "dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - passed.",
        "dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - passed.",
        "python harness/scripts/run_install_cli_smoke.py` - passed.",
        "python harness/scripts/run_harness.py` - passed.",
        "git diff --check` - passed.",
        "Stage AC3 remote validation:",
        "PR #130 Windows Harness run `25587827078` - passed.",
        "PR #130 merged as `79637edd43ac15b425d5a2600a61472c9e27e031`.",
        "Post-merge `main` Windows Harness run `25587885292` - passed.",
        "Stage AC4 initialization:",
        "python -m pytest tests/test_compatibility_contracts.py tests/test_mcp_tools.py tests/test_phase6_privacy_scorecard.py tests/test_watcher_events.py tests/test_state_compatibility.py tests/test_memory_pipeline.py tests/test_version_identity.py -q` - passed, 45 tests.",
        "matches are existing disabled-surface contracts, sentinels",
        "matches are prior compatibility sweep command text, historical plan evidence",
        "Stage AC4 local validation:",
        "python -m pytest tests/test_version_identity.py tests/test_compatibility_evidence_docs.py tests/test_operator_diagnostics_docs.py -q` - passed, 45 tests.",
        "python -m pytest -q` - passed, 136 tests.",
        "Stage AC4 remote validation:",
        "PR #131 Windows Harness run `25588225151` - passed.",
        "PR #131 merged as `48994134a3d348745f735e2a6fad56ea82495266`.",
        "Post-merge `main` Windows Harness run `25588297846` - passed.",
        "Stage AC5 initialization:",
        "gh release view v0.1.15",
        "confirmed release not found before AC5 readiness",
        "Stage AC5 local validation:",
        "python -m pytest tests/test_version_identity.py tests/test_compatibility_evidence_docs.py tests/test_operator_diagnostics_docs.py -q` - passed, 46 tests.",
        "python -m pytest -q` - passed, 137 tests.",
        "printed `0.1.15`",
        "Stage AC5 remote validation:",
        "PR #132 Windows Harness run `25588833988` - passed.",
        "PR #132 merged as `7a7f065817b9d7f660248916935fd7b66fadbdd6`.",
        "Post-merge `main` Windows Harness run `25588898702` - passed.",
        "PR #133 Windows Harness run `25589110606` - passed.",
        "PR #133 merged as `4869ce7b5b0f6ad3ab41c844e4f010640c0c36c2`.",
        "Post-merge `main` Windows Harness run `25589165182` - passed.",
        "Stage AC5 publication validation:",
        "published at `2026-05-09T02:44:06Z`",
        "git rev-parse v0.1.15` - passed and printed `4869ce7b5b0f6ad3ab41c844e4f010640c0c36c2`.",
    ):
        assert expected in normalized


def test_post_v015_plan_is_active_without_expanding_scope():
    plan = (ROOT / "docs" / "next-round-plan-post-v0.1.15.md").read_text(
        encoding="utf-8"
    )
    normalized = " ".join(plan.split())

    for expected in (
        "`v0.1.15` is published at https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.15",
        "targets `4869ce7b5b0f6ad3ab41c844e4f010640c0c36c2`",
        "post-publication reconciliation on `main` is `54208c51819a45140e355272d8cb3f0e3fbff900`",
        "Windows Harness run `25589775129` passed",
        "reports `0.1.15`",
        "Current stage: AD5 - v0.1.16-rc.0 Published Prerelease Reconciliation.",
        "Stage status: AD5 complete; `v0.1.16-rc.0` is published as a prerelease",
        "AD4 added the post-v0.1.15 compatibility guardrail sweep",
        "merged as `2c7d0b0b24d9a159c084f262cb24ec7ee9873a39`",
        "post-merge `main` Windows Harness run `25595513141` passed",
        "Stage AD0 - Post-v0.1.15 Baseline Cursor",
        "Stage AD1 - Public Metadata And Evidence Freshness Follow-up",
        "Stage AD2 - Helper And Watcher Preview Diagnostics Review",
        "Stage AD3 - MCP And Memory Contract Review",
        "Stage AD4 - Compatibility Guardrail Sweep",
        "Stage AD5 - v0.1.16-rc.0 Release Candidate Readiness",
        "next prerelease target is `v0.1.16-rc.0`",
        "Phase 6 stays at spec/scorecard level",
        "MCP tool list remains unchanged and read-only",
        "Product CLI still does not expose targeted `--hwnd`, `--pid`",
        "Do not implement screenshot capture, OCR, audio recording",
        "Keep real UIA smoke manual and outside default CI",
        "trust = \"untrusted_observed_content\"",
        "Stage AD0 initialization:",
        "Stage AD0 completion:",
        "PR #135 Windows Harness run `25593554670`",
        "Stage AD1 initialization:",
        "empty description, homepage, and topics",
        "Stage AD1 completion:",
        "PR #136 Windows Harness run `25593788484`",
        "Stage AD2 initialization:",
        "docs/uia-helper-quality-matrix.md",
        "deterministic helper/watcher diagnostics coverage is present",
        "title-denylist skip reasons could echo matched window titles",
        "denylisted title pattern",
        "Stage AD2 completion:",
        "PR #137 Windows Harness run `25594230290`",
        "Stage AD3 initialization:",
        "docs/mcp-readonly-examples.md",
        "deterministic MCP/memory trust-boundary and exact-tool coverage is present",
        "MCP filtered search could miss valid matches beyond the first 50 raw results",
        "Stage AD3 completion:",
        "PR #138 Windows Harness run `25594817396`",
        "Stage AD4 initialization:",
        "48 tests passed",
        "matches are existing disabled-surface contracts",
        "No new runtime dependency or implementation path",
        "secret redaction guardrail did not cover newer obvious GitHub/Slack token families",
        "product helper/watcher pass-through arguments were not covered",
        "Stage AD4 focused drift-fix validation:",
        "Stage AD4 completion:",
        "PR #139 Windows Harness run `25595449096`",
        "post-AD4 `main` Windows Harness concluded `success`",
        "Stage AD5 initialization:",
        "gh release view v0.1.16",
        "git tag --list \"v0.1.16*\"",
        "prepares `v0.1.16-rc.0` instead",
        "Stage AD5 readiness PR completion:",
        "PR #140 Windows Harness run `25596082939`",
        "post-AD5-readiness `main` Windows Harness concluded `success`",
        "Stage AD5 CI evidence PR completion:",
        "PR #141 Windows Harness run `25596204971`",
        "final pre-publication `main` Windows Harness concluded `success`",
        "Stage AD5 prerelease publication:",
        "gh release view v0.1.16-rc.0",
        "published at `2026-05-09T08:18:01Z`",
        "git ls-remote --tags origin v0.1.16-rc.0",
        "Stage AD5 publication reconciliation:",
        "PR #142 Windows Harness run `25596387380`",
        "post-publication reconciliation `main` Windows Harness concluded `success`",
        "6 tests passed",
        "gh release view v0.1.15",
        "git rev-parse v0.1.15",
        "gh run view 25589775129",
        "gh run view 25593607384",
        "gh run view 25593871698",
        "gh run view 25594302410",
        "gh run view 25594896165",
        "printed `0.1.15`",
    ):
        assert expected in normalized


def test_v0116_final_release_plan_is_active_without_expanding_scope():
    plan = (ROOT / "docs" / "next-round-plan-v0.1.16-final-release.md").read_text(
        encoding="utf-8"
    )
    normalized = " ".join(plan.split())

    for expected in (
        "`v0.1.16-rc.0` is published as a prerelease",
        "https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.16-rc.0",
        "prerelease tag targets `70caf364f68d8c159eb74bbbc23e7469db22a244`",
        "current `main` baseline after prerelease publication reconciliation is `b260ebaa8808bddcce20da166038511de23bf3b5`",
        "Windows Harness run `25596579705` passed on that SHA",
        "diff from `v0.1.16-rc.0` to current `main` is documentation and documentation-test evidence only",
        "No product code, schemas, CLI/MCP JSON shape, helper/watcher behavior, privacy runtime behavior, or capture surfaces changed",
        "This plan was the active final-release cursor after `v0.1.16-rc.0`",
        "completed historical final-release evidence",
        "Direct final release proceeded only after fresh final gates",
        "If future release-readiness work requires any product or contract change, stop the direct final path and prepare a new release-candidate path instead",
        "Current stage: AE4 - v0.1.16 Final Publication Reconciliation.",
        "Stage status: AE4 complete",
        "`v0.1.16` is published as the latest stable release",
        "AE4 publication reconciliation PR #148 merged as",
        "`b36581c25a609f801a48cefda7354781d6dfb888`, PR Windows Harness run",
        "`25598038285` passed, and post-merge `main` Windows Harness run",
        "`25598080136` passed",
        "Last validation: `v0.1.16` release metadata",
        "Next atomic task: start the post-`v0.1.16` maintenance cursor",
        "Stage AE0 - Post-v0.1.16-rc.0 Final Baseline Decision",
        "Stage AE1 - Deterministic Final Gate Refresh",
        "Stage AE2 - Manual Final Smoke Refresh",
        "Stage AE3 - v0.1.16 Final Release Record And Publication",
        "Stage AE4 - v0.1.16 Final Publication Reconciliation",
        "Rerun fresh final manual UIA smoke instead of automatically inheriting",
        "Notepad targeted UIA smoke: hard gate",
        "Edge targeted UIA smoke: hard gate",
        "VS Code metadata smoke: hard gate",
        "VS Code strict Monaco marker: diagnostic and non-blocking",
        "Watcher preview live smoke: preview diagnostic/manual confidence gate",
        "Do not publish or retag `v0.1.16` during AE0",
        "MCP tool list remains unchanged and read-only",
        "Product CLI still does not expose targeted `--hwnd`, `--pid`",
        "Do not implement screenshot capture, OCR, audio recording",
        "Phase 6 remains privacy spec/scorecard only",
        "AE0: docs tests confirmed this final-release plan was the active cursor",
        "AE1: deterministic gates pass on the current final target",
        "AE2: fresh final manual UIA smoke is recorded",
        "AE3: final release record includes local, PR, post-merge",
        "AE4: publication reconciliation confirms `v0.1.16` is the latest published release",
        "Version identity is already aligned to `0.1.16`",
        "Fresh final manual UIA smoke is required by this plan before final publication",
        "Chose a direct-final planning cursor because `v0.1.16-rc.0` is published",
        "Chose fresh manual final smoke for AE2",
        "Completed AE0 through PR #144",
        "Kept the direct final path open after AE1",
        "Completed AE2 with fresh final manual UIA smoke",
        "Prepared `docs/release-v0.1.16.md` for AE3",
        "Stage AE0 initialization:",
        "gh release view v0.1.16-rc.0",
        "marked prerelease, published at `2026-05-09T08:18:01Z`",
        "git rev-parse v0.1.16-rc.0",
        "gh release view v0.1.16",
        "release not found",
        "git tag --list \"v0.1.16*\"",
        "printed only `v0.1.16-rc.0`",
        "git rev-parse HEAD",
        "gh run view 25596579705",
        "git diff --name-status v0.1.16-rc.0..HEAD",
        "the diff listed only documentation and documentation-test evidence files",
        "Stage AE0 completion:",
        "PR #144 Windows Harness run `25596958129`",
        "post-AE0 `main` Windows Harness concluded `success`",
        "Stage AE1 deterministic final gate refresh:",
        "151 tests passed",
        "python harness/scripts/run_install_cli_smoke.py",
        "python harness/scripts/run_harness.py",
        "Stage AE1 completion:",
        "PR #145 Windows Harness run `25597196866`",
        "post-AE1 `main` Windows Harness concluded `success`",
        "Stage AE2 manual final smoke validation:",
        "smoke-uia-notepad.ps1",
        "smoke-uia-edge.ps1",
        "smoke-uia-vscode.ps1",
        "passed with diagnostic warning",
        "diagnostic failure, non-blocking",
        "captures_written: 3",
        "heartbeats: 6",
        "Local artifacts were not committed",
        "Stage AE2 completion:",
        "PR #146 Windows Harness run `25597418104`",
        "post-AE2 `main` Windows Harness concluded `success`",
        "Stage AE3 final release record preparation:",
        "Added `docs/release-v0.1.16.md`",
        "Publication was pending until this AE3 PR",
        "Stage AE3 completion:",
        "PR #147 Windows Harness run `25597623991`",
        "post-AE3 `main` Windows Harness concluded `success`",
        "Stage AE3 final publication:",
        "gh release create v0.1.16",
        "published at `2026-05-09T09:31:17Z`",
        "git ls-remote --tags origin v0.1.16",
        "Stage AE4 publication reconciliation:",
        "PR #148 Windows Harness run `25598038285`",
        "post-AE4 `main` Windows Harness concluded `success`",
    ):
        assert expected in normalized


def test_public_metadata_audit_post_v015_records_manual_gaps_without_scope_expansion():
    audit = (ROOT / "docs" / "public-metadata-audit-post-v0.1.15.md").read_text(
        encoding="utf-8"
    )

    for expected in (
        "Public Metadata Audit After v0.1.15",
        "does not change product behavior, schemas,\nCLI/MCP JSON shape",
        "gh repo view YSCJRH/WinChronicle",
        "Visibility | `PUBLIC`",
        "Default branch | `main`",
        "Description | Empty",
        "Homepage URL | Empty",
        "Repository topics | Empty / not configured",
        "gh release view v0.1.15",
        "Release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.15",
        "Target | `4869ce7b5b0f6ad3ab41c844e4f010640c0c36c2`",
        "Draft | `false`",
        "Prerelease | `false`",
        "Published at | `2026-05-09T02:44:06Z`",
        "Run | `25593607384`",
        "Head SHA | `90fff5cc25b770634c92669e70c4067b58a8a6ea`",
        "README.md` starts with \"UIA-first local memory for Windows agents.\"",
        "docs/operator-quickstart.md` links release checklist",
        "active post-v0.1.15 plan",
        "docs/release-checklist.md`, `docs/release-evidence.md`",
        "GitHub repository description",
        "GitHub homepage URL",
        "GitHub topics",
        "Social preview image",
        "manual maintainer checklist item",
        "no required product-code change",
        "The next smallest implementation task is AD2",
    ):
        assert expected in audit

    assert "This audit does not authorize screenshots" in audit


def test_public_metadata_audit_post_v017_records_manual_gaps_without_scope_expansion():
    audit = (ROOT / "docs" / "public-metadata-audit-post-v0.1.17.md").read_text(
        encoding="utf-8"
    )

    for expected in (
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
        assert expected in audit

    assert "This audit does not authorize screenshots" in audit


def test_public_metadata_audit_post_v018_records_manual_gaps_without_scope_expansion():
    audit = (ROOT / "docs" / "public-metadata-audit-post-v0.1.18.md").read_text(
        encoding="utf-8"
    )

    for expected in (
        "Public Metadata Audit After v0.1.18",
        "does not change product behavior, schemas,\nCLI/MCP JSON shape",
        "gh repo view YSCJRH/WinChronicle",
        "Visibility | `PUBLIC`",
        "Default branch | `main`",
        "Archived | `false`",
        "Fork | `false`",
        "Private | `false`",
        "Description | Empty",
        "Homepage URL | Empty",
        "Repository topics | Empty / not configured",
        "Latest release | `v0.1.18`",
        "Custom OpenGraph image | `false`",
        "gh release view v0.1.18",
        "Release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.18",
        "Target | `2e22ec9805edb0efd48e5ef4aacbcff13f0490ec`",
        "Draft | `false`",
        "Prerelease | `false`",
        "Published at | `2026-05-09T21:38:33Z`",
        "gh release view v0.1.17",
        "Release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.17",
        "Target | `5b260edc3bddc48986e52179b2ffd261856a89ac`",
        "Run | `25613244560`",
        "Head SHA | `f4d24adf5bb60cd5ad6abfc21ada04fbbeae288c`",
        "README.md` starts with \"UIA-first local memory for Windows agents.\"",
        "docs/operator-quickstart.md` links release checklist",
        "active post-v0.1.18 plan",
        "current post-v0.1.18 audit",
        "published `v0.1.18` maintenance release",
        "previous stable `v0.1.17` maintenance release",
        "AH0 remote validation",
        "GitHub repository description",
        "GitHub homepage URL",
        "GitHub topics",
        "Social preview image",
        "manual maintainer checklist item",
        "`v0.1.18` manual UIA smoke remains fresh for the published `v0.1.18`\n  maintenance release record only",
        "no required product-code change",
        "The next smallest implementation task is AH2",
    ):
        assert expected in audit

    assert "This audit does not authorize screenshots" in audit


def test_public_metadata_audit_post_v016_records_manual_gaps_without_scope_expansion():
    audit = (ROOT / "docs" / "public-metadata-audit-post-v0.1.16.md").read_text(
        encoding="utf-8"
    )

    for expected in (
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
        "published `v0.1.16` final release",
        "historical `v0.1.16-rc.0` prerelease evidence",
        "GitHub repository description",
        "GitHub homepage URL",
        "GitHub topics",
        "Social preview image",
        "manual maintainer checklist item",
        "AE2 manual UIA smoke remains fresh for the published `v0.1.16` final release",
        "no required product-code change",
        "The next smallest implementation task is AF2",
    ):
        assert expected in audit

    assert "This audit does not authorize screenshots" in audit


def test_helper_watcher_diagnostics_sweep_post_v015_records_drift_fix():
    sweep = (
        ROOT / "docs" / "helper-watcher-diagnostics-sweep-post-v0.1.15.md"
    ).read_text(encoding="utf-8")

    for expected in (
        "Helper And Watcher Diagnostics Sweep After v0.1.15",
        "one compatible privacy diagnostic drift fix",
        "does not change\nschemas, CLI/MCP JSON shape",
        "Helper quality matrix",
        "Watcher preview docs",
        "Operator diagnostics",
        "Capture quality scorecard",
        "Deterministic tests",
        "Helper timeout",
        "Helper invalid JSON",
        "Helper empty stdout",
        "Helper nonzero exit",
        "Watcher nonzero exit",
        "Helper failure surfaced by watcher",
        "Malformed watcher JSONL",
        "Watcher timeout",
        "Heartbeat-only run",
        "Duplicate skip",
        "Denylist or lock-screen skip",
        "Raw watcher JSONL persistence",
        "AD2 found and fixed a narrow privacy diagnostic drift",
        "denylisted title pattern",
        "Fresh manual UIA smoke remains outside default\nCI",
        "does not change successful capture behavior",
        "The next smallest implementation task is AD3",
    ):
        assert expected in sweep

    for boundary in (
        "screenshot capture",
        "OCR",
        "audio recording",
        "keyboard capture",
        "clipboard capture",
        "network upload",
        "LLM calls",
        "desktop\ncontrol",
        "MCP write tools",
        "product targeted capture",
        "live UIA smoke in\ndefault CI",
    ):
        assert boundary in sweep


def test_helper_watcher_diagnostics_sweep_post_v017_records_current_review():
    sweep = (
        ROOT / "docs" / "helper-watcher-diagnostics-sweep-post-v0.1.17.md"
    ).read_text(encoding="utf-8")
    normalized = " ".join(sweep.split())

    for expected in (
        "Helper And Watcher Diagnostics Sweep After v0.1.17",
        "published `v0.1.17` maintenance release",
        "records then-current deterministic evidence",
        "This sweep is now historical",
        "active helper/watcher diagnostics review is the post-v0.1.18 AH2 sweep",
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
    ):
        assert expected in normalized

    for boundary in (
        "screenshot capture",
        "OCR",
        "audio recording",
        "keyboard capture",
        "clipboard capture",
        "network upload",
        "LLM calls",
        "desktop control",
        "MCP write tools",
        "arbitrary file read tools",
        "product targeted capture",
        "live UIA smoke in default CI",
    ):
        assert boundary in normalized


def test_helper_watcher_diagnostics_sweep_post_v018_records_current_review():
    sweep = (
        ROOT / "docs" / "helper-watcher-diagnostics-sweep-post-v0.1.18.md"
    ).read_text(encoding="utf-8")
    normalized = " ".join(sweep.split())

    for expected in (
        "Helper And Watcher Diagnostics Sweep After v0.1.18",
        "published `v0.1.18` maintenance release",
        "AH1 public metadata audit",
        "does not change schemas, successful CLI/MCP JSON shape",
        "Helper quality matrix",
        "Watcher preview docs",
        "Operator diagnostics",
        "Capture quality scorecard",
        "Deterministic tests",
        "tests/test_uia_helper_quality_matrix.py",
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
        "AH2 found no new helper/watcher diagnostics drift",
        "current `v0.1.18` manual-smoke matrix rows",
        "no observed-content echo",
        "raw watcher JSONL non-persistence",
        "product targeted-capture pass-through rejection",
        "No schema, successful CLI/MCP JSON, helper/watcher capture behavior",
        "Fresh manual UIA smoke remains outside default CI",
        "The `v0.1.18` release-readiness record reran fresh hard-gate manual UIA smoke",
        "The next smallest implementation task is to land this AH2 review",
        "Validation Log",
        "passed, 108 tests",
        "passed, 207 tests",
        "Current-entry stale AH1/current post-v0.1.17 helper/watcher wording scan",
        "printed no files, confirming AH2 is docs/tests only",
        "python harness/scripts/run_harness.py",
    ):
        assert expected in normalized

    for boundary in (
        "screenshot capture",
        "OCR",
        "audio recording",
        "keyboard capture",
        "clipboard capture",
        "network upload",
        "LLM calls",
        "desktop control",
        "MCP write tools",
        "arbitrary file read tools",
        "product targeted capture",
        "live UIA smoke in default CI",
    ):
        assert boundary in normalized


def test_helper_watcher_diagnostics_sweep_post_v016_records_historical_review():
    sweep = (
        ROOT / "docs" / "helper-watcher-diagnostics-sweep-post-v0.1.16.md"
    ).read_text(encoding="utf-8")
    normalized = " ".join(sweep.split())

    for expected in (
        "Helper And Watcher Diagnostics Sweep After v0.1.16",
        "added a narrow content-free CLI diagnostic fix",
        "records then-current deterministic evidence",
        "This sweep is now historical",
        "AG2 sweep superseded it",
        "active helper/watcher diagnostics review is the post-v0.1.18 AH2 sweep",
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
        "Harness smoke may use a temporary fake-helper event file",
        "Fresh manual UIA smoke remains outside default CI",
        "The next smallest implementation task is to land this AF2 review",
    ):
        assert expected in normalized

    for boundary in (
        "screenshot capture",
        "OCR",
        "audio recording",
        "keyboard capture",
        "clipboard capture",
        "network upload",
        "LLM calls",
        "desktop control",
        "MCP write tools",
        "arbitrary file read tools",
        "product targeted capture",
        "live UIA smoke in default CI",
    ):
        assert boundary in normalized


def test_mcp_memory_contract_sweep_post_v015_records_drift_fixes():
    sweep = (ROOT / "docs" / "mcp-memory-contract-sweep-post-v0.1.15.md").read_text(
        encoding="utf-8"
    )

    for expected in (
        "MCP And Memory Contract Sweep After v0.1.15",
        "documentation-only MCP example drift fix",
        "compatible read-only MCP\nfiltered-search parity fix",
        "does not change schemas",
        "MCP tool schemas",
        "MCP examples",
        "MCP scorecard",
        "Memory scorecard",
        "Deterministic demo",
        "Operator quickstart",
        "Deterministic tests",
        "current_context",
        "search_captures",
        "search_memory",
        "read_recent_capture",
        "recent_activity",
        "privacy_status",
        "trust = \"untrusted_observed_content\"",
        "MCP `search_memory` parity",
        "MCP `search_captures` parity",
        "Memory FTS",
        "Idempotent memory generation",
        "Secret exclusion",
        "Fixture-only demo",
        "AD3 found no required schema, tool-list, tool-schema",
        "`privacy_status` example omitted the existing `home`, `db_exists`, and\n  `capture_count` fields",
        "MCP `search_captures` and `search_memory` applied filters after a raw\n  50-result fetch",
        "No fresh manual UIA smoke is required for this AD3 sweep",
        "The next smallest implementation task is AD4",
    ):
        assert expected in sweep

    for boundary in (
        "MCP write tools",
        "arbitrary file reads",
        "screenshot\ncapture",
        "OCR",
        "audio recording",
        "keyboard capture",
        "clipboard capture",
        "network\nupload",
        "LLM calls",
        "desktop control",
        "product targeted capture",
        "live UIA smoke\nin default CI",
    ):
        assert boundary in sweep


def test_mcp_memory_contract_sweep_post_v016_records_trust_boundary_review():
    sweep = (ROOT / "docs" / "mcp-memory-contract-sweep-post-v0.1.16.md").read_text(
        encoding="utf-8"
    )
    normalized = " ".join(sweep.split())

    for expected in (
        "MCP And Memory Contract Sweep After v0.1.16",
        "published `v0.1.16` final release",
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
        "current_context",
        "search_captures",
        "search_memory",
        "read_recent_capture",
        "recent_activity",
        "privacy_status",
        "trust = \"untrusted_observed_content\"",
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
        "AF3 found no required schema, MCP tool-list, MCP tool-schema",
        "`generate-memory` manifest JSON included observed-derived titles",
        "`trust`, `untrusted_observed_content`, and `instruction`",
        "The standalone MCP smoke compared `tools/list` against implementation constants",
        "`desktop_control`, `control_desktop`, `press_key`, `capture_hwnd`",
        "No fresh manual UIA smoke is required to land this AF3 review",
        "future release-readiness record should make a fresh manual-smoke freshness decision",
        "The next smallest implementation task is to land this AF3 review",
    ):
        assert expected in normalized

    for boundary in (
        "MCP write tools",
        "arbitrary file reads",
        "screenshot capture",
        "OCR",
        "audio recording",
        "keyboard capture",
        "clipboard capture",
        "network upload",
        "LLM calls",
        "desktop control",
        "product targeted capture",
        "live UIA smoke in default CI",
    ):
        assert boundary in normalized


def test_mcp_memory_contract_sweep_post_v017_records_current_review():
    sweep = (ROOT / "docs" / "mcp-memory-contract-sweep-post-v0.1.17.md").read_text(
        encoding="utf-8"
    )
    normalized = " ".join(sweep.split())

    for expected in (
        "MCP And Memory Contract Sweep After v0.1.17",
        "published `v0.1.17` maintenance release",
        "AG2 helper/watcher diagnostics review",
        "found no new drift requiring product code",
        "does not change helper behavior, watcher product behavior",
        "MCP examples",
        "MCP scorecard",
        "Memory scorecard",
        "Deterministic demo",
        "Operator quickstart",
        "Deterministic tests",
        "current_context",
        "search_captures",
        "search_memory",
        "read_recent_capture",
        "recent_activity",
        "privacy_status",
        "trust = \"untrusted_observed_content\"",
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
        "AG3 found no required schema, MCP tool-list, MCP tool-schema",
        "`generate-memory` manifest JSON includes `trust`",
        "The standalone MCP smoke uses a literal expected tool list",
        "`desktop_control`, `control_desktop`, `press_key`",
        "No fresh manual UIA smoke is required to land this AG3 review",
        "future release-readiness record should make a fresh manual-smoke freshness decision",
        "The next smallest implementation task is to land this AG3 review",
        "Validation Log",
        "Found no new MCP/memory contract drift",
        "passed, 93 tests",
        "passed, 175 tests",
        "stale AG2 cursor scan",
        "python harness/scripts/run_harness.py",
    ):
        assert expected in normalized

    for boundary in (
        "MCP write tools",
        "arbitrary file reads",
        "screenshot capture",
        "OCR",
        "audio recording",
        "keyboard capture",
        "clipboard capture",
        "network upload",
        "LLM calls",
        "desktop control",
        "product targeted capture",
        "live UIA smoke in default CI",
    ):
        assert boundary in normalized


def test_mcp_memory_contract_sweep_post_v018_records_current_review():
    sweep = (ROOT / "docs" / "mcp-memory-contract-sweep-post-v0.1.18.md").read_text(
        encoding="utf-8"
    )
    normalized = " ".join(sweep.split())

    for expected in (
        "MCP And Memory Contract Sweep After v0.1.18",
        "published `v0.1.18` maintenance release",
        "AH2 helper/watcher diagnostics review",
        "found no new drift requiring product code",
        "does not change helper behavior, watcher product behavior",
        "MCP examples",
        "MCP scorecard",
        "Memory scorecard",
        "Deterministic demo",
        "Operator quickstart",
        "Deterministic tests",
        "current_context",
        "search_captures",
        "search_memory",
        "read_recent_capture",
        "recent_activity",
        "privacy_status",
        "trust = \"untrusted_observed_content\"",
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
        "AH3 found no required schema, MCP tool-list, MCP tool-schema",
        "`generate-memory` manifest JSON includes `trust`",
        "The standalone MCP smoke uses a literal expected tool list",
        "`desktop_control`, `control_desktop`, `press_key`",
        "No fresh manual UIA smoke is required to land this AH3 review",
        "future release-readiness record should make a fresh manual-smoke freshness decision",
        "The next smallest implementation task is to land this AH3 review",
        "Validation Log",
        "Found no new MCP/memory contract drift",
        "passed, 108 tests",
        "passed, 209 tests",
        "current-entry stale AH2/current post-v0.1.17 MCP/memory wording scan",
        "python harness/scripts/run_harness.py",
    ):
        assert expected in normalized

    for boundary in (
        "MCP write tools",
        "arbitrary file reads",
        "screenshot capture",
        "OCR",
        "audio recording",
        "keyboard capture",
        "clipboard capture",
        "network upload",
        "LLM calls",
        "desktop control",
        "product targeted capture",
        "live UIA smoke in default CI",
    ):
        assert boundary in normalized


def test_public_metadata_audit_post_v014_records_manual_gaps_without_scope_expansion():
    audit = (ROOT / "docs" / "public-metadata-audit-post-v0.1.14.md").read_text(
        encoding="utf-8"
    )

    for expected in (
        "Public Metadata Audit After v0.1.14",
        "does not change product behavior, schemas,\nCLI/MCP JSON shape",
        "gh repo view YSCJRH/WinChronicle",
        "Visibility | `PUBLIC`",
        "Default branch | `main`",
        "Description | Empty",
        "Homepage URL | Empty",
        "Repository topics | Empty / not configured",
        "gh release view v0.1.14",
        "Release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.14",
        "Target | `e7e339f4e08828b9954599db76b87201dbcb139b`",
        "Draft | `false`",
        "Prerelease | `false`",
        "Published at | `2026-05-08T23:52:43Z`",
        "README.md` starts with \"UIA-first local memory for Windows agents.\"",
        "docs/operator-quickstart.md` links release checklist",
        "active post-v0.1.14 plan",
        "docs/release-checklist.md`, `docs/release-evidence.md`",
        "GitHub repository description",
        "GitHub homepage URL",
        "GitHub topics",
        "Social preview image",
        "manual maintainer checklist item",
        "no required product-code change",
    ):
        assert expected in audit

    assert "This audit does not authorize screenshots" in audit


def test_helper_watcher_diagnostics_sweep_post_v014_records_no_drift():
    sweep = (
        ROOT / "docs" / "helper-watcher-diagnostics-sweep-post-v0.1.14.md"
    ).read_text(encoding="utf-8")

    for expected in (
        "Helper And Watcher Diagnostics Sweep After v0.1.14",
        "does not change product behavior, schemas, CLI/MCP JSON\nshape",
        "Helper quality matrix",
        "Watcher preview docs",
        "Operator diagnostics",
        "Capture quality scorecard",
        "Deterministic tests",
        "Helper timeout",
        "Helper invalid JSON",
        "Helper empty stdout",
        "Helper nonzero exit",
        "Watcher nonzero exit",
        "Helper failure surfaced by watcher",
        "Malformed watcher JSONL",
        "Watcher timeout",
        "Heartbeat-only run",
        "Duplicate skip",
        "Denylist or lock-screen skip",
        "Raw watcher JSONL persistence",
        "AC2 found no required helper or watcher product-code change",
        "No fresh manual UIA smoke is required for this AC2 sweep",
        "The next smallest implementation task is AC3",
    ):
        assert expected in sweep

    for boundary in (
        "screenshot capture",
        "OCR",
        "audio recording",
        "keyboard capture",
        "clipboard capture",
        "network upload",
        "LLM calls",
        "desktop\ncontrol",
        "MCP write tools",
        "product targeted capture",
        "live UIA smoke in\ndefault CI",
    ):
        assert boundary in sweep


def test_public_metadata_audit_records_manual_gaps_without_scope_expansion():
    audit = (ROOT / "docs" / "public-metadata-audit-post-v0.1.13.md").read_text(
        encoding="utf-8"
    )

    for expected in (
        "Public Metadata Audit After v0.1.13",
        "does not change product behavior, schemas,\nCLI/MCP JSON shape",
        "gh repo view YSCJRH/WinChronicle",
        "Visibility | `PUBLIC`",
        "Default branch | `main`",
        "Description | Empty",
        "Homepage URL | Empty",
        "Repository topics | Empty / not configured",
        "gh release view v0.1.13",
        "Release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.13",
        "Target | `1070343d9bcfd60c48238835e26b6c32f9060ae7`",
        "Draft | `false`",
        "Prerelease | `false`",
        "Published at | `2026-05-08T21:42:32Z`",
        "README.md` starts with \"UIA-first local memory for Windows agents.\"",
        "docs/operator-quickstart.md` links release checklist",
        "docs/roadmap.md` maps fixture/privacy, helper, watcher, MCP, memory",
        ".github/ISSUE_TEMPLATE/harness_first_task.yml",
        "docs/release-checklist.md`, `docs/release-evidence.md`",
        "GitHub repository description",
        "GitHub homepage URL",
        "GitHub topics",
        "Social preview image",
        "manual maintainer checklist item",
        "no required product-code change",
    ):
        assert expected in audit

    for forbidden in (
        "authorize screenshots",
        "OCR",
        "network upload",
        "LLM calls",
        "desktop control",
        "product targeted capture",
        "daemon/service install",
        "default background capture",
    ):
        assert forbidden in audit


def test_helper_watcher_diagnostics_sweep_records_no_drift_decision():
    sweep = (
        ROOT / "docs" / "helper-watcher-diagnostics-sweep-post-v0.1.13.md"
    ).read_text(encoding="utf-8")

    for expected in (
        "Helper And Watcher Diagnostics Sweep After v0.1.13",
        "does not change product behavior, schemas, CLI/MCP JSON\nshape",
        "docs/uia-helper-quality-matrix.md",
        "docs/watcher-preview.md",
        "docs/operator-diagnostics.md",
        "harness/scorecards/capture-quality.md",
        "tests/test_cli.py",
        "tests/test_uia_helper_contract.py",
        "tests/test_watcher_events.py",
        "tests/test_operator_diagnostics_docs.py",
        "Helper timeout",
        "Helper invalid JSON",
        "Helper empty stdout",
        "Helper nonzero exit",
        "Watcher nonzero exit",
        "Helper failure surfaced by watcher",
        "Malformed watcher JSONL",
        "Watcher timeout",
        "Heartbeat-only run",
        "Duplicate skip",
        "Denylist or lock-screen skip",
        "Raw watcher JSONL persistence",
        "AB2 found no required helper or watcher product-code change",
        "no required helper or watcher product-code change",
        "No fresh manual UIA smoke is required",
        "does not change helper behavior, watcher product\nbehavior",
        "AB3: re-check read-only MCP examples",
    ):
        assert expected in sweep

    for boundary in (
        "does not authorize screenshot capture",
        "OCR",
        "audio recording",
        "keyboard capture",
        "clipboard capture",
        "network upload",
        "LLM calls",
        "desktop\ncontrol",
        "MCP write tools",
        "product targeted capture",
        "daemon/service install",
        "polling capture loops",
        "default background capture",
        "live UIA smoke in\ndefault CI",
    ):
        assert boundary in sweep


def test_mcp_memory_contract_sweep_records_no_drift_decision():
    sweep = (ROOT / "docs" / "mcp-memory-contract-sweep-post-v0.1.13.md").read_text(
        encoding="utf-8"
    )

    for expected in (
        "MCP And Memory Contract Sweep After v0.1.13",
        "does not change product behavior, schemas, CLI/MCP JSON\nshape",
        "MCP tool schemas",
        "docs/mcp-readonly-examples.md",
        "docs/deterministic-demo.md",
        "harness/scorecards/mcp-quality.md",
        "harness/scorecards/memory-quality.md",
        "tests/test_mcp_tools.py",
        "tests/test_memory_pipeline.py",
        "tests/test_compatibility_contracts.py",
        "tests/test_state_compatibility.py",
        "current_context",
        "search_captures",
        "search_memory",
        "read_recent_capture",
        "recent_activity",
        "privacy_status",
        "trust = \"untrusted_observed_content\"",
        "Exact MCP tool list",
        "Read-only MCP boundary",
        "Observed-content trust boundary",
        "MCP `search_memory` parity",
        "Durable memory Markdown",
        "Memory FTS",
        "Idempotent memory generation",
        "Secret exclusion",
        "Fixture-only demo",
        "AB3 found no required MCP or memory product-code change",
        "exact read-only MCP\ntools",
        "CLI/MCP memory-search parity",
        "durable memory\ngoldens",
        "No fresh manual UIA smoke is required",
        "AB4: re-run compatibility guardrails",
    ):
        assert expected in sweep

    for boundary in (
        "does not authorize MCP write tools",
        "arbitrary file reads",
        "screenshot\ncapture",
        "OCR",
        "audio recording",
        "keyboard capture",
        "clipboard capture",
        "network\nupload",
        "LLM calls",
        "desktop control",
        "product targeted capture",
        "daemon/service\ninstall",
        "polling capture loops",
        "default background capture",
        "live UIA smoke\nin default CI",
    ):
        assert boundary in sweep


def test_post_v014_mcp_memory_contract_sweep_records_no_drift_decision():
    sweep = (ROOT / "docs" / "mcp-memory-contract-sweep-post-v0.1.14.md").read_text(
        encoding="utf-8"
    )

    for expected in (
        "MCP And Memory Contract Sweep After v0.1.14",
        "does not change product behavior, schemas, CLI/MCP JSON\nshape",
        "MCP tool schemas",
        "MCP examples",
        "MCP scorecard",
        "Memory scorecard",
        "Deterministic demo",
        "Operator quickstart",
        "Deterministic tests",
        "docs/mcp-readonly-examples.md",
        "harness/scorecards/mcp-quality.md",
        "harness/scorecards/memory-quality.md",
        "docs/deterministic-demo.md",
        "tests/test_mcp_tools.py",
        "tests/test_memory_pipeline.py",
        "tests/test_compatibility_contracts.py",
        "tests/test_state_compatibility.py",
        "current_context",
        "search_captures",
        "search_memory",
        "read_recent_capture",
        "recent_activity",
        "privacy_status",
        "trust = \"untrusted_observed_content\"",
        "Exact MCP tool list",
        "Read-only MCP boundary",
        "Observed-content trust boundary",
        "MCP `search_memory` parity",
        "Durable memory Markdown",
        "Memory FTS",
        "Idempotent memory generation",
        "Secret exclusion",
        "Fixture-only demo",
        "AC3 found no required MCP or memory product-code change",
        "exact read-only MCP\ntools",
        "CLI/MCP memory-search parity",
        "durable memory\ngoldens",
        "No fresh manual UIA smoke is required",
        "The next smallest implementation task is AC4",
    ):
        assert expected in sweep

    for boundary in (
        "does not authorize MCP write tools",
        "arbitrary file reads",
        "screenshot\ncapture",
        "OCR",
        "audio recording",
        "keyboard capture",
        "clipboard capture",
        "network\nupload",
        "LLM calls",
        "desktop control",
        "product targeted capture",
        "daemon/service\ninstall",
        "polling capture loops",
        "default background capture",
        "live UIA smoke\nin default CI",
    ):
        assert boundary in sweep


def test_blueprint_gap_audit_records_evidence_and_no_scope_expansion():
    audit = (ROOT / "docs" / "blueprint-gap-audit-post-v0.1.12.md").read_text(
        encoding="utf-8"
    )

    for expected in (
        "This audit compares the published `v0.1.12` baseline with `WinChronicle.md`.",
        "It records evidence and follow-up candidates only.",
        "new\ncapture surfaces",
        "North star and README positioning",
        "CLI command surface",
        "Fixture capture and SQLite search",
        "UIA helper preview",
        "Watcher preview",
        "Read-only MCP",
        "Durable memory",
        "Phase 6 boundary",
        "Deterministic public demo",
        "Roadmap",
        "Issue templates",
        "Contribution entry",
        "Manual smoke freshness",
        "GitHub metadata/social surface",
        "The absence of screenshot/OCR implementation is intentional",
        "The absence of product targeted capture flags is intentional",
        "AA1 finds no required product-code change",
        "AA2: consolidate deterministic demo/operator\ninstructions",
    ):
        assert expected in audit


def test_deterministic_demo_is_fixture_only_and_covers_operator_route():
    demo = (ROOT / "docs" / "deterministic-demo.md").read_text(encoding="utf-8")

    for expected in (
        "without reading the live desktop",
        "synthetic fixtures",
        "temporary local state",
        "python -m winchronicle status",
        "screenshot, OCR, audio, keyboard, clipboard",
        "product targeted capture",
        "python -m winchronicle capture-once --fixture harness/fixtures/uia/terminal_error.json",
        "python -m winchronicle capture-once --fixture harness/fixtures/uia/vscode_editor.json",
        "python -m winchronicle capture-once --fixture harness/fixtures/uia/edge_browser.json",
        "python -m winchronicle search-captures \"AssertionError\"",
        "python -m winchronicle search-captures \"test_capture_redacts_passwords\"",
        "python -m winchronicle search-captures \"OpenChronicle\"",
        "trust = \"untrusted_observed_content\"",
        "python -m winchronicle generate-memory --date 2026-04-25",
        "python -m winchronicle search-memory \"AssertionError\"",
        "python -m winchronicle search-memory \"OpenChronicle\"",
        "python -m winchronicle watch --events harness/fixtures/watcher/notepad_burst.jsonl",
        "python -m winchronicle search-captures \"Watcher burst\"",
        "python harness/scripts/run_mcp_smoke.py",
        "python harness/scripts/run_install_cli_smoke.py",
        "python harness/scripts/run_harness.py",
        "Real UIA Notepad, Edge, VS\nCode, and watcher preview smoke stay manual",
        "Do not commit those files, raw helper JSON, raw watcher\nJSONL",
        "observed-content diagnostics",
    ):
        assert expected in demo

    forbidden_phrases = (
        "git add",
        "git commit",
        "commit observed",
        "save observed",
        "run capture-frontmost",
    )
    for forbidden in forbidden_phrases:
        assert forbidden not in demo


def test_roadmap_contribution_and_issue_templates_keep_harness_first_scope():
    roadmap = (ROOT / "docs" / "roadmap.md").read_text(encoding="utf-8")
    contributing = (ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
    harness_issue = (
        ROOT / ".github" / "ISSUE_TEMPLATE" / "harness_first_task.yml"
    ).read_text(encoding="utf-8")
    privacy_issue = (
        ROOT / ".github" / "ISSUE_TEMPLATE" / "privacy_boundary_review.yml"
    ).read_text(encoding="utf-8")
    issue_config = (ROOT / ".github" / "ISSUE_TEMPLATE" / "config.yml").read_text(
        encoding="utf-8"
    )
    pr_template = (ROOT / ".github" / "pull_request_template.md").read_text(
        encoding="utf-8"
    )

    for expected in (
        "does not authorize new capture surfaces",
        "The current stable baseline is the `v0.2` monitor-session baseline",
        "fixture/privacy maintenance loop that\nfollowed `v0.1.18` is closed for now",
        "Do not turn\nthose records into another autonomous maintenance loop.",
        "needs explicit human product approval",
        "These are options for human review, not an automatically authorized backlog.",
        "Fixture and privacy baseline",
        "UIA helper hardening",
        "Monitor sessions",
        "Watcher preview",
        "Read-only MCP",
        "Durable memory",
        "Screenshot/OCR enrichment",
        "Product targeted capture flags",
        "Daemon/service install, default background capture, polling loops",
        "MCP write tools, arbitrary file reads, desktop control",
        "LLM reducer/classifier calls, network upload",
        "Any screenshot or OCR implementation",
        "Do not commit generated state, captures, memory artifacts",
    ):
        assert expected in roadmap

    for expected in (
        "Start by reading\n`AGENTS.md`, `docs/operator-quickstart.md`, `docs/deterministic-demo.md`, and\n`docs/roadmap.md`",
        "Harness-first Workflow",
        "python harness/scripts/run_install_cli_smoke.py",
        "python harness/scripts/run_harness.py",
        "Do not add screenshot capture, OCR, audio recording, keyboard capture, clipboard",
        "Do not commit local state, raw helper JSON, raw watcher JSONL",
        "trust = \"untrusted_observed_content\"",
        "open a privacy boundary review issue before implementation",
    ):
        assert expected in contributing

    for expected in (
        "Roadmap lane",
        "Fixture and privacy baseline",
        "UIA helper hardening",
        "Watcher preview",
        "Read-only MCP",
        "Durable memory",
        "Docs and deterministic demo",
        "Phase 6 privacy spec only",
        "Do not attach or paste observed-content artifacts",
        "This does not add screenshot capture, OCR, audio recording, keyboard capture, clipboard capture",
        "This does not require committing local state, raw helper JSON, raw watcher JSONL",
    ):
        assert expected in harness_issue

    for expected in (
        "Privacy boundary review",
        "capture\n        surfaces, privacy behavior, schema shape, CLI/MCP JSON shape",
        "Tests-first plan",
        "This review does not authorize screenshot capture, OCR, audio recording",
        "This review will not include committed observed-content artifacts",
    ):
        assert expected in privacy_issue

    assert "blank_issues_enabled: false" in issue_config
    assert "Operator quickstart" in issue_config
    assert "Roadmap" in issue_config

    for expected in (
        "## Summary",
        "## Validation",
        "## Privacy and scope",
        "Product CLI/MCP shape unchanged unless explicitly called out",
        "No observed-content artifact",
    ):
        assert expected in pr_template


def test_compatibility_guardrail_sweep_records_no_drift_decision():
    sweep = (
        ROOT / "docs" / "compatibility-guardrail-sweep-post-v0.1.12.md"
    ).read_text(encoding="utf-8")

    for expected in (
        "does not change product behavior, schemas, CLI/MCP JSON shape",
        "Version identity",
        "Exact read-only MCP tool list",
        "Disabled privacy surfaces",
        "Observed-content trust boundary",
        "Watcher preview limits",
        "Durable memory contract",
        "Phase 6 spec-only status",
        "Product targeted capture absence",
        "No write/control/file/screenshot/OCR/audio/keyboard/clipboard/network tools found",
        "No screenshot/OCR implementation found",
        "Product targeted capture remains absent",
        "45 passed",
        "matches are existing disabled-surface contracts, sentinels",
        "No new product CLI/MCP targeted capture",
        "No new runtime\ndependency or implementation path was found",
        "No compatibility drift was found",
    ):
        assert expected in sweep


def test_post_v013_compatibility_guardrail_sweep_records_no_drift_decision():
    sweep = (
        ROOT / "docs" / "compatibility-guardrail-sweep-post-v0.1.13.md"
    ).read_text(encoding="utf-8")

    for expected in (
        "Compatibility Guardrail Sweep After v0.1.13",
        "does not change product behavior, schemas, CLI/MCP JSON shape",
        "Version identity",
        "Exact read-only MCP tool list",
        "Disabled privacy surfaces",
        "Observed-content trust boundary",
        "Watcher preview limits",
        "Durable memory contract",
        "Phase 6 spec-only status",
        "Product targeted capture absence",
        "No write/control/file/screenshot/OCR/audio/keyboard/clipboard/network tools found",
        "No screenshot/OCR implementation found",
        "Product targeted capture remains absent",
        "45 passed",
        "matches are existing disabled-surface contracts, sentinels",
        "allowed helper-only harness wording",
        "No new product CLI/MCP targeted capture",
        "No new runtime dependency or\nimplementation path was found",
        "AB4 found no compatibility drift",
        "compatible `v0.1.14` maintenance target",
        "explicit release approval",
    ):
        assert expected in sweep


def test_post_v014_compatibility_guardrail_sweep_records_no_drift_decision():
    sweep = (
        ROOT / "docs" / "compatibility-guardrail-sweep-post-v0.1.14.md"
    ).read_text(encoding="utf-8")

    for expected in (
        "Compatibility Guardrail Sweep After v0.1.14",
        "does not change product behavior, schemas, CLI/MCP JSON\nshape",
        "MCP tool schemas",
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
        "trust = \"untrusted_observed_content\"",
        "No write/control/file/screenshot/OCR/audio/keyboard/clipboard/network tools found",
        "No screenshot/OCR implementation found",
        "Product targeted capture remains absent",
        "45 passed",
        "matches are existing disabled-surface contracts, sentinels",
        "allowed helper-only harness wording",
        "No new product CLI/MCP targeted capture",
        "No new runtime dependency or implementation path was\nfound",
        "AC4 found no compatibility drift",
        "compatible `v0.1.15` maintenance target",
        "explicit release approval",
    ):
        assert expected in sweep


def test_post_v015_compatibility_guardrail_sweep_records_drift_fixes():
    sweep = (
        ROOT / "docs" / "compatibility-guardrail-sweep-post-v0.1.15.md"
    ).read_text(encoding="utf-8")

    for expected in (
        "Compatibility Guardrail Sweep After v0.1.15",
        "broader\nobvious-secret redaction canaries",
        "product helper/watcher pass-through\nrejection",
        "does not\nchange schemas, CLI/MCP JSON shape",
        "MCP tool schemas",
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
        "trust = \"untrusted_observed_content\"",
        "No write/control/file/screenshot/OCR/audio/keyboard/clipboard/network tools found",
        "No screenshot/OCR implementation found",
        "Product targeted capture remains absent",
        "48 passed",
        "6 passed",
        "matches are existing disabled-surface contracts, sentinels",
        "AD4 pass-through rejection tests",
        "allowed helper-only harness wording",
        "No new product CLI/MCP targeted capture",
        "No new runtime dependency or implementation path was\nfound",
        "fixed two narrow compatibility guardrail drifts",
        "newer obvious GitHub/Slack token\n  families",
        "disabled\n  target/control/privacy-surface flags",
        "compatible `v0.1.16` maintenance target",
        "explicit release approval",
    ):
        assert expected in sweep


def test_post_v016_compatibility_guardrail_sweep_records_precision_fixes():
    sweep = (
        ROOT / "docs" / "compatibility-guardrail-sweep-post-v0.1.16.md"
    ).read_text(encoding="utf-8")
    normalized = " ".join(sweep.split())

    for expected in (
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
        assert expected in normalized


def test_post_v017_compatibility_guardrail_sweep_records_current_review():
    sweep = (
        ROOT / "docs" / "compatibility-guardrail-sweep-post-v0.1.17.md"
    ).read_text(encoding="utf-8")
    normalized = " ".join(sweep.split())

    for expected in (
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
        assert expected in normalized

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


def test_post_v018_compatibility_guardrail_sweep_records_current_review():
    sweep = (
        ROOT / "docs" / "compatibility-guardrail-sweep-post-v0.1.18.md"
    ).read_text(encoding="utf-8")
    normalized = " ".join(sweep.split())

    for expected in (
        "Compatibility Guardrail Sweep After v0.1.18",
        "AH4 compatibility check",
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
        "tests/test_privacy_policy_contract.py",
        "Result: `161 passed`",
        "Result: `211 passed`",
        "Result: passed",
        "Result: no matches",
        "WinChronicle harness passed",
        "watcher fake-helper smoke",
        "Boundary scan",
        "Background install/polling scan",
        "Control/capture dependency scan",
        "Stale cursor scan",
        "AH4 found no required schema",
        "The next smallest implementation task is to land this AH4 review",
    ):
        assert expected in normalized

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


def test_post_v017_release_readiness_decision_records_no_release_path():
    decision = (
        ROOT / "docs" / "release-readiness-decision-post-v0.1.17.md"
    ).read_text(encoding="utf-8")
    normalized = " ".join(decision.split())

    for expected in (
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
        assert expected in normalized

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


def test_post_v018_release_readiness_decision_records_no_release_path():
    decision = (
        ROOT / "docs" / "release-readiness-decision-post-v0.1.18.md"
    ).read_text(encoding="utf-8")
    normalized = " ".join(decision.split())

    for expected in (
        "Release-Readiness Decision After v0.1.18",
        "AH5 record",
        "do not start a new release-readiness or publication path",
        "Do not retag `v0.1.18`",
        "documentation, evidence, deterministic-test, and compatibility guardrail maintenance only",
        "do not change runtime code",
        "Is a release-readiness path warranted? | No.",
        "Is immediate publication warranted? | No.",
        "Should `v0.1.18` be retagged? | No.",
        "Should the next release-readiness target be chosen here? | No.",
        "Is fresh manual UIA smoke decided here? | No.",
        "Start the next blueprint implementation lane",
        "`docs/` | Added AH1 public metadata audit",
        "`tests/` | Hardened documentation and compatibility assertions",
        "`src/winchronicle`, `resources`, `pyproject.toml` | No diff",
        "Latest published release remains",
        "https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.18",
        "`v0.1.18` is not a draft or prerelease",
        "AH4 completion merged as `a773bcd6535bcac9bdfef87162aa1c5f8fc23369`",
        "through PR #193 at `2026-05-09T23:33:38Z`",
        "AH4 PR Windows Harness run `25614535578` concluded `success`",
        "post-merge `main` Windows Harness run `25614585178`",
        "AH5 PR Windows Harness run `25614929381` concluded `success`",
        "AH5 merged as `0bc33714d8fe2e9926d6c4753c8c7780fb1e9e00` through PR #194",
        "post-merge `main` Windows Harness run `25614978807`",
        "git fetch origin tag v0.1.18",
        "git diff --name-status v0.1.18..HEAD",
        "runtime/resource/version diff commands printed no files",
        "focused docs/version validation reported 91 tests",
        "full pytest reported 213 tests",
        "stale AH4 cursor scan returned no matches",
        "full deterministic harness passed",
        "AH5 PR and post-merge validation:",
        "PR #194 merged at `2026-05-09T23:56:35Z`",
        "PR Windows Harness run `25614929381` concluded `success`",
        "post-AH5 `main` Windows Harness run `25614978807` concluded `success`",
        "AH5 does not authorize implementation of screenshot capture",
        "privacy-neutral guardrails and evidence maintenance",
        "Start the next blueprint implementation lane with contracts",
        "Do not implement screenshot capture, OCR, raw screenshot caches",
    ):
        assert expected in normalized

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


def test_release_evidence_freshness_guard_labels_inherited_manual_smoke():
    checklist = (ROOT / "docs" / "release-checklist.md").read_text(encoding="utf-8")
    evidence = (ROOT / "docs" / "release-evidence.md").read_text(encoding="utf-8")
    plan = (ROOT / "docs" / "next-round-plan-post-v0.1.4.md").read_text(
        encoding="utf-8"
    )

    for expected in (
        "## Evidence Freshness",
        "current published baseline is `v0.2.0`",
        "fresh Notepad and Edge manual\n  UIA smoke",
        "fake-helper monitor watcher smoke",
        "`v0.2.0` is the latest published release",
        "tag target\n  `76005d7b3f115df36ce024ba69b02da28e239ff8`",
        "`v0.1.19` is the previous stable release",
        "`v0.1.18` is historical stable release evidence",
        "`v0.1.16` is historical stable release evidence",
        "`v0.1.16-rc.0` is historical prerelease evidence",
        "active post-v0.1.18 execution cursor records `v0.1.18` publication",
        "completed post-v0.1.17 execution cursor records `v0.1.17` publication",
        "AF7\n  publication reconciliation",
        "PR Windows Harness run `25601966464`",
        "post-merge Windows Harness run `25602018700`",
        "post-v0.1.17 baseline",
        "completed post-v0.1.16 execution cursor records the `v0.1.16` baseline",
        "final tag target\n  `5b260edc3bddc48986e52179b2ffd261856a89ac`",
        "PR #159",
        "PR #160",
        "release metadata/tag\n  verification",
        "completed post-v0.1.14 execution cursor records `v0.1.15` publication",
        "PR #132, PR #133, publication reconciliation PR #134, post-merge Windows",
        "Harness run `25589775129`",
        "completed post-v0.1.13 execution cursor records `v0.1.14` publication",
        "PR #125, and post-merge Windows Harness run `25585147402`",
        "completed post-v0.1.13 execution cursor also records the `v0.1.14`",
        "post-publication reconciliation PR #126 plus post-merge Windows Harness run",
        "`25585707220`",
        "post-v0.1.13 execution cursor also records the initial `v0.1.13`",
        "PR #119 plus post-merge Windows Harness run\n  `25581662790`",
        "post-v0.1.12 execution cursor is completed historical context",
        "PR #118 plus post-merge Windows Harness run `25580877004`",
        "post-v0.1.11 execution cursor is completed historical context",
        "post-merge Windows Harness run `25576867729`",
        "post-v0.1.10 execution cursor is completed historical context",
        "post-merge Windows Harness run `25569567825`",
        "post-v0.1.9 execution cursor is completed historical context",
        "X0 PR #97 plus\n  post-merge Windows Harness run `25566750349`",
        "X3 PR #100 plus post-merge Windows Harness run\n  `25568639603`",
        "post-v0.1.8 execution cursor is completed historical context",
        "post-v0.1.7 execution cursor is completed historical context",
        "post-v0.1.6 execution cursor is completed historical context",
        "post-v0.1.5 execution cursor is completed historical context",
        "manual UIA smoke inherited from an earlier release is labeled as inherited or",
        "inherited `v0.1.0` manual",
        "post-v0.1.5 compatible maintenance path that published `v0.1.6`",
        "inherited `v0.1.0` manual smoke was explicitly accepted by S4",
        "post-v0.1.6 compatible maintenance path toward `v0.1.7`",
        "inherited\n  `v0.1.0` manual smoke is explicitly accepted by the T4",
        "completed post-v0.1.7 compatible maintenance path toward `v0.1.8`",
        "remained stale/inherited after the U1",
        "explicitly accepted by the U4",
        "completed post-v0.1.8 maintenance path",
        "stale/inherited after the W1 freshness decision",
        "not\n  fresh or current release evidence",
        "completed post-v0.1.8 compatible maintenance path toward `v0.1.9`",
        "inherited `v0.1.0` manual smoke is explicitly accepted by the W4",
        "completed post-v0.1.9 compatible maintenance path",
        "inherited `v0.1.0`\n  manual smoke is explicitly accepted by the X1",
        "did not make inherited manual smoke fresh or current release\n  evidence",
        "completed `v0.1.10` release-readiness path",
        "explicitly accepted by the X4 release-readiness record",
        "completed `v0.1.11` release-readiness path",
        "explicitly accepted by the Y4 release-readiness record",
        "completed post-v0.1.10 compatible maintenance path",
        "manual smoke is explicitly accepted by the Y1 freshness decision",
        "the Y1 decision does not make inherited manual smoke fresh or current release",
        "completed post-v0.1.11 compatible maintenance path",
        "manual smoke is explicitly accepted by the Z1 freshness decision",
        "the Z1 decision does not make inherited manual smoke fresh or current release",
        "the Z4 release-readiness record explicitly accepted inherited",
        "completed post-v0.1.12 compatible maintenance path",
        "explicitly accepted by the AA5 release-readiness",
        "`v0.1.13` publication",
        "capture-surface behavior changed before release",
        "no observed-content artifact is committed to refresh evidence",
        "deterministic harness smoke changes require fresh deterministic gate",
    ):
        assert expected in checklist

    for expected in (
        "Release evidence must name which facts are current",
        "`v0.2.0` is the current published baseline",
        "fake-helper monitor watcher smoke",
        "`v0.2.0` is the latest published release",
        "tag target\n  `76005d7b3f115df36ce024ba69b02da28e239ff8`",
        "`v0.1.19` is the previous stable release",
        "`v0.1.18` is historical stable release evidence",
        "`v0.1.16` is historical stable release evidence",
        "`v0.1.16-rc.0` is historical prerelease evidence",
        "active post-v0.1.18 execution cursor records `v0.1.18` publication",
        "completed post-v0.1.17 execution cursor records `v0.1.17` publication",
        "AF7\n  publication reconciliation",
        "PR Windows Harness run `25601966464`",
        "post-merge Windows Harness run `25602018700`",
        "post-v0.1.17 baseline",
        "completed post-v0.1.16 execution cursor records the `v0.1.16` baseline",
        "final tag target\n  `5b260edc3bddc48986e52179b2ffd261856a89ac`",
        "PR #159",
        "PR #160",
        "release metadata/tag\n  verification",
        "completed post-v0.1.14 execution cursor records `v0.1.15` publication",
        "PR #132, PR #133, publication reconciliation PR #134, post-merge Windows",
        "Harness run `25589775129`",
        "completed post-v0.1.13 execution cursor records `v0.1.14` publication",
        "PR #125, and post-merge Windows Harness run `25585147402`",
        "completed post-v0.1.13 execution cursor also records the `v0.1.14`",
        "post-publication reconciliation PR #126 plus post-merge Windows Harness run",
        "`25585707220`",
        "post-v0.1.13 execution cursor also records the initial `v0.1.13`",
        "PR #119 plus post-merge Windows Harness run\n  `25581662790`",
        "post-v0.1.12 execution cursor is completed historical context",
        "PR #118 plus post-merge Windows Harness run `25580877004`",
        "post-v0.1.11 execution cursor is completed historical context",
        "post-merge Windows Harness run `25576867729`",
        "post-v0.1.10 execution cursor is completed historical context",
        "post-merge Windows Harness run `25569567825`",
        "post-v0.1.9 execution cursor is completed historical context",
        "X0 PR #97 plus\n  post-merge Windows Harness run `25566750349`",
        "X3 PR #100 plus post-merge Windows Harness run\n  `25568639603`",
        "post-v0.1.8 execution cursor is completed historical context",
        "post-v0.1.7 execution cursor is completed historical context",
        "post-v0.1.6 execution cursor is completed historical context",
        "post-v0.1.5 execution cursor is completed historical context",
        "manual UIA smoke evidence inherited from `v0.1.0`",
        "must be labeled as inherited or stale",
        "must not present inherited manual smoke as freshly run",
        "post-v0.1.5 compatible maintenance path that published `v0.1.6`",
        "inherited `v0.1.0` manual smoke was explicitly accepted by S4",
        "post-v0.1.6 compatible maintenance path toward `v0.1.7`",
        "inherited\n  `v0.1.0` manual smoke is explicitly accepted by the T4",
        "completed post-v0.1.7 compatible maintenance path toward `v0.1.8`",
        "remained stale/inherited after the U1",
        "explicitly accepted by the U4",
        "completed post-v0.1.8 maintenance path",
        "stale/inherited after the W1 freshness decision",
        "not\n  fresh or current release evidence",
        "completed post-v0.1.8 compatible maintenance path toward `v0.1.9`",
        "inherited `v0.1.0` manual smoke is explicitly accepted by the W4",
        "completed post-v0.1.9 compatible maintenance path",
        "inherited `v0.1.0`\n  manual smoke is explicitly accepted by the X1",
        "did not make inherited manual smoke fresh or current release\n  evidence",
        "completed `v0.1.10` release-readiness path",
        "explicitly accepted by the X4 release-readiness record",
        "completed `v0.1.11` release-readiness path",
        "explicitly accepted by the Y4 release-readiness record",
        "completed post-v0.1.10 compatible maintenance path",
        "manual smoke is explicitly accepted by the Y1 freshness decision",
        "the Y1 decision does not make inherited manual smoke fresh or current release",
        "completed post-v0.1.11 compatible maintenance path",
        "manual smoke is explicitly accepted by the Z1 freshness decision",
        "the Z1 decision does not make inherited manual smoke fresh or current release",
        "the Z4 release-readiness record explicitly accepted inherited",
        "completed post-v0.1.12 compatible maintenance path",
        "explicitly accepted by the AA5 release-readiness",
        "`v0.1.13` publication",
        "capture-surface behavior changed before release",
        "never observed content",
        "deterministic harness smoke changes require fresh deterministic gate",
    ):
        assert expected in evidence

    assert "Stage P2 - Manual Smoke Freshness Decision" in plan


def test_manual_smoke_ledger_tracks_freshness_without_observed_artifacts():
    ledger = (ROOT / "docs" / "manual-smoke-evidence-ledger.md").read_text(
        encoding="utf-8"
    )
    quickstart = (ROOT / "docs" / "operator-quickstart.md").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    checklist = (ROOT / "docs" / "release-checklist.md").read_text(encoding="utf-8")
    evidence = (ROOT / "docs" / "release-evidence.md").read_text(encoding="utf-8")
    plan = (ROOT / "docs" / "next-round-plan-post-v0.1.4.md").read_text(
        encoding="utf-8"
    )

    for gate in (
        "Notepad targeted UIA smoke",
        "Edge targeted UIA smoke",
        "VS Code metadata smoke",
        "VS Code strict Monaco marker",
        "Watcher preview live smoke",
    ):
        assert gate in ledger

    for expected in (
        "Stable release baseline | `v0.2.0`",
        "Current maintenance plan | [Post-v0.1.18 maintenance plan]",
        "Current public metadata audit | [Public metadata audit after v0.1.18]",
        "Current helper/watcher diagnostics sweep | [Helper and watcher diagnostics sweep after v0.1.18]",
        "Current MCP/memory contract sweep | [MCP and memory contract sweep after v0.1.18]",
        "Current compatibility guardrail sweep | [Compatibility guardrail sweep after v0.1.18]",
        "Latest release-readiness decision | [Release-readiness decision after v0.1.18]",
        "Current next blueprint lane selection | [Next blueprint lane selection after v0.1.18]",
        "Completed watcher privacy fixture parity | [Watcher privacy fixture parity after v0.1.18]",
        "Completed fixture/helper privacy index parity | [Fixture/helper privacy index parity after v0.1.18]",
        "Completed fixture/privacy parity matrix | [Fixture/privacy parity matrix after v0.1.18]",
        "Completed fixture/privacy residual gap audit | [Fixture/privacy residual gap audit after v0.1.18]",
        "Current privacy-output release-readiness decision | [Privacy-output release-readiness decision after v0.1.18]",
        "Current release record | [v0.2.0 release record]",
        "Previous release-readiness decision | [v0.1.18 maintenance release record]",
        "Previous pre-v0.1.18 release-readiness decision | [Privacy-check release-readiness decision after v0.1.17]",
        "Previous maintenance plan | [Post-v0.1.17 maintenance plan]",
        "Previous pre-v0.1.17 maintenance plan | [Post-v0.1.16 maintenance plan]",
        "Previous public metadata audit | [Public metadata audit after v0.1.17]",
        "Previous post-v0.1.16 release-readiness decision | [Release-readiness decision after v0.1.16]",
        "Previous release record | [v0.1.18 maintenance release record]",
        "Completed final-release plan | [v0.1.16 final-release plan]",
        "Previous prerelease record | [v0.1.16-rc.0 release candidate record]",
        "Previous pre-v0.1.16 maintenance plan | [Post-v0.1.15 maintenance plan]",
        "Published release record | [v0.2.0 release record]",
        "Latest published release record | [v0.2.0 release record]",
        "Previous stable release record | [v0.1.19 maintenance release record]",
        "Latest full manual UIA smoke source | [v0.2.0 release record]",
        "Last freshness decision | For the published `v0.2.0` monitor-session release",
        "fresh hard-gate manual UIA smoke was rerun because product CLI/MCP shape and monitor-session output changed after `v0.1.19`",
        "Notepad and Edge passed, VS Code metadata passed with the known Monaco diagnostic warning",
        "VS Code strict remains a diagnostic non-blocking failure",
        "Previous freshness decision | For the published `v0.1.18` maintenance release",
        "fresh hard-gate manual UIA smoke was rerun because privacy-check validation behavior changed after `v0.1.17`",
        "manual smoke was explicitly accepted by the S4 release record",
        "`v0.1.0` manual smoke is explicitly accepted by the T4 release-readiness",
        "then is explicitly accepted by the U4",
        "manual smoke is explicitly accepted by the W4",
        "manual smoke is accepted by the X1 freshness decision as",
        "Fresh for the published `v0.1.18` maintenance release; previous fresh source was published `v0.1.17` maintenance in AF6",
        "Fresh diagnostic for the published `v0.1.18` maintenance release",
        "Heartbeat-only liveness diagnostic; `captures_written: 0`, `heartbeats: 9`, `duplicates_skipped: 0`, `denylisted_skipped: 0`",
        "Fresh for the published `v0.1.19` maintenance release",
        "Fresh for the published `v0.2.0` monitor-session release",
        "Fake-helper monitor watcher",
        "`captures_written: 1`, `heartbeats: 3`",
        "Heartbeat-only liveness diagnostic; `captures_written: 0`, `heartbeats: 10`, `duplicates_skipped: 0`, `denylisted_skipped: 0`",
        "manual smoke is explicitly accepted by the T4 release-readiness\n  record",
        "For the completed post-v0.1.7 compatible maintenance path toward `v0.1.8`",
        "then is explicitly accepted by the U4",
        "For the completed post-v0.1.8 path, inherited `v0.1.0` manual smoke remains",
        "stale/inherited after the W1 freshness decision",
        "not fresh or current\n  release evidence",
        "For the completed post-v0.1.8 compatible maintenance path toward `v0.1.9`",
        "manual smoke is explicitly accepted by the W4",
        "For the completed post-v0.1.9 compatible maintenance path, inherited",
        "manual smoke is accepted by the X1 freshness decision as",
        "the X4 release-readiness record now explicitly accepts",
        "For the completed post-v0.1.9 compatible maintenance path that published",
        "manual smoke is explicitly accepted by the X4\n  release-readiness record",
        "For the completed post-v0.1.10 compatible maintenance path",
        "inherited manual\n  smoke is accepted by the Y1 freshness decision as",
        "the Y4\n  release-readiness record now explicitly accepts inherited evidence",
        "compatible `v0.1.11` path",
        "For the completed post-v0.1.11 compatible maintenance path",
        "inherited manual\n  smoke was accepted by the Z1 freshness decision as",
        "Z4 release-readiness record explicitly accepted inherited evidence",
        "compatible `v0.1.12` path",
        "Fresh manual smoke is required if any helper, watcher, smoke script",
        "Do not paste observed text",
        "Do not save or commit raw watcher JSONL",
        "inherited/stale unless rerun",
        "The AF5 post-v0.1.16 release-readiness decision starts a narrow `v0.1.17`",
        "`v0.1.17` release-readiness record must decide whether to inherit or rerun",
        "AF1-AF4 include compatible public CLI/runtime output\n  changes",
        "The AF6 `v0.1.17` release-readiness record reran fresh hard-gate manual UIA",
        "The published `v0.1.17` maintenance release kept that AF6 manual smoke as",
        "live watcher preview returned heartbeat-only liveness evidence",
        "The privacy-check release-readiness decision after `v0.1.17` starts a",
        "narrow `v0.1.18` release-readiness path",
        "does not decide manual smoke freshness",
        "The `v0.1.18` release-readiness record reran fresh hard-gate manual UIA",
        "smoke because privacy-check validation behavior changed after `v0.1.17`",
        "The post-v0.1.18 release-readiness decision does not open a new publication",
        "does not make a fresh manual UIA smoke\n  decision",
        "The privacy-output release-readiness decision after `v0.1.18` starts a",
        "narrow `v0.1.19` release-readiness path",
        "published `v0.1.19` maintenance release record\n  resolves that question",
        "The `v0.1.19` maintenance release record reran fresh hard-gate manual UIA",
        "privacy-output and read-only MCP response behavior changed",
        "The `v0.2.0` release record reran fresh hard-gate manual UIA",
        "product CLI/MCP shape and monitor-session output changed",
        "VS Code strict remains diagnostic and\n  non-blocking",
        "Deterministic harness smoke changes require fresh deterministic gate",
    ):
        assert expected in ledger

    assert "The published `v0.1.17` maintenance release keeps that AF6 manual smoke" not in ledger

    assert "[Manual smoke evidence ledger](manual-smoke-evidence-ledger.md)" in quickstart
    assert "[Manual smoke evidence ledger](docs/manual-smoke-evidence-ledger.md)" in readme
    assert "Manual smoke evidence ledger" in checklist
    assert "Manual smoke evidence ledger" in evidence
    assert "Current stage: G - v0.1.5 Published Baseline Reconciliation." in plan
    assert "Stage status: G - v0.1.5 published; baseline reconciliation complete." in plan
    assert "Windows Harness run `25432718007` passed on that SHA" in plan
    assert "Stage P0 - Post-v0.1.4 Baseline Cursor" in plan
    assert "Stage P1 entry-hygiene validation:" in plan
    assert "Stage P2 manual-smoke freshness validation:" in plan
    assert "Stage P3 compatibility guardrail validation:" in plan
    assert "Stage P4 release-readiness validation:" in plan
    assert "Stage P0 local validation:" in plan
    assert "Stage P2 - Manual Smoke Freshness Decision" in plan
    assert "observed-content\n  artifacts remain uncommitted" in plan
