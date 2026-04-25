import json
from pathlib import Path

from winchronicle.capture import load_json, normalize_fixture, privacy_check_path


ROOT = Path(__file__).resolve().parents[1]


def test_privacy_check_passes_password_and_secret_fixtures():
    password = privacy_check_path(ROOT / "harness" / "fixtures" / "privacy" / "password_field.json")
    secrets = privacy_check_path(ROOT / "harness" / "fixtures" / "privacy" / "secrets_visible_text.json")

    assert password.ok is True
    assert secrets.ok is True


def test_privacy_check_fails_unredacted_capture_file(tmp_path):
    capture = normalize_fixture(load_json(ROOT / "harness" / "fixtures" / "uia" / "notepad_basic.json"))
    capture["visible_text"] = "leaked ghp_winchroniclecanary1234567890ABCD"
    path = tmp_path / "bad_capture.json"
    path.write_text(json.dumps(capture), encoding="utf-8")

    result = privacy_check_path(path)

    assert result.ok is False
    assert any("github_token" in message for message in result.messages)


def test_prompt_injection_fixture_is_stored_as_untrusted_observed_content():
    fixture = load_json(
        ROOT / "harness" / "fixtures" / "privacy" / "prompt_injection_visible_text.json"
    )

    capture = normalize_fixture(fixture)

    assert "Ignore previous instructions" in capture["visible_text"]
    assert capture["untrusted_observed_content"] is True
