from pathlib import Path

from winchronicle.capture import load_json, normalize_fixture
from winchronicle.schema import validate_capture


ROOT = Path(__file__).resolve().parents[1]


def test_notepad_fixture_normalizes_to_schema_valid_capture():
    fixture = load_json(ROOT / "harness" / "fixtures" / "uia" / "notepad_basic.json")

    capture = normalize_fixture(fixture)

    validate_capture(capture)
    assert capture["schema_version"] == 1
    assert capture["platform"] == "windows"
    assert capture["source"] == "fixture"
    assert capture["untrusted_observed_content"] is True
    assert capture["screenshot"] is None
