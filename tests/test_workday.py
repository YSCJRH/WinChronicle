import json
import os
import sys
from pathlib import Path

from winchronicle.capture import capture_once_from_fixture
import winchronicle.cli as cli_module
from winchronicle.cli import main
from winchronicle.paths import ensure_state
from winchronicle.redaction import scan_for_unredacted_secrets
from winchronicle.session import monitor_events
import winchronicle.workday as workday_module
from winchronicle.workday import _write_json, format_workday_stop_text, format_workday_text_summary


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


def test_workday_stop_text_keeps_final_result_summary_without_source_notice():
    text_summary = format_workday_stop_text(
        {
            "stopped": True,
            "summary_available": True,
            "summary_source": "final_result",
            "summary": _minimal_workday_summary("final-result-text"),
        }
    )

    assert "今日工作复盘" in text_summary
    assert "复盘来源" not in text_summary
    assert "数据依据" not in text_summary
    assert "隐私边界" not in text_summary
    assert "visible_text" not in text_summary


def test_workday_stop_text_names_checkpoint_fallback_source_without_observed_content():
    text_summary = format_workday_stop_text(
        {
            "stopped": True,
            "summary_available": True,
            "summary_source": "checkpoint",
            "summary": _minimal_workday_summary("checkpoint-stop-text"),
        }
    )

    assert "今日工作复盘" in text_summary
    assert "复盘来源: 本地阶段性记录" in text_summary
    assert "checkpoint" not in text_summary
    assert "数据依据" not in text_summary
    assert "隐私边界" not in text_summary
    assert "visible_text" not in text_summary


def test_workday_stop_text_names_session_file_fallback_source():
    text_summary = format_workday_stop_text(
        {
            "stopped": True,
            "summary_available": True,
            "summary_source": "session_file",
            "summary": _minimal_workday_summary("session-file-stop-text"),
        }
    )

    assert "今日工作复盘" in text_summary
    assert "复盘来源: 本地已保存记录" in text_summary
    assert "session_file" not in text_summary
    assert "checkpoint" not in text_summary
    assert "visible_text" not in text_summary


def test_workday_stop_text_names_capture_buffer_recovery_source():
    text_summary = format_workday_stop_text(
        {
            "stopped": True,
            "summary_available": True,
            "summary_source": "capture_buffer_recovery",
            "recovered_from_capture_buffer": True,
            "summary": _minimal_workday_summary("capture-recovery-stop-text"),
        }
    )

    assert "今日工作复盘" in text_summary
    assert "复盘来源: 本地恢复记录" in text_summary
    assert "capture_buffer_recovery" not in text_summary
    assert "visible_text" not in text_summary


def test_workday_stop_text_command_names_checkpoint_fallback_source(
    tmp_path, monkeypatch, capsys
):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    paths = ensure_state(home)
    session_id = "checkpoint-stop-text-command"
    checkpoint_file = paths["logs"] / f"{session_id}.workday-checkpoint.json"
    _write_json(
        checkpoint_file,
        {
            "active": True,
            "summary_available": True,
            "summary_source": "checkpoint",
            "summary": _minimal_workday_summary(session_id, paths=paths),
            "trust": "local_workday_session_status",
            "capture_surface": "explicit_finite_monitor_session",
        },
    )
    _write_json(
        paths["workday_active"],
        _workday_active_marker(paths, session_id, pid="not-a-pid", checkpoint_file=checkpoint_file),
    )

    assert (
        main(["workday", "stop", "--wait-seconds", "0", "--format", "text", "--language", "zh-CN"])
        == 0
    )
    text_summary = capsys.readouterr().out

    assert "今日工作复盘" in text_summary
    assert "复盘来源: 本地阶段性记录" in text_summary
    assert "checkpoint" not in text_summary
    assert "summary_source" not in text_summary
    assert "visible_text" not in text_summary


def test_workday_stop_text_command_names_capture_buffer_recovery_source(
    tmp_path, monkeypatch, capsys
):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    paths = ensure_state(home)
    result = capture_once_from_fixture(
        ROOT / "harness" / "fixtures" / "uia" / "terminal_error.json",
        home,
    )
    assert result.path is not None

    session_id = "capture-buffer-stop-text-command"
    _write_json(
        paths["workday_active"],
        _workday_active_marker(
            paths,
            session_id,
            result_file=paths["logs"] / "missing-result.json",
        ),
    )

    assert (
        main(["workday", "stop", "--wait-seconds", "0", "--format", "text", "--language", "zh-CN"])
        == 0
    )
    text_summary = capsys.readouterr().out

    assert "今日工作复盘" in text_summary
    assert "复盘来源: 本地恢复记录" in text_summary
    assert "capture_buffer_recovery" not in text_summary
    assert "summary_source" not in text_summary
    assert "visible_text" not in text_summary
    assert (home / "sessions" / f"{session_id}.json").is_file()
    assert (home / "reports" / f"{session_id}.html").is_file()
    assert not (home / "workday-active.json").exists()
    assert list(home.rglob("*.jsonl")) == []


def test_workday_stop_text_command_keeps_source_notice_in_technical_style(
    tmp_path, monkeypatch, capsys
):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    paths = ensure_state(home)
    session_id = "phase-stop-technical-command"
    checkpoint_file = paths["logs"] / f"{session_id}.workday-checkpoint.json"
    _write_json(
        checkpoint_file,
        {
            "active": True,
            "summary_available": True,
            "summary_source": "checkpoint",
            "summary": _minimal_workday_summary(session_id, paths=paths),
            "trust": "local_workday_session_status",
            "capture_surface": "explicit_finite_monitor_session",
        },
    )
    _write_json(
        paths["workday_active"],
        _workday_active_marker(paths, session_id, pid="not-a-pid", checkpoint_file=checkpoint_file),
    )

    assert (
        main(
            [
                "workday",
                "stop",
                "--wait-seconds",
                "0",
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
    assert "复盘来源: 本地阶段性记录" in technical_summary
    assert "应用活动" in technical_summary
    assert "checkpoint" not in technical_summary
    assert "visible_text" not in technical_summary


def test_workday_summarize_text_does_not_add_stop_source_notice(tmp_path, monkeypatch, capsys):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    paths = ensure_state(home)
    session_id = "summarize-without-stop-source"
    _write_minimal_session_summary(paths, session_id)

    assert main(["workday", "summarize", session_id, "--format", "text", "--language", "zh-CN"]) == 0
    text_summary = capsys.readouterr().out

    assert "今日工作复盘" in text_summary
    assert "复盘来源" not in text_summary
    assert "visible_text" not in text_summary


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

    assert main(["workday", "status", "--format", "text", "--language", "zh-CN"]) == 0
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


def test_workday_start_reports_safe_json_when_default_build_output_is_missing(
    tmp_path, monkeypatch, capsys
):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))

    def missing_default_watcher() -> list[str]:
        raise workday_module.WorkdayError(
            "default watcher build output is missing; run dotnet build first"
        )

    monkeypatch.setattr(cli_module, "default_watcher_command", missing_default_watcher)

    assert main(["workday", "start", "--session-id", "missing-default-build"]) == 1
    payload = json.loads(capsys.readouterr().out)

    assert payload == {
        "active": False,
        "error": "default watcher build output is missing; run dotnet build first",
    }
    assert not (home / "workday-active.json").exists()


def test_workday_start_reports_safe_json_when_default_helper_build_output_is_missing(
    tmp_path, monkeypatch, capsys
):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))

    def existing_default_watcher() -> list[str]:
        return ["dotnet", "watcher.dll"]

    def missing_default_helper() -> list[str]:
        raise workday_module.WorkdayError(
            "default helper build output is missing; run dotnet build first"
        )

    monkeypatch.setattr(cli_module, "default_watcher_command", existing_default_watcher)
    monkeypatch.setattr(cli_module, "default_helper_command", missing_default_helper)

    assert main(["workday", "start", "--session-id", "missing-default-helper-build"]) == 1
    payload = json.loads(capsys.readouterr().out)

    assert payload == {
        "active": False,
        "error": "default helper build output is missing; run dotnet build first",
    }
    assert not (home / "workday-active.json").exists()


def test_workday_intent_execute_start_reports_safe_text_when_default_build_output_is_missing(
    tmp_path, monkeypatch, capsys
):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))

    def missing_default_watcher() -> list[str]:
        raise workday_module.WorkdayError(
            "default watcher build output is missing; run dotnet build first"
        )

    monkeypatch.setattr(cli_module, "default_watcher_command", missing_default_watcher)

    assert main(["workday", "intent", "开始记录工作", "--execute"]) == 1
    start_text = capsys.readouterr().out

    assert "工作记录未开始" in start_text
    assert "default watcher build output is missing" in start_text
    assert "WorkdayError" not in start_text
    assert "Traceback" not in start_text
    assert "capture_surface" not in start_text
    assert "visible_text" not in start_text
    assert not (home / "workday-active.json").exists()


def test_workday_start_reports_safe_json_when_runner_launch_fails(
    tmp_path, monkeypatch, capsys
):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))

    def fail_runner_launch(*args, **kwargs):
        raise OSError("simulated launch failure ghp_winchroniclecanary1234567890ABCD")

    monkeypatch.setattr(workday_module.subprocess, "Popen", fail_runner_launch)

    assert (
        main(
            [
                "workday",
                "start",
                "--watcher",
                sys.executable,
                "--watcher-arg",
                "fake-watcher.py",
                "--session-id",
                "runner-launch-fails",
            ]
        )
        == 1
    )
    payload = json.loads(capsys.readouterr().out)

    assert payload == {
        "active": False,
        "error": "workday_runner_start_failed",
    }
    assert "ghp_winchroniclecanary" not in json.dumps(payload)
    assert not (home / "workday-active.json").exists()
    assert not list((home / "logs").glob("runner-launch-fails*"))


def test_workday_start_keeps_safe_error_when_runner_launch_cleanup_fails(
    tmp_path, monkeypatch, capsys
):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))

    def fail_runner_launch(*args, **kwargs):
        raise OSError("simulated launch failure ghp_winchroniclecanary1234567890ABCD")

    original_unlink = Path.unlink

    def fail_launch_log_cleanup(self: Path, missing_ok: bool = False):
        if self.name.endswith((".workday-stdout.json", ".workday-stderr.txt")):
            raise OSError("simulated cleanup failure ghp_cleanupcanary1234567890ABCD")
        return original_unlink(self, missing_ok=missing_ok)

    monkeypatch.setattr(workday_module.subprocess, "Popen", fail_runner_launch)
    monkeypatch.setattr(Path, "unlink", fail_launch_log_cleanup)

    assert (
        main(
            [
                "workday",
                "start",
                "--watcher",
                sys.executable,
                "--watcher-arg",
                "fake-watcher.py",
                "--session-id",
                "runner-launch-cleanup-fails",
            ]
        )
        == 1
    )
    payload = json.loads(capsys.readouterr().out)

    assert payload == {
        "active": False,
        "error": "workday_runner_start_failed",
    }
    serialized = json.dumps(payload)
    assert "ghp_winchroniclecanary" not in serialized
    assert "ghp_cleanupcanary" not in serialized
    assert not (home / "workday-active.json").exists()


def test_workday_intent_execute_start_reports_safe_text_when_runner_launch_fails(
    tmp_path, monkeypatch, capsys
):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))

    def fail_runner_launch(*args, **kwargs):
        raise OSError("simulated launch failure ghp_winchroniclecanary1234567890ABCD")

    monkeypatch.setattr(workday_module.subprocess, "Popen", fail_runner_launch)

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
                "fake-watcher.py",
                "--session-id",
                "intent-runner-launch-fails",
            ]
        )
        == 1
    )
    start_text = capsys.readouterr().out

    assert "工作记录未开始" in start_text
    assert "本地工作记录进程启动失败" in start_text
    assert "winchronicle doctor" in start_text
    assert "workday_runner_start_failed" not in start_text
    assert "ghp_winchroniclecanary" not in start_text
    assert "OSError" not in start_text
    assert "Traceback" not in start_text
    assert "capture_surface" not in start_text
    assert "visible_text" not in start_text
    assert not (home / "workday-active.json").exists()
    assert not list((home / "logs").glob("intent-runner-launch-fails*"))


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


def test_workday_status_does_not_mark_checkpoint_available_without_checkpoint_summary(
    tmp_path, monkeypatch, capsys
):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    paths = ensure_state(home)
    session_id = "checkpoint-race"
    monitor_events(WATCHER_FIXTURE, home, session_id=session_id)
    checkpoint_file = paths["logs"] / f"{session_id}.workday-checkpoint.json"
    result_file = paths["logs"] / f"{session_id}.workday-result.json"
    checkpoint_file.write_text(json.dumps({"checkpoint": True}) + "\n", encoding="utf-8")
    paths["workday_active"].write_text(
        json.dumps(
            {
                "schema_version": 1,
                "active": True,
                "session_id": session_id,
                "pid": os.getpid(),
                "started_at": "2026-04-25T13:30:00+08:00",
                "duration_seconds": 60,
                "state_home": str(paths["home"]),
                "stop_file": str(paths["logs"] / f"{session_id}.stop"),
                "result_file": str(result_file),
                "checkpoint_file": str(checkpoint_file),
                "stdout_path": str(paths["logs"] / f"{session_id}.stdout.json"),
                "stderr_path": str(paths["logs"] / f"{session_id}.stderr.txt"),
                "trust": "untrusted_observed_content",
                "capture_surface": "explicit_finite_monitor_session",
                "bounded": True,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    assert main(["workday", "status"]) == 0
    status = json.loads(capsys.readouterr().out)

    assert status["active"] is True
    assert status["summary_source"] == "session_file"
    assert status["summary_available"] is True
    assert status["checkpoint_available"] is False


def test_workday_status_text_reports_recoverable_stale_checkpoint_summary(
    tmp_path, monkeypatch, capsys
):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    paths = ensure_state(home)
    session_id = "stale-checkpoint-status"
    checkpoint_file = paths["logs"] / f"{session_id}.workday-checkpoint.json"
    _write_json(
        checkpoint_file,
        {
            "active": True,
            "summary_available": True,
            "summary_source": "checkpoint",
            "summary": {
                "session_id": session_id,
                "mode": "workday",
                "captures_written": 1,
                "trust": "untrusted_observed_content",
            },
            "trust": "local_workday_session_status",
            "capture_surface": "explicit_finite_monitor_session",
        },
    )
    _write_json(
        paths["workday_active"],
        _workday_active_marker(paths, session_id, pid="not-a-pid", checkpoint_file=checkpoint_file),
    )

    assert main(["workday", "status", "--format", "text", "--language", "zh-CN"]) == 0
    text_status = capsys.readouterr().out

    assert "上一段工作记录的进程已不在运行" in text_status
    assert "本地 checkpoint 阶段性总结仍可查看" in text_status
    assert "session 文件总结" not in text_status
    assert f"winchronicle workday summarize {session_id} --format text --language zh-CN" in text_status
    assert "要开始时说：开始记录工作" not in text_status
    assert "Watcher burst should write one deterministic capture" not in text_status
    assert "visible_text" not in text_status

    assert main(["workday", "status"]) == 0
    status = json.loads(capsys.readouterr().out)
    assert status["active"] is False
    assert status["running"] is False
    assert status["active_marker_present"] is True
    assert status["recoverable_stale_session"] is True
    assert status["summary_available"] is True
    assert status["summary_source"] == "checkpoint"


def test_workday_status_text_reports_recoverable_stale_session_file_summary(
    tmp_path, monkeypatch, capsys
):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    paths = ensure_state(home)
    session_id = "stale-session-file-status"
    _write_minimal_session_summary(paths, session_id)
    _write_json(
        paths["workday_active"],
        _workday_active_marker(paths, session_id, pid="not-a-pid"),
    )

    assert main(["workday", "intent", "查看工作记录状态", "--execute"]) == 0
    text_status = capsys.readouterr().out

    assert "上一段工作记录的进程已不在运行" in text_status
    assert "本地 session 文件总结仍可查看" in text_status
    assert "checkpoint 阶段性总结" not in text_status
    assert f"winchronicle workday summarize {session_id} --format text --language zh-CN" in text_status
    assert "要开始时说：开始记录工作" not in text_status
    assert "Watcher burst should write one deterministic capture" not in text_status
    assert "visible_text" not in text_status

    assert main(["workday", "status"]) == 0
    status = json.loads(capsys.readouterr().out)
    assert status["active"] is False
    assert status["running"] is False
    assert status["active_marker_present"] is True
    assert status["recoverable_stale_session"] is True
    assert status["summary_available"] is True
    assert status["summary_source"] == "session_file"
    assert status["checkpoint_available"] is False


def test_workday_doctor_reports_recoverable_stale_checkpoint_summary(
    tmp_path, monkeypatch, capsys
):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    paths = ensure_state(home)
    session_id = "stale-checkpoint-doctor"
    checkpoint_file = paths["logs"] / f"{session_id}.workday-checkpoint.json"
    _write_json(
        checkpoint_file,
        {
            "active": True,
            "summary_available": True,
            "summary_source": "checkpoint",
            "summary": {
                "session_id": session_id,
                "mode": "workday",
                "captures_written": 1,
                "trust": "untrusted_observed_content",
            },
            "trust": "local_workday_session_status",
            "capture_surface": "explicit_finite_monitor_session",
        },
    )
    _write_json(
        paths["workday_active"],
        _workday_active_marker(paths, session_id, pid="not-a-pid", checkpoint_file=checkpoint_file),
    )

    assert main(["workday", "doctor", "--checkpoint-stale-seconds", "30"]) == 0
    doctor = json.loads(capsys.readouterr().out)

    assert doctor["active"] is False
    assert doctor["running"] is False
    assert doctor["active_marker_present"] is True
    assert doctor["recoverable_stale_session"] is True
    assert doctor["summary_available"] is True
    assert doctor["summary_source"] == "checkpoint"
    assert doctor["checkpoint_available"] is True
    assert _check(doctor, "runner_process")["ok"] is False
    assert _check(doctor, "checkpoint_available")["ok"] is True
    assert _check(doctor, "summary_available")["ok"] is True
    recovery_check = _check(doctor, "stale_session_recovery")
    assert recovery_check["ok"] is True
    assert "recoverable checkpoint summary is available" in recovery_check["detail"]
    assert (
        f"winchronicle workday summarize {session_id} --format text --language zh-CN"
        in recovery_check["detail"]
    )
    assert "Watcher burst should write one deterministic capture" not in json.dumps(doctor)
    assert "visible_text" not in json.dumps(doctor)


def test_workday_doctor_reports_recoverable_stale_session_file_summary(
    tmp_path, monkeypatch, capsys
):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    paths = ensure_state(home)
    session_id = "stale-session-file-doctor"
    _write_minimal_session_summary(paths, session_id)
    _write_json(
        paths["workday_active"],
        _workday_active_marker(paths, session_id, pid="not-a-pid"),
    )

    assert main(["workday", "doctor", "--checkpoint-stale-seconds", "30"]) == 0
    doctor = json.loads(capsys.readouterr().out)

    assert doctor["active"] is False
    assert doctor["running"] is False
    assert doctor["active_marker_present"] is True
    assert doctor["recoverable_stale_session"] is True
    assert doctor["summary_available"] is True
    assert doctor["summary_source"] == "session_file"
    assert doctor["checkpoint_available"] is False
    recovery_check = _check(doctor, "stale_session_recovery")
    assert recovery_check["ok"] is True
    assert "recoverable session file summary is available" in recovery_check["detail"]
    assert "checkpoint summary" not in recovery_check["detail"]
    assert (
        f"winchronicle workday summarize {session_id} --format text --language zh-CN"
        in recovery_check["detail"]
    )
    assert "Watcher burst should write one deterministic capture" not in json.dumps(doctor)
    assert "visible_text" not in json.dumps(doctor)


def test_workday_doctor_reports_unrecoverable_stale_marker_without_summary(
    tmp_path, monkeypatch, capsys
):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    paths = ensure_state(home)
    session_id = "stale-no-summary-doctor"
    _write_json(
        paths["workday_active"],
        _workday_active_marker(paths, session_id, pid="not-a-pid"),
    )

    assert main(["workday", "doctor", "--checkpoint-stale-seconds", "30"]) == 0
    doctor = json.loads(capsys.readouterr().out)

    assert doctor["active"] is False
    assert doctor["running"] is False
    assert doctor["active_marker_present"] is True
    assert doctor["recoverable_stale_session"] is False
    assert doctor["summary_available"] is False
    assert doctor["summary_source"] is None
    recovery_check = _check(doctor, "stale_session_recovery")
    assert recovery_check["ok"] is False
    assert "no checkpoint or session-file summary is available yet" in recovery_check["detail"]
    assert f"winchronicle workday summarize {session_id}" not in recovery_check["detail"]
    assert "Watcher burst should write one deterministic capture" not in json.dumps(doctor)
    assert "visible_text" not in json.dumps(doctor)


def test_workday_status_treats_malformed_active_pid_as_not_running(
    tmp_path, monkeypatch, capsys
):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    paths = ensure_state(home)
    session_id = "malformed-pid-status"
    _write_json(
        paths["workday_active"],
        _workday_active_marker(paths, session_id, pid="not-a-pid"),
    )

    assert main(["workday", "status"]) == 0
    status = json.loads(capsys.readouterr().out)

    assert status["active"] is False
    assert status["running"] is False
    assert status["summary_available"] is False


def test_workday_start_replaces_stale_marker_with_malformed_pid(
    tmp_path, monkeypatch, capsys
):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    paths = ensure_state(home)
    fake_watcher = _write_sleeping_watcher(tmp_path)
    _write_json(
        paths["workday_active"],
        _workday_active_marker(paths, "malformed-pid-stale", pid="not-a-pid"),
    )

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
                "--session-id",
                "malformed-pid-new",
            ]
        )
        == 0
    )
    started = json.loads(capsys.readouterr().out)

    assert started["active"] is True
    assert started["session_id"] == "malformed-pid-new"
    assert json.loads(paths["workday_active"].read_text(encoding="utf-8"))["session_id"] == (
        "malformed-pid-new"
    )

    assert main(["workday", "stop", "--wait-seconds", "10"]) == 0
    capsys.readouterr()


def test_workday_start_reports_fixed_error_when_stale_marker_cleanup_fails(
    tmp_path, monkeypatch, capsys
):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    paths = ensure_state(home)
    fake_watcher = _write_sleeping_watcher(tmp_path)
    _write_json(
        paths["workday_active"],
        _workday_active_marker(paths, "stale-cleanup-blocked", pid="not-a-pid"),
    )
    _fail_path_unlink(monkeypatch, paths["workday_active"])

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
                "--session-id",
                "blocked-stale-cleanup",
            ]
        )
        == 1
    )
    payload = json.loads(capsys.readouterr().out)

    assert payload["active"] is False
    assert payload["error"] == "workday_active_state_cleanup_failed"
    assert json.loads(paths["workday_active"].read_text(encoding="utf-8"))["session_id"] == (
        "stale-cleanup-blocked"
    )
    assert not (paths["logs"] / "blocked-stale-cleanup.workday-stdout.json").exists()
    assert not (paths["logs"] / "blocked-stale-cleanup.workday-stderr.txt").exists()


def test_workday_start_reports_fixed_error_when_start_artifact_cleanup_fails(
    tmp_path, monkeypatch, capsys
):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    paths = ensure_state(home)
    fake_watcher = _write_sleeping_watcher(tmp_path)
    session_id = "blocked-artifact-cleanup"
    result_file = paths["logs"] / f"{session_id}.workday-result.json"
    _write_json(result_file, {"stale": True})
    _fail_path_unlink(monkeypatch, result_file)

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
                "--session-id",
                session_id,
            ]
        )
        == 1
    )
    payload = json.loads(capsys.readouterr().out)

    assert payload["active"] is False
    assert payload["error"] == "workday_start_artifact_cleanup_failed"
    assert result_file.exists()
    assert not paths["workday_active"].exists()
    assert not (paths["logs"] / f"{session_id}.workday-stdout.json").exists()
    assert not (paths["logs"] / f"{session_id}.workday-stderr.txt").exists()


def test_workday_stop_uses_checkpoint_when_active_pid_is_malformed(
    tmp_path, monkeypatch, capsys
):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    paths = ensure_state(home)
    session_id = "malformed-pid-stop"
    checkpoint_file = paths["logs"] / f"{session_id}.workday-checkpoint.json"
    _write_json(
        checkpoint_file,
        {
            "active": True,
            "summary_available": True,
            "summary_source": "checkpoint",
            "summary": {
                "session_id": session_id,
                "mode": "workday",
                "captures_written": 1,
                "trust": "untrusted_observed_content",
            },
            "trust": "local_workday_session_status",
            "capture_surface": "explicit_finite_monitor_session",
        },
    )
    _write_json(
        paths["workday_active"],
        _workday_active_marker(paths, session_id, pid="not-a-pid", checkpoint_file=checkpoint_file),
    )

    assert main(["workday", "stop", "--wait-seconds", "0"]) == 0
    stopped = json.loads(capsys.readouterr().out)

    assert stopped["active"] is False
    assert stopped["stopped"] is True
    assert stopped["summary_available"] is True
    assert stopped["summary_source"] == "checkpoint"
    assert stopped["summary"]["session_id"] == session_id
    assert not paths["workday_active"].exists()


def test_workday_stop_uses_checkpoint_when_stop_marker_parent_is_missing(
    tmp_path, monkeypatch, capsys
):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    paths = ensure_state(home)
    session_id = "missing-stop-parent"
    checkpoint_file = paths["logs"] / f"{session_id}.workday-checkpoint.json"
    stop_file = home / "missing-stop-dir" / f"{session_id}.stop"
    result_file = paths["logs"] / f"{session_id}.workday-result.json"
    _write_json(
        checkpoint_file,
        {
            "active": True,
            "summary_available": True,
            "summary_source": "checkpoint",
            "summary": {
                "session_id": session_id,
                "mode": "workday",
                "captures_written": 1,
                "trust": "untrusted_observed_content",
            },
            "trust": "local_workday_session_status",
            "capture_surface": "explicit_finite_monitor_session",
        },
    )
    _write_json(
        paths["workday_active"],
        _workday_active_marker(
            paths,
            session_id,
            stop_file=stop_file,
            result_file=result_file,
            checkpoint_file=checkpoint_file,
        ),
    )

    assert main(["workday", "stop", "--wait-seconds", "0"]) == 0
    stopped = json.loads(capsys.readouterr().out)

    assert stopped["active"] is False
    assert stopped["stopped"] is True
    assert stopped["summary_available"] is True
    assert stopped["summary_source"] == "checkpoint"
    assert stopped["summary"]["session_id"] == session_id
    assert stop_file.is_file()
    assert not paths["workday_active"].exists()


def test_workday_stop_preserves_unrecovered_runner_failure_source(
    tmp_path, monkeypatch, capsys
):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    paths = ensure_state(home)
    session_id = "unrecovered-runner-failure"
    result_file = paths["logs"] / f"{session_id}.workday-result.json"
    _write_json(
        result_file,
        {
            "active": False,
            "stopped": False,
            "summary_available": False,
            "summary_source": None,
            "summary": None,
            "runner_status": "failed_unrecovered",
            "runner_error": "workday_watcher_start_failed",
            "trust": "local_workday_session_status",
            "capture_surface": "explicit_finite_monitor_session",
        },
    )
    _write_json(
        paths["workday_active"],
        _workday_active_marker(paths, session_id, result_file=result_file),
    )

    assert main(["workday", "stop", "--wait-seconds", "0"]) == 0
    stopped = json.loads(capsys.readouterr().out)
    serialized = json.dumps(stopped)

    assert stopped["active"] is False
    assert stopped["stopped"] is True
    assert stopped["summary_available"] is False
    assert stopped["summary_source"] is None
    assert stopped["summary"] is None
    assert stopped["runner_status"] == "failed_unrecovered"
    assert stopped["runner_error"] == "workday_watcher_start_failed"
    assert "final_result" not in serialized
    assert "Traceback" not in serialized
    assert "visible_text" not in serialized
    assert not paths["workday_active"].exists()


def test_workday_stop_returns_final_result_when_active_marker_cleanup_fails(
    tmp_path, monkeypatch, capsys
):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    paths = ensure_state(home)
    session_id = "active-cleanup-final"
    result_file = paths["logs"] / f"{session_id}.workday-result.json"
    _write_json(
        result_file,
        {
            "active": True,
            "summary_available": True,
            "summary": {
                "session_id": session_id,
                "mode": "workday",
                "captures_written": 2,
                "trust": "untrusted_observed_content",
            },
            "trust": "local_workday_session_status",
            "capture_surface": "explicit_finite_monitor_session",
        },
    )
    _write_json(
        paths["workday_active"],
        _workday_active_marker(paths, session_id, result_file=result_file),
    )
    _fail_active_marker_unlink(monkeypatch, paths["workday_active"])

    assert main(["workday", "stop", "--wait-seconds", "0"]) == 0
    stopped = json.loads(capsys.readouterr().out)

    assert stopped["active"] is False
    assert stopped["stopped"] is True
    assert stopped["summary_available"] is True
    assert stopped["summary_source"] == "final_result"
    assert stopped["summary"]["session_id"] == session_id
    assert stopped["active_state_cleanup_failed"] is True
    assert stopped["active_state_cleanup_error"] == "workday_active_state_cleanup_failed"
    assert paths["workday_active"].exists()


def test_workday_stop_uses_checkpoint_when_active_marker_cleanup_fails(
    tmp_path, monkeypatch, capsys
):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    paths = ensure_state(home)
    session_id = "active-cleanup-checkpoint"
    checkpoint_file = paths["logs"] / f"{session_id}.workday-checkpoint.json"
    _write_json(
        checkpoint_file,
        {
            "active": True,
            "summary_available": True,
            "summary_source": "checkpoint",
            "summary": {
                "session_id": session_id,
                "mode": "workday",
                "captures_written": 1,
                "trust": "untrusted_observed_content",
            },
            "trust": "local_workday_session_status",
            "capture_surface": "explicit_finite_monitor_session",
        },
    )
    _write_json(
        paths["workday_active"],
        _workday_active_marker(paths, session_id, checkpoint_file=checkpoint_file),
    )
    _fail_active_marker_unlink(monkeypatch, paths["workday_active"])

    assert main(["workday", "stop", "--wait-seconds", "0"]) == 0
    stopped = json.loads(capsys.readouterr().out)

    assert stopped["active"] is False
    assert stopped["stopped"] is True
    assert stopped["summary_available"] is True
    assert stopped["summary_source"] == "checkpoint"
    assert stopped["summary"]["session_id"] == session_id
    assert stopped["active_state_cleanup_failed"] is True
    assert stopped["active_state_cleanup_error"] == "workday_active_state_cleanup_failed"
    assert paths["workday_active"].exists()


def test_workday_json_state_write_preserves_previous_payload_when_temp_replace_fails(
    tmp_path, monkeypatch
):
    target = tmp_path / "checkpoint.json"
    target.write_text('{"status": "old"}\n', encoding="utf-8")
    original_replace = Path.replace

    def fail_replace(self: Path, target_path: Path) -> Path:
        if target_path == target:
            raise OSError("simulated replace failure")
        return original_replace(self, target_path)

    monkeypatch.setattr(Path, "replace", fail_replace)

    try:
        _write_json(target, {"status": "new"})
    except OSError:
        pass
    else:
        raise AssertionError("expected simulated replace failure")

    assert json.loads(target.read_text(encoding="utf-8")) == {"status": "old"}
    assert list(tmp_path.glob("*.tmp")) == []


def test_workday_start_cleans_up_runner_when_active_marker_write_fails(
    tmp_path, monkeypatch, capsys
):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    watcher_pid_file = tmp_path / "watcher.pid"
    fake_watcher = _write_sentinel_sleeping_watcher(tmp_path, watcher_pid_file)
    original_write_json = workday_module._write_json
    original_terminate = workday_module._terminate_process_tree
    terminated_pids: list[int] = []

    def fail_active_write(path: Path, payload: dict[str, object]) -> None:
        if path.name == "workday-active.json":
            for _ in range(50):
                if watcher_pid_file.exists():
                    break
                _sleep(0.1)
            raise OSError("simulated active marker write failure")
        original_write_json(path, payload)

    def record_terminate(pid: int) -> None:
        terminated_pids.append(pid)
        original_terminate(pid)

    monkeypatch.setattr(workday_module, "_write_json", fail_active_write)
    monkeypatch.setattr(workday_module, "_terminate_process_tree", record_terminate)

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
                "--session-id",
                "active-write-failure",
            ]
        )
        == 1
    )
    payload = json.loads(capsys.readouterr().out)

    assert payload["active"] is False
    assert payload["error"] == "workday_active_state_write_failed"
    assert terminated_pids
    assert _wait_for_pid_exit(terminated_pids[-1])
    assert watcher_pid_file.exists()
    assert _wait_for_pid_exit(int(watcher_pid_file.read_text(encoding="utf-8")))
    assert not (home / "workday-active.json").exists()


def test_workday_run_cleans_up_watcher_when_checkpoint_write_fails(tmp_path, monkeypatch):
    home = tmp_path / "state"
    fake_watcher = _write_slow_repeating_watcher(tmp_path)
    logs = home / "logs"
    logs.mkdir(parents=True, exist_ok=True)
    original_write_checkpoint = workday_module._write_checkpoint
    original_terminate = workday_module._terminate_process_tree
    terminated_pids: list[int] = []

    def fail_checkpoint_once(*args, **kwargs):
        raise OSError("simulated checkpoint write failure")

    def record_terminate(pid: int) -> None:
        terminated_pids.append(pid)
        original_terminate(pid)

    monkeypatch.setattr(workday_module, "_write_checkpoint", fail_checkpoint_once)
    monkeypatch.setattr(workday_module, "_terminate_process_tree", record_terminate)

    try:
        workday_module.run_workday(
            watcher_command=[sys.executable, str(fake_watcher)],
            helper_command=None,
            stop_file=logs / "checkpoint-failure.stop",
            result_file=logs / "checkpoint-failure.result.json",
            checkpoint_file=logs / "checkpoint-failure.checkpoint.json",
            home=home,
            session_id="checkpoint-failure",
            duration_seconds=60,
            depth=8,
            debounce_ms=100,
            heartbeat_ms=250,
            checkpoint_seconds=1,
            capture_on_start=False,
            exclude_apps=[],
        )
    except OSError:
        pass
    else:
        raise AssertionError("expected simulated checkpoint write failure")

    assert terminated_pids
    assert _wait_for_pid_exit(terminated_pids[-1])
    monkeypatch.setattr(workday_module, "_write_checkpoint", original_write_checkpoint)


def test_workday_run_reports_safe_error_when_watcher_launch_fails(tmp_path, monkeypatch):
    home = tmp_path / "state"
    paths = ensure_state(home)

    def fail_watcher_launch(*args, **kwargs):
        raise OSError("simulated watcher launch failure ghp_runwatchercanary1234567890ABCD")

    monkeypatch.setattr(workday_module.subprocess, "Popen", fail_watcher_launch)

    try:
        workday_module.run_workday(
            watcher_command=["missing-watcher"],
            helper_command=None,
            stop_file=paths["logs"] / "watcher-launch-failure.stop",
            result_file=paths["logs"] / "watcher-launch-failure.result.json",
            checkpoint_file=paths["logs"] / "watcher-launch-failure.checkpoint.json",
            home=home,
            session_id="watcher-launch-failure",
            duration_seconds=60,
            depth=8,
            debounce_ms=100,
            heartbeat_ms=250,
            checkpoint_seconds=1,
            capture_on_start=False,
            exclude_apps=[],
        )
    except workday_module.WorkdayError as exc:
        assert str(exc) == "workday_watcher_start_failed"
        assert exc.__cause__ is None
    else:
        raise AssertionError("expected safe WorkdayError for watcher launch failure")


def test_workday_run_cli_writes_safe_result_when_watcher_launch_fails(
    tmp_path, monkeypatch, capsys
):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    paths = ensure_state(home)
    result_file = paths["logs"] / "cli-watcher-launch-failure.result.json"
    checkpoint_file = paths["logs"] / "cli-watcher-launch-failure.checkpoint.json"
    stop_file = paths["logs"] / "cli-watcher-launch-failure.stop"

    def fail_watcher_launch(*args, **kwargs):
        raise OSError("simulated watcher launch failure ghp_runwatchercanary1234567890ABCD")

    monkeypatch.setattr(workday_module.subprocess, "Popen", fail_watcher_launch)

    assert (
        main(
            [
                "workday",
                "run",
                "--session-id",
                "cli-watcher-launch-failure",
                "--stop-file",
                str(stop_file),
                "--result-file",
                str(result_file),
                "--checkpoint-file",
                str(checkpoint_file),
                "--watcher-arg",
                "missing-watcher",
                "--duration",
                "60",
                "--depth",
                "8",
                "--heartbeat-ms",
                "250",
            ]
        )
        == 1
    )
    output = capsys.readouterr().out
    payload = json.loads(result_file.read_text(encoding="utf-8"))
    serialized = json.dumps(payload)

    assert "ERROR: workday runner could not write a safe session summary" in output
    assert payload["runner_status"] == "failed_unrecovered"
    assert payload["runner_error"] == "workday_watcher_start_failed"
    assert payload["summary_available"] is False
    assert "ghp_runwatchercanary" not in output
    assert "ghp_runwatchercanary" not in serialized
    assert "OSError" not in output
    assert "Traceback" not in output
    assert "capture_surface" not in output
    assert "visible_text" not in output


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


def _workday_active_marker(
    paths,
    session_id: str,
    *,
    pid=0,
    stop_file: Path | None = None,
    result_file: Path | None = None,
    checkpoint_file: Path | None = None,
) -> dict[str, object]:
    logs = paths["logs"]
    return {
        "schema_version": 1,
        "active": True,
        "session_id": session_id,
        "pid": pid,
        "started_at": "2026-04-25T09:00:00+08:00",
        "duration_seconds": 43200,
        "state_home": str(paths["home"]),
        "stop_file": str(stop_file or logs / f"{session_id}.stop"),
        "result_file": str(result_file or logs / f"{session_id}.workday-result.json"),
        "checkpoint_file": str(checkpoint_file or logs / f"{session_id}.workday-checkpoint.json"),
        "stdout_path": str(logs / f"{session_id}.workday-stdout.json"),
        "stderr_path": str(logs / f"{session_id}.workday-stderr.txt"),
        "trust": "local_workday_session_status",
        "capture_surface": "explicit_finite_monitor_session",
        "bounded": True,
    }


def _write_minimal_session_summary(paths, session_id: str) -> Path:
    session_path = paths["sessions"] / f"{session_id}.json"
    _write_json(session_path, _minimal_workday_summary(session_id, paths=paths))
    return session_path


def _minimal_workday_summary(session_id: str, paths=None) -> dict[str, object]:
    report_path = (
        str(paths["reports"] / f"{session_id}.html")
        if paths is not None
        else f"{session_id}.html"
    )
    return {
        "session_schema_version": 1,
        "session_id": session_id,
        "mode": "workday",
        "started_at": "2026-04-25T09:00:00+08:00",
        "ended_at": "2026-04-25T09:05:00+08:00",
        "duration_seconds": 300,
        "trust": "untrusted_observed_content",
        "instruction": "Monitor a bounded local workday session",
        "untrusted_observed_content": True,
        "captures_written": 1,
        "duplicates_skipped": 0,
        "denylisted_skipped": 0,
        "excluded_skipped": 0,
        "heartbeats": 0,
        "app_segments": [],
        "suggestions": [],
        "source_capture_paths": [],
        "storage_policy": {
            "raw_watcher_jsonl_saved": False,
            "html_report_contains_visible_text": False,
            "max_app_segments": 500,
            "max_title_chars": 120,
            "source_capture_paths_limit": 1000,
        },
        "storage_usage": {"session_json_bytes": 2048, "html_report_bytes": 1024},
        "report_path": report_path,
    }


def _fail_active_marker_unlink(monkeypatch, active_path: Path) -> None:
    _fail_path_unlink(monkeypatch, active_path)


def _fail_path_unlink(monkeypatch, failed_path: Path) -> None:
    original_unlink = Path.unlink

    def fail_active_unlink(self: Path, missing_ok: bool = False) -> None:
        if self == failed_path:
            raise OSError("simulated cleanup failure")
        original_unlink(self, missing_ok=missing_ok)

    monkeypatch.setattr(Path, "unlink", fail_active_unlink)


def _write_sentinel_sleeping_watcher(tmp_path: Path, pid_file: Path) -> Path:
    fake_watcher = tmp_path / "fake_workday_watcher.py"
    fake_watcher.write_text(
        "\n".join(
            [
                "from pathlib import Path",
                "import os",
                "import sys",
                "import time",
                f"Path({str(pid_file)!r}).write_text(str(os.getpid()), encoding='utf-8')",
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


def _wait_for_pid_exit(pid: int) -> bool:
    for _ in range(30):
        if not workday_module._is_process_running(pid):
            return True
        _sleep(0.1)
    return False


def _wait_for_checkpoint(capsys, *, timeout_seconds: float = 30.0) -> dict[str, object]:
    import time

    status: dict[str, object] = {}
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        assert main(["workday", "status"]) == 0
        status = json.loads(capsys.readouterr().out)
        if status.get("checkpoint_available"):
            return status
        _sleep(0.25)
    raise AssertionError(f"checkpoint was not created; last status: {status!r}")


def _check(payload: dict[str, object], name: str) -> dict[str, object]:
    for check in payload["checks"]:
        if check["name"] == name:
            return check
    raise AssertionError(f"missing check: {name}")
