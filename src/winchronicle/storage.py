from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

from .paths import state_paths


CAPTURES_SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS captures (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    path TEXT NOT NULL UNIQUE,
    timestamp TEXT NOT NULL,
    app_name TEXT NOT NULL,
    title TEXT NOT NULL,
    visible_text TEXT NOT NULL,
    focused_text TEXT NOT NULL,
    url TEXT
);
"""

FTS_SCHEMA_SQL = """
CREATE VIRTUAL TABLE IF NOT EXISTS captures_fts USING fts5(
    path UNINDEXED,
    app_name,
    title,
    visible_text,
    focused_text,
    url
);
"""


def init_db(db_path: Path) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        conn.executescript(CAPTURES_SCHEMA_SQL)
        if _ensure_fts_table(conn):
            _backfill_fts(conn)
        conn.commit()


def index_capture(capture: dict[str, Any], capture_path: Path, home: Path | str | None = None) -> None:
    paths = state_paths(home)
    init_db(paths["db"])
    focused = capture["focused_element"]
    window = capture["window_meta"]
    with sqlite3.connect(paths["db"]) as conn:
        conn.execute(
            """
            INSERT OR REPLACE INTO captures
                (path, timestamp, app_name, title, visible_text, focused_text, url)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                str(capture_path),
                capture["timestamp"],
                window["app_name"],
                window["title"],
                capture["visible_text"],
                focused.get("text") or focused.get("value") or "",
                capture.get("url"),
            ),
        )
        if _fts_table_exists(conn):
            conn.execute("DELETE FROM captures_fts WHERE path = ?", (str(capture_path),))
            conn.execute(
                """
                INSERT INTO captures_fts
                    (path, app_name, title, visible_text, focused_text, url)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    str(capture_path),
                    window["app_name"],
                    window["title"],
                    capture["visible_text"],
                    focused.get("text") or focused.get("value") or "",
                    capture.get("url") or "",
                ),
            )
        conn.commit()


def capture_count(home: Path | str | None = None) -> int:
    paths = state_paths(home)
    if not paths["db"].exists():
        return 0
    with sqlite3.connect(paths["db"]) as conn:
        try:
            row = conn.execute("SELECT COUNT(*) FROM captures").fetchone()
        except sqlite3.OperationalError:
            return 0
    return int(row[0])


def search_captures(query: str, home: Path | str | None = None, limit: int = 10) -> list[dict[str, str]]:
    if not query.strip():
        return []

    paths = state_paths(home)
    if not paths["db"].exists():
        return []

    with sqlite3.connect(paths["db"]) as conn:
        conn.row_factory = sqlite3.Row
        if _fts_table_exists(conn):
            rows = _search_fts(conn, query, limit)
        else:
            rows = _search_like_fallback(conn, query, limit)

    return [_row_to_result(row, query) for row in rows]


def list_captures(
    home: Path | str | None = None,
    *,
    limit: int = 10,
    app_name: str | None = None,
    since: str | None = None,
    until: str | None = None,
) -> list[dict[str, str]]:
    paths = state_paths(home)
    if not paths["db"].exists():
        return []

    clauses: list[str] = []
    params: list[str | int] = []
    if app_name:
        clauses.append("app_name = ?")
        params.append(app_name)
    if since:
        clauses.append("timestamp >= ?")
        params.append(since)
    if until:
        clauses.append("timestamp <= ?")
        params.append(until)

    where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
    params.append(max(0, limit))

    with sqlite3.connect(paths["db"]) as conn:
        conn.row_factory = sqlite3.Row
        try:
            rows = conn.execute(
                f"""
                SELECT path, timestamp, app_name, title, visible_text, focused_text, url
                FROM captures
                {where}
                ORDER BY timestamp DESC, path ASC
                LIMIT ?
                """,
                tuple(params),
            ).fetchall()
        except sqlite3.OperationalError:
            return []

    return [_capture_row_to_dict(row) for row in rows]


def recent_capture(
    home: Path | str | None = None,
    *,
    at: str | None = None,
    app_name: str | None = None,
) -> dict[str, str] | None:
    rows = list_captures(
        home,
        limit=1,
        app_name=app_name,
        until=at,
    )
    return rows[0] if rows else None


def _ensure_fts_table(conn: sqlite3.Connection) -> bool:
    try:
        conn.executescript(FTS_SCHEMA_SQL)
    except sqlite3.OperationalError as exc:
        if _is_fts_unavailable(exc):
            return False
        raise
    return _fts_table_exists(conn)


def _fts_table_exists(conn: sqlite3.Connection) -> bool:
    row = conn.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'captures_fts'"
    ).fetchone()
    return row is not None


def _backfill_fts(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        INSERT INTO captures_fts (path, app_name, title, visible_text, focused_text, url)
        SELECT path, app_name, title, visible_text, focused_text, coalesce(url, '')
        FROM captures
        WHERE path NOT IN (SELECT path FROM captures_fts)
        """
    )


def _fts_query(query: str) -> str:
    escaped = query.strip().replace('"', '""')
    return f'"{escaped}"' if escaped else '""'


def _search_fts(
    conn: sqlite3.Connection, query: str, limit: int
) -> list[sqlite3.Row]:
    try:
        return conn.execute(
            """
            SELECT
                captures.path,
                captures.timestamp,
                captures.app_name,
                captures.title,
                captures.visible_text,
                captures.focused_text,
                captures.url
            FROM captures_fts
            JOIN captures ON captures.path = captures_fts.path
            WHERE captures_fts MATCH ?
            ORDER BY bm25(captures_fts), captures.timestamp DESC
            LIMIT ?
            """,
            (_fts_query(query), limit),
        ).fetchall()
    except sqlite3.OperationalError as exc:
        if _is_fts_unavailable(exc):
            return _search_like_fallback(conn, query, limit)
        raise


def _search_like_fallback(
    conn: sqlite3.Connection, query: str, limit: int
) -> list[sqlite3.Row]:
    like = f"%{query.lower()}%"
    try:
        return conn.execute(
            """
            SELECT path, timestamp, app_name, title, visible_text, focused_text, url
            FROM captures
            WHERE lower(visible_text) LIKE ?
               OR lower(focused_text) LIKE ?
               OR lower(title) LIKE ?
               OR lower(app_name) LIKE ?
               OR lower(coalesce(url, '')) LIKE ?
            ORDER BY timestamp DESC
            LIMIT ?
            """,
            (like, like, like, like, like, limit),
        ).fetchall()
    except sqlite3.OperationalError:
        return []


def _is_fts_unavailable(exc: sqlite3.OperationalError) -> bool:
    message = str(exc).lower()
    return "fts" in message and (
        "no such module" in message
        or "no such table" in message
        or "unable to use function" in message
    )


def _row_to_result(row: sqlite3.Row, query: str) -> dict[str, str]:
    haystack = row["visible_text"] or row["focused_text"] or row["title"]
    snippet = _snippet(haystack, query)
    return {
        "timestamp": row["timestamp"],
        "app_name": row["app_name"],
        "title": row["title"],
        "snippet": snippet,
        "path": row["path"],
    }


def _capture_row_to_dict(row: sqlite3.Row) -> dict[str, str]:
    return {
        "path": row["path"],
        "timestamp": row["timestamp"],
        "app_name": row["app_name"],
        "title": row["title"],
        "visible_text": row["visible_text"],
        "focused_text": row["focused_text"],
        "url": row["url"] or "",
    }


def _snippet(text: str, query: str, radius: int = 48) -> str:
    lowered = text.lower()
    index = lowered.find(query.lower())
    if index == -1:
        return text[: radius * 2].replace("\n", " ")
    start = max(0, index - radius)
    end = min(len(text), index + len(query) + radius)
    return text[start:end].replace("\n", " ")


def read_capture_file(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))
