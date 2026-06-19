import json
import sqlite3
from pathlib import Path

import pytest

from winchronicle.capture import capture_once_from_fixture
from winchronicle.cli import main
from winchronicle.memory import generate_memory_entries
from winchronicle.mcp.server import search_memory_tool
from winchronicle.paths import state_paths
from winchronicle.privacy import TRUST, TRUST_BOUNDARY_INSTRUCTION
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


def test_memory_manifest_matches_golden_fixture(tmp_path, monkeypatch):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    for fixture_name in ("terminal_error.json", "vscode_editor.json", "edge_browser.json"):
        capture_once_from_fixture(ROOT / "harness" / "fixtures" / "uia" / fixture_name, home)

    results = generate_memory_entries(home, date="2026-04-25")
    actual = _normalize_memory_manifest([result.to_json() for result in results], home)
    expected = json.loads(
        (ROOT / "harness" / "golden" / "memory_manifest_2026_04_25.expected.json").read_text(
            encoding="utf-8"
        )
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


def test_generate_memory_preserves_existing_entry_when_atomic_replace_fails(
    tmp_path, monkeypatch
):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    for fixture_name in ("terminal_error.json", "vscode_editor.json", "edge_browser.json"):
        capture_once_from_fixture(ROOT / "harness" / "fixtures" / "uia" / fixture_name, home)

    generate_memory_entries(home, date="2026-04-25")
    before_matches = search_memory_entries("harness README", home)
    with sqlite3.connect(state_paths(home)["db"]) as conn:
        before_rows = conn.execute(
            """
            SELECT path, entry_type, title, body, content_fingerprint
            FROM entries
            ORDER BY path
            """
        ).fetchall()

    event_path = home / "memory" / "event-2026-04-25.md"
    previous_body = "# Previous memory entry\n\ntrust: untrusted_observed_content\n"
    event_path.write_text(previous_body, encoding="utf-8")
    capture_once_from_fixture(ROOT / "harness" / "fixtures" / "uia" / "notepad_basic.json", home)
    original_replace = Path.replace

    def fail_event_memory_replace(self: Path, target_path: Path) -> Path:
        if target_path == event_path:
            raise OSError("simulated memory replace failure")
        return original_replace(self, target_path)

    monkeypatch.setattr(Path, "replace", fail_event_memory_replace)

    try:
        generate_memory_entries(home, date="2026-04-25")
    except OSError:
        pass
    else:
        raise AssertionError("expected simulated memory replace failure")

    assert event_path.read_text(encoding="utf-8") == previous_body
    assert list((home / "memory").glob("*.tmp")) == []
    with sqlite3.connect(state_paths(home)["db"]) as conn:
        after_rows = conn.execute(
            """
            SELECT path, entry_type, title, body, content_fingerprint
            FROM entries
            ORDER BY path
            """
        ).fetchall()

    assert after_rows == before_rows
    assert search_memory_entries("harness README", home) == before_matches


def test_generate_memory_restores_existing_entry_when_indexing_fails(
    tmp_path, monkeypatch
):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    for fixture_name in ("terminal_error.json", "vscode_editor.json", "edge_browser.json"):
        capture_once_from_fixture(ROOT / "harness" / "fixtures" / "uia" / fixture_name, home)

    generate_memory_entries(home, date="2026-04-25")
    event_path = home / "memory" / "event-2026-04-25.md"
    before_body = event_path.read_text(encoding="utf-8")
    before_matches = search_memory_entries("harness README", home)
    with sqlite3.connect(state_paths(home)["db"]) as conn:
        before_rows = conn.execute(
            """
            SELECT path, entry_type, title, body, content_fingerprint
            FROM entries
            ORDER BY path
            """
        ).fetchall()

    capture_once_from_fixture(ROOT / "harness" / "fixtures" / "uia" / "notepad_basic.json", home)

    def fail_event_index(_entry, entry_path: Path, *_args, **_kwargs) -> None:
        if entry_path == event_path:
            raise RuntimeError("simulated memory index failure")

    monkeypatch.setattr("winchronicle.memory.index_memory_entry", fail_event_index)

    try:
        generate_memory_entries(home, date="2026-04-25")
    except RuntimeError:
        pass
    else:
        raise AssertionError("expected simulated memory index failure")

    assert event_path.read_text(encoding="utf-8") == before_body
    assert list((home / "memory").glob("*.tmp")) == []
    with sqlite3.connect(state_paths(home)["db"]) as conn:
        after_rows = conn.execute(
            """
            SELECT path, entry_type, title, body, content_fingerprint
            FROM entries
            ORDER BY path
            """
        ).fetchall()

    assert after_rows == before_rows
    assert search_memory_entries("harness README", home) == before_matches


def test_generate_memory_removes_new_entry_when_storage_indexing_fails(
    tmp_path, monkeypatch
):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    for fixture_name in ("terminal_error.json", "vscode_editor.json", "edge_browser.json"):
        capture_once_from_fixture(ROOT / "harness" / "fixtures" / "uia" / fixture_name, home)

    monkeypatch.setattr("winchronicle.storage.init_db", lambda _db_path: None)

    def fail_after_base_row(_conn):
        raise RuntimeError("simulated memory FTS indexing failure")

    monkeypatch.setattr("winchronicle.storage._entries_fts_table_exists", fail_after_base_row)

    try:
        generate_memory_entries(home, date="2026-04-25")
    except RuntimeError:
        pass
    else:
        raise AssertionError("expected simulated memory storage failure")

    assert not (home / "memory" / "event-2026-04-25.md").exists()
    assert list((home / "memory").glob("*.tmp")) == []
    with sqlite3.connect(state_paths(home)["db"]) as conn:
        assert conn.execute("SELECT COUNT(*) FROM entries").fetchone() == (0,)


def test_memory_sqlite_entries_preserve_source_paths_and_public_search_shape(tmp_path, monkeypatch):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    for fixture_name in ("terminal_error.json", "vscode_editor.json", "edge_browser.json"):
        capture_once_from_fixture(ROOT / "harness" / "fixtures" / "uia" / fixture_name, home)

    generate_memory_entries(home, date="2026-04-25")

    with sqlite3.connect(state_paths(home)["db"]) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            """
            SELECT entry_type, title, body, trust, source_capture_paths
            FROM entries
            ORDER BY entry_type, title
            """
        ).fetchall()

    assert len(rows) == 6
    for row in rows:
        source_paths = json.loads(row["source_capture_paths"])
        assert row["trust"] == TRUST
        assert source_paths
        assert all((Path(path).exists() and "capture-buffer" in path) for path in source_paths)
        assert all(path in row["body"] for path in source_paths)

    event_row = next(row for row in rows if row["entry_type"] == "event")
    assert len(json.loads(event_row["source_capture_paths"])) == 3

    matches = search_memory_entries("OpenChronicle", home)
    assert matches
    assert all(
        set(match)
        == {
            "entry_type",
            "title",
            "start_timestamp",
            "end_timestamp",
            "snippet",
            "path",
            "trust",
        }
        for match in matches
    )
    assert all(match["trust"] == TRUST for match in matches)


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


def test_memory_secret_canaries_are_absent_from_sqlite_search_and_mcp(tmp_path, monkeypatch):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    for fixture_name in ("password_field.json", "secrets_visible_text.json"):
        capture_once_from_fixture(ROOT / "harness" / "fixtures" / "privacy" / fixture_name, home)

    generate_memory_entries(home)
    raw_canaries = (
        "CorrectHorseBatteryStaple!",
        "sk-winchronicle-test-canary",
        "ghp_winchroniclecanary",
        "xoxb-winchronicle-canary-token",
        "eyJhbGciOiJIUzI1NiJ9",
        "-----BEGIN PRIVATE KEY-----",
    )

    with sqlite3.connect(state_paths(home)["db"]) as conn:
        entry_bodies = [row[0] for row in conn.execute("SELECT body FROM entries").fetchall()]
        fts_exists = conn.execute(
            "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = 'entries_fts'"
        ).fetchone()
        fts_bodies = (
            [row[0] for row in conn.execute("SELECT body FROM entries_fts").fetchall()]
            if fts_exists
            else []
        )

    for body in entry_bodies + fts_bodies:
        for canary in raw_canaries:
            assert canary not in body

    for canary in raw_canaries:
        assert search_memory_entries(canary, home) == []
        tool_result = search_memory_tool(canary, home=home)
        assert tool_result["result"]["matches"] == []


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
    assert all(entry["trust"] == TRUST for entry in generated)
    assert all(entry["untrusted_observed_content"] is True for entry in generated)
    assert all(entry["instruction"] == TRUST_BOUNDARY_INSTRUCTION for entry in generated)

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


def _normalize_memory_manifest(manifest: list[dict[str, object]], home: Path) -> list[dict[str, object]]:
    home_text = str(home)
    normalized = []
    for entry in manifest:
        normalized_entry = dict(entry)
        normalized_entry["path"] = str(normalized_entry["path"]).replace(home_text, "<STATE>").replace("\\", "/")
        normalized.append(normalized_entry)
    return normalized
