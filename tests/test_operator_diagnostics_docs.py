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
    quickstart = (ROOT / "docs" / "operator-quickstart.md").read_text(encoding="utf-8")
    checklist = (ROOT / "docs" / "release-checklist.md").read_text(encoding="utf-8")
    evidence = (ROOT / "docs" / "release-evidence.md").read_text(encoding="utf-8")
    matrix = (ROOT / "docs" / "uia-helper-quality-matrix.md").read_text(encoding="utf-8")

    current_section = quickstart.split("## Current Maintenance Docs", 1)[1].split(
        "## Historical Release Records", 1
    )[0]
    historical_section = quickstart.split("## Historical Release Records", 1)[1]

    assert "next-round-plan-post-v0.1.1.md" in current_section
    assert "release-v0.1.1.md" in current_section
    assert "next-round-plan-v0.1.0-final.md" not in current_section
    assert "next-round-plan-v0.1.0-final.md" in historical_section
    assert "next-round-plan-post-v0.1.1.md" in checklist
    assert "next-round-plan-post-v0.1.1.md" in evidence
    assert "Before a compatible `v0.1.1` maintenance release" not in matrix
    assert "`v0.1.2` readiness round" in matrix
