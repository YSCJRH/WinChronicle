from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVALS = ROOT / "benchmarks" / "evals"
FIXTURES = EVALS / "fixtures"
EXPECTED = EVALS / "expected"

REQUIRED_SCENARIOS = (
    "terminal_test_failure",
    "vscode_metadata_context",
    "browser_research_context",
    "github_pr_review_context",
    "monitor_session_summary",
    "prompt_injection_resistance",
    "secret_redaction_regression",
)
REQUIRED_FIXTURE_KEYS = {"id", "scenario", "source", "trust", "input", "expected"}
REQUIRED_INPUT_KEYS = {
    "app",
    "window_title",
    "focused_element",
    "visible_text",
    "source_ids",
}
REQUIRED_EXPECTED_KEYS = {
    "trust",
    "redaction_required",
    "redacted",
    "must_not_leak",
    "must_include_limitations",
    "confidence_band",
    "should_help_agent_recover",
    "forbidden_behaviors",
    "safe_exposed_summary",
    "expected_agent_recovery",
}
SECRET_LIKE_RE = re.compile(
    r"(ghp_[A-Za-z0-9_]+|xoxb-[A-Za-z0-9-]+|eyJ[A-Za-z0-9._-]+|"
    r"-----BEGIN PRIVATE KEY-----|token=[A-Za-z0-9_-]+)"
)
SYNTHETIC_MARKERS = ("synthetic", "eval", "canary", "example.invalid")


def main() -> int:
    try:
        scenarios = [_validate_scenario(scenario) for scenario in REQUIRED_SCENARIOS]
    except AssertionError as exc:
        print(f"FAIL: {exc}")
        return 1

    for scenario in scenarios:
        band = scenario["expected"]["confidence_band"]
        print(
            "PASS:",
            scenario["scenario"],
            f"confidence_band={band[0]}-{band[1]}",
            f"redaction_required={scenario['expected']['redaction_required']}",
        )
    print(f"PASS: validated {len(scenarios)} synthetic eval scenarios")
    return 0


def _validate_scenario(scenario: str) -> dict[str, Any]:
    fixture_path = FIXTURES / f"{scenario}.json"
    expected_path = EXPECTED / f"{scenario}.expected.json"
    assert fixture_path.is_file(), f"missing fixture {fixture_path}"
    assert expected_path.is_file(), f"missing expected file {expected_path}"

    fixture = _load_json(fixture_path)
    expected = _load_json(expected_path)
    assert set(fixture) >= REQUIRED_FIXTURE_KEYS, f"{scenario} fixture keys incomplete"
    assert set(fixture["input"]) >= REQUIRED_INPUT_KEYS, f"{scenario} input keys incomplete"
    assert set(fixture["expected"]) >= REQUIRED_EXPECTED_KEYS, (
        f"{scenario} expected keys incomplete"
    )
    assert fixture["expected"] == expected, f"{scenario} embedded expected mismatch"
    assert fixture["id"] == scenario
    assert fixture["scenario"] == scenario
    assert fixture["source"] == "synthetic_fixture"
    assert fixture["trust"] == "untrusted_observed_content"
    assert expected["trust"] == "untrusted_observed_content"
    _validate_confidence(scenario, expected["confidence_band"])
    _validate_no_safe_leakage(scenario, fixture, expected)
    return fixture


def _validate_confidence(scenario: str, band: list[float]) -> None:
    assert isinstance(band, list) and len(band) == 2, f"{scenario} confidence band invalid"
    assert 0.0 <= band[0] <= band[1] <= 0.85, f"{scenario} confidence band out of range"


def _validate_no_safe_leakage(
    scenario: str, fixture: dict[str, Any], expected: dict[str, Any]
) -> None:
    exposed_text = json.dumps(
        {
            "safe_exposed_summary": expected.get("safe_exposed_summary", ""),
            "expected_agent_recovery": expected.get("expected_agent_recovery", ""),
            "metadata_notes": expected.get("metadata_notes", ""),
            "source_ids": fixture["input"]["source_ids"],
        },
        sort_keys=True,
    )
    for raw_value in expected["must_not_leak"]:
        assert raw_value not in exposed_text, f"{scenario} leaks {raw_value!r}"

    for source_id in fixture["input"]["source_ids"]:
        assert not SECRET_LIKE_RE.search(source_id), f"{scenario} has secret-like source id"

    combined = json.dumps(fixture, sort_keys=True)
    for match in SECRET_LIKE_RE.findall(combined):
        if match == "-----BEGIN PRIVATE KEY-----":
            assert "winchronicle_eval_canary_private_key" in combined
            continue
        assert any(marker in match.lower() for marker in SYNTHETIC_MARKERS), (
            f"{scenario} has non-synthetic secret-like value {match!r}"
        )


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    raise SystemExit(main())
