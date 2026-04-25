import json
from pathlib import Path

from winchronicle.cli import main


ROOT = Path(__file__).resolve().parents[1]


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
