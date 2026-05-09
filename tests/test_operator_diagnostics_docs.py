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
    assert "[Blueprint gap audit after v0.1.12](blueprint-gap-audit-post-v0.1.12.md)" in quickstart
    assert (
        "[Compatibility guardrail sweep after v0.1.12](compatibility-guardrail-sweep-post-v0.1.12.md)"
        in quickstart
    )
    assert "[Deterministic demo](deterministic-demo.md)" in quickstart
    assert "[Roadmap](roadmap.md)" in quickstart
    assert "[Contributing](../CONTRIBUTING.md)" in quickstart
    assert "[Post-v0.1.14 maintenance plan](next-round-plan-post-v0.1.14.md)" in quickstart
    assert (
        "[v0.1.15 maintenance release record](release-v0.1.15.md)"
        in quickstart
    )
    assert (
        "[Public metadata audit after v0.1.14](public-metadata-audit-post-v0.1.14.md)"
        in quickstart
    )
    assert (
        "[Helper and watcher diagnostics sweep after v0.1.14](helper-watcher-diagnostics-sweep-post-v0.1.14.md)"
        in quickstart
    )
    assert (
        "[MCP and memory contract sweep after v0.1.14](mcp-memory-contract-sweep-post-v0.1.14.md)"
        in quickstart
    )
    assert (
        "[Compatibility guardrail sweep after v0.1.14](compatibility-guardrail-sweep-post-v0.1.14.md)"
        in quickstart
    )
    assert "[Post-v0.1.13 maintenance plan](next-round-plan-post-v0.1.13.md)" in quickstart
    assert (
        "[Public metadata audit after v0.1.13](public-metadata-audit-post-v0.1.13.md)"
        in quickstart
    )
    assert (
        "[Helper and watcher diagnostics sweep after v0.1.13](helper-watcher-diagnostics-sweep-post-v0.1.13.md)"
        in quickstart
    )
    assert (
        "[MCP and memory contract sweep after v0.1.13](mcp-memory-contract-sweep-post-v0.1.13.md)"
        in quickstart
    )
    assert (
        "[Compatibility guardrail sweep after v0.1.13](compatibility-guardrail-sweep-post-v0.1.13.md)"
        in quickstart
    )
    assert "[v0.1.13 maintenance release record](release-v0.1.13.md)" in quickstart
    assert (
        "[v0.1.14 maintenance release record](release-v0.1.14.md)"
        in quickstart
    )
    assert "[Operator diagnostics](docs/operator-diagnostics.md)" in readme
    assert (
        "[Blueprint gap audit after v0.1.12](docs/blueprint-gap-audit-post-v0.1.12.md)"
        in readme
    )
    assert (
        "[Compatibility guardrail sweep after v0.1.12](docs/compatibility-guardrail-sweep-post-v0.1.12.md)"
        in readme
    )
    assert "[Deterministic demo](docs/deterministic-demo.md)" in readme
    assert "[Roadmap](docs/roadmap.md)" in readme
    assert "[Contributing](CONTRIBUTING.md)" in readme
    assert "[Post-v0.1.14 maintenance plan](docs/next-round-plan-post-v0.1.14.md)" in readme
    assert (
        "[v0.1.15 maintenance release record](docs/release-v0.1.15.md)"
        in readme
    )
    assert (
        "[Public metadata audit after v0.1.14](docs/public-metadata-audit-post-v0.1.14.md)"
        in readme
    )
    assert (
        "[Helper and watcher diagnostics sweep after v0.1.14](docs/helper-watcher-diagnostics-sweep-post-v0.1.14.md)"
        in readme
    )
    assert (
        "[MCP and memory contract sweep after v0.1.14](docs/mcp-memory-contract-sweep-post-v0.1.14.md)"
        in readme
    )
    assert (
        "[Compatibility guardrail sweep after v0.1.14](docs/compatibility-guardrail-sweep-post-v0.1.14.md)"
        in readme
    )
    assert "[Post-v0.1.13 maintenance plan](docs/next-round-plan-post-v0.1.13.md)" in readme
    assert (
        "[Public metadata audit after v0.1.13](docs/public-metadata-audit-post-v0.1.13.md)"
        in readme
    )
    assert (
        "[Helper and watcher diagnostics sweep after v0.1.13](docs/helper-watcher-diagnostics-sweep-post-v0.1.13.md)"
        in readme
    )
    assert (
        "[MCP and memory contract sweep after v0.1.13](docs/mcp-memory-contract-sweep-post-v0.1.13.md)"
        in readme
    )
    assert (
        "[Compatibility guardrail sweep after v0.1.13](docs/compatibility-guardrail-sweep-post-v0.1.13.md)"
        in readme
    )
    assert "[v0.1.13 maintenance release record](docs/release-v0.1.13.md)" in readme
    assert (
        "[v0.1.14 maintenance release record](docs/release-v0.1.14.md)"
        in readme
    )


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

    assert "active post-v0.1.14 maintenance plan" in readme_intro_normalized
    assert "latest published `v0.1.15` release record" in readme_intro_normalized
    assert "previous published `v0.1.14` release record" in readme_intro_normalized
    assert "completed post-v0.1.13 maintenance plan" in readme_intro_normalized
    assert "completed post-v0.1.12 maintenance plan" in readme_intro_normalized
    assert "latest published `v0.1.5` release" not in readme_intro
    assert "latest published `v0.1.3` release" not in readme_intro
    assert "v0.1.12 maintenance release record" in readme_operator_docs
    assert "v0.1.13 maintenance release record" in readme_operator_docs
    assert "v0.1.14 maintenance release record" in readme_operator_docs
    assert "v0.1.15 maintenance release record" in readme_operator_docs
    assert "Post-v0.1.14 maintenance plan" in readme_operator_docs
    assert "Public metadata audit after v0.1.14" in readme_operator_docs
    assert "Helper and watcher diagnostics sweep after v0.1.14" in readme_operator_docs
    assert "MCP and memory contract sweep after v0.1.14" in readme_operator_docs
    assert "Compatibility guardrail sweep after v0.1.14" in readme_operator_docs
    assert "Post-v0.1.13 maintenance plan" in readme_operator_docs
    assert "Public metadata audit after v0.1.13" in readme_operator_docs
    assert "Helper and watcher diagnostics sweep after v0.1.13" in readme_operator_docs
    assert "MCP and memory contract sweep after v0.1.13" in readme_operator_docs
    assert "Compatibility guardrail sweep after v0.1.13" in readme_operator_docs
    assert "Post-v0.1.12 maintenance plan" in readme_operator_docs
    assert "Post-v0.1.11 maintenance plan" in readme_operator_docs
    assert "v0.1.11 maintenance release record" in readme_operator_docs
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
    assert readme_operator_docs.index("Public metadata audit after v0.1.13") < readme_operator_docs.index(
        "Helper and watcher diagnostics sweep after v0.1.13"
    )
    assert readme_operator_docs.index("Helper and watcher diagnostics sweep after v0.1.13") < readme_operator_docs.index(
        "MCP and memory contract sweep after v0.1.13"
    )
    assert readme_operator_docs.index("MCP and memory contract sweep after v0.1.13") < readme_operator_docs.index(
        "Compatibility guardrail sweep after v0.1.13"
    )
    assert readme_operator_docs.index("Compatibility guardrail sweep after v0.1.13") < readme_operator_docs.index(
        "Blueprint gap audit after v0.1.12"
    )
    assert readme_operator_docs.index("Post-v0.1.14 maintenance plan") < readme_operator_docs.index(
        "v0.1.15 maintenance release record"
    )
    assert readme_operator_docs.index("v0.1.15 maintenance release record") < readme_operator_docs.index(
        "v0.1.14 maintenance release record"
    )
    assert readme_operator_docs.index("v0.1.14 maintenance release record") < readme_operator_docs.index(
        "Public metadata audit after v0.1.14"
    )
    assert readme_operator_docs.index("Public metadata audit after v0.1.14") < readme_operator_docs.index(
        "Helper and watcher diagnostics sweep after v0.1.14"
    )
    assert readme_operator_docs.index("Helper and watcher diagnostics sweep after v0.1.14") < readme_operator_docs.index(
        "MCP and memory contract sweep after v0.1.14"
    )
    assert readme_operator_docs.index("MCP and memory contract sweep after v0.1.14") < readme_operator_docs.index(
        "Compatibility guardrail sweep after v0.1.14"
    )
    assert readme_operator_docs.index("Compatibility guardrail sweep after v0.1.14") < readme_operator_docs.index(
        "Public metadata audit after v0.1.13"
    )
    assert readme_operator_docs.index("Public metadata audit after v0.1.13") < readme_operator_docs.index(
        "Post-v0.1.13 maintenance plan"
    )
    assert readme_operator_docs.index("Post-v0.1.13 maintenance plan") < readme_operator_docs.index(
        "v0.1.13 maintenance release record"
    )
    assert readme_operator_docs.index("v0.1.13 maintenance release record") < readme_operator_docs.index(
        "v0.1.12 maintenance release record"
    )
    assert readme_operator_docs.index("v0.1.12 maintenance release record") < readme_operator_docs.index(
        "Post-v0.1.12 maintenance plan"
    )
    assert readme_operator_docs.index("Post-v0.1.12 maintenance plan") < readme_operator_docs.index(
        "Post-v0.1.11 maintenance plan"
    )
    assert readme_operator_docs.index("Post-v0.1.11 maintenance plan") < readme_operator_docs.index(
        "v0.1.11 maintenance release record"
    )
    assert readme_operator_docs.index("v0.1.11 maintenance release record") < readme_operator_docs.index(
        "v0.1.10 maintenance release record"
    )
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
    assert "next-round-plan-post-v0.1.14.md" in current_section
    assert "public-metadata-audit-post-v0.1.14.md" in current_section
    assert "helper-watcher-diagnostics-sweep-post-v0.1.14.md" in current_section
    assert "mcp-memory-contract-sweep-post-v0.1.14.md" in current_section
    assert "compatibility-guardrail-sweep-post-v0.1.14.md" in current_section
    assert "public-metadata-audit-post-v0.1.13.md" in current_section
    assert "helper-watcher-diagnostics-sweep-post-v0.1.13.md" in current_section
    assert "mcp-memory-contract-sweep-post-v0.1.13.md" in current_section
    assert "compatibility-guardrail-sweep-post-v0.1.13.md" in current_section
    assert "release-v0.1.15.md" in current_section
    assert "release-v0.1.14.md" in current_section
    assert "release-v0.1.13.md" in current_section
    assert "release-v0.1.12.md" in current_section
    assert "next-round-plan-post-v0.1.13.md" not in current_section
    assert "next-round-plan-post-v0.1.13.md" in historical_section
    assert "next-round-plan-post-v0.1.12.md" not in current_section
    assert "next-round-plan-post-v0.1.12.md" in historical_section
    assert "next-round-plan-post-v0.1.11.md" not in current_section
    assert "release-v0.1.11.md" not in current_section
    assert "next-round-plan-post-v0.1.11.md" in historical_section
    assert "release-v0.1.11.md" in historical_section
    assert "release-v0.1.10.md" not in current_section
    assert "next-round-plan-post-v0.1.10.md" not in current_section
    assert "release-v0.1.10.md" in historical_section
    assert "next-round-plan-post-v0.1.10.md" in historical_section
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
    assert "release-v0.1.13.md" not in checklist
    assert "release-v0.1.13.md" not in evidence
    assert "release-v0.1.14.md" in checklist
    assert "release-v0.1.14.md" in evidence
    assert "release-v0.1.15.md" in checklist
    assert "release-v0.1.15.md" in evidence
    assert "next-round-plan-post-v0.1.14.md" in checklist
    assert "next-round-plan-post-v0.1.14.md" in evidence
    assert "next-round-plan-post-v0.1.13.md" in checklist
    assert "next-round-plan-post-v0.1.13.md" in evidence
    assert "v0.1.15` is the latest published release" in checklist
    assert "v0.1.15` is the latest published release" in evidence
    assert "public metadata and evidence-freshness checks" in checklist
    assert "public metadata evidence should record" in evidence
    assert "next-round-plan-post-v0.1.12.md" in checklist
    assert "next-round-plan-post-v0.1.12.md" in evidence
    assert "release-v0.1.10.md" not in checklist
    assert "release-v0.1.10.md" not in evidence
    assert "next-round-plan-post-v0.1.10.md" not in checklist
    assert "next-round-plan-post-v0.1.10.md" not in evidence
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
    assert "post-v0.1.10 plan is completed historical evidence" in checklist
    assert "post-v0.1.10 cursor is completed historical evidence" in evidence
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
        "without\nauthorizing new capture surfaces",
        "Fixture and privacy baseline",
        "UIA helper hardening",
        "Watcher preview",
        "Read-only MCP",
        "Durable memory",
        "Docs and deterministic demo",
        "Phase 6 privacy enrichment",
        "Do not add product `--hwnd`, `--pid`, or title-targeted capture",
        "Do not add daemon/service install, default background capture, or polling capture loops",
        "Do not add LLM reducer/classifier calls or network upload",
        "Do not implement screenshot capture or OCR in v0.1 maintenance",
        "Do not commit generated state or memory artifacts",
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


def test_release_evidence_freshness_guard_labels_inherited_manual_smoke():
    checklist = (ROOT / "docs" / "release-checklist.md").read_text(encoding="utf-8")
    evidence = (ROOT / "docs" / "release-evidence.md").read_text(encoding="utf-8")
    plan = (ROOT / "docs" / "next-round-plan-post-v0.1.4.md").read_text(
        encoding="utf-8"
    )

    for expected in (
        "## Evidence Freshness",
        "stable baseline is `v0.1.15`",
        "`v0.1.15` is the latest published release",
        "completed post-v0.1.14 execution cursor records `v0.1.15` publication",
        "PR #132, PR #133, post-merge Windows Harness run `25589165182`",
        "completed post-v0.1.13 execution cursor records `v0.1.14` publication",
        "PR #125, and post-merge Windows Harness run `25585147402`",
        "post-v0.1.14 execution cursor is active and records post-publication",
        "reconciliation PR #126 plus post-merge Windows Harness run `25585707220`",
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
        "`v0.1.15` is the stable baseline",
        "`v0.1.15` is the latest published release",
        "completed post-v0.1.14 execution cursor records `v0.1.15` publication",
        "PR #132, PR #133, post-merge Windows Harness run `25589165182`",
        "completed post-v0.1.13 execution cursor records `v0.1.14` publication",
        "PR #125, and post-merge Windows Harness run `25585147402`",
        "post-v0.1.14 execution cursor is active and records post-publication",
        "reconciliation PR #126 plus post-merge Windows Harness run `25585707220`",
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
        "Stable release baseline | `v0.1.15`",
        "Current maintenance plan | [Post-v0.1.14 maintenance plan]",
        "Latest completed maintenance plan | [Post-v0.1.13 maintenance plan]",
        "Current release-readiness record | None; `v0.1.15` is published",
        "Published release record | [v0.1.15 maintenance release record]",
        "Latest published release record | [v0.1.15 maintenance release record]",
        "Latest full manual UIA smoke source | [v0.1.0 final release readiness record]",
        "Last freshness decision | For the post-v0.1.14 compatible maintenance path that published `v0.1.15`",
        "inherited `v0.1.0` Notepad, Edge, VS Code metadata",
        "accepted by AC5 because AC0-AC5 did not change helper behavior",
        "explicitly accepted by S4 for the compatible `v0.1.6` path",
        "explicitly accepted by T4 for the compatible `v0.1.7` path",
        "explicitly accepted by U4 for the compatible `v0.1.8` path",
        "explicitly accepted by W4 for the compatible `v0.1.9` path",
        "accepted by X1 as inherited/stale evidence for the post-v0.1.9 path",
        "historically accepted for `v0.1.5` as diagnostic context",
        "Next freshness decision | The next maintenance plan after `v0.1.15` publication must decide",
        "whether inherited manual evidence remains acceptable",
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
