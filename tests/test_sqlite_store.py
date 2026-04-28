import sqlite3
from pathlib import Path

import pytest

from winchronicle.capture import capture_once_from_fixture
from winchronicle.paths import state_paths
from winchronicle.privacy import TRUST
from winchronicle import storage
from winchronicle.storage import capture_fingerprint_exists, search_captures


ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize(
    ("fixture_name", "query", "expected_app"),
    [
        ("terminal_error.json", "AssertionError", "Windows Terminal"),
        ("vscode_editor.json", "written_json", "Visual Studio Code"),
        ("edge_browser.json", "OpenChronicle", "Microsoft Edge"),
    ],
)
def test_search_finds_terminal_editor_and_browser_fixtures(
    tmp_path, monkeypatch, fixture_name, query, expected_app
):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    capture_once_from_fixture(ROOT / "harness" / "fixtures" / "uia" / fixture_name)

    results = search_captures(query, home)

    assert len(results) == 1
    assert set(results[0]) == {"timestamp", "app_name", "title", "snippet", "path", "trust"}
    assert results[0]["app_name"] == expected_app
    assert results[0]["trust"] == TRUST
    assert query.lower() in results[0]["snippet"].lower()


def test_capture_index_creates_fts_table(tmp_path, monkeypatch):
    if not _sqlite_supports_fts5():
        pytest.skip("SQLite FTS5 is unavailable in this Python build.")

    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    capture_once_from_fixture(ROOT / "harness" / "fixtures" / "uia" / "terminal_error.json")

    with sqlite3.connect(state_paths(home)["db"]) as conn:
        fts_row = conn.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'captures_fts'"
        ).fetchone()
        capture_count = conn.execute("SELECT COUNT(*) FROM captures").fetchone()[0]
        fts_count = conn.execute("SELECT COUNT(*) FROM captures_fts").fetchone()[0]

    assert fts_row == ("captures_fts",)
    assert capture_count == 1
    assert fts_count == 1


def test_capture_index_persists_content_fingerprint(tmp_path, monkeypatch):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    result = capture_once_from_fixture(
        ROOT / "harness" / "fixtures" / "uia" / "terminal_error.json"
    )
    fingerprint = result.capture["content_fingerprint"]

    with sqlite3.connect(state_paths(home)["db"]) as conn:
        row = conn.execute(
            """
            SELECT content_fingerprint
            FROM captures
            WHERE path = ?
            """,
            (str(result.path),),
        ).fetchone()

    assert row == (fingerprint,)
    assert capture_fingerprint_exists(fingerprint, home) is True


def test_search_falls_back_when_fts5_is_unavailable(tmp_path, monkeypatch):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    monkeypatch.setattr(
        storage,
        "FTS_SCHEMA_SQL",
        """
        CREATE VIRTUAL TABLE IF NOT EXISTS captures_fts USING missing_fts5(
            path,
            visible_text
        );
        """,
    )

    capture_once_from_fixture(ROOT / "harness" / "fixtures" / "uia" / "terminal_error.json")

    results = search_captures("AssertionError", home)

    with sqlite3.connect(state_paths(home)["db"]) as conn:
        captures_row = conn.execute(
            "SELECT COUNT(*) FROM captures WHERE visible_text LIKE '%AssertionError%'"
        ).fetchone()
        fts_row = conn.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'captures_fts'"
        ).fetchone()

    assert len(results) == 1
    assert results[0]["app_name"] == "Windows Terminal"
    assert captures_row == (1,)
    assert fts_row is None


def test_blank_search_returns_no_results(tmp_path, monkeypatch):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    capture_once_from_fixture(ROOT / "harness" / "fixtures" / "uia" / "terminal_error.json")

    assert search_captures("", home) == []


def _sqlite_supports_fts5() -> bool:
    with sqlite3.connect(":memory:") as conn:
        try:
            conn.execute("CREATE VIRTUAL TABLE probe USING fts5(value)")
        except sqlite3.OperationalError:
            return False

    return True
