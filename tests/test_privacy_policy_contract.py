import re
from pathlib import Path

from winchronicle.capture import load_json, normalize_fixture, privacy_check_path
from winchronicle.mcp.server import privacy_status
from winchronicle.privacy import (
    APP_DENYLIST,
    DISABLED_SURFACE_STATUS,
    TITLE_DENYLIST_REGEX,
    TRUST,
    TRUST_BOUNDARY_INSTRUCTION,
    denylist_reason,
    privacy_contract_payload,
)
from winchronicle.redaction import REDACTION_RULES


ROOT = Path(__file__).resolve().parents[1]
PRIVACY_POLICY = ROOT / "harness" / "specs" / "privacy-policy.md"
PRIVACY_GATES = ROOT / "harness" / "scorecards" / "privacy-gates.md"
PRIVACY_FIXTURES = ROOT / "harness" / "fixtures" / "privacy"

EXPECTED_DISABLED_SURFACE_PHRASES = {
    "screenshots_enabled": "Screenshots.",
    "ocr_enabled": "OCR.",
    "audio_enabled": "Audio recording.",
    "keyboard_capture_enabled": "Keyboard capture.",
    "clipboard_capture_enabled": "Clipboard capture.",
    "network_upload_enabled": "Network upload of captured content.",
    "cloud_upload_enabled": "Cloud upload of captured content.",
    "desktop_control_enabled": "Desktop control actions.",
    "mcp_write_tools_enabled": "MCP write tools.",
    "product_targeted_capture_enabled": "Product targeted capture by HWND, PID, or window-title.",
    "llm_calls_enabled": "LLM calls or summarization.",
}
EXPECTED_REDACTION_RULES = {
    "api_key",
    "github_token",
    "jwt",
    "password_field",
    "private_key",
    "slack_token",
    "token_canary",
}
EXPECTED_PRIVACY_FIXTURES = {
    "denylisted_app.json",
    "lock_app.json",
    "password_field.json",
    "prompt_injection_visible_text.json",
    "secrets_visible_text.json",
}


def test_privacy_policy_disabled_surfaces_match_status_and_mcp(tmp_path):
    spec = _normalized(PRIVACY_POLICY.read_text(encoding="utf-8"))
    scorecard = _normalized(PRIVACY_GATES.read_text(encoding="utf-8"))
    payload = privacy_contract_payload()
    mcp_result = privacy_status(home=tmp_path / "state")["result"]

    assert set(DISABLED_SURFACE_STATUS) == set(EXPECTED_DISABLED_SURFACE_PHRASES)
    assert all(value is False for value in DISABLED_SURFACE_STATUS.values())
    for key, policy_phrase in EXPECTED_DISABLED_SURFACE_PHRASES.items():
        assert policy_phrase in spec
        assert payload[key] is False
        assert mcp_result[key] is False

    assert "CLI `status` and MCP `privacy_status` must report the same disabled privacy surfaces" in scorecard
    assert "Direct fixture and synthesized UIA helper captures must prove raw passwords" in scorecard
    assert "Targeted UIA capture is harness-only helper behavior" in spec


def test_privacy_policy_denylist_matches_runtime_and_fixture_coverage():
    spec = PRIVACY_POLICY.read_text(encoding="utf-8")
    policy_app_names = {
        app_name.lower()
        for app_name in re.findall(r"^- `([^`]+\.exe)`$", spec, flags=re.MULTILINE)
    }

    assert policy_app_names == APP_DENYLIST
    assert {path.name for path in PRIVACY_FIXTURES.glob("*.json")} == EXPECTED_PRIVACY_FIXTURES

    denylisted_app = load_json(PRIVACY_FIXTURES / "denylisted_app.json")
    lock_app = load_json(PRIVACY_FIXTURES / "lock_app.json")
    assert denylist_reason(denylisted_app).startswith("denylisted app:")
    assert denylist_reason(lock_app).startswith("denylisted app:")

    assert privacy_check_path(PRIVACY_FIXTURES / "lock_app.json").messages == [
        "PASS: denylisted app capture would be skipped"
    ]


def test_privacy_policy_title_denylist_uses_content_free_reason():
    spec = PRIVACY_POLICY.read_text(encoding="utf-8")
    policy_signals = set(
        re.findall(r"^- `([^`]+)`$", _section(spec, "Denylist Rules"), flags=re.MULTILINE)
    ) - {app for app in re.findall(r"^- `([^`]+\.exe)`$", spec, flags=re.MULTILINE)}
    runtime_signals = {pattern.pattern.removeprefix("(?i)") for pattern in TITLE_DENYLIST_REGEX}

    assert policy_signals == runtime_signals
    for signal in runtime_signals:
        sensitive_title = f"Sensitive {signal} workspace"
        record = {"window": {"process_name": "notepad.exe", "title": sensitive_title}}
        reason = denylist_reason(record)
        assert reason == "denylisted title pattern"
        assert sensitive_title not in reason

    assert "Denylist diagnostics must not echo the matched window title" in spec
    assert "stable content-free reason" in spec


def test_privacy_policy_redaction_rules_match_runtime_non_goal():
    spec = PRIVACY_POLICY.read_text(encoding="utf-8")
    rule_names = {name for name, _ in REDACTION_RULES}

    assert rule_names == EXPECTED_REDACTION_RULES
    for rule_name in EXPECTED_REDACTION_RULES - {"password_field"}:
        assert f"- `{rule_name}`:" in spec
    assert "Password fields are redacted by field semantics" in spec
    assert "focused_element.is_password" in spec
    assert "Credit-card Luhn-positive redaction" in spec
    assert "not implemented in v0.1" in spec
    assert "credit_card" not in rule_names


def test_privacy_policy_trust_boundary_matches_capture_status_and_mcp(tmp_path):
    spec = PRIVACY_POLICY.read_text(encoding="utf-8")
    scorecard = PRIVACY_GATES.read_text(encoding="utf-8")
    capture = normalize_fixture(load_json(PRIVACY_FIXTURES / "prompt_injection_visible_text.json"))
    payload = privacy_contract_payload()
    mcp_result = privacy_status(home=tmp_path / "state")["result"]

    assert capture["untrusted_observed_content"] is True
    assert payload["observed_content_trust"] == TRUST
    assert payload["trust_boundary_instruction"] == TRUST_BOUNDARY_INSTRUCTION
    assert mcp_result["observed_content_trust"] == TRUST
    assert mcp_result["trust_boundary_instruction"] == TRUST_BOUNDARY_INSTRUCTION
    assert '"trust": "untrusted_observed_content"' in spec
    assert "Prompt injection text may be stored only as untrusted observed content." in scorecard


def _section(text: str, heading: str) -> str:
    return text.split(f"## {heading}", 1)[1].split("\n## ", 1)[0]


def _normalized(text: str) -> str:
    return " ".join(text.split())
