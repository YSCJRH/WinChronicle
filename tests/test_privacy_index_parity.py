import json
import sqlite3
from pathlib import Path

from winchronicle.capture import (
    capture_once_from_fixture,
    capture_once_from_uia_helper_record,
)
from winchronicle.memory import generate_memory_entries
from winchronicle.mcp.server import search_memory_tool
from winchronicle.schema import validate_capture, validate_uia_helper_output
from winchronicle.storage import search_captures, search_memory_entries


ROOT = Path(__file__).resolve().parents[1]

RAW_SECRET_TERMS = (
    "CorrectHorseBatteryStaple!",
    "sk-winchronicle-test-canary-1234567890abcdef",
    "ghp_winchroniclecanary1234567890ABCD",
    "xoxb-winchronicle-canary-token",
    "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ3aW5jaHJvbmljbGUifQ.signature12345",
    "-----BEGIN PRIVATE KEY-----",
)


def test_fixture_privacy_capture_and_memory_indexes_exclude_raw_terms(
    tmp_path, monkeypatch
):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))

    for fixture_name in ("password_field.json", "secrets_visible_text.json"):
        result = capture_once_from_fixture(
            ROOT / "harness" / "fixtures" / "privacy" / fixture_name,
            home,
        )
        assert result.path is not None
        assert result.capture is not None

    generate_memory_entries(home, date="2026-04-25")

    captures = _read_capture_files(home)
    serialized = json.dumps(captures, sort_keys=True)
    password_capture = next(
        capture for capture in captures if capture["window_meta"]["app_name"] == "Example Login"
    )

    assert len(captures) == 2
    assert {capture["source"] for capture in captures} == {"fixture"}
    assert {capture["trigger"]["source"] for capture in captures} == {"manual"}
    assert all(capture["untrusted_observed_content"] is True for capture in captures)
    for capture in captures:
        validate_capture(capture)
    assert password_capture["focused_element"]["value"] == "[REDACTED:password_field]"
    assert password_capture["focused_element"]["text"] == "[REDACTED:password_field]"
    assert password_capture["focused_element"]["value_length"] == 0
    assert password_capture["focused_element"]["text_length"] == 0
    assert "[REDACTED:api_key]" in serialized
    assert "[REDACTED:github_token]" in serialized
    assert "[REDACTED:slack_token]" in serialized
    assert "[REDACTED:jwt]" in serialized
    assert "[REDACTED:private_key]" in serialized

    _assert_raw_terms_not_indexed(home, RAW_SECRET_TERMS)


def test_uia_helper_privacy_capture_and_memory_indexes_exclude_raw_terms(
    tmp_path, monkeypatch
):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))

    for fixture_name in ("password_field", "secrets_visible_text"):
        output = _helper_output_from_privacy_fixture(fixture_name)
        validate_uia_helper_output(output)
        result = capture_once_from_uia_helper_record(
            output,
            home,
            f"helper-{fixture_name}",
        )
        assert result.path is not None
        assert result.capture is not None

    generate_memory_entries(home, date="2026-04-25")

    captures = _read_capture_files(home)
    serialized = json.dumps(captures, sort_keys=True)
    password_capture = next(
        capture for capture in captures if capture["window_meta"]["app_name"] == "Example Login"
    )

    assert len(captures) == 2
    assert {capture["source"] for capture in captures} == {"uia_helper"}
    assert {capture["trigger"]["source"] for capture in captures} == {"win_uia_helper"}
    assert all(capture["untrusted_observed_content"] is True for capture in captures)
    for capture in captures:
        validate_capture(capture)
    assert password_capture["focused_element"]["value"] == "[REDACTED:password_field]"
    assert password_capture["focused_element"]["text"] == "[REDACTED:password_field]"
    assert password_capture["focused_element"]["value_length"] == 0
    assert password_capture["focused_element"]["text_length"] == 0
    assert "[REDACTED:api_key]" in serialized
    assert "[REDACTED:github_token]" in serialized
    assert "[REDACTED:slack_token]" in serialized
    assert "[REDACTED:jwt]" in serialized
    assert "[REDACTED:private_key]" in serialized

    _assert_raw_terms_not_indexed(home, RAW_SECRET_TERMS)


def _helper_output_from_privacy_fixture(fixture_name: str) -> dict:
    fixture_path = ROOT / "harness" / "fixtures" / "privacy" / f"{fixture_name}.json"
    output = json.loads(fixture_path.read_text(encoding="utf-8"))
    output.pop("fixture_name", None)
    output["helper_schema_version"] = 1
    output["source"] = "win-uia-helper"
    output["command"] = "capture-frontmost"
    visible_text = output.get("visible_text", "")
    node_count = 1 + len(output.get("uia_tree", {}).get("children", []))
    output["limits"] = {
        "depth": 80,
        "max_nodes": 5000,
        "max_text_chars": 20000,
        "node_count": node_count,
    }
    output["uia_stats"] = {
        "nodes_visited": node_count,
        "nodes_skipped": 0,
        "stale_nodes_skipped": 0,
        "exceptions_skipped": 0,
        "chars_collected": len(visible_text),
        "elapsed_ms": 10,
        "max_depth_observed": 1,
        "time_budget_ms": 3000,
        "time_budget_exceeded": False,
        "max_nodes_reached": False,
        "max_depth_reached": False,
        "max_chars_reached": False,
    }
    output["capture_target"] = {
        "kind": "frontmost",
        "hwnd": output["window"]["hwnd"],
        "requested_pid": None,
        "resolved_pid": output["window"]["pid"],
        "frontmost_at_capture": True,
        "harness_only": True,
    }
    output["truncated"] = False
    output["capture_surfaces"] = {
        "screenshots": False,
        "ocr": False,
        "audio": False,
        "keyboard": False,
        "clipboard": False,
        "desktop_control": False,
    }
    return output


def _assert_raw_terms_not_indexed(home: Path, raw_terms: tuple[str, ...]) -> None:
    capture_payload = "\n".join(
        path.read_text(encoding="utf-8")
        for path in sorted((home / "capture-buffer").glob("*.json"))
    )
    memory_payload = "\n".join(
        path.read_text(encoding="utf-8")
        for path in sorted((home / "memory").glob("*.md"))
    )
    sqlite_payload = _sqlite_text_payload(home)
    for term in raw_terms:
        assert term not in capture_payload
        assert term not in memory_payload
        assert term not in sqlite_payload
        assert search_captures(term, home) == []
        assert search_memory_entries(term, home) == []
        assert search_memory_tool(term, home=home)["result"]["matches"] == []


def _read_capture_files(home: Path) -> list[dict]:
    return [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted((home / "capture-buffer").glob("*.json"))
    ]


def _sqlite_text_payload(home: Path) -> str:
    db_path = home / "index.db"
    if not db_path.exists():
        return ""

    tables = ("captures", "captures_fts", "entries", "entries_fts")
    payload: list[str] = []
    with sqlite3.connect(db_path) as conn:
        for table in tables:
            exists = conn.execute(
                "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = ?",
                (table,),
            ).fetchone()
            if not exists:
                continue
            for row in conn.execute(f"SELECT * FROM {table}"):
                payload.append(json.dumps([str(value) for value in row], sort_keys=True))
    return "\n".join(payload)
