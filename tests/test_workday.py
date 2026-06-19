import json
import sys
from pathlib import Path

from winchronicle.capture import capture_once_from_fixture
from winchronicle.cli import main
from winchronicle.redaction import scan_for_unredacted_secrets
from winchronicle.workday import format_workday_text_summary


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
                "--checkpoint-seconds",
                "1",
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
    assert "运行中" in text_status
    assert "正在记录今天的工作" in text_status
    assert "最长记录" in text_status
    assert "停止工作并总结" in text_status
    assert "会话:" not in text_status
    assert "capture_surface" not in text_status
    assert "local_workday_session_status" not in text_status
    assert "explicit_finite_monitor_session" not in text_status
    assert "只读取本地 session metadata" in text_status
    assert "Watcher burst should write one deterministic capture" not in text_status
    assert "visible_text" not in text_status
    _wait_for_checkpoint(capsys)

    assert main(["workday", "stop", "--wait-seconds", "15"]) == 0
    stopped = json.loads(capsys.readouterr().out)
    assert stopped["active"] is False
    assert stopped["stopped"] is True
    assert stopped["summary_available"] is True
    assert stopped["summary_source"] in {"final_result", "checkpoint", "capture_buffer_recovery"}
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

    assert "今日工作复盘" in text_summary
    assert "今日工作结论" in text_summary
    assert "工作进行情况" in text_summary
    assert "明天改进建议" in text_summary
    assert "可考虑方向" in text_summary
    assert "待确认问题" not in text_summary
    assert "数据依据" not in text_summary
    assert "隐私边界" not in text_summary
    assert "untrusted_observed_content" not in text_summary
    assert "不调用 LLM" not in text_summary
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


def test_workday_intent_maps_short_user_phrases_without_capture_by_default(
    tmp_path, monkeypatch, capsys
):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))

    assert main(["workday", "intent", "开始工作"]) == 0
    start_plan = json.loads(capsys.readouterr().out)
    assert start_plan["matched"] is True
    assert start_plan["execute"] is False
    assert start_plan["intent"] == "start_workday"
    assert start_plan["command"] == ["winchronicle", "workday", "start"]
    assert start_plan["capture_surface"] == "explicit_finite_monitor_session"
    assert not (home / "workday-active.json").exists()

    assert main(["workday", "intent", "结束工作并总结"]) == 0
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
    assert not (home / "workday-active.json").exists()


def test_workday_intent_accepts_natural_today_aliases_without_capture(
    tmp_path, monkeypatch, capsys
):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))

    for phrase in ["开始记录今天的工作", "开始记录今天工作"]:
        assert main(["workday", "intent", phrase]) == 0
        start_plan = json.loads(capsys.readouterr().out)
        assert start_plan["matched"] is True
        assert start_plan["execute"] is False
        assert start_plan["intent"] == "start_workday"
        assert start_plan["command"] == ["winchronicle", "workday", "start"]
        assert start_plan["capture_surface"] == "explicit_finite_monitor_session"
        assert not (home / "workday-active.json").exists()

    assert main(["workday", "intent", "结束今天的工作并总结"]) == 0
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
    assert not (home / "workday-active.json").exists()


def test_workday_intent_maps_status_phrase_without_capture_by_default(
    tmp_path, monkeypatch, capsys
):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))

    assert main(["workday", "intent", "查看工作记录状态"]) == 0
    status_plan = json.loads(capsys.readouterr().out)
    assert status_plan["matched"] is True
    assert status_plan["execute"] is False
    assert status_plan["intent"] == "status_workday"
    assert status_plan["command"] == [
        "winchronicle",
        "workday",
        "status",
        "--format",
        "text",
        "--language",
        "zh-CN",
    ]
    assert status_plan["capture_surface"] == "none"
    assert status_plan["bounded"] is True
    assert status_plan["trust"] == "local_workday_intent_mapping"
    assert not (home / "workday-active.json").exists()


def test_workday_intent_execute_status_phrase_prints_text_status_without_capture(
    tmp_path, monkeypatch, capsys
):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))

    assert main(["workday", "intent", "查看工作记录状态", "--execute"]) == 0
    text_status = capsys.readouterr().out
    assert "工作记录状态" in text_status
    assert "当前没有在记录" in text_status
    assert "开始记录工作" in text_status
    assert "会话: 无" not in text_status
    assert "visible_text" not in text_status
    assert "focused_text" not in text_status
    assert not (home / "workday-active.json").exists()


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
    start_text = capsys.readouterr().out
    assert "已开始记录今天的工作" in start_text
    assert "intent-day" in start_text
    assert "查看工作记录状态" in start_text
    assert "停止工作并总结" in start_text
    assert "capture_surface" not in start_text
    assert "local_workday_session_status" not in start_text
    assert "visible_text" not in start_text

    assert main(["workday", "intent", "停止工作并总结", "--execute", "--wait-seconds", "15"]) == 0
    text_summary = capsys.readouterr().out
    assert "今日工作复盘" in text_summary
    assert "今日工作结论" in text_summary
    assert "工作进行情况" in text_summary
    assert "明天改进建议" in text_summary
    assert "可考虑方向" in text_summary
    assert "数据依据" not in text_summary
    assert "工作概览" not in text_summary
    assert "untrusted_observed_content" not in text_summary
    assert "Watcher burst should write one deterministic capture" not in text_summary
    assert not (home / "workday-active.json").exists()


def test_workday_intent_execute_duplicate_start_prints_human_text(
    tmp_path, monkeypatch, capsys
):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    fake_watcher = _write_sleeping_watcher(tmp_path)

    argv = [
        "workday",
        "intent",
        "开始记录今天的工作",
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
        "duplicate-intent",
    ]

    assert main(argv) == 0
    capsys.readouterr()

    assert main(argv) == 1
    duplicate_text = capsys.readouterr().out
    assert "已经在记录中" in duplicate_text
    assert "duplicate-intent" in duplicate_text
    assert "停止工作并总结" in duplicate_text
    assert "workday_session_already_active" not in duplicate_text
    assert "capture_surface" not in duplicate_text
    assert "visible_text" not in duplicate_text

    assert main(["workday", "stop", "--wait-seconds", "15"]) == 0
    capsys.readouterr()


def test_workday_intent_execute_stop_without_active_session_prints_human_text(
    tmp_path, monkeypatch, capsys
):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))

    assert main(["workday", "intent", "停止工作并总结", "--execute", "--wait-seconds", "0"]) == 0
    stop_text = capsys.readouterr().out
    assert "当前没有在记录" in stop_text
    assert "无需结束" in stop_text
    assert "开始记录工作" in stop_text
    assert "summary_available" not in stop_text
    assert "capture_surface" not in stop_text
    assert "visible_text" not in stop_text
    assert not (home / "workday-active.json").exists()


def test_workday_intent_start_phrase_can_carry_focus_note(tmp_path, monkeypatch, capsys):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    fake_watcher = _write_sleeping_watcher(tmp_path)

    assert (
        main(
            [
                "workday",
                "intent",
                "开始记录工作：今天主要做论文整理和项目A需求文档",
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
                "focus-day",
            ]
        )
        == 0
    )
    start_text = capsys.readouterr().out
    assert "已开始记录今天的工作" in start_text
    assert "今天主要做论文整理和项目A需求文档" in start_text
    assert "operator_focus" not in start_text
    assert "capture_surface" not in start_text

    assert main(["workday", "intent", "停止工作并总结", "--execute", "--wait-seconds", "15"]) == 0
    text_summary = capsys.readouterr().out
    assert "今日关注事项" in text_summary
    assert "论文整理和项目A需求文档" in text_summary
    assert not (home / "workday-active.json").exists()


def test_workday_intent_redacts_secret_like_focus_note_before_storage(
    tmp_path, monkeypatch, capsys
):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    fake_watcher = _write_sleeping_watcher(tmp_path)
    secret_focus = "今天排查 OPENAI_API_KEY=sk-winchroniclecanary0123456789abcd"

    assert (
        main(
            [
                "workday",
                "intent",
                f"开始记录工作：{secret_focus}",
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
                "redacted-focus-day",
            ]
        )
        == 0
    )
    start_text = capsys.readouterr().out
    active_text = (home / "workday-active.json").read_text(encoding="utf-8")

    assert "sk-winchroniclecanary0123456789abcd" not in start_text
    assert "sk-winchroniclecanary0123456789abcd" not in active_text
    assert "[REDACTED:api_key]" in start_text
    assert scan_for_unredacted_secrets(start_text) == []
    assert scan_for_unredacted_secrets(active_text) == []

    assert main(["workday", "intent", "停止工作并总结", "--execute", "--wait-seconds", "15"]) == 0
    text_summary = capsys.readouterr().out
    session_text = (home / "sessions" / "redacted-focus-day.json").read_text(encoding="utf-8")

    assert "sk-winchroniclecanary0123456789abcd" not in text_summary
    assert "sk-winchroniclecanary0123456789abcd" not in session_text
    assert "[REDACTED:api_key]" in text_summary
    assert scan_for_unredacted_secrets(text_summary) == []
    assert scan_for_unredacted_secrets(session_text) == []
    assert not (home / "workday-active.json").exists()


def test_workday_intent_rejects_unknown_phrase_without_capture(tmp_path, monkeypatch, capsys):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))

    assert main(["workday", "intent", "请帮我读取剪贴板"]) == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload["matched"] is False
    assert payload["error"] == "unsupported_workday_intent"
    assert "开始记录工作" in payload["supported_phrases"]
    assert "开始工作" in payload["supported_phrases"]
    assert "停止工作并总结" in payload["supported_phrases"]
    assert "结束工作并总结" in payload["supported_phrases"]
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
                "--checkpoint-seconds",
                "1",
                "--session-id",
                "summary-check",
            ]
        )
        == 0
    )
    capsys.readouterr()
    _wait_for_checkpoint(capsys)
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
    assert "今日工作复盘" in text_summary
    assert "今日工作结论" in text_summary
    assert "工作进行情况" in text_summary
    assert "明天改进建议" in text_summary
    assert "可考虑方向" in text_summary
    assert "待确认问题" not in text_summary
    assert "数据依据" not in text_summary
    assert "隐私边界" not in text_summary
    assert "untrusted_observed_content" not in text_summary
    assert "不调用 LLM" not in text_summary
    assert "截图/OCR/剪贴板/键盘记录/音频/云上传/桌面控制/MCP 写工具" not in text_summary
    assert "Watcher burst should write one deterministic capture" not in text_summary
    assert "visible_text" not in text_summary

    assert (
        main(
            [
                "workday",
                "summarize",
                "summary-check",
                "--format",
                "text",
                "--language",
                "zh-CN",
                "--summary-style",
                "technical",
            ]
        )
        == 0
    )
    technical_summary = capsys.readouterr().out
    assert "工作概览" in technical_summary
    assert "应用活动" in technical_summary
    assert "数据看板" in technical_summary

    assert (
        main(
            [
                "workday",
                "summarize",
                "summary-check",
                "--format",
                "text",
                "--language",
                "zh-CN",
                "--note",
                "今天确认完成了工作日总结文案校准。",
            ]
        )
        == 0
    )
    noted_summary = capsys.readouterr().out
    assert "用户确认事实" in noted_summary
    assert "今天确认完成了工作日总结文案校准" in noted_summary


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


def test_workday_runner_failure_writes_checkpoint_fallback_result(tmp_path, monkeypatch, capsys):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    fake_watcher = _write_checkpoint_then_bad_watcher(tmp_path)
    logs = home / "logs"
    logs.mkdir(parents=True, exist_ok=True)
    result_file = logs / "runner-fallback.result.json"
    checkpoint_file = logs / "runner-fallback.checkpoint.json"

    assert (
        main(
            [
                "workday",
                "run",
                "--session-id",
                "runner-fallback",
                "--stop-file",
                str(logs / "runner-fallback.stop"),
                "--result-file",
                str(result_file),
                "--checkpoint-file",
                str(checkpoint_file),
                "--watcher-arg",
                sys.executable,
                "--watcher-arg",
                str(fake_watcher),
                "--duration",
                "5",
                "--checkpoint-seconds",
                "1",
            ]
        )
        == 0
    )
    payload = json.loads(capsys.readouterr().out)

    assert payload["summary_available"] is True
    assert payload["summary_source"] == "checkpoint"
    assert payload["runner_status"] == "failed_recovered"
    assert payload["runner_error"] == "workday_runner_failed_before_final_result"
    assert payload["summary"]["session_id"] == "runner-fallback"
    assert result_file.is_file()
    assert checkpoint_file.is_file()


def test_workday_text_summary_explains_error_signals_without_observed_text():
    session = {
        "session_id": "explain-errors",
        "mode": "workday",
        "trust": "untrusted_observed_content",
        "captures_written": 3,
        "duplicates_skipped": 0,
        "denylisted_skipped": 0,
        "excluded_skipped": 0,
        "started_at": "2026-04-25T13:45:00+08:00",
        "ended_at": "2026-04-25T14:00:00+08:00",
        "duration_seconds": 900,
        "source_capture_paths": [],
        "app_segments": [],
        "suggestions": ["Error-like text appeared in the session; inspect the related capture before continuing."],
        "storage_policy": {
            "raw_watcher_jsonl_saved": False,
            "html_report_contains_visible_text": False,
            "max_app_segments": 500,
            "source_capture_paths_limit": 1000,
        },
        "storage_usage": {"session_json_bytes": 2048, "html_report_bytes": 1024},
        "error_signals": {
            "schema_version": 1,
            "trust": "untrusted_observed_content",
            "contains_observed_text": False,
            "total_count": 2,
            "sample_limit": 25,
            "by_app": [{"app_name": "Codex", "count": 2}],
            "by_field": [{"field": "visible_text", "count": 2}],
            "by_keyword": [{"keyword": "failed", "count": 2}],
            "time_buckets": [{"bucket_start": "2026-04-25T13:45+08:00", "count": 2}],
            "samples": [
                {
                    "timestamp": "2026-04-25T13:45:00+08:00",
                    "time_bucket": "2026-04-25T13:45+08:00",
                    "app_name": "Codex",
                    "fields": ["visible_text"],
                    "keywords": ["failed"],
                    "source_id": "capture-abc123def456",
                }
            ],
        },
    }

    text = format_workday_text_summary(session, project_snapshot={"projects": []})

    assert "今日工作复盘" in text
    assert "复盘小提醒" in text
    assert "不代表工作质量" in text
    assert "2 次错误" not in text
    assert "真正影响推进" in text
    assert "调试或异常线索" in text
    assert "错误或失败相关提示" not in text
    assert "是否已解决需要确认" not in text
    assert "命中次数: 2" not in text
    assert "Codex: 2" not in text
    assert "failed: 2" not in text
    assert "capture-abc123def456" not in text
    assert "test_payment_flow" not in text
    assert "ghp_winchroniclecanary1234567890ABCD" not in text

    technical_text = format_workday_text_summary(
        session,
        project_snapshot={"projects": []},
        summary_style="technical",
    )

    assert "错误信号" in technical_text
    assert "命中次数: 2" in technical_text
    assert "Codex: 2" in technical_text
    assert "failed: 2" in technical_text
    assert "capture-abc123def456" in technical_text
    assert "observed text" not in technical_text
    assert "test_payment_flow" not in technical_text
    assert "ghp_winchroniclecanary1234567890ABCD" not in technical_text


def test_workday_human_summary_does_not_make_error_counts_scary():
    session = {
        "session_id": "error-tone",
        "mode": "workday",
        "trust": "untrusted_observed_content",
        "captures_written": 20,
        "duplicates_skipped": 0,
        "denylisted_skipped": 0,
        "excluded_skipped": 0,
        "started_at": "2026-06-08T06:00:00+08:00",
        "ended_at": "2026-06-08T07:00:00+08:00",
        "duration_seconds": 3600,
        "source_capture_paths": [],
        "app_segments": [{"app_name": "Codex", "title": "Codex", "capture_count": 20}],
        "suggestions": [],
        "storage_policy": {
            "raw_watcher_jsonl_saved": False,
            "html_report_contains_visible_text": False,
            "max_app_segments": 500,
            "source_capture_paths_limit": 1000,
        },
        "storage_usage": {"session_json_bytes": 2048, "html_report_bytes": 1024},
        "error_signals": {"total_count": 164},
    }

    text = format_workday_text_summary(session, project_snapshot={"projects": []})

    assert "164 次错误" not in text
    assert "阻塞线索" not in text
    assert "未收尾的问题分支" not in text
    assert "错误统计" not in text
    assert "命中次数" not in text
    assert "复盘小提醒" in text
    assert "需要留意的事项" not in text
    assert "真实问题数量" not in text
    assert "不代表工作质量" in text
    assert "真正影响推进" in text
    assert "只需要确认" not in text
    assert "明天先看真正影响推进的一两件事" in text
    assert "错误或失败相关提示" not in text
    assert "已解决 / 未解决 / 误报" not in text


def test_workday_text_summary_includes_allowlisted_project_metadata_only():
    session = {
        "session_id": "useful-summary",
        "mode": "workday",
        "trust": "untrusted_observed_content",
        "captures_written": 12,
        "duplicates_skipped": 1,
        "denylisted_skipped": 0,
        "excluded_skipped": 0,
        "started_at": "2026-04-25T09:00:00+08:00",
        "ended_at": "2026-04-25T10:00:00+08:00",
        "duration_seconds": 3600,
        "source_capture_paths": [],
        "app_segments": [
            {"app_name": "Codex", "title": "WinChronicle", "capture_count": 8},
            {"app_name": "Chrome", "title": "Docs", "capture_count": 4},
        ],
        "suggestions": ["Multiple apps appeared in the session; review context switches."],
        "storage_policy": {
            "raw_watcher_jsonl_saved": False,
            "html_report_contains_visible_text": False,
            "max_app_segments": 500,
            "source_capture_paths_limit": 1000,
        },
        "storage_usage": {"session_json_bytes": 2048, "html_report_bytes": 1024},
        "error_signals": {"total_count": 0},
    }
    project_snapshot = {
        "projects": [
            {
                "name": "WinChronicle",
                "exists": True,
                "is_git_repo": True,
                "branch": "main",
                "changed_file_count": 2,
                "changed_files": ["src/winchronicle/workday.py", "tests/test_workday.py"],
                "diff_stat": {"insertions": 30, "deletions": 4},
                "recent_commits": [{"hash": "abc1234", "subject": "Improve workday summary"}],
            }
        ]
    }

    text = format_workday_text_summary(
        session,
        project_snapshot=project_snapshot,
        confirmation_notes=["今天主要在改进工作日总结质量。"],
    )

    assert "今日工作复盘" in text
    assert "今日工作结论" in text
    assert "记录推断" not in text
    assert "主要推进了 WinChronicle" in text
    assert "根据本地记录" in text
    assert "工作进行情况" in text
    assert "正在推进" in text
    assert "用户确认事实" in text
    assert "明天改进建议" in text
    assert "可考虑方向" in text
    assert "待确认问题" not in text
    assert "数据依据" not in text
    assert "隐私边界" not in text
    assert "今天主要在改进工作日总结质量" in text
    assert "SECRET_CONTENT_SHOULD_NOT_APPEAR" not in text
    assert "full diff" not in text
    assert "不读取文件内容" not in text
    assert text.index("今日工作结论") < text.index("可考虑方向")


def test_workday_text_summary_turns_unregistered_app_activity_into_questions():
    session = {
        "session_id": "mixed-work",
        "mode": "workday",
        "trust": "untrusted_observed_content",
        "operator_focus": ["今天主要做 WinChronicle、论文整理和项目A需求文档"],
        "captures_written": 30,
        "duplicates_skipped": 1,
        "denylisted_skipped": 0,
        "excluded_skipped": 0,
        "started_at": "2026-04-25T09:00:00+08:00",
        "ended_at": "2026-04-25T11:00:00+08:00",
        "duration_seconds": 7200,
        "source_capture_paths": [],
        "app_segments": [
            {"app_name": "Codex", "title": "WinChronicle", "capture_count": 12},
            {"app_name": "WINWORD", "title": "Document", "capture_count": 9},
            {"app_name": "chrome", "title": "Research", "capture_count": 7},
            {"app_name": "explorer", "title": "Folder", "capture_count": 2},
        ],
        "suggestions": [],
        "storage_policy": {
            "raw_watcher_jsonl_saved": False,
            "html_report_contains_visible_text": False,
            "max_app_segments": 500,
            "source_capture_paths_limit": 1000,
        },
        "storage_usage": {"session_json_bytes": 2048, "html_report_bytes": 1024},
        "error_signals": {"total_count": 0},
    }
    project_snapshot = {
        "projects": [
            {
                "name": "WinChronicle",
                "exists": True,
                "is_git_repo": True,
                "branch": "main",
                "changed_file_count": 2,
                "changed_files": ["src/winchronicle/workday.py", "tests/test_workday.py"],
                "diff_stat": {"insertions": 30, "deletions": 4},
                "recent_commits": [],
            }
        ]
    }

    text = format_workday_text_summary(session, project_snapshot=project_snapshot)

    assert "今日关注事项" in text
    assert "论文整理和项目A需求文档" in text
    assert "还较多使用了" in text
    assert "Word 文档" in text
    assert "浏览器" in text
    assert "文件管理器" in text
    assert "可考虑方向" in text
    assert "可能对应其它项目、写作、调研或沟通" in text
    assert "其它工作线索" not in text
    assert "暂时无法判断具体属于哪个项目" not in text
    assert "如果希望下次按项目呈现这些活动" in text
    assert "先补充相关项目文件夹" not in text
    assert "这些应用活动是否对应其它项目、写作、调研或沟通工作" not in text
    assert "需要人工确认" not in text
    assert "Document" not in text
    assert "Research" not in text


def test_workday_text_summary_adds_title_derived_workstream_clues_without_raw_titles():
    session = {
        "session_id": "title-clues",
        "mode": "workday",
        "trust": "untrusted_observed_content",
        "captures_written": 20,
        "duplicates_skipped": 0,
        "denylisted_skipped": 0,
        "excluded_skipped": 0,
        "started_at": "2026-06-08T06:00:00+08:00",
        "ended_at": "2026-06-08T07:00:00+08:00",
        "duration_seconds": 3600,
        "source_capture_paths": [],
        "app_segments": [
            {"app_name": "chrome", "title": "Codex 订阅额度问题 - Google Chrome", "capture_count": 6},
            {"app_name": "chrome", "title": "NC论文优化 - Excel 数据审查与分析 - Google Chrome", "capture_count": 5},
            {"app_name": "wechatdevtools", "title": "微信开发者工具 Stable", "capture_count": 4},
            {"app_name": "chrome", "title": "Inbox (95) - user@example.com - Gmail - Google Chrome", "capture_count": 3},
        ],
        "suggestions": [],
        "storage_policy": {
            "raw_watcher_jsonl_saved": False,
            "html_report_contains_visible_text": False,
            "max_app_segments": 500,
            "source_capture_paths_limit": 1000,
        },
        "storage_usage": {"session_json_bytes": 2048, "html_report_bytes": 1024},
        "error_signals": {"total_count": 0},
    }

    text = format_workday_text_summary(session, project_snapshot={"projects": []})

    assert "今日工作线索" in text
    assert "Codex/OpenAI 相关调研或工具使用" in text
    assert "论文、Excel 或数据审查工作" in text
    assert "微信/小程序相关配置或开发" in text
    assert "邮箱、账号或服务配置处理" in text
    assert "user@example.com" not in text
    assert "Inbox (95)" not in text
    assert "Google Chrome" not in text


def test_workday_human_summary_avoids_project_jargon_in_default_text():
    session = {
        "session_id": "plain-project-language",
        "mode": "workday",
        "trust": "untrusted_observed_content",
        "captures_written": 30,
        "duplicates_skipped": 0,
        "denylisted_skipped": 0,
        "excluded_skipped": 0,
        "started_at": "2026-06-08T06:00:00+08:00",
        "ended_at": "2026-06-08T07:00:00+08:00",
        "duration_seconds": 3600,
        "source_capture_paths": [],
        "app_segments": [
            {"app_name": "chrome", "title": "Codex 订阅额度问题 - Google Chrome", "capture_count": 20},
            {"app_name": "Codex", "title": "Codex", "capture_count": 10},
        ],
        "suggestions": [],
        "storage_policy": {
            "raw_watcher_jsonl_saved": False,
            "html_report_contains_visible_text": False,
            "max_app_segments": 500,
            "source_capture_paths_limit": 1000,
        },
        "storage_usage": {"session_json_bytes": 2048, "html_report_bytes": 1024},
        "error_signals": {"total_count": 0},
    }
    project_snapshot = {
        "projects": [
            {
                "name": "WinChronicle",
                "exists": True,
                "is_git_repo": True,
                "branch": "main",
                "changed_file_count": 4,
                "changed_files": ["AGENTS.md", "src/winchronicle/workday.py", "tests/test_workday.py"],
                "diff_stat": {"insertions": 91, "deletions": 0},
                "recent_commits": [],
            }
        ]
    }

    text = format_workday_text_summary(session, project_snapshot=project_snapshot)

    assert "allowlist" not in text
    assert "`main`" not in text
    assert "分支有" not in text
    assert "+91/-0" not in text
    assert "规模约" not in text
    assert "已有 4 个本地改动" in text
    assert "可能对应其它项目、写作、调研或沟通" in text
    assert "项目协作说明" in text
    assert "AGENTS.md" not in text
    assert "浏览器" in text
    assert "chrome" not in text


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


def _write_checkpoint_then_bad_watcher(tmp_path: Path) -> Path:
    fake_watcher = tmp_path / "fake_checkpoint_then_bad_watcher.py"
    fake_watcher.write_text(
        "\n".join(
            [
                "from pathlib import Path",
                "import sys",
                "import time",
                f"sys.stdout.write(Path({str(WATCHER_FIXTURE)!r}).read_text(encoding='utf-8'))",
                "sys.stdout.flush()",
                "time.sleep(1.2)",
                "print('{not-json', flush=True)",
            ]
        ),
        encoding="utf-8",
    )
    return fake_watcher


def _sleep(seconds: float) -> None:
    import time

    time.sleep(seconds)


def _wait_for_checkpoint(capsys) -> dict[str, object]:
    status: dict[str, object] = {}
    for _ in range(30):
        assert main(["workday", "status"]) == 0
        status = json.loads(capsys.readouterr().out)
        if status.get("checkpoint_available"):
            return status
        _sleep(0.2)
    raise AssertionError("checkpoint was not created")


def _check(payload: dict[str, object], name: str) -> dict[str, object]:
    for check in payload["checks"]:
        if check["name"] == name:
            return check
    raise AssertionError(f"missing check: {name}")
