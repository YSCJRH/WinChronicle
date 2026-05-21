import json
import sys
from pathlib import Path

from winchronicle.cli import main


ROOT = Path(__file__).resolve().parents[1]
WATCHER_FIXTURE = ROOT / "harness" / "fixtures" / "watcher" / "notepad_burst.jsonl"


def test_workday_start_stop_writes_summary_without_raw_jsonl(tmp_path, monkeypatch, capsys):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    fake_watcher = _write_sleeping_watcher(tmp_path)

    assert (
        main(
            [
                "workday",
                "start",
                "--watcher",
                sys.executable,
                "--watcher-arg",
                str(fake_watcher),
                "--duration",
                "60",
                "--heartbeat-ms",
                "250",
                "--session-id",
                "today",
            ]
        )
        == 0
    )
    started = json.loads(capsys.readouterr().out)
    assert started["active"] is True
    assert started["session_id"] == "today"
    assert started["duration_seconds"] == 60
    assert started["capture_surface"] == "explicit_finite_monitor_session"

    assert main(["workday", "status"]) == 0
    status = json.loads(capsys.readouterr().out)
    assert status["active"] is True
    assert status["session_id"] == "today"

    assert main(["workday", "stop", "--wait-seconds", "15"]) == 0
    stopped = json.loads(capsys.readouterr().out)
    assert stopped["active"] is False
    assert stopped["stopped"] is True
    assert stopped["summary_available"] is True
    assert stopped["summary"]["session_id"] == "today"
    assert stopped["summary"]["captures_written"] == 1
    assert stopped["summary"]["mode"] == "workday"
    assert stopped["summary"]["storage_policy"]["raw_watcher_jsonl_saved"] is False
    assert stopped["summary"]["storage_policy"]["html_report_contains_visible_text"] is False
    assert stopped["summary"]["storage_usage"]["html_report_bytes"] > 0
    assert stopped["summary"]["storage_usage"]["session_json_bytes"] > 0
    assert not (home / "workday-active.json").exists()
    assert list(home.rglob("*.jsonl")) == []


def test_workday_duplicate_start_is_rejected_until_stopped(tmp_path, monkeypatch, capsys):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    fake_watcher = _write_sleeping_watcher(tmp_path)

    argv = [
        "workday",
        "start",
        "--watcher",
        sys.executable,
        "--watcher-arg",
        str(fake_watcher),
        "--duration",
        "60",
        "--heartbeat-ms",
        "250",
        "--session-id",
        "duplicate-guard",
    ]
    assert main(argv) == 0
    capsys.readouterr()

    assert main(argv) == 1
    duplicate = json.loads(capsys.readouterr().out)
    assert duplicate["active"] is True
    assert duplicate["error"] == "workday_session_already_active"
    assert "observed" not in json.dumps(duplicate).lower()

    assert main(["workday", "stop", "--wait-seconds", "15"]) == 0
    capsys.readouterr()


def test_workday_summarize_reads_named_session(tmp_path, monkeypatch, capsys):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    fake_watcher = _write_sleeping_watcher(tmp_path)

    assert (
        main(
            [
                "workday",
                "start",
                "--watcher",
                sys.executable,
                "--watcher-arg",
                str(fake_watcher),
                "--duration",
                "60",
                "--heartbeat-ms",
                "250",
                "--session-id",
                "summary-check",
            ]
        )
        == 0
    )
    capsys.readouterr()
    assert main(["workday", "stop", "--wait-seconds", "15"]) == 0
    capsys.readouterr()

    assert main(["workday", "summarize", "summary-check"]) == 0
    summary = json.loads(capsys.readouterr().out)
    assert summary["session_id"] == "summary-check"
    assert summary["trust"] == "untrusted_observed_content"
    assert summary["captures_written"] == 1


def _write_sleeping_watcher(tmp_path: Path) -> Path:
    fake_watcher = tmp_path / "fake_workday_watcher.py"
    fake_watcher.write_text(
        "\n".join(
            [
                "from pathlib import Path",
                "import sys",
                "import time",
                f"sys.stdout.write(Path({str(WATCHER_FIXTURE)!r}).read_text(encoding='utf-8'))",
                "sys.stdout.flush()",
                "time.sleep(60)",
            ]
        ),
        encoding="utf-8",
    )
    return fake_watcher
