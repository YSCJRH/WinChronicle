import json
from pathlib import Path

from winchronicle.capture import capture_once_from_fixture
from winchronicle.redaction import scan_for_unredacted_secrets
from winchronicle.storage import search_captures


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
