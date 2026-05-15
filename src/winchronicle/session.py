from __future__ import annotations

import hashlib
import html
import json
import re
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable, Sequence

from .capture import normalize_uia_helper_output, persist_capture
from .memory import TRUST, TRUST_BOUNDARY_INSTRUCTION
from .paths import ensure_state, state_paths
from .privacy import denylist_reason
from .schema import validate_session_report, validate_uia_helper_output, validate_watcher_event
from .storage import capture_fingerprint_exists


CAPTURE_EVENT_TYPES = {"foreground_changed", "name_changed", "value_changed"}


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
    counts = {
        "captures_written": 0,
        "duplicates_skipped": 0,
        "denylisted_skipped": 0,
        "excluded_skipped": 0,
        "heartbeats": 0,
    }
    seen_fingerprints: set[str] = set()
    timeline: list[dict[str, str]] = []
    timestamps: list[str] = []
    excluded = {app.casefold() for app in exclude_apps}

    for record in records:
        validate_watcher_event(record)
        timestamps.append(record["timestamp"])
        event_type = record["event_type"]
        if event_type == "heartbeat":
            counts["heartbeats"] += 1
            continue
        if event_type not in CAPTURE_EVENT_TYPES:
            continue

        output = record.get("capture")
        if not isinstance(output, dict):
            raise ValueError(f"{event_type} watcher event requires capture")
        validate_uia_helper_output(output)

        app_name = str(output.get("window", {}).get("app_name", ""))
        if app_name.casefold() in excluded:
            counts["excluded_skipped"] += 1
            continue
        if denylist_reason(output):
            counts["denylisted_skipped"] += 1
            continue

        capture = normalize_uia_helper_output(output)
        fingerprint = capture["content_fingerprint"]
        if fingerprint in seen_fingerprints or capture_fingerprint_exists(fingerprint, paths["home"]):
            counts["duplicates_skipped"] += 1
            continue

        seen_fingerprints.add(fingerprint)
        result = persist_capture(capture, str(record.get("event_id") or event_type), paths["home"])
        if result.path is None or result.capture is None:
            continue
        counts["captures_written"] += 1
        timeline.append(_timeline_capture(result.capture, result.path))

    session = _build_session_report(
        paths,
        session_id=_slug(session_id) if session_id else _session_id(timestamps, timeline),
        mode=mode,
        timestamps=timestamps,
        timeline=timeline,
        counts=counts,
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
        "source_capture_paths": [item["path"] for item in timeline],
        "report_path": str(report_path),
    }
    validate_session_report(session)
    return session


def _write_session(paths: dict[str, Path], session: dict[str, Any]) -> MonitorSessionResult:
    session_path = paths["sessions"] / f"{session['session_id']}.json"
    report_path = Path(session["report_path"])
    session_path.write_text(json.dumps(session, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report_path.write_text(_render_html_report(session) + "\n", encoding="utf-8")
    return MonitorSessionResult(session_path, report_path, session)


def _app_segments(timeline: list[dict[str, str]]) -> list[dict[str, Any]]:
    segments: list[dict[str, Any]] = []
    for item in timeline:
        if segments and segments[-1]["app_name"] == item["app_name"] and segments[-1]["title"] == item["title"]:
            segments[-1]["end_timestamp"] = item["timestamp"]
            segments[-1]["capture_count"] += 1
            continue
        segments.append(
            {
                "app_name": item["app_name"],
                "title": item["title"],
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
    return any(term in haystack for term in ("error", "exception", "failed", "failure", "traceback"))


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


def _slug(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9]+", "-", value).strip("-").lower()
    return slug or "session"
