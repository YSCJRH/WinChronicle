import json
import sys
from pathlib import Path

from winchronicle.cli import main


ROOT = Path(__file__).resolve().parents[1]

SEARCH_RESULT_KEYS = {"timestamp", "app_name", "title", "snippet", "path"}


def test_search_captures_cli_returns_indexed_fixture(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("WINCHRONICLE_HOME", str(tmp_path / "state"))

    assert main(
        [
            "capture-once",
            "--fixture",
            str(ROOT / "harness" / "fixtures" / "uia" / "terminal_error.json"),
        ]
    ) == 0
    capsys.readouterr()

    assert main(["search-captures", "AssertionError"]) == 0
    output = capsys.readouterr().out
    results = json.loads(output)

    assert len(results) == 1
    assert results[0]["app_name"] == "Windows Terminal"


def test_search_captures_cli_returns_deterministic_json_shape(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("WINCHRONICLE_HOME", str(tmp_path / "state"))
    scenarios = [
        ("terminal_error.json", "AssertionError", "Windows Terminal"),
        ("vscode_editor.json", "written_json", "Visual Studio Code"),
        ("edge_browser.json", "OpenChronicle", "Microsoft Edge"),
    ]

    for fixture_name, query, expected_app in scenarios:
        assert main(
            [
                "capture-once",
                "--fixture",
                str(ROOT / "harness" / "fixtures" / "uia" / fixture_name),
            ]
        ) == 0
        capsys.readouterr()

        assert main(["search-captures", query]) == 0
        output = capsys.readouterr().out
        results = json.loads(output)

        assert len(results) == 1
        assert set(results[0]) == SEARCH_RESULT_KEYS
        assert results[0]["app_name"] == expected_app
        assert query.lower() in results[0]["snippet"].lower()


def test_capture_frontmost_cli_uses_fake_helper_output(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("WINCHRONICLE_HOME", str(tmp_path / "state"))
    fake_helper = tmp_path / "fake_helper.py"
    fixture = ROOT / "harness" / "fixtures" / "uia-helper" / "notepad_frontmost.json"
    fake_helper.write_text(
        "from pathlib import Path\n"
        f"print(Path({str(fixture)!r}).read_text(encoding='utf-8'))\n",
        encoding="utf-8",
    )

    assert main(
        [
            "capture-frontmost",
            "--helper",
            sys.executable,
            "--helper-arg",
            str(fake_helper),
            "--depth",
            "2",
        ]
    ) == 0
    capture_path = Path(capsys.readouterr().out.strip())
    capture = json.loads(capture_path.read_text(encoding="utf-8"))

    assert capture["source"] == "uia_helper"
    assert capture["window_meta"]["app_name"] == "Notepad"
    assert capture["trigger"]["event_type"] == "capture_frontmost"

    assert main(["search-captures", "helper contract"]) == 0
    results = json.loads(capsys.readouterr().out)
    assert len(results) == 1
    assert results[0]["app_name"] == "Notepad"


def test_capture_frontmost_cli_skips_when_helper_returns_no_capture(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("WINCHRONICLE_HOME", str(tmp_path / "state"))
    fake_helper = tmp_path / "fake_skip_helper.py"
    fake_helper.write_text("", encoding="utf-8")

    assert main(
        [
            "capture-frontmost",
            "--helper",
            sys.executable,
            "--helper-arg",
            str(fake_helper),
        ]
    ) == 0

    assert capsys.readouterr().out.strip() == "SKIPPED: helper returned no capture"
    assert not (tmp_path / "state" / "capture-buffer").exists()


def test_capture_frontmost_cli_reports_invalid_helper_json_without_stderr_leak(
    tmp_path, monkeypatch, capsys
):
    monkeypatch.setenv("WINCHRONICLE_HOME", str(tmp_path / "state"))
    fake_helper = tmp_path / "fake_invalid_helper.py"
    fake_helper.write_text(
        "import sys\n"
        "print('observed secret must not echo', file=sys.stderr)\n"
        "print('{not json')\n",
        encoding="utf-8",
    )

    assert main(
        [
            "capture-frontmost",
            "--helper",
            sys.executable,
            "--helper-arg",
            str(fake_helper),
        ]
    ) == 1

    output = capsys.readouterr().out
    assert output.strip() == "ERROR: helper returned invalid JSON"
    assert "observed secret" not in output


def test_capture_frontmost_cli_reports_nonzero_helper_without_stderr_leak(
    tmp_path, monkeypatch, capsys
):
    monkeypatch.setenv("WINCHRONICLE_HOME", str(tmp_path / "state"))
    fake_helper = tmp_path / "fake_failed_helper.py"
    fake_helper.write_text(
        "import sys\n"
        "print('visible password must not echo', file=sys.stderr)\n"
        "raise SystemExit(9)\n",
        encoding="utf-8",
    )

    assert main(
        [
            "capture-frontmost",
            "--helper",
            sys.executable,
            "--helper-arg",
            str(fake_helper),
        ]
    ) == 1

    output = capsys.readouterr().out
    assert output.strip() == "ERROR: helper failed with exit code 9"
    assert "visible password" not in output
