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
        "Targeted capture remains helper-only harness smoke",
    ):
        assert content_guard in diagnostics


def test_operator_quickstart_links_diagnostics_playbook():
    quickstart = (ROOT / "docs" / "operator-quickstart.md").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")

    assert "[Operator diagnostics](operator-diagnostics.md)" in quickstart
    assert "[Operator diagnostics](docs/operator-diagnostics.md)" in readme


def test_operator_entry_points_distinguish_current_cursor_from_history():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    quickstart = (ROOT / "docs" / "operator-quickstart.md").read_text(encoding="utf-8")
    checklist = (ROOT / "docs" / "release-checklist.md").read_text(encoding="utf-8")
    evidence = (ROOT / "docs" / "release-evidence.md").read_text(encoding="utf-8")
    matrix = (ROOT / "docs" / "uia-helper-quality-matrix.md").read_text(encoding="utf-8")

    readme_intro = readme.split("## Why WinChronicle", 1)[0]
    readme_operator_docs = readme.split("## Operator Docs", 1)[1].split(
        "Screenshot/OCR enrichment", 1
    )[0]
    current_section = quickstart.split("## Current Maintenance Docs", 1)[1].split(
        "## Historical Release Records", 1
    )[0]
    historical_section = quickstart.split("## Historical Release Records", 1)[1]
    readme_intro_normalized = " ".join(readme_intro.split())

    assert "latest published `v0.1.10` release record" in readme_intro_normalized
    assert "active post-v0.1.10 maintenance plan" in readme_intro_normalized
    assert "completed post-v0.1.9 maintenance plan" in readme_intro_normalized
    assert "latest published `v0.1.5` release" not in readme_intro
    assert "latest published `v0.1.3` release" not in readme_intro
    assert "v0.1.10 maintenance release record" in readme_operator_docs
    assert "Post-v0.1.10 maintenance plan" in readme_operator_docs
    assert "v0.1.9 maintenance release record" in readme_operator_docs
    assert "Post-v0.1.9 maintenance plan" in readme_operator_docs
    assert "v0.1.8 maintenance release record" in readme_operator_docs
    assert "Post-v0.1.8 maintenance plan" in readme_operator_docs
    assert "v0.1.7 maintenance release record" in readme_operator_docs
    assert "Post-v0.1.7 maintenance plan" in readme_operator_docs
    assert "Post-v0.1.6 maintenance plan" in readme_operator_docs
    assert "Post-v0.1.5 maintenance plan" in readme_operator_docs
    assert "v0.1.6 maintenance release record" in readme_operator_docs
    assert "Post-v0.1.4 maintenance plan" in readme_operator_docs
    assert "v0.1.5 maintenance release record" in readme_operator_docs
    assert "v0.1.4 maintenance release record" in readme_operator_docs
    assert readme_operator_docs.index("v0.1.10 maintenance release record") < readme_operator_docs.index(
        "Post-v0.1.10 maintenance plan"
    )
    assert readme_operator_docs.index("Post-v0.1.10 maintenance plan") < readme_operator_docs.index(
        "v0.1.9 maintenance release record"
    )
    assert readme_operator_docs.index("v0.1.9 maintenance release record") < readme_operator_docs.index(
        "Post-v0.1.9 maintenance plan"
    )
    assert readme_operator_docs.index("Post-v0.1.9 maintenance plan") < readme_operator_docs.index(
        "v0.1.8 maintenance release record"
    )
    assert readme_operator_docs.index("v0.1.8 maintenance release record") < readme_operator_docs.index(
        "Post-v0.1.8 maintenance plan"
    )
    assert readme_operator_docs.index("Post-v0.1.8 maintenance plan") < readme_operator_docs.index(
        "Post-v0.1.7 maintenance plan"
    )
    assert readme_operator_docs.index("Post-v0.1.7 maintenance plan") < readme_operator_docs.index(
        "v0.1.7 maintenance release record"
    )
    assert readme_operator_docs.index("v0.1.7 maintenance release record") < readme_operator_docs.index(
        "Post-v0.1.6 maintenance plan"
    )
    assert readme_operator_docs.index("Post-v0.1.6 maintenance plan") < readme_operator_docs.index(
        "v0.1.6 maintenance release record"
    )
    assert "release-v0.1.10.md" in current_section
    assert "next-round-plan-post-v0.1.10.md" in current_section
    assert "release-v0.1.9.md" not in current_section
    assert "next-round-plan-post-v0.1.9.md" not in current_section
    assert "release-v0.1.9.md" in historical_section
    assert "next-round-plan-post-v0.1.9.md" in historical_section
    assert "release-v0.1.8.md" not in current_section
    assert "next-round-plan-post-v0.1.8.md" not in current_section
    assert "release-v0.1.8.md" in historical_section
    assert "next-round-plan-post-v0.1.8.md" in historical_section
    assert "release-v0.1.7.md" in historical_section
    assert "next-round-plan-post-v0.1.7.md" in historical_section
    assert "next-round-plan-post-v0.1.6.md" not in current_section
    assert "release-v0.1.6.md" not in current_section
    assert "next-round-plan-post-v0.1.6.md" in historical_section
    assert "release-v0.1.6.md" in historical_section
    assert readme_operator_docs.index("v0.1.6 maintenance release record") < readme_operator_docs.index(
        "Post-v0.1.5 maintenance plan"
    )
    assert readme_operator_docs.index("Post-v0.1.5 maintenance plan") < readme_operator_docs.index(
        "v0.1.5 maintenance release record"
    )
    assert readme_operator_docs.index("v0.1.5 maintenance release record") < readme_operator_docs.index(
        "Post-v0.1.4 maintenance plan"
    )
    assert readme_operator_docs.index("Post-v0.1.4 maintenance plan") < readme_operator_docs.index(
        "v0.1.4 maintenance release record"
    )
    assert readme_operator_docs.index("v0.1.4 maintenance release record") < readme_operator_docs.index(
        "v0.1.3 maintenance release record"
    )
    assert "next-round-plan-post-v0.1.5.md" not in current_section
    assert "release-v0.1.5.md" not in current_section
    assert "next-round-plan-post-v0.1.5.md" in historical_section
    assert "release-v0.1.5.md" in historical_section
    assert "next-round-plan-post-v0.1.4.md" not in current_section
    assert "release-v0.1.4.md" not in current_section
    assert "next-round-plan-post-v0.1.4.md" in historical_section
    assert "release-v0.1.4.md" in historical_section
    assert "next-round-plan-post-v0.1.3.md" not in current_section
    assert "release-v0.1.3.md" not in current_section
    assert "next-round-plan-post-v0.1.2.md" not in current_section
    assert "release-v0.1.2.md" not in current_section
    assert "next-round-plan-post-v0.1.1.md" not in current_section
    assert "next-round-plan-v0.1.0-final.md" not in current_section
    assert "next-round-plan-post-v0.1.3.md" in historical_section
    assert "release-v0.1.3.md" in historical_section
    assert "next-round-plan-post-v0.1.2.md" in historical_section
    assert "release-v0.1.2.md" in historical_section
    assert "next-round-plan-post-v0.1.1.md" in historical_section
    assert "release-v0.1.1.md" in historical_section
    assert "next-round-plan-v0.1.0-final.md" in historical_section
    assert "release-v0.1.10.md" in checklist
    assert "release-v0.1.10.md" in evidence
    assert "next-round-plan-post-v0.1.10.md" in checklist
    assert "next-round-plan-post-v0.1.10.md" in evidence
    assert "release-v0.1.9.md" not in checklist
    assert "release-v0.1.9.md" not in evidence
    assert "next-round-plan-post-v0.1.9.md" not in checklist
    assert "next-round-plan-post-v0.1.9.md" not in evidence
    assert "release-v0.1.8.md" not in checklist
    assert "release-v0.1.8.md" not in evidence
    assert "next-round-plan-post-v0.1.8.md" not in checklist
    assert "next-round-plan-post-v0.1.8.md" not in evidence
    assert "next-round-plan-post-v0.1.7.md" not in checklist
    assert "next-round-plan-post-v0.1.7.md" not in evidence
    assert "release-v0.1.7.md" not in checklist
    assert "release-v0.1.7.md" not in evidence
    assert "next-round-plan-post-v0.1.6.md" not in checklist
    assert "next-round-plan-post-v0.1.6.md" not in evidence
    assert "next-round-plan-post-v0.1.5.md" not in checklist
    assert "next-round-plan-post-v0.1.5.md" not in evidence
    assert "release-v0.1.6.md" not in checklist
    assert "release-v0.1.6.md" not in evidence
    assert "next-round-plan-post-v0.1.4.md" not in checklist
    assert "next-round-plan-post-v0.1.4.md" not in evidence
    assert "release-v0.1.5.md" not in checklist
    assert "release-v0.1.5.md" not in evidence
    assert "release-v0.1.4.md" not in checklist
    assert "release-v0.1.4.md" not in evidence
    assert "post-v0.1.9 plan is completed historical evidence" in checklist
    assert "post-v0.1.9 cursor is completed historical evidence" in evidence
    assert "Before a compatible `v0.1.1` maintenance release" not in matrix
    assert "For compatible maintenance releases after `v0.1.9`" in matrix
    assert "Historical\nmaintenance records from `v0.1.4` onward" in matrix
    assert "current\n`v0.1.3` readiness round" not in matrix


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


def test_post_v0110_plan_is_active_without_expanding_scope():
    plan = (ROOT / "docs" / "next-round-plan-post-v0.1.10.md").read_text(
        encoding="utf-8"
    )
    normalized = " ".join(plan.split())

    for expected in (
        "Current stage: Y1 - Evidence Freshness And Entry Hygiene.",
        "Stage status: B - Y1 evidence freshness docs/tests are implemented",
        "`v0.1.10` is published at https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.10",
        "targets `28b062a531519d4360911b51dfc083782b6dcbad`",
        "Windows Harness run `25569567825` passed",
        "Y0 PR #102 passed PR Windows Harness run `25570444498`",
        "merged as `049fbc3550efe71e553fb0e27be7344f4d686e5c`",
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
        "Stage Y0 initialization:",
        "Stage Y0 local validation:",
        "Stage Y0 remote validation:",
        "Stage Y1 evidence freshness validation:",
        "`python -m pytest -q` - passed, 116 tests.",
        "Pending PR Windows Harness.",
        "`python -m pytest -q` - passed, 116 tests.",
        "python -c \"import winchronicle; print(winchronicle.__version__)\"",
    ):
        assert expected in normalized


def test_release_evidence_freshness_guard_labels_inherited_manual_smoke():
    checklist = (ROOT / "docs" / "release-checklist.md").read_text(encoding="utf-8")
    evidence = (ROOT / "docs" / "release-evidence.md").read_text(encoding="utf-8")
    plan = (ROOT / "docs" / "next-round-plan-post-v0.1.4.md").read_text(
        encoding="utf-8"
    )

    for expected in (
        "## Evidence Freshness",
        "stable baseline is `v0.1.10`",
        "`v0.1.10` is the latest published release",
        "post-v0.1.10 execution cursor is active and records PR #101",
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
        "active post-v0.1.10 compatible maintenance path",
        "manual smoke is explicitly accepted by the Y1 freshness decision",
        "the Y1 decision does not make inherited manual smoke fresh or current release",
        "capture-surface behavior changed before release",
        "no observed-content artifact is committed to refresh evidence",
        "deterministic harness smoke changes require fresh deterministic gate",
    ):
        assert expected in checklist

    for expected in (
        "Release evidence must name which facts are current",
        "`v0.1.10` is the stable baseline",
        "`v0.1.10` is the latest published release",
        "post-v0.1.10 execution cursor is active and records PR #101",
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
        "active post-v0.1.10 compatible maintenance path",
        "manual smoke is explicitly accepted by the Y1 freshness decision",
        "the Y1 decision does not make inherited manual smoke fresh or current release",
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
        "Stable release baseline | `v0.1.10`",
        "Current maintenance plan | [Post-v0.1.10 maintenance plan]",
        "Latest completed maintenance plan | [Post-v0.1.9 maintenance plan]",
        "Published release record | [v0.1.10 maintenance release record]",
        "Latest published release record | [v0.1.10 maintenance release record]",
        "Latest full manual UIA smoke source | [v0.1.0 final release readiness record]",
        "Last freshness decision | For the active post-v0.1.10 compatible maintenance path",
        "inherited `v0.1.0` Notepad, Edge, VS Code metadata",
        "is explicitly accepted by Y1 as inherited/stale evidence",
        "Y0/Y1 changed only docs/tests",
        "explicitly accepted by S4 for the compatible `v0.1.6` path",
        "explicitly accepted by T4 for the compatible `v0.1.7` path",
        "explicitly accepted by U4 for the compatible `v0.1.8` path",
        "explicitly accepted by W4 for the compatible `v0.1.9` path",
        "accepted by X1 as inherited/stale evidence for the post-v0.1.9 path",
        "historically accepted for `v0.1.5` as diagnostic context",
        "Next freshness decision | Y4 release readiness must explicitly accept inherited manual evidence",
        "for `v0.1.11` publication or record fresh manual smoke",
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
        "For the active post-v0.1.10 compatible maintenance path",
        "inherited manual\n  smoke is accepted by the Y1 freshness decision as",
        "Y4\n  release readiness must explicitly accept inherited evidence",
        "Fresh manual smoke is required if any helper, watcher, smoke script",
        "Do not paste observed text",
        "Do not save or commit raw watcher JSONL",
        "inherited/stale unless rerun",
        "Deterministic harness smoke changes require fresh deterministic gate",
    ):
        assert expected in ledger

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
