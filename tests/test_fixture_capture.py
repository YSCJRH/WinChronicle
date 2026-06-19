import json
import sqlite3
from pathlib import Path

from winchronicle.capture import capture_once_from_fixture
from winchronicle.paths import state_paths
from winchronicle.redaction import scan_for_unredacted_secrets
from winchronicle.storage import init_db, search_captures


ROOT = Path(__file__).resolve().parents[1]


def test_capture_once_writes_redacted_schema_valid_capture(tmp_path, monkeypatch):
    monkeypatch.setenv("WINCHRONICLE_HOME", str(tmp_path / "state"))

    result = capture_once_from_fixture(
        ROOT / "harness" / "fixtures" / "privacy" / "secrets_visible_text.json"
    )

    assert result.path is not None
    assert result.path.exists()
    written = result.path.read_text(encoding="utf-8")
    assert "sk-winchronicle-test-canary" not in written
    assert "BEGIN PRIVATE KEY" not in written
    assert "ghp_winchroniclecanary" not in written
    assert "xoxb-winchronicle-canary-token" not in written
    capture = json.loads(written)
    assert capture["untrusted_observed_content"] is True


def test_capture_once_does_not_publish_file_when_atomic_replace_fails(
    tmp_path, monkeypatch
):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    original_replace = Path.replace

    def fail_capture_replace(self: Path, target_path: Path) -> Path:
        if target_path.parent.name == "capture-buffer" and target_path.suffix == ".json":
            raise OSError("simulated capture replace failure")
        return original_replace(self, target_path)

    monkeypatch.setattr(Path, "replace", fail_capture_replace)

    try:
        capture_once_from_fixture(ROOT / "harness" / "fixtures" / "uia" / "terminal_error.json")
    except OSError:
        pass
    else:
        raise AssertionError("expected simulated capture replace failure")

    capture_buffer = home / "capture-buffer"
    assert list(capture_buffer.glob("*.json")) == []
    assert list(capture_buffer.glob("*.tmp")) == []
    assert search_captures("AssertionError", home) == []


def test_capture_once_removes_published_file_when_indexing_fails(
    tmp_path, monkeypatch
):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))

    def fail_index(*_args, **_kwargs):
        raise RuntimeError("simulated capture index failure")

    monkeypatch.setattr("winchronicle.capture.index_capture", fail_index)

    try:
        capture_once_from_fixture(ROOT / "harness" / "fixtures" / "uia" / "terminal_error.json")
    except RuntimeError:
        pass
    else:
        raise AssertionError("expected simulated capture index failure")

    capture_buffer = home / "capture-buffer"
    assert list(capture_buffer.glob("*.json")) == []
    assert list(capture_buffer.glob("*.tmp")) == []
    assert search_captures("AssertionError", home) == []


def test_capture_once_restores_existing_file_when_indexing_fails(
    tmp_path, monkeypatch
):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    fixture_path = ROOT / "harness" / "fixtures" / "uia" / "terminal_error.json"

    result = capture_once_from_fixture(fixture_path)
    assert result.path is not None
    before_text = result.path.read_text(encoding="utf-8")
    before_matches = search_captures("AssertionError", home)

    def fail_index(*_args, **_kwargs):
        raise RuntimeError("simulated capture index failure")

    monkeypatch.setattr("winchronicle.capture.index_capture", fail_index)

    try:
        capture_once_from_fixture(fixture_path)
    except RuntimeError:
        pass
    else:
        raise AssertionError("expected simulated capture index failure")

    assert result.path.exists()
    assert result.path.read_text(encoding="utf-8") == before_text
    assert list((home / "capture-buffer").glob("*.tmp")) == []
    assert search_captures("AssertionError", home) == before_matches


def test_capture_once_rolls_back_file_and_sqlite_row_when_storage_indexing_fails(
    tmp_path, monkeypatch
):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    init_db(state_paths(home)["db"])

    monkeypatch.setattr("winchronicle.storage.init_db", lambda _db_path: None)

    def fail_after_base_row(_conn):
        raise RuntimeError("simulated capture FTS indexing failure")

    monkeypatch.setattr("winchronicle.storage._fts_table_exists", fail_after_base_row)

    try:
        capture_once_from_fixture(ROOT / "harness" / "fixtures" / "uia" / "terminal_error.json")
    except RuntimeError:
        pass
    else:
        raise AssertionError("expected simulated capture storage failure")

    assert list((home / "capture-buffer").glob("*.json")) == []
    assert list((home / "capture-buffer").glob("*.tmp")) == []
    with sqlite3.connect(state_paths(home)["db"]) as conn:
        assert conn.execute("SELECT COUNT(*) FROM captures").fetchone() == (0,)


def test_capture_once_redacts_secret_like_uia_metadata_before_storage(
    tmp_path, monkeypatch
):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    fixture = json.loads(
        (ROOT / "harness" / "fixtures" / "uia" / "notepad_basic.json").read_text(
            encoding="utf-8"
        )
    )
    fixture["fixture_name"] = "metadata-secret-redaction"
    fixture["window"]["process_name"] = (
        "OPENAI_API_KEY=sk-winchronicle-meta-canary-1234567890abcdef.exe"
    )
    fixture["window"]["exe_path"] = "C:\\Tools\\ACCESS_TOKEN=winchroniclecanary0123456789abcd\\app.exe"
    fixture["window"]["app_name"] = "github_pat_11AA22BB33CC44DD55EE66FF77HH99II00JJ"
    fixture["focused_element"]["automation_id"] = "SLACK_TOKEN=xoxb-winchronicle-canary-token"
    fixture["focused_element"]["class_name"] = (
        "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ3aW5jaHJvbmljbGUifQ.signature12345"
    )
    fixture_path = tmp_path / "metadata-secret-redaction.json"
    fixture_path.write_text(json.dumps(fixture), encoding="utf-8")

    result = capture_once_from_fixture(fixture_path)

    assert result.path is not None
    written = result.path.read_text(encoding="utf-8")
    assert scan_for_unredacted_secrets(written) == []
    for raw in (
        "sk-winchronicle-meta-canary-1234567890abcdef",
        "winchroniclecanary0123456789abcd",
        "github_pat_11AA22BB33CC44DD55EE66FF77HH99II00JJ",
        "xoxb-winchronicle-canary-token",
        "eyJhbGciOiJIUzI1NiJ9",
    ):
        assert raw not in written
        assert search_captures(raw, home) == []


def test_capture_once_does_not_use_fixture_name_in_durable_paths(
    tmp_path, monkeypatch
):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    fixture = json.loads(
        (ROOT / "harness" / "fixtures" / "uia" / "notepad_basic.json").read_text(
            encoding="utf-8"
        )
    )
    raw_hint = "customer-alpha-rollout"
    fixture["fixture_name"] = raw_hint
    fixture_path = tmp_path / "custom-fixture.json"
    fixture_path.write_text(json.dumps(fixture), encoding="utf-8")

    result = capture_once_from_fixture(fixture_path)
    matches = search_captures("harness README", home)
    serialized = json.dumps(
        {
            "path": str(result.path),
            "matches": matches,
        },
        sort_keys=True,
    )

    assert result.path is not None
    assert matches
    assert raw_hint not in serialized
    assert "customer-alpha" not in serialized


def test_denylisted_app_capture_is_skipped(tmp_path, monkeypatch):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))

    result = capture_once_from_fixture(
        ROOT / "harness" / "fixtures" / "privacy" / "denylisted_app.json"
    )

    assert result.skipped is True
    assert result.path is None
    assert not (home / "capture-buffer").exists()


def test_lock_app_capture_is_skipped(tmp_path, monkeypatch):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))

    result = capture_once_from_fixture(
        ROOT / "harness" / "fixtures" / "privacy" / "lock_app.json"
    )

    assert result.skipped is True
    assert result.path is None
    assert "LockApp.exe" in (result.reason or "")
    assert not (home / "capture-buffer").exists()


def test_fixture_capture_is_searchable(tmp_path, monkeypatch):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    capture_once_from_fixture(ROOT / "harness" / "fixtures" / "uia" / "terminal_error.json")

    results = search_captures("AssertionError", home)

    assert len(results) == 1
    assert results[0]["app_name"] == "Windows Terminal"
    assert "AssertionError" in results[0]["snippet"]
