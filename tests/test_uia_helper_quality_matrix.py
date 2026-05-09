from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "docs" / "uia-helper-quality-matrix.md"
WINDOWS_SMOKE = ROOT / "docs" / "windows-uia-smoke.md"


def test_uia_helper_quality_matrix_has_required_columns_and_rows():
    text = MATRIX.read_text(encoding="utf-8")
    rows = _matrix_rows()

    expected_header = (
        "| Gate type | App / scope | Expected signal | Current result | "
        "Artifact policy | Privacy risk | Blocking status |"
    )
    assert expected_header in text

    for row_label in (
        "Notepad fixture",
        "Password fixture",
        "Budget/stale traversal fixture",
        "Fake helper wrapper",
        "Targeted helper path",
        "Notepad",
        "Microsoft Edge",
        "VS Code metadata",
        "VS Code strict Monaco marker",
        "Operator-selected foreground app",
        "Any additional app",
    ):
        assert row_label in rows


def test_uia_helper_quality_matrix_preserves_gate_statuses():
    rows = _matrix_rows()

    expected_statuses = {
        "Notepad fixture": "Hard automated gate.",
        "Password fixture": "Hard automated privacy gate.",
        "Budget/stale traversal fixture": "Hard automated contract gate.",
        "Fake helper wrapper": "Hard automated gate.",
        "Targeted helper path": "Hard boundary gate.",
        "Notepad": "Hard manual release gate.",
        "Microsoft Edge": "Hard manual release gate.",
        "VS Code metadata": "Conditional hard manual release gate when `code.cmd` is available.",
        "VS Code strict Monaco marker": "Diagnostic, non-blocking for v0.1.",
        "Operator-selected foreground app": "Diagnostic/manual confidence gate.",
        "Any additional app": "Diagnostic by default unless a future scorecard promotes it.",
    }
    for app_or_scope, blocking_status in expected_statuses.items():
        assert rows[app_or_scope]["Blocking status"] == blocking_status


def test_uia_helper_quality_matrix_preserves_privacy_boundary():
    text = MATRIX.read_text(encoding="utf-8")

    for boundary in (
        "`--harness`",
        "WINCHRONICLE_HARNESS=1",
        "MCP remains read-only",
        "record only pass/fail status",
        "artifact paths",
        "Do not use this matrix to justify screenshots, OCR, audio recording",
        "product targeted capture",
    ):
        assert boundary in text


def test_uia_helper_quality_matrix_uses_latest_manual_smoke_evidence():
    text = MATRIX.read_text(encoding="utf-8")
    rows = _matrix_rows()

    assert "post-v0.1 helper-quality contract" in text
    assert "For compatible maintenance releases after `v0.1.9`" in text
    assert "Historical\nmaintenance records from `v0.1.4` onward" in text
    assert "current\n`v0.1.3` readiness round" not in text
    assert "Latest full manual `v0.1.17` release: pass" in rows["Notepad"][
        "Current result"
    ]
    assert "Latest full manual `v0.1.17` release: pass" in rows["Microsoft Edge"][
        "Current result"
    ]
    assert "Latest full manual `v0.1.17` release: pass with diagnostic warning" in rows[
        "VS Code metadata"
    ]["Current result"]
    assert "Latest full manual `v0.1.17` release: diagnostic failure" in rows[
        "VS Code strict Monaco marker"
    ]["Current result"]
    assert "docs/release-v0.1.17.md" in text
    assert "docs/manual-smoke-evidence-ledger.md" in text
    assert "Frontmost-only diagnostic last recorded `v0.1.0` final" in rows[
        "Operator-selected foreground app"
    ]["Current result"]
    assert "SKIPPED: helper returned no capture" in rows["Operator-selected foreground app"][
        "Current result"
    ]
    assert "`v0.1.0-rc.0`" not in text
    assert "Do not promote a new application to a hard gate from this matrix alone." in text


def test_windows_uia_smoke_points_to_latest_manual_smoke_source():
    text = WINDOWS_SMOKE.read_text(encoding="utf-8")

    assert "For the latest full manual UIA smoke source" in text
    assert "[v0.1.17 maintenance release record](release-v0.1.17.md)" in text
    assert "last recorded final-release smoke evidence" not in text
    assert "[v0.1.0 final release readiness record]" not in text


def _matrix_rows() -> dict[str, dict[str, str]]:
    lines = MATRIX.read_text(encoding="utf-8").splitlines()
    table_lines = [line for line in lines if line.startswith("|")]
    headers = _cells(table_lines[0])
    rows: dict[str, dict[str, str]] = {}
    for line in table_lines[2:]:
        values = _cells(line)
        row = dict(zip(headers, values))
        rows[row["App / scope"]] = row
    return rows


def _cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]
