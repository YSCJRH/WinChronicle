import json
import sqlite3
from pathlib import Path

import pytest

from winchronicle.capture import capture_once_from_fixture
from winchronicle.cli import main
from winchronicle.memory import generate_memory_entries
from winchronicle.paths import state_paths
from winchronicle.privacy import TRUST
from winchronicle.schema import validate_memory_entry
from winchronicle.storage import search_memory_entries


ROOT = Path(__file__).resolve().parents[1]


def test_generate_memory_creates_markdown_and_searchable_entry(tmp_path, monkeypatch):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    for fixture_name in ("terminal_error.json", "vscode_editor.json", "edge_browser.json"):
        capture_once_from_fixture(ROOT / "harness" / "fixtures" / "uia" / fixture_name, home)

    results = generate_memory_entries(home)

    assert {result.path.name for result in results} == {
        "event-2026-04-25.md",
        "project-openchronicle.md",
        "project-winchronicle.md",
        "tool-microsoft-edge.md",
        "tool-visual-studio-code.md",
        "tool-windows-terminal.md",
    }
    for result in results:
        validate_memory_entry(result.entry)

    by_path = {result.path.name: result for result in results}
    assert by_path["event-2026-04-25.md"].capture_count == 3
    assert by_path["project-winchronicle.md"].capture_count == 2
    assert by_path["project-openchronicle.md"].capture_count == 1
    assert by_path["tool-visual-studio-code.md"].entry["entry_type"] == "tool"
    assert by_path["project-winchronicle.md"].entry["entry_type"] == "project"

    markdown = by_path["event-2026-04-25.md"].path.read_text(encoding="utf-8")
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
        assert matches
        assert expected_title in {match["title"] for match in matches}
        assert all(match["trust"] == TRUST for match in matches)
        assert any(query.lower() in match["snippet"].lower() for match in matches)


def test_event_memory_markdown_matches_golden_fixture(tmp_path, monkeypatch):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    for fixture_name in ("terminal_error.json", "vscode_editor.json", "edge_browser.json"):
        capture_once_from_fixture(ROOT / "harness" / "fixtures" / "uia" / fixture_name, home)

    results = generate_memory_entries(home, date="2026-04-25")
    event = next(result for result in results if result.path.name == "event-2026-04-25.md")
    actual = _normalize_memory_markdown(event.path.read_text(encoding="utf-8"), home)
    expected = (ROOT / "harness" / "golden" / "memory_event_2026_04_25.expected.md").read_text(
        encoding="utf-8"
    )

    assert actual == expected


def test_generate_memory_is_idempotent_for_files_and_index(tmp_path, monkeypatch):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    for fixture_name in ("terminal_error.json", "vscode_editor.json", "edge_browser.json"):
        capture_once_from_fixture(ROOT / "harness" / "fixtures" / "uia" / fixture_name, home)

    first = generate_memory_entries(home, date="2026-04-25")
    first_bodies = {result.path.name: result.path.read_text(encoding="utf-8") for result in first}
    second = generate_memory_entries(home, date="2026-04-25")
    second_bodies = {result.path.name: result.path.read_text(encoding="utf-8") for result in second}

    with sqlite3.connect(state_paths(home)["db"]) as conn:
        entry_row = conn.execute("SELECT COUNT(*) FROM entries").fetchone()

    assert [result.path.name for result in first] == [result.path.name for result in second]
    assert first_bodies == second_bodies
    assert entry_row == (6,)


def test_memory_entries_fts_table_created_when_available(tmp_path, monkeypatch):
    if not _sqlite_supports_fts5():
        pytest.skip("SQLite FTS5 is unavailable in this Python build.")

    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    capture_once_from_fixture(ROOT / "harness" / "fixtures" / "uia" / "terminal_error.json", home)

    results = generate_memory_entries(home)

    with sqlite3.connect(state_paths(home)["db"]) as conn:
        entry_row = conn.execute("SELECT COUNT(*) FROM entries").fetchone()
        fts_row = conn.execute("SELECT COUNT(*) FROM entries_fts").fetchone()

    assert len(results) == 3
    assert entry_row == (3,)
    assert fts_row == (3,)


def test_memory_generation_does_not_write_unredacted_secret_canaries(tmp_path, monkeypatch):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    capture_once_from_fixture(ROOT / "harness" / "fixtures" / "privacy" / "secrets_visible_text.json", home)

    results = generate_memory_entries(home)

    for result in results:
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
    assert {entry["entry_type"] for entry in generated} == {"event", "project", "tool"}
    assert all(entry["capture_count"] == 1 for entry in generated)

    assert main(["search-memory", "OpenChronicle"]) == 0
    matches = json.loads(capsys.readouterr().out)
    assert matches
    assert {"event", "project", "tool"} <= {match["entry_type"] for match in matches}
    assert "WinChronicle events for 2026-04-25" in {match["title"] for match in matches}
    assert all(match["trust"] == TRUST for match in matches)


def _sqlite_supports_fts5() -> bool:
    with sqlite3.connect(":memory:") as conn:
        try:
            conn.execute("CREATE VIRTUAL TABLE probe USING fts5(value)")
        except sqlite3.OperationalError:
            return False

    return True


def _normalize_memory_markdown(markdown: str, home: Path) -> str:
    return markdown.replace(str(home), "<STATE>").replace("\\", "/")
