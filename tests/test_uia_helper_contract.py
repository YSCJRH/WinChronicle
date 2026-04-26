import json
import subprocess
import sys
from pathlib import Path

import pytest
from jsonschema.exceptions import ValidationError

from winchronicle.capture import (
    capture_once_from_uia_helper_output,
    load_json,
    normalize_uia_helper_output,
    privacy_check_path,
)
from winchronicle.schema import validate_capture, validate_uia_helper_output
from winchronicle.storage import search_captures


ROOT = Path(__file__).resolve().parents[1]


def test_uia_helper_output_fixture_validates_and_normalizes_to_capture():
    output = load_json(ROOT / "harness" / "fixtures" / "uia-helper" / "notepad_frontmost.json")

    validate_uia_helper_output(output)
    capture = normalize_uia_helper_output(output)

    validate_capture(capture)
    assert capture["source"] == "uia_helper"
    assert capture["trigger"] == {
        "source": "win_uia_helper",
        "event_type": "capture_frontmost",
    }
    assert capture["window_meta"]["app_name"] == "Notepad"
    assert capture["screenshot"] is None
    assert capture["untrusted_observed_content"] is True


def test_uia_helper_contract_rejects_enabled_capture_surfaces():
    output = load_json(ROOT / "harness" / "fixtures" / "uia-helper" / "notepad_frontmost.json")
    output["capture_surfaces"]["screenshots"] = True

    with pytest.raises(ValidationError):
        validate_uia_helper_output(output)


def test_uia_helper_contract_rejects_unbounded_depth():
    output = load_json(ROOT / "harness" / "fixtures" / "uia-helper" / "notepad_frontmost.json")
    output["limits"]["depth"] = 81

    with pytest.raises(ValidationError):
        validate_uia_helper_output(output)


def test_uia_helper_capture_indexes_searchable_redacted_output(tmp_path, monkeypatch):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))

    result = capture_once_from_uia_helper_output(
        ROOT / "harness" / "fixtures" / "uia-helper" / "notepad_frontmost.json"
    )

    assert result.path is not None
    assert result.path.exists()
    assert result.capture is not None
    assert result.capture["source"] == "uia_helper"

    results = search_captures("helper contract", home)

    assert len(results) == 1
    assert results[0]["app_name"] == "Notepad"


def test_uia_helper_password_output_stays_redacted(tmp_path, monkeypatch):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    fixture_path = ROOT / "harness" / "fixtures" / "uia-helper" / "password_frontmost.json"

    check = privacy_check_path(fixture_path)
    result = capture_once_from_uia_helper_output(fixture_path)

    assert check.ok is True
    assert result.path is not None
    written = result.path.read_text(encoding="utf-8")
    capture = json.loads(written)
    assert "CorrectHorseBatteryStaple!" not in written
    assert capture["focused_element"]["value"] == "[REDACTED:password_field]"
    assert capture["focused_element"]["text"] == "[REDACTED:password_field]"
    assert capture["focused_element"]["value_length"] == 0
    assert capture["focused_element"]["text_length"] == 0


def test_uia_helper_smoke_script_uses_fake_helper_without_printing_capture(tmp_path):
    fake_helper = tmp_path / "fake_helper.py"
    fixture = ROOT / "harness" / "fixtures" / "uia-helper" / "notepad_frontmost.json"
    fake_helper.write_text(
        "from pathlib import Path\n"
        f"print(Path({str(fixture)!r}).read_text(encoding='utf-8'))\n",
        encoding="utf-8",
    )

    completed = subprocess.run(
        [
            sys.executable,
            "harness/scripts/run_uia_helper_smoke.py",
            "--helper",
            sys.executable,
            "--helper-arg",
            str(fake_helper),
            "--expect-app",
            "Notepad",
            "--expect-text",
            "helper contract",
        ],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )

    assert completed.returncode == 0
    assert completed.stdout.strip() == "PASS: UIA helper smoke passed"
