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

    assert "latest published `v0.1.4` release" in readme_intro
    assert "active\npost-v0.1.4 maintenance plan" in readme_intro
    assert "latest published `v0.1.3` release" not in readme_intro
    assert "Post-v0.1.4 maintenance plan" in readme_operator_docs
    assert "v0.1.4 maintenance release record" in readme_operator_docs
    assert readme_operator_docs.index("Post-v0.1.4 maintenance plan") < readme_operator_docs.index(
        "Post-v0.1.3 maintenance plan"
    )
    assert readme_operator_docs.index("v0.1.4 maintenance release record") < readme_operator_docs.index(
        "v0.1.3 maintenance release record"
    )
    assert "next-round-plan-post-v0.1.4.md" in current_section
    assert "release-v0.1.4.md" in current_section
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
    assert "next-round-plan-post-v0.1.4.md" in checklist
    assert "next-round-plan-post-v0.1.4.md" in evidence
    assert "release-v0.1.4.md" in checklist
    assert "release-v0.1.4.md" in evidence
    assert "post-v0.1.3 plan is closed historical evidence" in checklist
    assert "post-v0.1.3 cursor is closed historical evidence" in evidence
    assert "Before a compatible `v0.1.1` maintenance release" not in matrix
    assert "For compatible maintenance releases after `v0.1.4`" in matrix
    assert "published\n`v0.1.4` maintenance release record" in matrix
    assert "any later maintenance round" in matrix
    assert "current\n`v0.1.3` readiness round" not in matrix


def test_post_v014_plan_is_active_without_expanding_scope():
    plan = (ROOT / "docs" / "next-round-plan-post-v0.1.4.md").read_text(
        encoding="utf-8"
    )

    for expected in (
        "Current stage: P2 - Manual Smoke Freshness Decision.",
        "Stage status: C - P2 complete; ready to enter P3 on the next turn.",
        "Windows Harness run `25432718007` passed on that SHA",
        "`v0.1.4` is published at\nhttps://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.4",
        "post-publication\nreconciliation `main` commit is",
        "small compatible maintenance pass toward `v0.1.5`",
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


def test_release_evidence_freshness_guard_labels_inherited_manual_smoke():
    checklist = (ROOT / "docs" / "release-checklist.md").read_text(encoding="utf-8")
    evidence = (ROOT / "docs" / "release-evidence.md").read_text(encoding="utf-8")
    plan = (ROOT / "docs" / "next-round-plan-post-v0.1.4.md").read_text(
        encoding="utf-8"
    )

    for expected in (
        "## Evidence Freshness",
        "stable baseline is `v0.1.4`",
        "`v0.1.4` is the latest published release",
        "active post-v0.1.4 execution cursor must be followed",
        "manual UIA smoke inherited from an earlier release is labeled as inherited or",
        "inherited `v0.1.0` manual",
        "P2 has\n  explicitly accepted inherited `v0.1.0` manual smoke",
        "capture-surface behavior changes",
        "no observed-content artifact is committed to refresh evidence",
        "deterministic harness smoke changes require fresh deterministic gate",
    ):
        assert expected in checklist

    for expected in (
        "Release evidence must name which facts are current",
        "`v0.1.4` is the stable baseline",
        "`v0.1.4` is the latest published release",
        "active post-v0.1.4",
        "manual UIA smoke evidence inherited from `v0.1.0`",
        "must be labeled as inherited or stale",
        "must not present inherited manual smoke as freshly run",
        "P2 has\n  explicitly accepted inherited `v0.1.0` manual smoke",
        "capture-surface behavior changes",
        "never observed content",
        "deterministic harness smoke changes require fresh deterministic gate",
    ):
        assert expected in evidence

    assert "manual smoke freshness before any release" in plan


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
        "Stable release baseline | `v0.1.4`",
        "Latest maintenance plan | [Post-v0.1.4 maintenance plan]",
        "Published release record | [v0.1.4 maintenance release record]",
        "Latest published release record | [v0.1.4 maintenance release record]",
        "Latest full manual UIA smoke source | [v0.1.0 final release readiness record]",
        "Last freshness decision | For the post-v0.1.4 compatible maintenance path toward",
        "inherited `v0.1.0` Notepad, Edge, VS Code metadata",
        "accepted by post-v0.1.4 P2 for the compatible `v0.1.5` path",
        "accepted by post-v0.1.4 P2 as diagnostic context",
        "is explicitly accepted by the P2 decision only when the remaining release",
        "Fresh manual smoke is required if any helper, watcher, smoke script",
        "Do not paste observed text",
        "Do not save or commit raw watcher JSONL",
        "not current evidence unless",
        "Deterministic harness smoke changes require fresh deterministic gate",
    ):
        assert expected in ledger

    assert "[Manual smoke evidence ledger](manual-smoke-evidence-ledger.md)" in quickstart
    assert "[Manual smoke evidence ledger](docs/manual-smoke-evidence-ledger.md)" in readme
    assert "Manual smoke evidence ledger" in checklist
    assert "Manual smoke evidence ledger" in evidence
    assert "Current stage: P2 - Manual Smoke Freshness Decision." in plan
    assert "Stage status: C - P2 complete; ready to enter P3 on the next turn." in plan
    assert "Windows Harness run `25432718007` passed on that SHA" in plan
    assert "Stage P0 - Post-v0.1.4 Baseline Cursor" in plan
    assert "Stage P1 entry-hygiene validation:" in plan
    assert "Stage P2 manual-smoke freshness validation:" in plan
    assert "Stage P0 local validation:" in plan
    assert "Stage P2 - Manual Smoke Freshness Decision" in plan
    assert "observed-content\n  artifacts remain uncommitted" in plan
