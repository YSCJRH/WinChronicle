from __future__ import annotations

import hashlib
import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence

from .paths import ensure_state
from .privacy import denylist_reason
from .redaction import redact_capture, scan_for_unredacted_secrets
from .schema import validate_capture, validate_uia_helper_output
from .storage import index_capture


@dataclass(frozen=True)
class CaptureResult:
    path: Path | None
    capture: dict[str, Any] | None
    skipped: bool = False
    reason: str | None = None


@dataclass(frozen=True)
class PrivacyCheckResult:
    ok: bool
    messages: list[str]


def load_json(path: Path | str) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def normalize_fixture(fixture: dict[str, Any]) -> dict[str, Any]:
    return _normalize_capture_record(
        record=fixture,
        source="fixture",
        trigger_source="manual",
        event_type="capture_once",
    )


def normalize_uia_helper_output(output: dict[str, Any]) -> dict[str, Any]:
    validate_uia_helper_output(output)
    return _normalize_capture_record(
        record=output,
        source="uia_helper",
        trigger_source="win_uia_helper",
        event_type="capture_frontmost",
    )


def _normalize_capture_record(
    record: dict[str, Any],
    source: str,
    trigger_source: str,
    event_type: str,
) -> dict[str, Any]:
    window = record["window"]
    focused = record["focused_element"]

    capture: dict[str, Any] = {
        "timestamp": record["timestamp"],
        "schema_version": 1,
        "platform": "windows",
        "source": source,
        "trigger": {
            "source": trigger_source,
            "event_type": event_type,
        },
        "window_meta": {
            "hwnd": str(window.get("hwnd", "")),
            "pid": int(window.get("pid", 0)),
            "process_name": str(window.get("process_name", "")),
            "exe_path": str(window.get("exe_path", "")),
            "app_name": str(window.get("app_name", "")),
            "title": str(window.get("title", "")),
            "bounds": [int(value) for value in window.get("bounds", [0, 0, 0, 0])],
            "elevated": bool(window.get("elevated", False)),
        },
        "focused_element": {
            "control_type": str(focused.get("control_type", "")),
            "name": str(focused.get("name", "")),
            "automation_id": str(focused.get("automation_id", "")),
            "class_name": str(focused.get("class_name", "")),
            "is_editable": bool(focused.get("is_editable", False)),
            "is_password": bool(focused.get("is_password", False)),
            "value": focused.get("value"),
            "text": focused.get("text"),
            "value_length": len(focused.get("value") or ""),
            "text_length": len(focused.get("text") or ""),
        },
        "visible_text": str(record.get("visible_text", "")),
        "url": record.get("url"),
        "uia_tree_hash": "sha256:" + _sha256_json(record.get("uia_tree", {})),
        "content_fingerprint": "sha256:" + ("0" * 64),
        "untrusted_observed_content": True,
        "redactions": [],
        "screenshot": None,
    }

    capture = redact_capture(capture)
    capture["content_fingerprint"] = "sha256:" + _sha256_json(
        {
            "window_meta": capture["window_meta"],
            "focused_element": capture["focused_element"],
            "visible_text": capture["visible_text"],
            "url": capture["url"],
        }
    )
    validate_capture(capture)
    return capture


def capture_once_from_fixture(fixture_path: Path | str, home: Path | str | None = None) -> CaptureResult:
    fixture_path = Path(fixture_path)
    fixture = load_json(fixture_path)
    reason = denylist_reason(fixture)
    if reason:
        return CaptureResult(path=None, capture=None, skipped=True, reason=reason)

    capture = normalize_fixture(fixture)
    return persist_capture(capture, fixture.get("fixture_name"), home)


def capture_once_from_uia_helper_output(
    helper_output_path: Path | str, home: Path | str | None = None
) -> CaptureResult:
    helper_output_path = Path(helper_output_path)
    output = load_json(helper_output_path)
    return capture_once_from_uia_helper_record(output, home, output.get("helper_name"))


def capture_once_from_uia_helper_record(
    output: dict[str, Any],
    home: Path | str | None = None,
    filename_hint: str | None = None,
) -> CaptureResult:
    reason = denylist_reason(output)
    if reason:
        return CaptureResult(path=None, capture=None, skipped=True, reason=reason)

    capture = normalize_uia_helper_output(output)
    return persist_capture(capture, filename_hint, home)


def persist_capture(
    capture: dict[str, Any],
    filename_hint: str | None,
    home: Path | str | None = None,
) -> CaptureResult:
    paths = ensure_state(home)
    output_path = paths["capture_buffer"] / _capture_filename(capture, filename_hint)
    output_path.write_text(json.dumps(capture, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    index_capture(capture, output_path, paths["home"])
    return CaptureResult(path=output_path, capture=capture)


def capture_frontmost_with_helper(
    helper_command: Sequence[str | Path],
    depth: int = 80,
    home: Path | str | None = None,
) -> CaptureResult:
    if not 0 <= depth <= 80:
        raise ValueError("depth must be between 0 and 80")
    if not helper_command:
        raise ValueError("helper command is required")

    command = [str(part) for part in helper_command]
    command.extend(["capture-frontmost", "--depth", str(depth)])
    completed = subprocess.run(
        command,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if completed.returncode != 0:
        raise RuntimeError(f"helper failed with exit code {completed.returncode}")
    if not completed.stdout.strip():
        return CaptureResult(
            path=None,
            capture=None,
            skipped=True,
            reason="helper returned no capture",
        )

    output = json.loads(completed.stdout)
    return capture_once_from_uia_helper_record(output, home, output.get("helper_name"))


def privacy_check_path(path: Path | str) -> PrivacyCheckResult:
    record = load_json(path)

    if denylist_reason(record):
        return PrivacyCheckResult(True, ["PASS: denylisted app capture would be skipped"])

    if record.get("schema_version") == 1:
        capture = record
        try:
            validate_capture(capture)
        except Exception as exc:  # pragma: no cover - jsonschema details are not stable.
            return PrivacyCheckResult(False, [f"FAIL: capture does not validate: {exc}"])
        raw_password_values: list[str] = []
    else:
        raw_password_values = _raw_password_values(record)
        try:
            if record.get("source") == "win-uia-helper":
                capture = normalize_uia_helper_output(record)
            else:
                capture = normalize_fixture(record)
        except Exception as exc:
            return PrivacyCheckResult(False, [f"FAIL: fixture could not be normalized: {exc}"])

    serialized = json.dumps(capture, sort_keys=True)
    failures = scan_for_unredacted_secrets(serialized)
    messages: list[str] = []

    for raw_value in raw_password_values:
        if raw_value and raw_value in serialized:
            failures.append("password_field")
            break

    if capture.get("untrusted_observed_content") is not True:
        failures.append("untrusted_observed_content")

    if failures:
        unique = sorted(set(failures))
        return PrivacyCheckResult(
            False,
            [f"FAIL: unredacted {name} would be written" for name in unique],
        )

    messages.extend(
        [
            "PASS: no password value persisted",
            "PASS: no API key canary persisted",
            "PASS: no private key persisted",
            "PASS: no JWT/GitHub/Slack token persisted",
            "PASS: observed content marked untrusted",
        ]
    )
    return PrivacyCheckResult(True, messages)


def _raw_password_values(fixture: dict[str, Any]) -> list[str]:
    focused = fixture.get("focused_element", {})
    if not focused.get("is_password"):
        return []
    values = [focused.get("value"), focused.get("text")]
    return [
        value
        for value in values
        if isinstance(value, str) and value and not value.startswith("[REDACTED:")
    ]


def _capture_filename(capture: dict[str, Any], fixture_name: str | None) -> str:
    stem = _slug(fixture_name or capture["window_meta"]["app_name"] or "capture")
    timestamp = _slug(capture["timestamp"])
    digest = capture["content_fingerprint"].split(":", 1)[1][:12]
    return f"{timestamp}-{stem}-{digest}.json"


def _slug(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9]+", "-", value).strip("-").lower()
    return slug or "capture"


def _sha256_json(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()
