from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Sequence

from .capture import normalize_uia_helper_output, persist_capture
from .privacy import denylist_reason
from .schema import validate_uia_helper_output, validate_watcher_event
from .storage import capture_fingerprint_exists


CAPTURE_EVENT_TYPES = {"foreground_changed", "name_changed", "value_changed"}


@dataclass(frozen=True)
class DispatchResult:
    captures_written: int = 0
    duplicates_skipped: int = 0
    denylisted_skipped: int = 0
    heartbeats: int = 0

    def to_json(self) -> dict[str, int]:
        return {
            "captures_written": self.captures_written,
            "duplicates_skipped": self.duplicates_skipped,
            "denylisted_skipped": self.denylisted_skipped,
            "heartbeats": self.heartbeats,
        }


def dispatch_watcher_events(
    event_path: Path | str,
    home: Path | str | None = None,
) -> DispatchResult:
    return dispatch_watcher_records(_read_jsonl(event_path), home)


def dispatch_watcher_event_lines(
    lines: Iterable[str],
    home: Path | str | None = None,
) -> DispatchResult:
    events = [json.loads(line) for line in lines if line.strip()]
    return dispatch_watcher_records(events, home)


def dispatch_watcher_records(
    events: Iterable[dict[str, Any]],
    home: Path | str | None = None,
) -> DispatchResult:
    counts = {
        "captures_written": 0,
        "duplicates_skipped": 0,
        "denylisted_skipped": 0,
        "heartbeats": 0,
    }
    seen_fingerprints: set[str] = set()

    for event in events:
        validate_watcher_event(event)
        event_type = event["event_type"]
        if event_type == "heartbeat":
            counts["heartbeats"] += 1
            continue

        if event_type not in CAPTURE_EVENT_TYPES:
            continue

        output = event.get("capture")
        if not isinstance(output, dict):
            raise ValueError(f"{event_type} watcher event requires capture")
        validate_uia_helper_output(output)

        if denylist_reason(output):
            counts["denylisted_skipped"] += 1
            continue

        capture = normalize_uia_helper_output(output)
        fingerprint = capture["content_fingerprint"]
        if fingerprint in seen_fingerprints or capture_fingerprint_exists(fingerprint, home):
            counts["duplicates_skipped"] += 1
            continue

        seen_fingerprints.add(fingerprint)
        persist_capture(capture, str(event.get("event_id") or event_type), home)
        counts["captures_written"] += 1

    return DispatchResult(**counts)


def run_watcher_command(
    watcher_command: Sequence[str | Path],
    helper_command: Sequence[str | Path] | None = None,
    *,
    depth: int = 80,
    duration_seconds: int = 30,
    debounce_ms: int = 750,
    heartbeat_ms: int = 5000,
    capture_on_start: bool = False,
    home: Path | str | None = None,
) -> DispatchResult:
    if not watcher_command:
        raise ValueError("watcher command is required")
    if not 0 <= depth <= 80:
        raise ValueError("depth must be between 0 and 80")
    if duration_seconds < 0:
        raise ValueError("duration must be non-negative")

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

    completed = subprocess.run(
        command,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if completed.returncode != 0:
        raise RuntimeError(f"watcher failed with exit code {completed.returncode}")

    return dispatch_watcher_event_lines(completed.stdout.splitlines(), home)


def _read_jsonl(path: Path | str) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.strip():
            events.append(json.loads(line))
    return events
