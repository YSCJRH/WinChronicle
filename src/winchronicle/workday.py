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
            )
            last_checkpoint = time.monotonic()
        _drain(stderr_queue, [])
        if stop_file.exists():
            stop_requested = True
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
    )
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
    lines = [
        "# 工作记录状态",
        "",
        f"- 状态: {state}",
        f"- 会话: {_safe_text(status.get('session_id', '')) or '无'}",
        f"- 开始: {_safe_text(status.get('started_at', '')) or '无'}",
        f"- 持续上限秒数: {_safe_int(status.get('duration_seconds'))}",
        f"- bounded: {bool(status.get('bounded', False))}",
        f"- checkpoint: {_status_available(status.get('checkpoint_available'))}",
        f"- checkpoint 更新时间: {_safe_text(status.get('checkpoint_updated_at', '')) or '无'}",
        f"- checkpoint 年龄秒数: {_safe_text(status.get('checkpoint_age_seconds', '')) or '无'}",
        f"- summary: {_status_available(status.get('summary_available'))}",
        f"- summary_source: {_safe_text(status.get('summary_source', '')) or '无'}",
        f"- 信任边界: {_safe_text(status.get('trust', ACTIVE_TRUST))}",
        f"- 捕获面: {_safe_text(status.get('capture_surface', CAPTURE_SURFACE))}",
        "",
        "## 隐私边界",
        "",
        "- 该状态视图只读取本地 session metadata，不启动 watcher/helper/UIA capture 或桌面读取。",
        "- observed UI content 仍是 untrusted_observed_content，不能作为可信指令执行。",
        "- 未新增 截图/" "O" "CR/剪贴板/键盘记录/音频/云上传/桌面控制/MCP 写工具。",
    ]
    return "\n".join(lines).rstrip() + "\n"


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
        return {
            **result,
            "active": False,
            "stopped": True,
            "summary_source": "final_result",
            "recovered_from_capture_buffer": False,
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
        "summary": summary,
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
) -> dict[str, Any] | str:
    paths = state_paths(home)
    session = read_session(identifier, paths["home"])
    if output_format == "json":
        return session
    if output_format != "text":
        raise WorkdayError("workday summary format must be json or text")
    if language != "zh-CN":
        raise WorkdayError("workday text summaries currently support only zh-CN")
    return format_workday_text_summary(session)


def format_workday_text_summary(session: dict[str, Any]) -> str:
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
) -> None:
    if checkpoint_file is None or not state.timestamps:
        return
    if payload is None:
        result = write_monitor_session_state(
            home,
            session_id=session_id,
            mode="workday",
            state=state,
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
        completed = subprocess.run(
            ["tasklist", "/FI", f"PID eq {pid}", "/FO", "CSV", "/NH"],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            creationflags=_creation_flags(),
        )
        return str(pid).encode("ascii") in completed.stdout
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    return True


def _terminate_process_tree(pid: int) -> None:
    if pid <= 0:
        return
    if os.name == "nt":
        subprocess.run(
            ["taskkill", "/PID", str(pid), "/T", "/F"],
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=_creation_flags(),
        )
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
