import json
from pathlib import Path

import pytest

from winchronicle.capture import load_json, normalize_fixture


ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize(
    ("fixture_path", "golden_path"),
    [
        (
            ROOT / "harness" / "fixtures" / "uia" / "notepad_basic.json",
            ROOT / "harness" / "golden" / "capture_notepad_basic.normalized.json",
        ),
        (
            ROOT / "harness" / "fixtures" / "privacy" / "secrets_visible_text.json",
            ROOT / "harness" / "golden" / "redaction_secrets_visible_text.expected.json",
        ),
    ],
)
def test_normalized_fixture_matches_golden(fixture_path, golden_path):
    actual = normalize_fixture(load_json(fixture_path))
    expected = json.loads(golden_path.read_text(encoding="utf-8"))

    assert actual == expected
