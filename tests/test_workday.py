import json
import sys
from pathlib import Path

from winchronicle.capture import capture_once_from_fixture
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
    assert stopped["summary_source"] == "final_result"
    assert stopped["recovered_from_capture_buffer"] is False
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


def test_workday_status_reports_checkpoint_summary_while_runner_is_active(
    tmp_path, monkeypatch, capsys
):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    fake_watcher = _write_slow_repeating_watcher(tmp_path)

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
                "--checkpoint-seconds",
                "1",
                "--session-id",
                "checkpoint-day",
            ]
        )
        == 0
    )
    capsys.readouterr()

    status = {}
    for _ in range(30):
        assert main(["workday", "status"]) == 0
        status = json.loads(capsys.readouterr().out)
        if status.get("checkpoint_available"):
            break
        _sleep(0.2)

    assert status["active"] is True
    assert status["summary_available"] is True
    assert status["checkpoint_available"] is True
    assert status["summary_source"] == "checkpoint"
    assert status["checkpoint_updated_at"]
    assert status["checkpoint_age_seconds"] >= 0
    assert status["summary"]["session_id"] == "checkpoint-day"
    assert status["summary"]["captures_written"] >= 1
    assert (home / "sessions" / "checkpoint-day.json").is_file()
    assert (home / "reports" / "checkpoint-day.html").is_file()

    assert main(["workday", "stop", "--wait-seconds", "15"]) == 0
    capsys.readouterr()


def test_workday_stop_recovers_summary_from_capture_buffer_when_result_is_missing(
    tmp_path, monkeypatch, capsys
):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    result = capture_once_from_fixture(
        ROOT / "harness" / "fixtures" / "uia" / "terminal_error.json",
        home,
    )
    assert result.path is not None

    logs = home / "logs"
    logs.mkdir(parents=True, exist_ok=True)
    active = {
        "schema_version": 1,
        "active": True,
        "session_id": "fallback-day",
        "pid": 0,
        "started_at": "2026-04-25T00:00:00+08:00",
        "duration_seconds": 43200,
        "state_home": str(home),
        "stop_file": str(logs / "fallback-day.stop"),
        "result_file": str(logs / "missing-result.json"),
        "stdout_path": str(logs / "fallback-day.stdout.json"),
        "stderr_path": str(logs / "fallback-day.stderr.txt"),
        "trust": "local_workday_session_status",
        "capture_surface": "explicit_finite_monitor_session",
        "bounded": True,
    }
    (home / "workday-active.json").write_text(
        json.dumps(active, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    assert main(["workday", "stop", "--wait-seconds", "0"]) == 0
    stopped = json.loads(capsys.readouterr().out)

    assert stopped["active"] is False
    assert stopped["stopped"] is True
    assert stopped["summary_available"] is True
    assert stopped["summary_source"] == "capture_buffer_recovery"
    assert stopped["recovered_from_capture_buffer"] is True
    assert stopped["summary"]["session_id"] == "fallback-day"
    assert stopped["summary"]["mode"] == "workday"
    assert stopped["summary"]["captures_written"] == 1
    assert stopped["summary"]["trust"] == "untrusted_observed_content"
    assert stopped["summary"]["storage_policy"]["raw_watcher_jsonl_saved"] is False
    assert stopped["summary"]["storage_policy"]["html_report_contains_visible_text"] is False
    assert (home / "sessions" / "fallback-day.json").is_file()
    assert (home / "reports" / "fallback-day.html").is_file()
    assert not (home / "workday-active.json").exists()
    assert list(home.rglob("*.jsonl")) == []


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


def _write_slow_repeating_watcher(tmp_path: Path) -> Path:
    fake_watcher = tmp_path / "fake_slow_workday_watcher.py"
    fake_watcher.write_text(
        "\n".join(
            [
                "from pathlib import Path",
                "import sys",
                "import time",
                f"lines = Path({str(WATCHER_FIXTURE)!r}).read_text(encoding='utf-8').splitlines()",
                "for line in lines:",
                "    print(line, flush=True)",
                "    time.sleep(0.2)",
                "time.sleep(60)",
            ]
        ),
        encoding="utf-8",
    )
    return fake_watcher


def _sleep(seconds: float) -> None:
    import time

    time.sleep(seconds)
