import json
from pathlib import Path

from winchronicle.capture import load_json, normalize_fixture
from winchronicle.redaction import redact_text, scan_for_unredacted_secrets


ROOT = Path(__file__).resolve().parents[1]


def test_redact_text_removes_obvious_secret_tokens():
    raw = """OPENAI_API_KEY=sk-winchronicle-test-canary-1234567890abcdef
GITHUB_TOKEN=ghp_winchroniclecanary1234567890ABCD
SLACK_TOKEN=xoxb-winchronicle-canary-token
JWT=eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ3aW5jaHJvbmljbGUifQ.signature12345
-----BEGIN PRIVATE KEY-----
abc123
-----END PRIVATE KEY-----"""

    redacted, counts = redact_text(raw)

    assert "sk-winchronicle-test-canary" not in redacted
    assert "ghp_winchroniclecanary" not in redacted
    assert "xoxb-winchronicle-canary-token" not in redacted
    assert "BEGIN PRIVATE KEY" not in redacted
    assert counts["api_key"] == 1
    assert counts["github_token"] == 1
    assert counts["slack_token"] == 1
    assert counts["jwt"] == 1
    assert counts["private_key"] == 1
    assert scan_for_unredacted_secrets(redacted) == []


def test_password_field_value_is_not_in_normalized_capture():
    fixture_path = ROOT / "harness" / "fixtures" / "privacy" / "password_field.json"
    capture = normalize_fixture(load_json(fixture_path))
    serialized = json.dumps(capture, sort_keys=True)

    assert "CorrectHorseBatteryStaple!" not in serialized
    assert capture["focused_element"]["value"] == "[REDACTED:password_field]"
    assert capture["focused_element"]["text"] == "[REDACTED:password_field]"
