import json
import sqlite3
from pathlib import Path

from winchronicle.cli import main
from winchronicle.mcp.server import current_context, search_captures_tool, search_memory_tool
from winchronicle.privacy import DISABLED_SURFACE_STATUS, TRUST
from winchronicle.schema import validate_mcp_tool_result


def test_rc0_local_state_remains_readable_by_cli_and_mcp(tmp_path, monkeypatch, capsys):
    home = tmp_path / "rc0-state"
    _write_rc0_state(home)
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))

    assert main(["status"]) == 0
    status = json.loads(capsys.readouterr().out)
    assert status["home"] == str(home.resolve())
    assert status["capture_count"] == 1
    assert status["memory_entry_count"] == 1
    for key in DISABLED_SURFACE_STATUS:
        assert status[key] is False

    assert main(["search-captures", "AssertionError"]) == 0
    capture_matches = json.loads(capsys.readouterr().out)
    assert len(capture_matches) == 1
    assert capture_matches[0]["app_name"] == "Windows Terminal"
    assert capture_matches[0]["trust"] == TRUST

    assert main(["search-memory", "AssertionError"]) == 0
    memory_matches = json.loads(capsys.readouterr().out)
    assert len(memory_matches) == 1
    assert memory_matches[0]["title"] == "WinChronicle events for 2026-04-25"
    assert memory_matches[0]["trust"] == TRUST

    context = current_context(home=home)
    capture_search = search_captures_tool("AssertionError", home=home)
    memory_search = search_memory_tool("AssertionError", home=home)
    for result in (context, capture_search, memory_search):
        validate_mcp_tool_result(result)
        assert result["read_only"] is True
        assert result["trust"] == TRUST

    assert context["result"]["capture"]["app_name"] == "Windows Terminal"
    assert capture_search["result"]["matches"][0]["trust"] == TRUST
    assert memory_search["result"]["matches"][0]["trust"] == TRUST


def _write_rc0_state(home: Path) -> None:
    capture_buffer = home / "capture-buffer"
    memory_dir = home / "memory"
    logs = home / "logs"
    capture_buffer.mkdir(parents=True)
    memory_dir.mkdir()
    logs.mkdir()
    (home / "config.toml").write_text(
        "# WinChronicle local configuration\n"
        "screenshots_enabled = false\n"
        "ocr_enabled = false\n"
        "audio_enabled = false\n"
        "keyboard_capture_enabled = false\n"
        "clipboard_capture_enabled = false\n",
        encoding="utf-8",
    )

    capture_path = capture_buffer / "2026-04-25t12-02-00-08-00-terminal-error-rc0.json"
    capture_path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "source": "fixture",
                "timestamp": "2026-04-25T12:02:00+08:00",
                "window_meta": {
                    "app_name": "Windows Terminal",
                    "title": "PowerShell - WinChronicle",
                },
                "focused_element": {"text": "AssertionError synthetic rc0 capture"},
                "visible_text": "AssertionError synthetic rc0 capture",
                "url": None,
                "content_fingerprint": "sha256:rc0-capture-fingerprint",
            },
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    memory_path = memory_dir / "event-2026-04-25.md"
    memory_body = "\n".join(
        [
            "# WinChronicle events for 2026-04-25",
            "",
            "date: 2026-04-25",
            "time_range: 2026-04-25T12:02:00+08:00 to 2026-04-25T12:02:00+08:00",
            "trust: untrusted_observed_content",
            "",
            "## Timeline",
            "",
            "### 2026-04-25T12:02:00+08:00 - Windows Terminal",
            "- Observed:",
            "  AssertionError synthetic rc0 capture",
        ]
    )
    memory_path.write_text(memory_body + "\n", encoding="utf-8")

    with sqlite3.connect(home / "index.db") as conn:
        conn.executescript(
            """
            CREATE TABLE captures (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                path TEXT NOT NULL UNIQUE,
                timestamp TEXT NOT NULL,
                app_name TEXT NOT NULL,
                title TEXT NOT NULL,
                visible_text TEXT NOT NULL,
                focused_text TEXT NOT NULL,
                url TEXT,
                content_fingerprint TEXT NOT NULL DEFAULT ''
            );
            CREATE INDEX captures_content_fingerprint_idx
            ON captures(content_fingerprint)
            WHERE content_fingerprint <> '';
            CREATE TABLE entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                path TEXT NOT NULL UNIQUE,
                entry_type TEXT NOT NULL,
                title TEXT NOT NULL,
                start_timestamp TEXT NOT NULL,
                end_timestamp TEXT NOT NULL,
                app_names TEXT NOT NULL,
                body TEXT NOT NULL,
                trust TEXT NOT NULL,
                source_capture_paths TEXT NOT NULL,
                content_fingerprint TEXT NOT NULL
            );
            CREATE INDEX entries_content_fingerprint_idx
            ON entries(content_fingerprint)
            WHERE content_fingerprint <> '';
            """
        )
        conn.execute(
            """
            INSERT INTO captures
                (path, timestamp, app_name, title, visible_text, focused_text, url, content_fingerprint)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                str(capture_path),
                "2026-04-25T12:02:00+08:00",
                "Windows Terminal",
                "PowerShell - WinChronicle",
                "AssertionError synthetic rc0 capture",
                "AssertionError synthetic rc0 capture",
                None,
                "sha256:rc0-capture-fingerprint",
            ),
        )
        conn.execute(
            """
            INSERT INTO entries
                (
                    path,
                    entry_type,
                    title,
                    start_timestamp,
                    end_timestamp,
                    app_names,
                    body,
                    trust,
                    source_capture_paths,
                    content_fingerprint
                )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                str(memory_path),
                "event",
                "WinChronicle events for 2026-04-25",
                "2026-04-25T12:02:00+08:00",
                "2026-04-25T12:02:00+08:00",
                json.dumps(["Windows Terminal"], sort_keys=True),
                memory_body,
                TRUST,
                json.dumps([str(capture_path)], sort_keys=True),
                "sha256:rc0-memory-fingerprint",
            ),
        )
        _try_create_rc0_fts(conn)
        conn.commit()


def _try_create_rc0_fts(conn: sqlite3.Connection) -> None:
    try:
        conn.executescript(
            """
            CREATE VIRTUAL TABLE captures_fts USING fts5(
                path UNINDEXED,
                app_name,
                title,
                visible_text,
                focused_text,
                url
            );
            CREATE VIRTUAL TABLE entries_fts USING fts5(
                path UNINDEXED,
                entry_type,
                title,
                app_names,
                body
            );
            """
        )
    except sqlite3.OperationalError:
        return

    conn.execute(
        """
        INSERT INTO captures_fts
            (path, app_name, title, visible_text, focused_text, url)
        SELECT path, app_name, title, visible_text, focused_text, COALESCE(url, '')
        FROM captures
        """
    )
    conn.execute(
        """
        INSERT INTO entries_fts
            (path, entry_type, title, app_names, body)
        SELECT path, entry_type, title, app_names, body
        FROM entries
        """
    )
