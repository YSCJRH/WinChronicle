import json
from pathlib import Path

from winchronicle.capture import capture_once_from_fixture
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


def test_denylisted_app_capture_is_skipped(tmp_path, monkeypatch):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))

    result = capture_once_from_fixture(
        ROOT / "harness" / "fixtures" / "privacy" / "denylisted_app.json"
    )

    assert result.skipped is True
    assert result.path is None
    assert not (home / "capture-buffer").exists()


def test_fixture_capture_is_searchable(tmp_path, monkeypatch):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    capture_once_from_fixture(ROOT / "harness" / "fixtures" / "uia" / "terminal_error.json")

    results = search_captures("AssertionError", home)

    assert len(results) == 1
    assert results[0]["app_name"] == "Windows Terminal"
    assert "AssertionError" in results[0]["snippet"]
