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

    assert main(["workday", "status", "--format", "text", "--language", "zh-CN"]) == 0
    text_status = capsys.readouterr().out
    assert "工作记录状态" in text_status
    assert "today" in text_status
    assert "运行中" in text_status
    assert "local_workday_session_status" in text_status
    assert "explicit_finite_monitor_session" in text_status
    assert "只读取本地 session metadata" in text_status
    assert "Watcher burst should write one deterministic capture" not in text_status
    assert "visible_text" not in text_status

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


def test_workday_stop_can_print_chinese_text_summary(tmp_path, monkeypatch, capsys):
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
                "text-stop-day",
            ]
        )
        == 0
    )
    capsys.readouterr()

    assert (
        main(["workday", "stop", "--wait-seconds", "15", "--format", "text", "--language", "zh-CN"])
        == 0
    )
    text_summary = capsys.readouterr().out

    assert "工作概览" in text_summary
    assert "text-stop-day" in text_summary
    assert "时间范围" in text_summary
    assert "应用活动" in text_summary
    assert "效率建议" in text_summary
    assert "隐私边界" in text_summary
    assert "untrusted_observed_content" in text_summary
    assert "未调用 LLM" in text_summary
    assert "Watcher burst should write one deterministic capture" not in text_summary
    assert "visible_text" not in text_summary
    assert not (home / "workday-active.json").exists()
    assert (home / "sessions" / "text-stop-day.json").is_file()
    assert list(home.rglob("*.jsonl")) == []


def test_workday_intent_maps_chinese_phrases_without_capture_by_default(
    tmp_path, monkeypatch, capsys
):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))

    assert main(["workday", "intent", "开始记录工作"]) == 0
    start_plan = json.loads(capsys.readouterr().out)
    assert start_plan["matched"] is True
    assert start_plan["execute"] is False
    assert start_plan["intent"] == "start_workday"
    assert start_plan["command"] == ["winchronicle", "workday", "start"]
    assert start_plan["bounded"] is True
    assert start_plan["capture_surface"] == "explicit_finite_monitor_session"
    assert start_plan["trust"] == "local_workday_intent_mapping"
    assert not (home / "workday-active.json").exists()

    assert main(["workday", "intent", "停止工作并总结"]) == 0
    stop_plan = json.loads(capsys.readouterr().out)
    assert stop_plan["matched"] is True
    assert stop_plan["execute"] is False
    assert stop_plan["intent"] == "stop_and_summarize_workday"
    assert stop_plan["command"] == [
        "winchronicle",
        "workday",
        "stop",
        "--format",
        "text",
        "--language",
        "zh-CN",
    ]
    assert "observed" not in json.dumps(stop_plan).lower()


def test_workday_intent_execute_runs_existing_bounded_commands(tmp_path, monkeypatch, capsys):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    fake_watcher = _write_sleeping_watcher(tmp_path)

    assert (
        main(
            [
                "workday",
                "intent",
                "开始记录工作",
                "--execute",
                "--watcher",
                sys.executable,
                "--watcher-arg",
                str(fake_watcher),
                "--duration",
                "60",
                "--heartbeat-ms",
                "250",
                "--session-id",
                "intent-day",
            ]
        )
        == 0
    )
    started = json.loads(capsys.readouterr().out)
    assert started["active"] is True
    assert started["session_id"] == "intent-day"
    assert started["capture_surface"] == "explicit_finite_monitor_session"

    assert main(["workday", "intent", "停止工作并总结", "--execute", "--wait-seconds", "15"]) == 0
    text_summary = capsys.readouterr().out
    assert "工作概览" in text_summary
    assert "intent-day" in text_summary
    assert "untrusted_observed_content" in text_summary
    assert "Watcher burst should write one deterministic capture" not in text_summary
    assert not (home / "workday-active.json").exists()


def test_workday_intent_rejects_unknown_phrase_without_capture(tmp_path, monkeypatch, capsys):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))

    assert main(["workday", "intent", "请帮我读取剪贴板"]) == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload["matched"] is False
    assert payload["error"] == "unsupported_workday_intent"
    assert "开始记录工作" in payload["supported_phrases"]
    assert "停止工作并总结" in payload["supported_phrases"]
    assert not (home / "workday-active.json").exists()


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

    assert (
        main(["workday", "summarize", "summary-check", "--format", "text", "--language", "zh-CN"])
        == 0
    )
    text_summary = capsys.readouterr().out
    assert "工作概览" in text_summary
    assert "summary-check" in text_summary
    assert "时间范围" in text_summary
    assert "应用活动" in text_summary
    assert "效率建议" in text_summary
    assert "隐私边界" in text_summary
    assert "untrusted_observed_content" in text_summary
    assert "未调用 LLM" in text_summary
    assert "截图/OCR/剪贴板/键盘记录/音频/云上传/桌面控制/MCP 写工具" in text_summary
    assert "Watcher burst should write one deterministic capture" not in text_summary
    assert "visible_text" not in text_summary


def test_workday_doctor_reports_no_active_session_without_capture_artifacts(
    tmp_path, monkeypatch, capsys
):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))

    assert main(["workday", "doctor"]) == 0
    payload = json.loads(capsys.readouterr().out)

    assert payload["command"] == "workday doctor"
    assert payload["active"] is False
    assert payload["running"] is False
    assert payload["summary_available"] is False
    assert payload["summary_source"] is None
    assert payload["checkpoint_available"] is False
    assert payload["checkpoint_fresh"] is None
    assert payload["capture_surface"] == "explicit_finite_monitor_session"
    assert payload["screenshots_enabled"] is False
    assert payload["ocr_enabled"] is False
    assert payload["clipboard_capture_enabled"] is False
    assert payload["desktop_control_enabled"] is False
    assert {check["name"] for check in payload["checks"]} >= {
        "active_session",
        "privacy_surfaces",
        "capture_surface",
    }
    assert "observed" not in json.dumps(payload).lower()
    assert list(home.rglob("*.json")) == []


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

    assert main(["workday", "doctor", "--checkpoint-stale-seconds", "30"]) == 0
    doctor = json.loads(capsys.readouterr().out)
    assert doctor["active"] is True
    assert doctor["running"] is True
    assert doctor["summary_available"] is True
    assert doctor["summary_source"] == "checkpoint"
    assert doctor["checkpoint_available"] is True
    assert doctor["checkpoint_fresh"] is True
    assert doctor["checkpoint_age_seconds"] >= 0
    assert _check(doctor, "checkpoint_fresh")["ok"] is True
    assert _check(doctor, "runner_process")["ok"] is True
    assert "Watcher burst should write one deterministic capture" not in json.dumps(doctor)

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


def _check(payload: dict[str, object], name: str) -> dict[str, object]:
    for check in payload["checks"]:
        if check["name"] == name:
            return check
    raise AssertionError(f"missing check: {name}")
