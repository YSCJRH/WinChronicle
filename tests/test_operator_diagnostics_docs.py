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

    assert "latest published `v0.1.6` release record" in readme_intro_normalized
    assert "active post-v0.1.6 maintenance plan" in readme_intro_normalized
    assert "`v0.1.7` release-readiness record" in readme_intro_normalized
    assert "latest published `v0.1.5` release" not in readme_intro
    assert "latest published `v0.1.3` release" not in readme_intro
    assert "v0.1.7 maintenance release record" in readme_operator_docs
    assert "Post-v0.1.6 maintenance plan" in readme_operator_docs
    assert "Post-v0.1.5 maintenance plan" in readme_operator_docs
    assert "v0.1.6 maintenance release record" in readme_operator_docs
    assert "Post-v0.1.4 maintenance plan" in readme_operator_docs
    assert "v0.1.5 maintenance release record" in readme_operator_docs
    assert "v0.1.4 maintenance release record" in readme_operator_docs
    assert readme_operator_docs.index("v0.1.7 maintenance release record") < readme_operator_docs.index(
        "v0.1.6 maintenance release record"
    )
    assert readme_operator_docs.index("v0.1.6 maintenance release record") < readme_operator_docs.index(
        "Post-v0.1.6 maintenance plan"
    )
    assert "release-v0.1.7.md" in current_section
    assert readme_operator_docs.index("Post-v0.1.6 maintenance plan") < readme_operator_docs.index(
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
    assert "next-round-plan-post-v0.1.6.md" in current_section
    assert "release-v0.1.6.md" in current_section
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
    assert "next-round-plan-post-v0.1.6.md" in checklist
    assert "next-round-plan-post-v0.1.6.md" in evidence
    assert "release-v0.1.7.md" in checklist
    assert "release-v0.1.7.md" in evidence
    assert "next-round-plan-post-v0.1.5.md" not in checklist
    assert "next-round-plan-post-v0.1.5.md" not in evidence
    assert "release-v0.1.6.md" in checklist
    assert "release-v0.1.6.md" in evidence
    assert "next-round-plan-post-v0.1.4.md" not in checklist
    assert "next-round-plan-post-v0.1.4.md" not in evidence
    assert "release-v0.1.5.md" not in checklist
    assert "release-v0.1.5.md" not in evidence
    assert "release-v0.1.4.md" not in checklist
    assert "release-v0.1.4.md" not in evidence
    assert "post-v0.1.5 plan is completed historical evidence" in checklist
    assert "post-v0.1.5 cursor is completed historical evidence" in evidence
    assert "Before a compatible `v0.1.1` maintenance release" not in matrix
    assert "For compatible maintenance releases after `v0.1.4`" in matrix
    assert "published\n`v0.1.4` maintenance release record" in matrix
    assert "any later maintenance round" in matrix
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


def test_post_v016_plan_is_active_without_expanding_scope():
    plan = (ROOT / "docs" / "next-round-plan-post-v0.1.6.md").read_text(
        encoding="utf-8"
    )
    normalized = " ".join(plan.split())

    for expected in (
        "Current stage: T4 - v0.1.7 Release Readiness.",
        "Stage status: B - T4 local release-readiness changes and validation are",
        "`v0.1.6` is published at https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.6",
        "targets `914cf361ac5864fa31d393d125d14e45eeba96bc`",
        "Publication reconciliation PR #80 passed PR Windows Harness run `25552120656`",
        "merged as `371060498c70a4e1ff4e075b3fd247b704c6d3f7`",
        "Windows Harness run `25552214063` passed",
        "PR #81 Windows Harness run `25553025094` - passed",
        "Post-merge `main` Windows Harness run `25553238476` - passed",
        "T2 PR #83 passed PR Windows Harness run `25554431580`",
        "merged as `fb84fb2b2bf47cfe89680c898f3694f543d75c52`",
        "post-merge `main` Windows Harness run `25554520036` passed",
        "T3 PR #84 passed PR Windows Harness run `25555063537`",
        "merged as `6d1d8f94c56636c23daafcb4ceae24053ff226aa`",
        "post-merge `main` Windows Harness run `25555180274` passed",
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
        "not expand the capture surface or start Phase 6 implementation",
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
        "stable baseline is `v0.1.6`",
        "`v0.1.6` is the latest published release",
        "post-v0.1.6 execution cursor must be followed before any new",
        "post-v0.1.5 execution cursor is completed historical context",
        "manual UIA smoke inherited from an earlier release is labeled as inherited or",
        "inherited `v0.1.0` manual",
        "post-v0.1.5 compatible maintenance path that published `v0.1.6`",
        "inherited `v0.1.0` manual smoke was explicitly accepted by S4",
        "post-v0.1.6 compatible maintenance path toward `v0.1.7`",
        "inherited\n  `v0.1.0` manual smoke is explicitly accepted by the T4",
        "capture-surface behavior changed before release",
        "no observed-content artifact is committed to refresh evidence",
        "deterministic harness smoke changes require fresh deterministic gate",
    ):
        assert expected in checklist

    for expected in (
        "Release evidence must name which facts are current",
        "`v0.1.6` is the stable baseline",
        "`v0.1.6` is the latest published release",
        "post-v0.1.6 execution cursor must be followed before implementation",
        "post-v0.1.5 execution cursor is completed historical context",
        "manual UIA smoke evidence inherited from `v0.1.0`",
        "must be labeled as inherited or stale",
        "must not present inherited manual smoke as freshly run",
        "post-v0.1.5 compatible maintenance path that published `v0.1.6`",
        "inherited `v0.1.0` manual smoke was explicitly accepted by S4",
        "post-v0.1.6 compatible maintenance path toward `v0.1.7`",
        "inherited\n  `v0.1.0` manual smoke is explicitly accepted by the T4",
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
        "Stable release baseline | `v0.1.6`",
        "Current maintenance plan | [Post-v0.1.6 maintenance plan]",
        "Latest completed maintenance plan | [Post-v0.1.5 maintenance plan]",
        "Published release record | [v0.1.6 maintenance release record]",
        "Latest published release record | [v0.1.6 maintenance release record]",
        "Active release-readiness record | [v0.1.7 maintenance release record]",
        "Latest full manual UIA smoke source | [v0.1.0 final release readiness record]",
        "Last freshness decision | For the post-v0.1.6 compatible maintenance path toward `v0.1.7`",
        "inherited `v0.1.0` Notepad, Edge, VS Code metadata",
        "is explicitly accepted by the T4 release-readiness record",
        "explicitly accepted by S4 for the compatible `v0.1.6` path",
        "explicitly accepted by T4 for the compatible `v0.1.7` path",
        "historically accepted for `v0.1.5` as diagnostic context",
        "Next freshness decision | After any `v0.1.7` publication",
        "manual smoke is explicitly accepted by the T4 release-readiness record",
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
