from __future__ import annotations

import hashlib
import html
import json
import os
import re
import subprocess
import time
from collections import Counter
from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable, Sequence

from .capture import normalize_uia_helper_output, persist_capture
from .memory import TRUST, TRUST_BOUNDARY_INSTRUCTION
from .paths import ensure_state, state_paths
from .privacy import denylist_reason
from .redaction import redact_text
from .schema import validate_capture, validate_session_report, validate_uia_helper_output, validate_watcher_event
from .storage import capture_fingerprint_exists


CAPTURE_EVENT_TYPES = {"foreground_changed", "name_changed", "value_changed"}
MAX_APP_SEGMENTS = 500
MAX_TITLE_CHARS = 240
SOURCE_CAPTURE_PATHS_LIMIT = 1000
ERROR_SIGNAL_SAMPLE_LIMIT = 25
ERROR_SIGNAL_ROW_LIMIT = 25
ERROR_SIGNAL_TEXT_LIMIT = 120
ERROR_SIGNAL_TERMS = ("error", "exception", "failed", "failure", "traceback")


@dataclass(frozen=True)
class MonitorSessionResult:
    path: Path
    report_path: Path
    session: dict[str, Any]

    def to_json(self) -> dict[str, Any]:
        return {
            **self.session,
            "path": str(self.path),
            "report_path": str(self.report_path),
        }


@dataclass
class MonitorSessionState:
    counts: dict[str, int]
    seen_fingerprints: set[str]
    timeline: list[dict[str, str]]
    timestamps: list[str]


def monitor_events(
    event_path: Path | str,
    home: Path | str | None = None,
    *,
    session_id: str | None = None,
    exclude_apps: Sequence[str] = (),
) -> MonitorSessionResult:
    return monitor_event_lines(
        Path(event_path).read_text(encoding="utf-8").splitlines(),
        home,
        session_id=session_id,
        mode="events",
        exclude_apps=exclude_apps,
    )


def monitor_event_lines(
    lines: Iterable[str],
    home: Path | str | None = None,
    *,
    session_id: str | None = None,
    mode: str = "events",
    exclude_apps: Sequence[str] = (),
) -> MonitorSessionResult:
    records: list[dict[str, Any]] = []
    for line_number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ValueError(f"watcher JSONL line {line_number} is malformed") from exc
    return monitor_records(
        records,
        home,
        session_id=session_id,
        mode=mode,
        exclude_apps=exclude_apps,
    )


def monitor_records(
    records: Iterable[dict[str, Any]],
    home: Path | str | None = None,
    *,
    session_id: str | None = None,
    mode: str = "events",
    exclude_apps: Sequence[str] = (),
) -> MonitorSessionResult:
    paths = ensure_state(home)
    state = create_monitor_session_state()
    append_monitor_records(records, paths["home"], state=state, exclude_apps=exclude_apps)
    return write_monitor_session_state(
        paths["home"],
        session_id=_slug(session_id) if session_id else _session_id(state.timestamps, state.timeline),
        mode=mode,
        state=state,
    )


def create_monitor_session_state() -> MonitorSessionState:
    return MonitorSessionState(
        counts={
            "captures_written": 0,
            "duplicates_skipped": 0,
            "denylisted_skipped": 0,
            "excluded_skipped": 0,
            "heartbeats": 0,
        },
        seen_fingerprints=set(),
        timeline=[],
        timestamps=[],
    )


def append_monitor_records(
    records: Iterable[dict[str, Any]],
    home: Path | str | None = None,
    *,
    state: MonitorSessionState,
    exclude_apps: Sequence[str] = (),
) -> None:
    paths = ensure_state(home)
    excluded = {app.casefold() for app in exclude_apps}

    for record in records:
        validate_watcher_event(record)
        state.timestamps.append(record["timestamp"])
        event_type = record["event_type"]
        if event_type == "heartbeat":
            state.counts["heartbeats"] += 1
            continue
        if event_type not in CAPTURE_EVENT_TYPES:
            continue

        output = record.get("capture")
        if not isinstance(output, dict):
            raise ValueError(f"{event_type} watcher event requires capture")
        validate_uia_helper_output(output)

        app_name = str(output.get("window", {}).get("app_name", ""))
        if app_name.casefold() in excluded:
            state.counts["excluded_skipped"] += 1
            continue
        if denylist_reason(output):
            state.counts["denylisted_skipped"] += 1
            continue

        capture = normalize_uia_helper_output(output)
        fingerprint = capture["content_fingerprint"]
        if fingerprint in state.seen_fingerprints or capture_fingerprint_exists(fingerprint, paths["home"]):
            state.counts["duplicates_skipped"] += 1
            continue

        state.seen_fingerprints.add(fingerprint)
        result = persist_capture(capture, str(record.get("event_id") or event_type), paths["home"])
        if result.path is None or result.capture is None:
            continue
        state.counts["captures_written"] += 1
        state.timeline.append(_timeline_capture(result.capture, result.path))


def write_monitor_session_state(
    home: Path | str | None,
    *,
    session_id: str,
    mode: str,
    state: MonitorSessionState,
    extra_suggestions: Sequence[str] = (),
    operator_focus: Sequence[str] = (),
) -> MonitorSessionResult:
    paths = ensure_state(home)
    session = _build_session_report(
        paths,
        session_id=_slug(session_id),
        mode=mode,
        timestamps=list(state.timestamps),
        timeline=list(state.timeline),
        counts=dict(state.counts),
    )
    for suggestion in extra_suggestions:
        if suggestion not in session["suggestions"]:
            session["suggestions"].append(suggestion)
    focus = _safe_operator_focus(operator_focus)
    if focus:
        session["operator_focus"] = focus
    return _write_session(paths, session)


def recover_session_from_capture_buffer(
    home: Path | str | None,
    *,
    session_id: str,
    started_at: str,
    ended_at: str | None = None,
    mode: str = "workday",
    minimum_captures: int = 0,
) -> MonitorSessionResult:
    paths = ensure_state(home)
    timeline: list[dict[str, str]] = []
    for path in sorted(paths["capture_buffer"].glob("*.json")):
        try:
            capture = json.loads(path.read_text(encoding="utf-8"))
            validate_capture(capture)
        except Exception:
            continue
        timestamp = str(capture.get("timestamp", ""))
        if not _timestamp_in_range(timestamp, started_at, ended_at):
            continue
        timeline.append(_timeline_capture(capture, path))

    timeline.sort(key=lambda item: (item["timestamp"], item["path"]))
    if len(timeline) < minimum_captures:
        raise ValueError("recovered capture count is lower than the existing checkpoint")
    timestamps = [item["timestamp"] for item in timeline]
    if started_at:
        timestamps.append(started_at)
    if ended_at:
        timestamps.append(ended_at)
    counts = {
        "captures_written": len(timeline),
        "duplicates_skipped": 0,
        "denylisted_skipped": 0,
        "excluded_skipped": 0,
        "heartbeats": 0,
    }
    session = _build_session_report(
        paths,
        session_id=_slug(session_id),
        mode=mode,
        timestamps=timestamps,
        timeline=timeline,
        counts=counts,
    )
    session["suggestions"].append(
        "Session summary was recovered from persisted redacted captures after the final workday result was unavailable; skipped-event and heartbeat counts may be incomplete."
    )
    return _write_session(paths, session)


def run_monitor_watcher_command(
    watcher_command: Sequence[str | Path],
    helper_command: Sequence[str | Path] | None = None,
    *,
    depth: int = 80,
    duration_seconds: int = 30,
    debounce_ms: int = 750,
    heartbeat_ms: int = 5000,
    capture_on_start: bool = False,
    home: Path | str | None = None,
    session_id: str | None = None,
    exclude_apps: Sequence[str] = (),
    timeout_seconds: float | None = None,
) -> MonitorSessionResult:
    if not watcher_command:
        raise ValueError("watcher command is required")
    command = [str(part) for part in watcher_command]
    command.extend(
        [
            "watch",
            "--depth",
            str(depth),
            "--debounce-ms",
            str(max(0, debounce_ms)),
            "--duration-ms",
            str(duration_seconds * 1000),
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

    timeout = timeout_seconds if timeout_seconds is not None else max(duration_seconds + 10, 10)
    try:
        completed = subprocess.run(
            command,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError("watcher timed out") from exc
    if completed.returncode != 0:
        raise RuntimeError(f"watcher failed with exit code {completed.returncode}")
    try:
        return monitor_event_lines(
            completed.stdout.splitlines(),
            home,
            session_id=session_id,
            mode="watcher",
            exclude_apps=exclude_apps,
        )
    except ValueError as exc:
        raise RuntimeError(str(exc)) from exc


def read_session(identifier: str | Path, home: Path | str | None = None) -> dict[str, Any]:
    session_id = _slug(str(identifier))
    path = state_paths(home)["sessions"] / f"{session_id}.json"
    session = json.loads(path.read_text(encoding="utf-8"))
    validate_session_report(session)
    return session


def session_count(home: Path | str | None = None) -> int:
    sessions = state_paths(home)["sessions"]
    if not sessions.exists():
        return 0
    return len(list(sessions.glob("*.json")))


def list_sessions(
    home: Path | str | None = None,
    *,
    limit: int = 5,
) -> list[dict[str, Any]]:
    sessions = state_paths(home)["sessions"]
    if not sessions.exists():
        return []
    results: list[dict[str, Any]] = []
    for path in sorted(sessions.glob("*.json")):
        try:
            session = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        results.append(
            {
                "session_id": session.get("session_id", ""),
                "started_at": session.get("started_at", ""),
                "ended_at": session.get("ended_at", ""),
                "captures_written": int(session.get("captures_written", 0)),
                "app_segments": session.get("app_segments", []),
                "suggestions": session.get("suggestions", []),
                "report_path": session.get("report_path", ""),
                "trust": TRUST,
                "untrusted_observed_content": True,
                "instruction": TRUST_BOUNDARY_INSTRUCTION,
            }
        )
    results.sort(key=lambda item: (item["ended_at"], item["session_id"]), reverse=True)
    return results[: max(0, limit)]


def _timeline_capture(capture: dict[str, Any], path: Path) -> dict[str, str]:
    focused = capture["focused_element"]
    return {
        "timestamp": capture["timestamp"],
        "app_name": capture["window_meta"]["app_name"],
        "title": capture["window_meta"]["title"],
        "visible_text": capture["visible_text"],
        "focused_text": focused.get("text") or focused.get("value") or "",
        "path": str(path),
    }


def _build_session_report(
    paths: dict[str, Path],
    *,
    session_id: str,
    mode: str,
    timestamps: list[str],
    timeline: list[dict[str, str]],
    counts: dict[str, int],
) -> dict[str, Any]:
    started_at = min(timestamps) if timestamps else ""
    ended_at = max(timestamps) if timestamps else started_at
    report_path = paths["reports"] / f"{session_id}.html"
    session = {
        "session_schema_version": 1,
        "session_id": session_id,
        "mode": mode,
        "started_at": started_at,
        "ended_at": ended_at,
        "duration_seconds": _duration_seconds(started_at, ended_at),
        "trust": TRUST,
        "instruction": TRUST_BOUNDARY_INSTRUCTION,
        "untrusted_observed_content": True,
        **counts,
        "app_segments": _app_segments(timeline),
        "suggestions": _suggestions(timeline, counts),
        "error_signals": _error_signals(timeline),
        "source_capture_paths": [item["path"] for item in timeline][:SOURCE_CAPTURE_PATHS_LIMIT],
        "storage_policy": {
            "raw_watcher_jsonl_saved": False,
            "html_report_contains_visible_text": False,
            "max_app_segments": MAX_APP_SEGMENTS,
            "max_title_chars": MAX_TITLE_CHARS,
            "source_capture_paths_limit": SOURCE_CAPTURE_PATHS_LIMIT,
        },
        "storage_usage": {
            "session_json_bytes": 0,
            "html_report_bytes": 0,
        },
        "report_path": str(report_path),
    }
    return session


def _write_session(paths: dict[str, Path], session: dict[str, Any]) -> MonitorSessionResult:
    persisted_session = deepcopy(session)
    session_path = paths["sessions"] / f"{persisted_session['session_id']}.json"
    report_path = Path(persisted_session["report_path"])
    html_text = _render_html_report(persisted_session) + "\n"
    persisted_session["storage_usage"]["html_report_bytes"] = len(html_text.encode("utf-8"))
    persisted_session["storage_usage"]["session_json_bytes"] = 0
    json_text = ""
    for _ in range(5):
        json_text = json.dumps(persisted_session, indent=2, sort_keys=True) + "\n"
        size = len(json_text.encode("utf-8"))
        if persisted_session["storage_usage"]["session_json_bytes"] == size:
            break
        persisted_session["storage_usage"]["session_json_bytes"] = size
    json_text = json.dumps(persisted_session, indent=2, sort_keys=True) + "\n"
    validate_session_report(persisted_session)
    report_temp: Path | None = None
    session_temp: Path | None = None
    old_report_bytes = report_path.read_bytes() if report_path.exists() else None
    try:
        report_temp = _write_temp_bytes(report_path, html_text.encode("utf-8"))
        session_temp = _write_temp_bytes(session_path, json_text.encode("utf-8"))
        report_temp.replace(report_path)
        report_temp = None
        try:
            session_temp.replace(session_path)
            session_temp = None
        except Exception:
            _restore_file(report_path, old_report_bytes)
            raise
    finally:
        if report_temp is not None:
            report_temp.unlink(missing_ok=True)
        if session_temp is not None:
            session_temp.unlink(missing_ok=True)
    return MonitorSessionResult(session_path, report_path, persisted_session)


def _write_temp_bytes(path: Path, data: bytes) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.with_name(f".{path.name}.{os.getpid()}.{time.monotonic_ns()}.tmp")
    try:
        with temp_path.open("wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
    except Exception:
        temp_path.unlink(missing_ok=True)
        raise
    return temp_path


def _restore_file(path: Path, data: bytes | None) -> None:
    if data is None:
        path.unlink(missing_ok=True)
        return
    temp_path = _write_temp_bytes(path, data)
    try:
        temp_path.replace(path)
    finally:
        temp_path.unlink(missing_ok=True)


def _safe_operator_focus(notes: Sequence[str]) -> list[str]:
    safe: list[str] = []
    for note in notes:
        redacted, _counts = redact_text(" ".join(str(note).split()))
        text = (redacted or "")[:240]
        if text and text not in safe:
            safe.append(text)
        if len(safe) >= 5:
            break
    return safe


def _app_segments(timeline: list[dict[str, str]]) -> list[dict[str, Any]]:
    segments: list[dict[str, Any]] = []
    for item in timeline:
        if segments and segments[-1]["app_name"] == item["app_name"] and segments[-1]["title"] == item["title"]:
            segments[-1]["end_timestamp"] = item["timestamp"]
            segments[-1]["capture_count"] += 1
            continue
        if len(segments) >= MAX_APP_SEGMENTS:
            segments[-1]["end_timestamp"] = item["timestamp"]
            segments[-1]["capture_count"] += 1
            continue
        segments.append(
            {
                "app_name": _clip_text(item["app_name"], MAX_TITLE_CHARS),
                "title": _clip_text(item["title"], MAX_TITLE_CHARS),
                "start_timestamp": item["timestamp"],
                "end_timestamp": item["timestamp"],
                "capture_count": 1,
            }
        )
    return segments


def _suggestions(timeline: list[dict[str, str]], counts: dict[str, int]) -> list[str]:
    suggestions: list[str] = []
    if counts["duplicates_skipped"]:
        suggestions.append("Repeated UI state was observed; collapse unchanged steps in the next review.")
    if len({item["app_name"] for item in timeline if item["app_name"]}) >= 3:
        suggestions.append("Multiple apps appeared in one session; review whether task context switching is avoidable.")
    if any(_looks_like_error(item) for item in timeline):
        suggestions.append("Error-like text appeared in the session; inspect the related capture before continuing.")
    if counts["denylisted_skipped"] or counts["excluded_skipped"]:
        suggestions.append("Some windows were intentionally skipped by privacy or operator controls.")
    if not suggestions:
        suggestions.append("Session captured stable UIA context; no deterministic friction signal was found.")
    return suggestions


def _looks_like_error(item: dict[str, str]) -> bool:
    haystack = f"{item['title']} {item['visible_text']} {item['focused_text']}".casefold()
    return any(term in haystack for term in ERROR_SIGNAL_TERMS)


def _error_signals(timeline: list[dict[str, str]]) -> dict[str, Any]:
    app_counts: Counter[str] = Counter()
    field_counts: Counter[str] = Counter()
    keyword_counts: Counter[str] = Counter()
    bucket_counts: Counter[str] = Counter()
    samples: list[dict[str, Any]] = []
    total = 0

    for item in timeline:
        field_hits = _error_field_hits(item)
        if not field_hits:
            continue
        total += 1
        app_name = _signal_text(item.get("app_name", "") or "unknown")
        bucket = _error_time_bucket(item.get("timestamp", ""))
        keywords = sorted({term for terms in field_hits.values() for term in terms})
        app_counts[app_name] += 1
        if bucket:
            bucket_counts[bucket] += 1
        for field, terms in field_hits.items():
            field_counts[field] += 1
            for term in terms:
                keyword_counts[term] += 1
        if len(samples) < ERROR_SIGNAL_SAMPLE_LIMIT:
            samples.append(
                {
                    "timestamp": _error_signal_timestamp(item.get("timestamp", "")),
                    "time_bucket": bucket,
                    "app_name": app_name,
                    "fields": _ordered_fields(field_hits),
                    "keywords": keywords,
                    "source_id": _source_id(item.get("path", "")),
                }
            )

    return {
        "schema_version": 1,
        "trust": TRUST,
        "contains_observed_text": False,
        "total_count": total,
        "sample_limit": ERROR_SIGNAL_SAMPLE_LIMIT,
        "by_app": _counter_rows(app_counts, "app_name", limit=ERROR_SIGNAL_ROW_LIMIT),
        "by_field": _counter_rows(
            field_counts,
            "field",
            order=("visible_text", "focused_text", "title"),
            limit=ERROR_SIGNAL_ROW_LIMIT,
        ),
        "by_keyword": _counter_rows(keyword_counts, "keyword", limit=ERROR_SIGNAL_ROW_LIMIT),
        "time_buckets": _counter_rows(bucket_counts, "bucket_start", limit=ERROR_SIGNAL_ROW_LIMIT),
        "samples": samples,
    }


def _error_field_hits(item: dict[str, str]) -> dict[str, list[str]]:
    hits: dict[str, list[str]] = {}
    fields = {
        "title": item.get("title", ""),
        "visible_text": item.get("visible_text", ""),
        "focused_text": item.get("focused_text", ""),
    }
    for field, value in fields.items():
        value_folded = value.casefold()
        terms = [term for term in ERROR_SIGNAL_TERMS if term in value_folded]
        if terms:
            hits[field] = terms
    return hits


def _ordered_fields(field_hits: dict[str, list[str]]) -> list[str]:
    preferred = ("visible_text", "focused_text", "title")
    return [field for field in preferred if field in field_hits]


def _error_time_bucket(timestamp: str) -> str:
    try:
        parsed = datetime.fromisoformat(timestamp)
    except ValueError:
        return ""
    bucket_minute = (parsed.minute // 15) * 15
    bucketed = parsed.replace(minute=bucket_minute, second=0, microsecond=0)
    return bucketed.isoformat(timespec="minutes")


def _error_signal_timestamp(timestamp: str) -> str:
    try:
        return datetime.fromisoformat(timestamp).isoformat(timespec="seconds")
    except ValueError:
        return ""


def _source_id(path: str) -> str:
    suffix = Path(path).stem.rsplit("-", 1)[-1]
    if re.fullmatch(r"[0-9a-f]{12}", suffix):
        return f"capture-{suffix}"
    return ""


def _signal_text(value: str) -> str:
    return _clip_text(value, ERROR_SIGNAL_TEXT_LIMIT)


def _counter_rows(
    counter: Counter[str],
    name_key: str,
    *,
    order: Sequence[str] = (),
    limit: int | None = None,
) -> list[dict[str, Any]]:
    order_index = {key: index for index, key in enumerate(order)}
    rows = [
        {name_key: _signal_text(key), "count": count}
        for key, count in sorted(
            counter.items(),
            key=lambda item: (-item[1], order_index.get(item[0], len(order_index)), item[0]),
        )
    ]
    if limit is None:
        return rows
    return rows[: max(0, limit)]


def _render_html_report(session: dict[str, Any]) -> str:
    rows = "\n".join(
        "<tr>"
        f"<td>{html.escape(segment['start_timestamp'])}</td>"
        f"<td>{html.escape(segment['end_timestamp'])}</td>"
        f"<td>{html.escape(segment['app_name'])}</td>"
        f"<td>{html.escape(segment['title'])}</td>"
        f"<td>{segment['capture_count']}</td>"
        "</tr>"
        for segment in session["app_segments"]
    )
    suggestions = "\n".join(f"<li>{html.escape(text)}</li>" for text in session["suggestions"])
    return "\n".join(
        [
            "<!doctype html>",
            "<meta charset=\"utf-8\">",
            f"<title>{html.escape(session['session_id'])}</title>",
            f"<h1>WinChronicle session {html.escape(session['session_id'])}</h1>",
            f"<p>Trust: {html.escape(session['trust'])}</p>",
            f"<p>{html.escape(session['instruction'])}</p>",
            "<h2>Summary</h2>",
            "<ul>",
            f"<li>Started: {html.escape(session['started_at'])}</li>",
            f"<li>Ended: {html.escape(session['ended_at'])}</li>",
            f"<li>Captures: {session['captures_written']}</li>",
            f"<li>Duplicates skipped: {session['duplicates_skipped']}</li>",
            f"<li>Privacy skipped: {session['denylisted_skipped']}</li>",
            f"<li>Operator excluded: {session['excluded_skipped']}</li>",
            f"<li>Heartbeats: {session['heartbeats']}</li>",
            "</ul>",
            "<h2>Suggestions</h2>",
            f"<ul>{suggestions}</ul>",
            "<h2>Timeline</h2>",
            "<table>",
            "<thead><tr><th>Start</th><th>End</th><th>App</th><th>Title</th><th>Captures</th></tr></thead>",
            f"<tbody>{rows}</tbody>",
            "</table>",
        ]
    )


def _session_id(timestamps: list[str], timeline: list[dict[str, str]]) -> str:
    seed = json.dumps({"timestamps": timestamps, "paths": [item["path"] for item in timeline]}, sort_keys=True)
    digest = hashlib.sha256(seed.encode("utf-8")).hexdigest()[:12]
    base = _slug(timestamps[0] if timestamps else "empty-session")
    return f"session-{base}-{digest}"


def _duration_seconds(started_at: str, ended_at: str) -> int:
    try:
        start = datetime.fromisoformat(started_at)
        end = datetime.fromisoformat(ended_at)
    except ValueError:
        return 0
    return max(0, int((end - start).total_seconds()))


def _timestamp_in_range(timestamp: str, started_at: str, ended_at: str | None) -> bool:
    try:
        current = datetime.fromisoformat(timestamp)
        start = datetime.fromisoformat(started_at) if started_at else None
        end = datetime.fromisoformat(ended_at) if ended_at else None
    except ValueError:
        after_start = not started_at or timestamp >= started_at
        before_end = not ended_at or timestamp <= ended_at
        return after_start and before_end

    if start is not None and current < start:
        return False
    if end is not None and current > end:
        return False
    return True


def _slug(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9]+", "-", value).strip("-").lower()
    return slug or "session"


def _clip_text(value: str, limit: int) -> str:
    if len(value) <= limit:
        return value
    return value[: max(0, limit - 3)] + "..."
