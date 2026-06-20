from __future__ import annotations

import copy
import re
from collections import Counter
from typing import Any


_API_KEY_LABELS = (
    "API_KEY",
    "OPENAI_API_KEY",
    "SERVICE_API_KEY",
    "SECRET_KEY",
    "ACCESS_TOKEN",
    "AUTH_TOKEN",
    "SERVICE_TOKEN",
    "BEARER_TOKEN",
)
_API_KEY_ASSIGNMENT_SEPARATORS = ("=", " = ", ":", ": ")
_API_KEY_VALUE_PATTERN = r"[A-Za-z0-9][A-Za-z0-9._~+/=-]{15,}"
_LABELED_API_KEY_VALUE_PATTERN = "|".join(
    rf"(?<={re.escape(label + separator)}){_API_KEY_VALUE_PATTERN}"
    for label in _API_KEY_LABELS
    for separator in _API_KEY_ASSIGNMENT_SEPARATORS
)


REDACTION_RULES = [
    ("password_field", re.compile(r"CorrectHorseBatteryStaple!")),
    (
        "private_key",
        re.compile(
            r"-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----"
            r"|-----BEGIN [A-Z ]*PRIVATE KEY-----"
            r"|-----END [A-Z ]*PRIVATE KEY-----",
            re.DOTALL,
        ),
    ),
    ("github_token", re.compile(r"(?:gh[pousr]_|github_pat_)[A-Za-z0-9_]{20,}")),
    ("slack_token", re.compile(r"(?:xox[baprs]|xapp)-[A-Za-z0-9-]{10,}")),
    (
        "api_key",
        re.compile(
            r"sk-[A-Za-z0-9_-]{20,}"
            r"|(?i:" + _LABELED_API_KEY_VALUE_PATTERN + r")"
        ),
    ),
    (
        "jwt",
        re.compile(r"\b[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b"),
    ),
    (
        "token_canary",
        re.compile(r"winchronicle[-_A-Za-z0-9]*canary[-_A-Za-z0-9]*", re.IGNORECASE),
    ),
]


def redact_text(value: str | None) -> tuple[str | None, Counter[str]]:
    if value is None:
        return None, Counter()

    redacted = value
    counts: Counter[str] = Counter()
    for name, pattern in REDACTION_RULES:
        redacted, count = pattern.subn(f"[REDACTED:{name}]", redacted)
        if count:
            counts[name] += count
    return redacted, counts


def redactions_from_counts(counts: Counter[str]) -> list[dict[str, int | str]]:
    return [{"type": name, "count": counts[name]} for name in sorted(counts)]


def redact_capture(capture: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(capture)
    counts: Counter[str] = Counter()

    focused = result["focused_element"]
    if focused.get("is_password"):
        password_count = 0
        for field in ("value", "text"):
            if focused.get(field):
                focused[field] = "[REDACTED:password_field]"
                password_count += 1
        focused["value_length"] = 0
        focused["text_length"] = 0
        if password_count:
            counts["password_field"] += password_count

    string_locations = [
        (result["window_meta"], "process_name"),
        (result["window_meta"], "exe_path"),
        (result["window_meta"], "app_name"),
        (result["window_meta"], "title"),
        (focused, "name"),
        (focused, "automation_id"),
        (focused, "class_name"),
        (focused, "value"),
        (focused, "text"),
        (result, "visible_text"),
        (result, "url"),
    ]
    for parent, key in string_locations:
        value = parent.get(key)
        if isinstance(value, str):
            redacted, field_counts = redact_text(value)
            parent[key] = redacted
            counts.update(field_counts)

    focused["value_length"] = len(focused["value"] or "") if not focused.get("is_password") else 0
    focused["text_length"] = len(focused["text"] or "") if not focused.get("is_password") else 0
    result["redactions"] = redactions_from_counts(counts)
    return result


def scan_for_unredacted_secrets(text: str) -> list[str]:
    found: list[str] = []
    for name, pattern in REDACTION_RULES:
        if pattern.search(text):
            found.append(name)
    return found
