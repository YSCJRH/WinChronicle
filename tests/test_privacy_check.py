import json
from pathlib import Path

from winchronicle.capture import (
    capture_once_from_fixture,
    load_json,
    normalize_fixture,
    privacy_check_path,
)
from winchronicle.privacy import denylist_reason


ROOT = Path(__file__).resolve().parents[1]


def test_privacy_check_passes_password_and_secret_fixtures():
    password = privacy_check_path(ROOT / "harness" / "fixtures" / "privacy" / "password_field.json")
    secrets = privacy_check_path(ROOT / "harness" / "fixtures" / "privacy" / "secrets_visible_text.json")
    lock_app = privacy_check_path(ROOT / "harness" / "fixtures" / "privacy" / "lock_app.json")

    assert password.ok is True
    assert secrets.ok is True
    assert lock_app.ok is True
    assert lock_app.messages == ["PASS: denylisted app capture would be skipped"]


def test_title_denylist_reason_does_not_echo_window_title(tmp_path, monkeypatch):
    monkeypatch.setenv("WINCHRONICLE_HOME", str(tmp_path / "state"))
    sensitive_title = "Seed phrase for production wallet"
    fixture = load_json(ROOT / "harness" / "fixtures" / "uia" / "notepad_basic.json")
    fixture["window"]["title"] = sensitive_title
    fixture_path = tmp_path / "title_denylisted.json"
    fixture_path.write_text(json.dumps(fixture), encoding="utf-8")

    reason = denylist_reason(fixture)
    result = capture_once_from_fixture(fixture_path)

    assert reason == "denylisted title pattern"
    assert sensitive_title not in reason
    assert result.skipped is True
    assert result.reason == "denylisted title pattern"
    assert sensitive_title not in result.reason
    assert not (tmp_path / "state" / "capture-buffer").exists()


def test_privacy_check_fails_unredacted_capture_file(tmp_path):
    capture = normalize_fixture(load_json(ROOT / "harness" / "fixtures" / "uia" / "notepad_basic.json"))
    capture["visible_text"] = "leaked ghp_winchroniclecanary1234567890ABCD"
    path = tmp_path / "bad_capture.json"
    path.write_text(json.dumps(capture), encoding="utf-8")

    result = privacy_check_path(path)

    assert result.ok is False
    assert any("github_token" in message for message in result.messages)


def test_privacy_check_fails_plain_token_canary_in_normalized_capture(tmp_path):
    capture = normalize_fixture(load_json(ROOT / "harness" / "fixtures" / "uia" / "notepad_basic.json"))
    capture["visible_text"] = "leaked winchronicle_plain_canary_token"
    path = tmp_path / "bad_token_canary_capture.json"
    path.write_text(json.dumps(capture), encoding="utf-8")

    result = privacy_check_path(path)

    assert result.ok is False
    assert any("token_canary" in message for message in result.messages)


def test_privacy_check_fails_existing_normalized_denylisted_capture(tmp_path):
    capture = normalize_fixture(
        load_json(ROOT / "harness" / "fixtures" / "privacy" / "lock_app.json")
    )
    path = tmp_path / "bad_lock_app_capture.json"
    path.write_text(json.dumps(capture), encoding="utf-8")

    result = privacy_check_path(path)

    assert result.ok is False
    assert result.messages == ["FAIL: denylisted normalized capture would already be stored"]


def test_privacy_check_fails_existing_normalized_raw_password_field(tmp_path):
    capture = normalize_fixture(
        load_json(ROOT / "harness" / "fixtures" / "privacy" / "password_field.json")
    )
    capture["focused_element"]["value"] = "operator-entered-password"
    capture["focused_element"]["text"] = "operator-entered-password"
    capture["focused_element"]["value_length"] = len("operator-entered-password")
    capture["focused_element"]["text_length"] = len("operator-entered-password")
    path = tmp_path / "bad_password_capture.json"
    path.write_text(json.dumps(capture), encoding="utf-8")

    result = privacy_check_path(path)

    assert result.ok is False
    assert result.messages == ["FAIL: unredacted password_field would be written"]


def test_prompt_injection_fixture_is_stored_as_untrusted_observed_content():
    fixture = load_json(
        ROOT / "harness" / "fixtures" / "privacy" / "prompt_injection_visible_text.json"
    )

    capture = normalize_fixture(fixture)

    assert "Ignore previous instructions" in capture["visible_text"]
    assert capture["untrusted_observed_content"] is True
