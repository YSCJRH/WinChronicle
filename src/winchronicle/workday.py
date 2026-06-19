from __future__ import annotations

import json
import os
import queue
import re
import signal
import subprocess
import sys
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Sequence

from .paths import ensure_state, state_paths
from .privacy import DISABLED_SURFACE_STATUS, privacy_contract_payload
from .projects import snapshot_projects
from .redaction import redact_text
from .session import (
    MonitorSessionState,
    append_monitor_records,
    create_monitor_session_state,
    read_session,
    recover_session_from_capture_buffer,
    write_monitor_session_state,
)


DEFAULT_DURATION_SECONDS = 12 * 60 * 60
MAX_DURATION_SECONDS = 12 * 60 * 60
DEFAULT_CHECKPOINT_SECONDS = 5 * 60
CAPTURE_SURFACE = "explicit_finite_monitor_session"
ACTIVE_TRUST = "local_workday_session_status"


class WorkdayError(RuntimeError):
    pass


def default_watcher_command() -> list[str]:
    watcher = _repo_root() / "resources" / "win-uia-watcher" / "bin" / "Debug" / "net8.0-windows" / "win-uia-watcher.dll"
    if not watcher.exists():
        raise WorkdayError("default watcher build output is missing; run dotnet build first")
    return ["dotnet", str(watcher)]


def default_helper_command() -> list[str]:
    helper = _repo_root() / "resources" / "win-uia-helper" / "bin" / "Debug" / "net8.0-windows" / "win-uia-helper.dll"
    if not helper.exists():
        raise WorkdayError("default helper build output is missing; run dotnet build first")
    return ["dotnet", str(helper)]


def start_workday(
    *,
    watcher_command: Sequence[str],
    helper_command: Sequence[str] | None = None,
    home: Path | str | None = None,
    session_id: str | None = None,
    duration_seconds: int = DEFAULT_DURATION_SECONDS,
    depth: int = 80,
    debounce_ms: int = 750,
    heartbeat_ms: int = 5000,
    checkpoint_seconds: int = DEFAULT_CHECKPOINT_SECONDS,
    capture_on_start: bool = True,
    exclude_apps: Sequence[str] = (),
    operator_focus: Sequence[str] = (),
) -> dict[str, Any]:
    if duration_seconds < 0 or duration_seconds > MAX_DURATION_SECONDS:
        raise WorkdayError(f"duration must be between 0 and {MAX_DURATION_SECONDS} seconds")
    paths = ensure_state(home)
    active_path = paths["workday_active"]
    existing = _read_json(active_path)
    if existing and _is_process_running(int(existing.get("pid", 0))):
        return {
            "active": True,
            "error": "workday_session_already_active",
            "session_id": existing.get("session_id", ""),
            "pid": existing.get("pid", 0),
            "trust": ACTIVE_TRUST,
            "capture_surface": CAPTURE_SURFACE,
        }
    if existing:
        active_path.unlink(missing_ok=True)

    session = _slug(session_id or f"workday-{_local_timestamp()}")
    stop_file = paths["logs"] / f"{session}.stop"
    result_file = paths["logs"] / f"{session}.workday-result.json"
    checkpoint_file = paths["logs"] / f"{session}.workday-checkpoint.json"
    stdout_path = paths["logs"] / f"{session}.workday-stdout.json"
    stderr_path = paths["logs"] / f"{session}.workday-stderr.txt"
    for path in (stop_file, result_file, checkpoint_file):
        path.unlink(missing_ok=True)

    runner_args = [
        sys.executable,
        "-m",
        "winchronicle",
        "workday",
        "run",
        "--session-id",
        session,
        "--stop-file",
        str(stop_file),
        "--result-file",
        str(result_file),
        "--duration",
        str(duration_seconds),
        "--depth",
        str(depth),
        "--debounce-ms",
        str(debounce_ms),
        "--heartbeat-ms",
        str(heartbeat_ms),
        "--checkpoint-seconds",
        str(checkpoint_seconds),
        "--checkpoint-file",
        str(checkpoint_file),
    ]
    for part in watcher_command:
        runner_args.extend(["--watcher-arg", str(part)])
    if helper_command:
        for part in helper_command:
            runner_args.extend(["--helper-arg", str(part)])
    if capture_on_start:
        runner_args.append("--capture-on-start")
    for app in exclude_apps:
        runner_args.extend(["--exclude-app", app])
    focus_notes = _safe_focus_notes(operator_focus)
    for note in focus_notes:
        runner_args.extend(["--focus", note])

    env = os.environ.copy()
    env["WINCHRONICLE_HOME"] = str(paths["home"])
    stdout_handle = stdout_path.open("w", encoding="utf-8")
    stderr_handle = stderr_path.open("w", encoding="utf-8")
    try:
        process = subprocess.Popen(
            runner_args,
            cwd=_repo_root(),
            env=env,
            stdout=stdout_handle,
            stderr=stderr_handle,
            creationflags=_creation_flags(),
        )
    finally:
        stdout_handle.close()
        stderr_handle.close()

    active = {
        "schema_version": 1,
        "active": True,
        "session_id": session,
        "pid": process.pid,
        "started_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "duration_seconds": duration_seconds,
        "state_home": str(paths["home"]),
        "stop_file": str(stop_file),
        "result_file": str(result_file),
        "checkpoint_file": str(checkpoint_file),
        "stdout_path": str(stdout_path),
        "stderr_path": str(stderr_path),
        "trust": ACTIVE_TRUST,
        "capture_surface": CAPTURE_SURFACE,
        "bounded": True,
    }
    if focus_notes:
        active["operator_focus"] = focus_notes
    _write_json(active_path, active)
    return active


def run_workday(
    *,
    watcher_command: Sequence[str],
    helper_command: Sequence[str] | None,
    stop_file: Path,
    result_file: Path,
    checkpoint_file: Path | None = None,
    home: Path | str | None = None,
    session_id: str,
    duration_seconds: int,
    depth: int,
    debounce_ms: int,
    heartbeat_ms: int,
    checkpoint_seconds: int,
    capture_on_start: bool,
    exclude_apps: Sequence[str],
    operator_focus: Sequence[str] = (),
) -> dict[str, Any]:
    paths = ensure_state(home)
    command = _watcher_command(
        watcher_command,
        helper_command,
        depth=depth,
        duration_seconds=duration_seconds,
        debounce_ms=debounce_ms,
        heartbeat_ms=heartbeat_ms,
        capture_on_start=capture_on_start,
    )
    lines: list[str] = []
    stdout_queue: queue.Queue[str] = queue.Queue()
    stderr_queue: queue.Queue[str] = queue.Queue()
    process = subprocess.Popen(
        command,
        cwd=_repo_root(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
        creationflags=_creation_flags(),
    )
    _start_reader(process.stdout, stdout_queue)
    _start_reader(process.stderr, stderr_queue)
    deadline = time.monotonic() + max(0, duration_seconds)
    checkpoint_interval = max(1, checkpoint_seconds)
    last_checkpoint = time.monotonic()
    state = create_monitor_session_state()
    stop_requested = False

    while process.poll() is None:
        lines.clear()
        _drain(stdout_queue, lines)
        if lines:
            append_monitor_records(
                _parse_event_lines(lines),
                paths["home"],
                state=state,
                exclude_apps=exclude_apps,
            )
        if time.monotonic() - last_checkpoint >= checkpoint_interval:
            _write_checkpoint(
                paths["home"],
                session_id=session_id,
                state=state,
                checkpoint_file=checkpoint_file,
                operator_focus=operator_focus,
            )
            last_checkpoint = time.monotonic()
        _drain(stderr_queue, [])
        if stop_file.exists():
            stop_requested = True
            _drain_stdout_until_quiet(
                stdout_queue,
                paths["home"],
                state=state,
                exclude_apps=exclude_apps,
            )
            _terminate_process_tree(process.pid)
            break
        if duration_seconds >= 0 and time.monotonic() > deadline + 5:
            _terminate_process_tree(process.pid)
            break
        time.sleep(0.1)

    try:
        process.wait(timeout=10)
    except subprocess.TimeoutExpired:
        _terminate_process_tree(process.pid)
        process.wait(timeout=5)
    lines.clear()
    _drain(stdout_queue, lines)
    if lines:
        append_monitor_records(
            _parse_event_lines(lines),
            paths["home"],
            state=state,
            exclude_apps=exclude_apps,
        )
    _drain(stderr_queue, [])

    result = write_monitor_session_state(
        paths["home"],
        session_id=session_id,
        mode="workday",
        state=state,
        operator_focus=operator_focus,
    )
    payload = {
        "active": False,
        "stopped": stop_requested,
        "summary_available": True,
        "summary_source": "final_result",
        "recovered_from_capture_buffer": False,
        "summary": result.session,
        "path": str(result.path),
        "report_path": str(result.report_path),
        "trust": ACTIVE_TRUST,
        "capture_surface": CAPTURE_SURFACE,
    }
    _write_json(result_file, payload)
    _write_checkpoint(
        paths["home"],
        session_id=session_id,
        state=state,
        checkpoint_file=checkpoint_file,
        payload=payload,
        operator_focus=operator_focus,
    )
    return payload


def recover_workday_runner_failure(
    *,
    session_id: str,
    result_file: Path,
    checkpoint_file: Path | None = None,
    home: Path | str | None = None,
    stopped: bool = False,
) -> dict[str, Any]:
    paths = ensure_state(home)
    summary_source = None
    summary = _summary_from_payload(_read_json(checkpoint_file)) if checkpoint_file else None
    if summary is not None:
        summary_source = "checkpoint"

    recovered = False
    if summary is None:
        active = _read_json(paths["workday_active"]) or {}
        started_at = str(active.get("started_at", ""))
        if started_at:
            try:
                recovered_result = recover_session_from_capture_buffer(
                    paths["home"],
                    session_id=session_id,
                    started_at=started_at,
                    ended_at=datetime.now().astimezone().isoformat(timespec="seconds"),
                )
                summary = recovered_result.session
                summary_source = "capture_buffer_recovery"
                recovered = True
            except Exception:
                pass

    if summary is None:
        summary = _read_session_or_none(session_id, paths["home"])
        if summary is not None:
            summary_source = "session_file"

    payload = {
        "active": False,
        "stopped": stopped,
        "summary_available": summary is not None,
        "summary_source": summary_source,
        "recovered_from_capture_buffer": recovered,
        "summary": summary,
        "runner_status": "failed_recovered" if summary is not None else "failed_unrecovered",
        "runner_error": "workday_runner_failed_before_final_result",
        "trust": ACTIVE_TRUST,
        "capture_surface": CAPTURE_SURFACE,
    }
    _attach_focus_to_payload(payload, _active_focus_notes(paths["workday_active"]))
    _write_json(result_file, payload)
    return payload


def status_workday(home: Path | str | None = None) -> dict[str, Any]:
    paths = state_paths(home)
    active = _read_json(paths["workday_active"])
    if not active:
        return {"active": False, "trust": ACTIVE_TRUST, "capture_surface": CAPTURE_SURFACE}
    running = _is_process_running(int(active.get("pid", 0)))
    result = _read_json(Path(active.get("result_file", "")))
    checkpoint_path = Path(active.get("checkpoint_file", ""))
    checkpoint = _read_json(checkpoint_path)
    summary, summary_source = _active_summary_details(
        result=result,
        checkpoint=checkpoint,
        session_id=active.get("session_id", ""),
        home=paths["home"],
    )
    return {
        **active,
        "active": running,
        "running": running,
        "summary_available": summary is not None,
        "checkpoint_available": bool(checkpoint or (summary and not result)),
        "checkpoint_updated_at": _checkpoint_updated_at(checkpoint_path),
        "checkpoint_age_seconds": _checkpoint_age_seconds(checkpoint_path),
        "summary_source": summary_source,
        "summary": summary,
    }


def format_workday_status_text(status: dict[str, Any]) -> str:
    active = bool(status.get("active", False))
    running = bool(status.get("running", False))
    if active and running:
        state = "运行中"
    elif active:
        state = "已记录但进程未运行"
    else:
        state = "未在记录"
    lines = ["# 工作记录状态", ""]
    if active:
        started = _safe_text(status.get("started_at", "")) or "未知时间"
        duration = _format_duration(_safe_int(status.get("duration_seconds")))
        summary_hint = "已有阶段性总结" if status.get("summary_available") else "阶段性总结还在生成中"
        lines.extend(
            [
                "正在记录今天的工作。",
                "",
                f"- 当前状态: {state}",
                f"- 从 {started} 开始，最长记录 {duration}。",
                f"- 当前总结: {summary_hint}。",
                "- 结束时直接说：停止工作并总结。",
            ]
        )
    else:
        lines.extend(
            [
                "当前没有在记录。",
                "",
                "- 要开始时说：开始记录工作。",
                "- 要查看状态时说：查看工作记录状态。",
            ]
        )
    lines.extend(
        [
            "",
            "## 安全说明",
            "",
            "- 该状态视图只读取本地 session metadata，不启动 watcher/helper/UIA capture 或桌面读取。",
            "- 记录仍是本地、有限时长、只读；未新增 截图/" "O" "CR/剪贴板/键盘记录/音频/云上传/桌面控制/MCP 写工具。",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def format_workday_start_text(payload: dict[str, Any]) -> str:
    session_id = _safe_text(payload.get("session_id", ""))
    duration = _format_duration(_safe_int(payload.get("duration_seconds")))
    focus_notes = _safe_focus_notes(payload.get("operator_focus", []))
    if payload.get("error") == "workday_session_already_active":
        lines = [
            "# 工作记录状态",
            "",
            "今天的工作记录已经在记录中，没有启动第二次记录。",
        ]
        if session_id:
            lines.append(f"- 当前记录: {session_id}")
        lines.extend(
            [
                "- 想看当前状态，可以说：查看工作记录状态。",
                "- 想结束并复盘，可以说：停止工作并总结。",
            ]
        )
        return "\n".join(lines).rstrip() + "\n"

    if payload.get("active"):
        lines = [
            "# 工作记录已开始",
            "",
            "已开始记录今天的工作。",
        ]
        if session_id:
            lines.append(f"- 当前记录: {session_id}")
        if duration:
            lines.append(f"- 这是一段有限时长的本地记录，最长 {duration}。")
        if focus_notes:
            lines.append(f"- 今天关注: {'；'.join(focus_notes)}。")
        lines.extend(
            [
                "- 想看当前状态，可以说：查看工作记录状态。",
                "- 想结束并复盘，可以说：停止工作并总结。",
            ]
        )
        return "\n".join(lines).rstrip() + "\n"

    lines = ["# 工作记录未开始", "", "这次没有启动工作记录。"]
    error = _safe_text(payload.get("error", ""))
    if error:
        lines.append(f"- 原因: {error}")
    lines.append("- 可以稍后再说：开始记录工作。")
    return "\n".join(lines).rstrip() + "\n"


def format_workday_stop_text(payload: dict[str, Any]) -> str:
    if payload.get("summary_available") and isinstance(payload.get("summary"), dict):
        return format_workday_text_summary(payload["summary"])

    if not payload.get("stopped"):
        return "\n".join(
            [
                "# 工作记录状态",
                "",
                "当前没有在记录，无需结束。",
                "",
                "- 要开始新的记录，可以说：开始记录工作。",
                "- 要查看状态，可以说：查看工作记录状态。",
            ]
        ).rstrip() + "\n"

    return "\n".join(
        [
            "# 工作记录已停止",
            "",
            "已请求停止记录，但这次没有生成可显示的工作复盘。",
            "",
            "- 可以稍后说：查看工作记录状态。",
            "- 如果你愿意，也可以补一句今天完成了什么。",
        ]
    ).rstrip() + "\n"


def doctor_workday(
    home: Path | str | None = None,
    *,
    checkpoint_stale_seconds: int = DEFAULT_CHECKPOINT_SECONDS * 2,
) -> dict[str, Any]:
    status = status_workday(home)
    privacy = privacy_contract_payload()
    disabled_surfaces = {key: privacy[key] for key in DISABLED_SURFACE_STATUS}
    active = bool(status.get("active", False))
    running = bool(status.get("running", False))
    checkpoint_available = bool(status.get("checkpoint_available", False))
    checkpoint_age = status.get("checkpoint_age_seconds")
    checkpoint_fresh = _checkpoint_fresh(
        checkpoint_available=checkpoint_available,
        checkpoint_age_seconds=checkpoint_age,
        stale_after_seconds=checkpoint_stale_seconds,
    )
    summary_available = bool(status.get("summary_available", False))
    checks = _doctor_checks(
        active=active,
        running=running,
        bounded=bool(status.get("bounded", False)),
        checkpoint_available=checkpoint_available,
        checkpoint_fresh=checkpoint_fresh,
        summary_available=summary_available,
        disabled_surfaces=disabled_surfaces,
    )

    return {
        "command": "workday doctor",
        "active": active,
        "running": running,
        "session_id": str(status.get("session_id", "")),
        "started_at": str(status.get("started_at", "")),
        "duration_seconds": int(status.get("duration_seconds", 0)),
        "bounded": bool(status.get("bounded", False)),
        "summary_available": summary_available,
        "summary_source": status.get("summary_source"),
        "checkpoint_available": checkpoint_available,
        "checkpoint_updated_at": str(status.get("checkpoint_updated_at", "")),
        "checkpoint_age_seconds": checkpoint_age,
        "checkpoint_fresh": checkpoint_fresh,
        "checkpoint_stale_seconds": max(0, checkpoint_stale_seconds),
        "trust": ACTIVE_TRUST,
        "capture_surface": CAPTURE_SURFACE,
        "checks": checks,
        **disabled_surfaces,
    }


def stop_workday(home: Path | str | None = None, *, wait_seconds: int = 30) -> dict[str, Any]:
    paths = state_paths(home)
    active_path = paths["workday_active"]
    active = _read_json(active_path)
    if not active:
        return {
            "active": False,
            "stopped": False,
            "summary_available": False,
            "trust": ACTIVE_TRUST,
            "capture_surface": CAPTURE_SURFACE,
        }

    stop_file = Path(active["stop_file"])
    result_file = Path(active["result_file"])
    stop_file.write_text(datetime.now().astimezone().isoformat(timespec="seconds"), encoding="utf-8")
    pid = int(active.get("pid", 0))
    deadline = time.monotonic() + max(0, wait_seconds)
    result = _read_json(result_file)
    while time.monotonic() < deadline and not result:
        if _is_process_running(pid):
            time.sleep(0.2)
        else:
            time.sleep(0.1)
        result = _read_json(result_file)
    if not result and _is_process_running(pid):
        _terminate_process_tree(pid)
        time.sleep(0.2)
        result = _read_json(result_file)

    active_path.unlink(missing_ok=True)
    if result:
        _attach_focus_to_payload(result, _safe_focus_notes(active.get("operator_focus", [])))
        return {
            **result,
            "active": False,
            "stopped": True,
            "summary_source": result.get("summary_source") or "final_result",
            "recovered_from_capture_buffer": bool(result.get("recovered_from_capture_buffer", False)),
        }
    summary_source = None
    checkpoint_summary = _summary_from_payload(_read_json(Path(active.get("checkpoint_file", ""))))
    if checkpoint_summary is not None:
        summary_source = "checkpoint"
    if checkpoint_summary is None:
        checkpoint_summary = _read_session_or_none(active["session_id"], paths["home"])
        if checkpoint_summary is not None:
            summary_source = "session_file"
    minimum_captures = int(checkpoint_summary.get("captures_written", 0)) if checkpoint_summary else 0
    summary = checkpoint_summary
    recovered = False
    try:
        recovered_result = recover_session_from_capture_buffer(
            paths["home"],
            session_id=active["session_id"],
            started_at=str(active.get("started_at", "")),
            ended_at=datetime.now().astimezone().isoformat(timespec="seconds"),
            minimum_captures=minimum_captures,
        )
        summary = recovered_result.session
        recovered = True
        summary_source = "capture_buffer_recovery"
    except Exception:
        pass
    return {
        "active": False,
        "stopped": True,
        "summary_available": summary is not None,
        "summary_source": summary_source,
        "summary": _with_focus(summary, _safe_focus_notes(active.get("operator_focus", []))),
        "recovered_from_capture_buffer": recovered,
        "trust": ACTIVE_TRUST,
        "capture_surface": CAPTURE_SURFACE,
    }


def summarize_workday(
    identifier: str,
    home: Path | str | None = None,
    *,
    output_format: str = "json",
    language: str = "zh-CN",
    confirmation_notes: Sequence[str] = (),
    summary_style: str = "human",
) -> dict[str, Any] | str:
    paths = state_paths(home)
    session = read_session(identifier, paths["home"])
    if output_format == "json":
        return session
    if output_format != "text":
        raise WorkdayError("workday summary format must be json or text")
    if language != "zh-CN":
        raise WorkdayError("workday text summaries currently support only zh-CN")
    return format_workday_text_summary(
        session,
        project_snapshot=snapshot_projects(paths["home"]),
        confirmation_notes=confirmation_notes,
        summary_style=summary_style,
    )


def format_workday_text_summary(
    session: dict[str, Any],
    *,
    project_snapshot: dict[str, Any] | None = None,
    confirmation_notes: Sequence[str] = (),
    summary_style: str = "human",
) -> str:
    if project_snapshot is None:
        project_snapshot = _safe_project_snapshot()
    if summary_style == "technical":
        return _format_workday_technical_text_summary(
            session,
            project_snapshot=project_snapshot,
            confirmation_notes=confirmation_notes,
        )
    if summary_style != "human":
        raise WorkdayError("workday text summary style must be human or technical")
    return _format_workday_human_text_summary(
        session,
        project_snapshot=project_snapshot,
        confirmation_notes=confirmation_notes,
    )


def _format_workday_human_text_summary(
    session: dict[str, Any],
    *,
    project_snapshot: dict[str, Any],
    confirmation_notes: Sequence[str] = (),
) -> str:
    lines = [
        "# 今日工作复盘",
        "",
        "## 今日工作结论",
        "",
    ]
    lines.extend(_format_work_conclusions(session, project_snapshot))
    lines.extend(_format_work_progress(session, project_snapshot))
    lines.extend(_format_confirmation_notes(confirmation_notes))
    lines.extend(_format_habit_improvements(session, project_snapshot))
    lines.extend(_format_consideration_directions(session, project_snapshot))
    return "\n".join(lines).rstrip() + "\n"


def _format_workday_technical_text_summary(
    session: dict[str, Any],
    *,
    project_snapshot: dict[str, Any],
    confirmation_notes: Sequence[str] = (),
) -> str:
    storage_usage = session.get("storage_usage", {})
    storage_policy = session.get("storage_policy", {})
    source_paths = session.get("source_capture_paths", [])
    app_segments = session.get("app_segments", [])
    suggestions = session.get("suggestions", [])
    error_signals = session.get("error_signals", {})

    lines = [
        "# 工作概览",
        "",
        f"- 会话: {_safe_text(session.get('session_id', ''))}",
        f"- 模式: {_safe_text(session.get('mode', 'workday'))}",
        f"- 信任边界: {_safe_text(session.get('trust', 'untrusted_observed_content'))}",
        f"- 捕获数量: {_safe_int(session.get('captures_written'))}",
        f"- 跳过数量: {_skipped_total(session)}",
        f"- 观察来源记录数: {len(source_paths)}",
        "",
        "## 时间范围",
        "",
        f"- 开始: {_safe_text(session.get('started_at', ''))}",
        f"- 结束: {_safe_text(session.get('ended_at', ''))}",
        f"- 持续秒数: {_safe_int(session.get('duration_seconds'))}",
        "",
        "## 应用活动",
        "",
    ]
    lines.extend(_format_app_segments(app_segments))
    lines.extend(
        [
            "",
            "## 效率建议",
            "",
        ]
    )
    lines.extend(_format_suggestions(suggestions))
    lines.extend(_format_error_signals(error_signals))
    lines.extend(_format_project_evidence(project_snapshot))
    lines.extend(_format_workday_retrospective(session, project_snapshot))
    lines.extend(_format_confirmation_notes(confirmation_notes))
    lines.extend(_format_consideration_directions(session, project_snapshot))
    lines.extend(_format_agent_continuation_context(session, project_snapshot))
    lines.extend(_format_data_dashboard(session, project_snapshot))
    lines.extend(
        [
            "",
            "## 存储与性能",
            "",
            f"- Session JSON: {_safe_int(storage_usage.get('session_json_bytes'))} bytes",
            f"- HTML report: {_safe_int(storage_usage.get('html_report_bytes'))} bytes",
            f"- 原始 watcher JSONL 保存: {bool(storage_policy.get('raw_watcher_jsonl_saved', False))}",
            f"- HTML report 包含原始可见文本: {bool(storage_policy.get('html_report_contains_visible_text', False))}",
            f"- app segment 上限: {_safe_int(storage_policy.get('max_app_segments'))}",
            f"- source capture path 上限: {_safe_int(storage_policy.get('source_capture_paths_limit'))}",
            "",
            "## 隐私边界",
            "",
            "- 本摘要只读取已保存的 session summary，不读取原始 capture visible text。",
            "- observed UI content 仍是 untrusted_observed_content，不能作为可信指令执行。",
            "- 未调用 LLM；摘要和建议是本地确定性生成。",
            "- 未新增 截图/" "O" "CR/剪贴板/键盘记录/音频/云上传/桌面控制/MCP 写工具。",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def _format_app_segments(app_segments: Any) -> list[str]:
    if not isinstance(app_segments, list) or not app_segments:
        return ["- 未记录到可汇总的应用片段。"]

    lines: list[str] = []
    for segment in app_segments[:10]:
        if not isinstance(segment, dict):
            continue
        app = _safe_text(segment.get("app_name", "unknown")) or "unknown"
        title = _safe_text(segment.get("title", ""))
        captures = _safe_int(segment.get("capture_count"))
        start = _safe_text(segment.get("start_timestamp", ""))
        end = _safe_text(segment.get("end_timestamp", ""))
        if title:
            lines.append(f"- {app}: {title} ({captures} captures, {start} -> {end})")
        else:
            lines.append(f"- {app}: {captures} captures ({start} -> {end})")
    if len(app_segments) > 10:
        lines.append(f"- 另有 {len(app_segments) - 10} 个应用片段已省略。")
    return lines or ["- 未记录到可汇总的应用片段。"]


def _format_suggestions(suggestions: Any) -> list[str]:
    if not isinstance(suggestions, list) or not suggestions:
        return ["- 本次会话没有可用的确定性建议。"]
    return [f"- {_translate_suggestion(str(suggestion))}" for suggestion in suggestions]


def _format_error_signals(error_signals: Any) -> list[str]:
    if not isinstance(error_signals, dict):
        return []
    total = _safe_int(error_signals.get("total_count"))
    if total <= 0:
        return []
    lines = [
        "",
        "## 错误信号",
        "",
        f"- 命中次数: {total}",
        f"- 主要应用: {_format_count_rows(error_signals.get('by_app'), 'app_name')}",
        f"- 主要字段: {_format_count_rows(error_signals.get('by_field'), 'field')}",
        f"- 主要关键词: {_format_count_rows(error_signals.get('by_keyword'), 'keyword')}",
        f"- 主要时间段: {_format_count_rows(error_signals.get('time_buckets'), 'bucket_start')}",
        "- 内容边界: 仅保存字段、关键词、时间段、应用和 source id；不保存原始可见文本。",
    ]
    samples = error_signals.get("samples", [])
    if isinstance(samples, list) and samples:
        source_ids = [
            _safe_text(sample.get("source_id", ""))
            for sample in samples
            if isinstance(sample, dict) and _safe_text(sample.get("source_id", ""))
        ][:3]
        if source_ids:
            lines.append(f"- 样本 source id: {', '.join(source_ids)}")
    return lines


def _format_project_evidence(project_snapshot: Any) -> list[str]:
    lines = [
        "",
        "## 今日推进线索",
        "",
    ]
    projects = _snapshot_projects(project_snapshot)
    if not projects:
        return [
            *lines,
            "- 未登记项目目录；本摘要只能根据应用活动和本地 session metadata 推断工作主题。",
            "- 如需跨项目日报，先用 `winchronicle projects add <path> --name <name>` 登记明确允许读取元数据的目录。",
        ]

    for project in projects[:8]:
        name = _safe_text(project.get("name", "project")) or "project"
        if not project.get("exists"):
            lines.append(f"- {name}: 目录当前不可用，未读取 git metadata。")
            continue
        if not project.get("is_git_repo"):
            lines.append(f"- {name}: 已登记，但不是 git 工作树；未读取文件内容。")
            continue
        branch = _safe_text(project.get("branch", "")) or "unknown"
        changed_count = _safe_int(project.get("changed_file_count"))
        changed_files = project.get("changed_files", [])
        diff_stat = project.get("diff_stat", {})
        recent = project.get("recent_commits", [])
        details = [f"branch {branch}", f"{changed_count} 个变更文件"]
        if isinstance(diff_stat, dict):
            insertions = _safe_int(diff_stat.get("insertions"))
            deletions = _safe_int(diff_stat.get("deletions"))
            if insertions or deletions:
                details.append(f"+{insertions}/-{deletions}")
        line = f"- {name}: " + "，".join(details)
        if isinstance(changed_files, list) and changed_files:
            filenames = ", ".join(_safe_text(path) for path in changed_files[:4])
            line += f"；文件线索: {filenames}"
        if isinstance(recent, list) and recent:
            subject = _safe_text(recent[0].get("subject", "")) if isinstance(recent[0], dict) else ""
            if subject:
                line += f"；最近提交: {subject}"
        lines.append(line)
    if len(projects) > 8:
        lines.append(f"- 另有 {len(projects) - 8} 个登记项目未展开。")
    lines.append("- 边界: 只读取 allowlist 项目的 git metadata、文件名、diff shortstat 和 commit 标题；不读取文件内容或 full diff。")
    return lines


def _format_work_conclusions(session: dict[str, Any], project_snapshot: Any) -> list[str]:
    projects = _snapshot_projects(project_snapshot)
    changed_projects = [project for project in projects if _safe_int(project.get("changed_file_count")) > 0]
    apps = _top_app_names(session.get("app_segments", []))
    error_count = _error_signal_count(session)
    focus_notes = _session_focus_notes(session)
    lines: list[str] = []

    if focus_notes:
        lines.append(f"- 今日关注事项: {'；'.join(focus_notes)}。")

    if changed_projects:
        for project in changed_projects[:3]:
            name = _safe_text(project.get("name", "project")) or "project"
            changed_count = _safe_int(project.get("changed_file_count"))
            clues = _project_file_clues(project)
            if clues:
                lines.append(f"- 根据本地记录，主要推进了 {name}：已有 {changed_count} 个本地改动，集中在{clues}。")
            else:
                lines.append(f"- 根据本地记录，主要推进了 {name}：已有 {changed_count} 个本地改动。")
        if len(changed_projects) > 3:
            lines.append(f"- 另有 {len(changed_projects) - 3} 个登记项目也出现了变更，适合按项目拆成独立收尾项。")
    elif projects:
        lines.append("- 根据本地记录，已登记项目目录但未看到明显 git 变更；今天更可能偏阅读、沟通、调研、文档查看，或成果尚未保存。")
    else:
        lines.append("- 根据本地记录，今天有工作活动，但未登记项目目录；系统还不能可靠判断具体项目产出。")

    if apps:
        lines.append(f"- 今天主要使用了 {_join_cn(apps[:5])}，这些软件活动显示当天混合了开发、资料查看或文档处理。")
    workstream_clues = _title_workstream_clues(session)
    if workstream_clues:
        lines.append(f"- 今日工作线索: 窗口标题显示还涉及 {'、'.join(workstream_clues)}。")
    if error_count:
        lines.append("- 复盘小提醒: 记录里出现过调试或异常线索；这不代表工作质量，只提示收尾时可以看一眼是否有真正影响推进的事项。")
    if _safe_int(session.get("captures_written")) == 0:
        lines.append("- 本次没有可用 capture；如果你愿意，可以补一句今天实际完成的事项，让复盘更完整。")
    return lines or ["- 本次会话缺少足够线索；如果你愿意，可以补一句今天实际完成的事项。"]


def _format_work_progress(session: dict[str, Any], project_snapshot: Any) -> list[str]:
    lines = [
        "",
        "## 工作进行情况",
        "",
    ]
    projects = _snapshot_projects(project_snapshot)
    if not projects:
        no_project_lines = [
            *lines,
            "- 今天已经记录到工作活动，但还没有看到你希望重点跟踪的项目文件夹，所以目前只能给出整体复盘。",
            "- 如果希望下次更像项目进展总结，可以告诉 WinChronicle 相关项目文件夹；不填写也会继续记录。",
        ]
        if _error_signal_count(session):
            no_project_lines.append("- 复盘小提醒: 记录里出现过调试或异常线索；这不代表工作质量。如果今天确实有卡住的事，明天先看真正影响推进的一两件事。")
        return no_project_lines

    for project in projects[:5]:
        name = _safe_text(project.get("name", "project")) or "project"
        if not project.get("exists"):
            lines.append(f"- {name}: 目录当前不可用，无法判断进展。")
            continue
        if not project.get("is_git_repo"):
            lines.append(f"- {name}: 已登记但不是 git 工作树；只能确认被纳入观察范围，不能判断代码进展。")
            continue
        changed_count = _safe_int(project.get("changed_file_count"))
        if changed_count:
            clues = _project_file_clues(project)
            suffix = f"，主要集中在{clues}" if clues else ""
            lines.append(f"- {name}: 正在推进，已有 {changed_count} 个本地改动{suffix}。")
        else:
            lines.append(f"- {name}: 未见未提交变更；可能已提交、偏阅读调研，或工作发生在其他项目。")

    unregistered_apps = _unregistered_activity_apps(session)
    if unregistered_apps:
        lines.append(
            f"- 还较多使用了 {_join_cn(unregistered_apps)}；这些活动可能对应其它项目、写作、调研或沟通，当前总结先按软件名保留。"
        )

    error_count = _error_signal_count(session)
    if error_count:
        lines.append("- 复盘小提醒: 记录里出现过调试或异常线索；这不代表工作质量。如果今天确实有卡住的事，明天先看真正影响推进的一两件事。")
    return lines


def _format_habit_improvements(session: dict[str, Any], project_snapshot: Any) -> list[str]:
    app_segments = session.get("app_segments", [])
    app_segment_count = len(app_segments) if isinstance(app_segments, list) else 0
    lines = [
        "",
        "## 明天改进建议",
        "",
    ]
    if not _snapshot_projects(project_snapshot):
        lines.append("- 如果希望日报更像项目复盘，可以在开始记录前告诉 WinChronicle 今天想关注的项目文件夹；不填写也会继续记录应用活动。")
    if app_segment_count >= 20:
        lines.append("- 把一天拆成 1-2 个任务块记录，减少跨应用切换后复盘困难。")
    if _error_signal_count(session):
        lines.append("- 如果今天有真正卡住的事，可以顺手记一句处理结果，避免明天重复排查。")
    if _safe_int(session.get("captures_written")) > 1000:
        lines.append("- 长时间记录后先看项目进展和可考虑方向，不要用记录条数判断工作质量。")
    lines.append("- 明天可以按 1-2 个任务块推进：先完成一个可交付结果，再切换到资料整理或沟通。")
    return lines


def _project_file_clues(project: dict[str, Any]) -> str:
    changed_files = project.get("changed_files", [])
    if not isinstance(changed_files, list) or not changed_files:
        return ""
    buckets: list[str] = []
    for path in [_safe_text(item) for item in changed_files[:8]]:
        if path == "AGENTS.md":
            bucket = "项目协作说明"
        elif path.startswith("docs/"):
            bucket = "文档"
        elif path.startswith("tests/"):
            bucket = "测试"
        elif path.startswith("plugins/") or "codex_plugins" in path:
            bucket = "插件"
        elif path.startswith("src/"):
            bucket = "核心代码"
        else:
            bucket = path.split("/", 1)[0] if "/" in path else path
        if bucket and bucket not in buckets:
            buckets.append(bucket)
    return "、".join(buckets[:4])


def _title_workstream_clues(session: dict[str, Any]) -> list[str]:
    segments = session.get("app_segments", [])
    if not isinstance(segments, list):
        return []
    rules = [
        ("Codex/OpenAI 相关调研或工具使用", ("codex", "openai", "chatgpt", "gpt")),
        ("论文、Excel 或数据审查工作", ("论文", "excel", "数据审查", "nc论文")),
        ("微信/小程序相关配置或开发", ("微信", "小程序", "wechatdevtools", "公众平台")),
        ("邮箱、账号或服务配置处理", ("gmail", "inbox", "登录", "仪表盘", "会员", "account")),
        ("网络、代理或环境配置", ("clash", "代理", "机场", "network", "vpn")),
    ]
    clues: list[str] = []
    for segment in segments:
        if not isinstance(segment, dict):
            continue
        haystack = " ".join(
            [
                _safe_text(segment.get("app_name", "")),
                _safe_text(segment.get("title", "")),
            ]
        ).lower()
        if not haystack.strip():
            continue
        for label, keywords in rules:
            if label in clues:
                continue
            if any(keyword.lower() in haystack for keyword in keywords):
                clues.append(label)
                break
        if len(clues) >= 4:
            break
    return clues


def _error_signal_count(session: dict[str, Any]) -> int:
    error_signals = session.get("error_signals")
    if not isinstance(error_signals, dict):
        return 0
    return _safe_int(error_signals.get("total_count"))


def _format_duration(seconds: int) -> str:
    if seconds <= 0:
        return "0 分钟"
    hours, remainder = divmod(seconds, 3600)
    minutes = max(1, round(remainder / 60)) if hours == 0 else round(remainder / 60)
    if hours and minutes:
        return f"{hours} 小时 {minutes} 分钟"
    if hours:
        return f"{hours} 小时"
    return f"{minutes} 分钟"


def _format_workday_retrospective(session: dict[str, Any], project_snapshot: Any) -> list[str]:
    app_segments = session.get("app_segments", [])
    apps = _top_app_names(app_segments)
    project_count = len(_snapshot_projects(project_snapshot))
    changed_project_count = _changed_project_count(project_snapshot)
    error_count = _safe_int(session.get("error_signals", {}).get("total_count")) if isinstance(session.get("error_signals"), dict) else 0
    lines = [
        "",
        "## 个人复盘",
        "",
    ]
    if changed_project_count:
        lines.append(f"- 可确认推进集中在 {changed_project_count} 个登记项目；优先按项目收尾比按应用收尾更清晰。")
    elif project_count:
        lines.append("- 已登记项目目录，但本轮没有明显 git 变更；工作可能偏阅读、沟通、调试或未保存。")
    else:
        lines.append("- 未登记项目目录，系统无法区分多个项目的真实推进，只能给出较粗的活动总结。")
    if apps:
        lines.append(f"- 主要应用线索: {', '.join(apps[:5])}。")
    if isinstance(app_segments, list) and len(app_segments) >= 6:
        lines.append("- 本轮上下文切换较多；下一轮可以按项目或任务块分段记录，减少复盘噪声。")
    if error_count:
        lines.append("- 复盘小提醒: 记录里出现过调试或异常线索；这只是收尾线索，不代表工作质量。真正卡住的事项可以顺手记一句处理结果。")
    if _safe_int(session.get("captures_written")) == 0:
        lines.append("- 本轮没有可用 capture；如果你愿意，可以补一句人工工作结果，避免日报只有空壳。")
    return lines


def _format_confirmation_notes(confirmation_notes: Sequence[str]) -> list[str]:
    notes = [_safe_text(note) for note in confirmation_notes if _safe_text(note)]
    if not notes:
        return []
    lines = [
        "",
        "## 用户确认事实",
        "",
    ]
    lines.extend(f"- {note}" for note in notes[:5])
    return lines


def _format_consideration_directions(session: dict[str, Any], project_snapshot: Any) -> list[str]:
    directions: list[str] = []
    unregistered_apps = _unregistered_activity_apps(session)
    if not _snapshot_projects(project_snapshot):
        directions.append("如果希望明晚更容易区分具体项目进展，可以告诉 WinChronicle 今天会持续推进哪些项目文件夹。")
    if _changed_project_count(project_snapshot) > 1:
        directions.append("多项目并行时，可以把每个项目拆成“完成项 / 阻塞 / 明天第一步”三个收尾标签。")
    if unregistered_apps:
        directions.append(
            f"如果希望下次按项目呈现这些活动，可以告诉 WinChronicle 相关项目文件夹；这次先保留软件名：{_join_cn(unregistered_apps)}。"
        )
    if _safe_int(session.get("error_signals", {}).get("total_count")) if isinstance(session.get("error_signals"), dict) else 0:
        directions.append("把调试或异常线索当作收尾提醒，不当成工作质量评价；明天先处理真正影响推进的一两件事。")
    directions.append(_workday_efficiency_direction(session))
    return [
        "",
        "## 可考虑方向",
        "",
        *[f"- {direction}" for direction in directions[:4]],
    ]


def _workday_efficiency_direction(session: dict[str, Any]) -> str:
    app_segments = session.get("app_segments", [])
    app_segment_count = len(app_segments) if isinstance(app_segments, list) else 0
    error_count = _error_signal_count(session)
    skipped = _skipped_total(session)
    captures = _safe_int(session.get("captures_written"))
    if error_count >= 10:
        return "明天先处理真正影响推进的事项：遇到真正卡住的问题先记录结论，再继续切换上下文。"
    if app_segment_count >= 20:
        return "明天可以减少上下文切换：把工作分成 1-2 个任务块，每块结束时写一句产出。"
    if captures and skipped > captures:
        return "明天可以减少重复窗口停留：长时间阅读或等待时可暂停记录，回到产出环节再继续。"
    return "明天可以降低信息整理成本：开始时说清目标，结束时补一句最重要完成项。"


def _format_agent_continuation_context(session: dict[str, Any], project_snapshot: Any) -> list[str]:
    lines = [
        "",
        "## 给下一线程的上下文",
        "",
        f"- session_id: {_safe_text(session.get('session_id', ''))}",
        f"- time_range: {_safe_text(session.get('started_at', ''))} -> {_safe_text(session.get('ended_at', ''))}",
        f"- capture_count: {_safe_int(session.get('captures_written'))}",
    ]
    projects = _snapshot_projects(project_snapshot)
    if projects:
        project_lines = []
        for project in projects[:5]:
            name = _safe_text(project.get("name", "project")) or "project"
            branch = _safe_text(project.get("branch", "")) or "unknown"
            changed_count = _safe_int(project.get("changed_file_count"))
            project_lines.append(f"{name}({branch}, {changed_count} files)")
        lines.append(f"- registered_projects: {', '.join(project_lines)}")
    else:
        lines.append("- registered_projects: none")
    lines.append("- privacy_boundary: no screen" "shots/" "O" "CR/clipboard/keylogging/audio/cloud upload/desktop control/MCP write tools")
    return lines


def _format_data_dashboard(session: dict[str, Any], project_snapshot: Any) -> list[str]:
    projects = _snapshot_projects(project_snapshot)
    changed_files = sum(_safe_int(project.get("changed_file_count")) for project in projects)
    return [
        "",
        "## 数据看板",
        "",
        f"- captures: {_safe_int(session.get('captures_written'))}",
        f"- skipped: {_skipped_total(session)}",
        f"- app_segments: {len(session.get('app_segments', [])) if isinstance(session.get('app_segments'), list) else 0}",
        f"- registered_projects: {len(projects)}",
        f"- changed_files_in_allowlist: {changed_files}",
        f"- error_signals: {_safe_int(session.get('error_signals', {}).get('total_count')) if isinstance(session.get('error_signals'), dict) else 0}",
    ]


def _safe_project_snapshot() -> dict[str, Any]:
    try:
        return snapshot_projects()
    except Exception:
        return {"projects": []}


def _snapshot_projects(project_snapshot: Any) -> list[dict[str, Any]]:
    if not isinstance(project_snapshot, dict):
        return []
    projects = project_snapshot.get("projects", [])
    if not isinstance(projects, list):
        return []
    return [project for project in projects if isinstance(project, dict)]


def _changed_project_count(project_snapshot: Any) -> int:
    return sum(1 for project in _snapshot_projects(project_snapshot) if _safe_int(project.get("changed_file_count")) > 0)


def _top_app_names(app_segments: Any) -> list[str]:
    if not isinstance(app_segments, list):
        return []
    counts: dict[str, int] = {}
    for segment in app_segments:
        if not isinstance(segment, dict):
            continue
        app = _safe_text(segment.get("app_name", ""))
        if not app:
            continue
        display = _friendly_app_name(app)
        counts[display] = counts.get(display, 0) + _safe_int(segment.get("capture_count"))
    return [
        app
        for app, _count in sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:5]
    ]


def _unregistered_activity_apps(session: dict[str, Any]) -> list[str]:
    app_segments = session.get("app_segments", [])
    if not isinstance(app_segments, list):
        return []
    interesting = {
        "chrome",
        "msedge",
        "firefox",
        "winword",
        "powerpnt",
        "excel",
        "explorer",
        "searchhost",
        "githubdesktop",
    }
    counts: dict[str, int] = {}
    display_names: dict[str, str] = {}
    for segment in app_segments:
        if not isinstance(segment, dict):
            continue
        app = _safe_text(segment.get("app_name", ""))
        key = app.casefold()
        if key not in interesting:
            continue
        counts[key] = counts.get(key, 0) + _safe_int(segment.get("capture_count"))
        display_names.setdefault(key, _friendly_app_name(app))
    return [
        display_names[key]
        for key, _count in sorted(counts.items(), key=lambda item: (-item[1], display_names[item[0]]))[:4]
    ]


def _friendly_app_name(app_name: str) -> str:
    key = _safe_text(app_name).casefold()
    names = {
        "chrome": "浏览器",
        "msedge": "浏览器",
        "firefox": "浏览器",
        "explorer": "文件管理器",
        "snippingtool": "截图工具",
        "winword": "Word 文档",
        "powerpnt": "PowerPoint",
        "excel": "Excel",
        "searchhost": "系统搜索",
        "clash-verge": "网络代理工具",
        "wechatdevtools": "微信开发者工具",
        "githubdesktop": "GitHub Desktop",
    }
    return names.get(key, _safe_text(app_name))


def _join_cn(items: Sequence[str]) -> str:
    return "、".join(_safe_text(item) for item in items if _safe_text(item))


def _session_focus_notes(session: dict[str, Any]) -> list[str]:
    return _safe_focus_notes(session.get("operator_focus", []))


def _safe_focus_notes(notes: Any) -> list[str]:
    if isinstance(notes, str):
        candidates: Sequence[Any] = [notes]
    elif isinstance(notes, Sequence):
        candidates = notes
    else:
        return []
    safe: list[str] = []
    for note in candidates:
        redacted, _counts = redact_text(" ".join(str(note).split()))
        text = (redacted or "")[:240]
        if text and text not in safe:
            safe.append(text)
        if len(safe) >= 5:
            break
    return safe


def _with_focus(summary: dict[str, Any] | None, focus_notes: Sequence[str]) -> dict[str, Any] | None:
    if summary is None:
        return None
    focus = _safe_focus_notes(focus_notes)
    if not focus or summary.get("operator_focus"):
        return summary
    updated = dict(summary)
    updated["operator_focus"] = focus
    return updated


def _attach_focus_to_payload(payload: dict[str, Any], focus_notes: Sequence[str]) -> None:
    summary = payload.get("summary")
    if isinstance(summary, dict):
        payload["summary"] = _with_focus(summary, focus_notes)


def _active_focus_notes(active_path: Path) -> list[str]:
    active = _read_json(active_path) or {}
    return _safe_focus_notes(active.get("operator_focus", []))


def _format_count_rows(rows: Any, key: str) -> str:
    if not isinstance(rows, list) or not rows:
        return "无"
    parts: list[str] = []
    for row in rows[:3]:
        if not isinstance(row, dict):
            continue
        name = _safe_text(row.get(key, ""))
        count = _safe_int(row.get("count"))
        if name:
            parts.append(f"{name}: {count}")
    return ", ".join(parts) if parts else "无"


def _status_available(value: Any) -> str:
    return "可用" if bool(value) else "不可用"


def _translate_suggestion(suggestion: str) -> str:
    if suggestion.startswith("Repeated UI state was observed"):
        return "检测到重复 UI 状态；复盘时可以合并未变化的步骤。"
    if suggestion.startswith("Multiple apps appeared"):
        return "本次会话涉及多个应用；可检查是否存在可减少的上下文切换。"
    if suggestion.startswith("Error-like text appeared"):
        return "会话中出现错误迹象；继续前建议检查相关 capture/source。"
    if suggestion.startswith("Some windows were intentionally skipped"):
        return "部分窗口因隐私规则或操作者设置被跳过。"
    if suggestion.startswith("Session captured stable UIA context"):
        return "本次会话没有发现确定性的低效信号。"
    if suggestion.startswith("Session summary was recovered"):
        return "摘要曾从已脱敏的本地 captures 恢复，跳过事件和 heartbeat 计数可能不完整。"
    return _safe_text(suggestion)


def _skipped_total(session: dict[str, Any]) -> int:
    keys = ("duplicates_skipped", "denylisted_skipped", "invalid_skipped", "excluded_skipped")
    return sum(_safe_int(session.get(key)) for key in keys)


def _safe_int(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def _safe_text(value: Any) -> str:
    return str(value or "").replace("\r", " ").replace("\n", " ").strip()


def _watcher_command(
    watcher_command: Sequence[str],
    helper_command: Sequence[str] | None,
    *,
    depth: int,
    duration_seconds: int,
    debounce_ms: int,
    heartbeat_ms: int,
    capture_on_start: bool,
) -> list[str]:
    if not watcher_command:
        raise WorkdayError("watcher command is required")
    command = [str(part) for part in watcher_command]
    command.extend(
        [
            "watch",
            "--depth",
            str(depth),
            "--debounce-ms",
            str(max(0, debounce_ms)),
            "--duration-ms",
            str(max(0, duration_seconds) * 1000),
            "--heartbeat-ms",
            str(max(250, heartbeat_ms)),
        ]
    )
    if helper_command:
        helper_parts = [str(part) for part in helper_command]
        command.extend(["--helper", helper_parts[0]])
        for helper_arg in helper_parts[1:]:
            command.extend(["--helper-arg", helper_arg])
    if capture_on_start:
        command.append("--capture-on-start")
    return command


def _start_reader(pipe: Any, destination: queue.Queue[str]) -> None:
    if pipe is None:
        return

    def read_lines() -> None:
        try:
            for line in pipe:
                destination.put(line)
        except Exception:
            return

    thread = threading.Thread(target=read_lines, daemon=True)
    thread.start()


def _drain(source: queue.Queue[str], destination: list[str]) -> None:
    while True:
        try:
            item = source.get_nowait()
        except queue.Empty:
            return
        destination.append(item)


def _drain_stdout_until_quiet(
    stdout_queue: queue.Queue[str],
    home: Path,
    *,
    state: MonitorSessionState,
    exclude_apps: Sequence[str],
    quiet_seconds: float = 0.2,
    max_seconds: float = 1.0,
) -> None:
    deadline = time.monotonic() + max_seconds
    quiet_deadline = time.monotonic() + quiet_seconds
    lines: list[str] = []
    while time.monotonic() < deadline:
        lines.clear()
        _drain(stdout_queue, lines)
        if lines:
            append_monitor_records(
                _parse_event_lines(lines),
                home,
                state=state,
                exclude_apps=exclude_apps,
            )
            quiet_deadline = time.monotonic() + quiet_seconds
        elif time.monotonic() >= quiet_deadline:
            return
        time.sleep(0.05)


def _parse_event_lines(lines: Sequence[str]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for line_number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ValueError(f"watcher JSONL line {line_number} is malformed") from exc
    return records


def _write_checkpoint(
    home: Path,
    *,
    session_id: str,
    state: MonitorSessionState,
    checkpoint_file: Path | None,
    payload: dict[str, Any] | None = None,
    operator_focus: Sequence[str] = (),
) -> None:
    if checkpoint_file is None or not state.timestamps:
        return
    if payload is None:
        result = write_monitor_session_state(
            home,
            session_id=session_id,
            mode="workday",
            state=state,
            operator_focus=operator_focus,
        )
        payload = {
            "active": True,
            "stopped": False,
            "summary_available": True,
            "summary": result.session,
            "path": str(result.path),
            "report_path": str(result.report_path),
            "trust": ACTIVE_TRUST,
            "capture_surface": CAPTURE_SURFACE,
            "checkpoint": True,
            "summary_source": "checkpoint",
        }
    _write_json(checkpoint_file, payload)


def _active_summary_details(
    *,
    result: dict[str, Any] | None,
    checkpoint: dict[str, Any] | None,
    session_id: str,
    home: Path,
) -> tuple[dict[str, Any] | None, str | None]:
    summary = _summary_from_payload(result)
    if summary is not None:
        return summary, "final_result"
    summary = _summary_from_payload(checkpoint)
    if summary is not None:
        return summary, "checkpoint"
    summary = _read_session_or_none(session_id, home)
    if summary is not None:
        return summary, "session_file"
    return None, None


def _summary_from_payload(payload: dict[str, Any] | None) -> dict[str, Any] | None:
    if not payload:
        return None
    summary = payload.get("summary")
    return summary if isinstance(summary, dict) else None


def _read_session_or_none(session_id: str, home: Path) -> dict[str, Any] | None:
    try:
        return read_session(session_id, home)
    except Exception:
        return None


def _checkpoint_fresh(
    *,
    checkpoint_available: bool,
    checkpoint_age_seconds: Any,
    stale_after_seconds: int,
) -> bool | None:
    if not checkpoint_available:
        return None
    if not isinstance(checkpoint_age_seconds, int):
        return False
    return checkpoint_age_seconds <= max(0, stale_after_seconds)


def _doctor_checks(
    *,
    active: bool,
    running: bool,
    bounded: bool,
    checkpoint_available: bool,
    checkpoint_fresh: bool | None,
    summary_available: bool,
    disabled_surfaces: dict[str, bool],
) -> list[dict[str, Any]]:
    privacy_ok = all(value is False for value in disabled_surfaces.values())
    checks = [
        {
            "name": "active_session",
            "ok": True,
            "detail": "active workday session found" if active else "no active workday session",
        },
        {
            "name": "capture_surface",
            "ok": True,
            "detail": CAPTURE_SURFACE,
        },
        {
            "name": "privacy_surfaces",
            "ok": privacy_ok,
            "detail": "disabled surfaces remain off" if privacy_ok else "disabled surface drift detected",
        },
    ]
    if active:
        checks.extend(
            [
                {
                    "name": "bounded_session",
                    "ok": bounded,
                    "detail": "session has a configured duration cap"
                    if bounded
                    else "active session is missing a duration cap",
                },
                {
                    "name": "runner_process",
                    "ok": running,
                    "detail": "recorded runner process is active"
                    if running
                    else "recorded runner process is not active",
                },
                {
                    "name": "checkpoint_available",
                    "ok": checkpoint_available,
                    "detail": "checkpoint summary is available"
                    if checkpoint_available
                    else "checkpoint summary is not available yet",
                },
                {
                    "name": "checkpoint_fresh",
                    "ok": checkpoint_fresh is True,
                    "detail": "checkpoint is within the freshness window"
                    if checkpoint_fresh is True
                    else "checkpoint is missing or stale",
                },
                {
                    "name": "summary_available",
                    "ok": summary_available,
                    "detail": "summary metadata is available"
                    if summary_available
                    else "summary metadata is not available yet",
                },
            ]
        )
    return checks


def _checkpoint_updated_at(path: Path) -> str:
    try:
        if not path.exists() or not path.is_file():
            return ""
        return (
            datetime.fromtimestamp(path.stat().st_mtime)
            .astimezone()
            .isoformat(timespec="seconds")
        )
    except Exception:
        return ""


def _checkpoint_age_seconds(path: Path) -> int | None:
    try:
        if not path.exists() or not path.is_file():
            return None
        return max(0, int(time.time() - path.stat().st_mtime))
    except Exception:
        return None


def _read_json(path: Path) -> dict[str, Any] | None:
    try:
        if not path.exists():
            return None
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _is_process_running(pid: int) -> bool:
    if pid <= 0:
        return False
    if os.name == "nt":
        import ctypes

        process_query_limited_information = 0x1000
        handle = ctypes.windll.kernel32.OpenProcess(
            process_query_limited_information,
            False,
            pid,
        )
        if not handle:
            return False
        ctypes.windll.kernel32.CloseHandle(handle)
        return True
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    return True


def _terminate_process_tree(pid: int) -> None:
    if pid <= 0:
        return
    if os.name == "nt":
        try:
            subprocess.run(
                ["taskkill", "/PID", str(pid), "/T", "/F"],
                check=False,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=_creation_flags(),
                timeout=2,
            )
        except subprocess.TimeoutExpired:
            try:
                os.kill(pid, signal.SIGTERM)
            except OSError:
                pass
        return
    try:
        os.kill(pid, signal.SIGTERM)
    except OSError:
        return


def _creation_flags() -> int:
    return subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _local_timestamp() -> str:
    return datetime.now().astimezone().strftime("%Y%m%d-%H%M%S")


def _slug(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9]+", "-", value).strip("-").lower()
    return slug or "workday"
