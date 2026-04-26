import json
import sqlite3
from pathlib import Path

import pytest

from winchronicle.capture import capture_once_from_fixture
from winchronicle.cli import main
from winchronicle.memory import generate_memory_entries
from winchronicle.paths import state_paths
from winchronicle.schema import validate_memory_entry
from winchronicle.storage import search_memory_entries


ROOT = Path(__file__).resolve().parents[1]


def test_generate_memory_creates_markdown_and_searchable_entry(tmp_path, monkeypatch):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    for fixture_name in ("terminal_error.json", "vscode_editor.json", "edge_browser.json"):
        capture_once_from_fixture(ROOT / "harness" / "fixtures" / "uia" / fixture_name, home)

    results = generate_memory_entries(home)

    assert len(results) == 1
    result = results[0]
    validate_memory_entry(result.entry)
    assert result.path.name == "event-2026-04-25.md"
    assert result.capture_count == 3

    markdown = result.path.read_text(encoding="utf-8")
    assert "trust: untrusted_observed_content" in markdown
    assert "## Source Captures" in markdown
    assert "Windows Terminal" in markdown
    assert "Visual Studio Code" in markdown
    assert "Microsoft Edge" in markdown
    assert "CorrectHorseBatteryStaple!" not in markdown

    for query, expected_title in (
        ("AssertionError", "WinChronicle events for 2026-04-25"),
        ("written_json", "WinChronicle events for 2026-04-25"),
        ("OpenChronicle", "WinChronicle events for 2026-04-25"),
    ):
        matches = search_memory_entries(query, home)
        assert len(matches) == 1
        assert matches[0]["title"] == expected_title
        assert query.lower() in matches[0]["snippet"].lower()


def test_memory_entries_fts_table_created_when_available(tmp_path, monkeypatch):
    if not _sqlite_supports_fts5():
        pytest.skip("SQLite FTS5 is unavailable in this Python build.")

    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    capture_once_from_fixture(ROOT / "harness" / "fixtures" / "uia" / "terminal_error.json", home)

    generate_memory_entries(home)

    with sqlite3.connect(state_paths(home)["db"]) as conn:
        entry_row = conn.execute("SELECT COUNT(*) FROM entries").fetchone()
        fts_row = conn.execute("SELECT COUNT(*) FROM entries_fts").fetchone()

    assert entry_row == (1,)
    assert fts_row == (1,)


def test_memory_generation_does_not_write_unredacted_secret_canaries(tmp_path, monkeypatch):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    capture_once_from_fixture(ROOT / "harness" / "fixtures" / "privacy" / "secrets_visible_text.json", home)

    result = generate_memory_entries(home)[0]
    markdown = result.path.read_text(encoding="utf-8")

    assert "sk-winchronicle-test-canary" not in markdown
    assert "ghp_winchroniclecanary" not in markdown
    assert "xoxb-winchronicle-canary-token" not in markdown
    assert "-----BEGIN PRIVATE KEY-----" not in markdown
    assert "[REDACTED:" in markdown


def test_generate_memory_and_search_memory_cli(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("WINCHRONICLE_HOME", str(tmp_path / "state"))
    assert main(
        [
            "capture-once",
            "--fixture",
            str(ROOT / "harness" / "fixtures" / "uia" / "edge_browser.json"),
        ]
    ) == 0
    capsys.readouterr()

    assert main(["generate-memory", "--date", "2026-04-25"]) == 0
    generated = json.loads(capsys.readouterr().out)
    assert len(generated) == 1
    assert generated[0]["capture_count"] == 1

    assert main(["search-memory", "OpenChronicle"]) == 0
    matches = json.loads(capsys.readouterr().out)
    assert len(matches) == 1
    assert matches[0]["entry_type"] == "event"
    assert matches[0]["title"] == "WinChronicle events for 2026-04-25"


def _sqlite_supports_fts5() -> bool:
    with sqlite3.connect(":memory:") as conn:
        try:
            conn.execute("CREATE VIRTUAL TABLE probe USING fts5(value)")
        except sqlite3.OperationalError:
            return False

    return True
