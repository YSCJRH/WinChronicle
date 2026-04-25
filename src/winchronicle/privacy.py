from __future__ import annotations

import re
from typing import Any


APP_DENYLIST = {
    "1password.exe",
    "bitwarden.exe",
    "dashlane.exe",
    "keepass.exe",
    "keepassxc.exe",
    "lastpass.exe",
}

TITLE_DENYLIST_REGEX = [
    re.compile(pattern)
    for pattern in [
        r"(?i)password",
        r"(?i)secret",
        r"(?i)private key",
        r"(?i)recovery phrase",
        r"(?i)seed phrase",
    ]
]


def denylist_reason(record: dict[str, Any]) -> str | None:
    window = record.get("window") or record.get("window_meta") or {}
    process_name = str(window.get("process_name", "")).lower()
    title = str(window.get("title", ""))

    if process_name in APP_DENYLIST:
        return f"denylisted app: {window.get('process_name')}"

    for pattern in TITLE_DENYLIST_REGEX:
        if pattern.search(title):
            return f"denylisted title: {title}"

    return None
