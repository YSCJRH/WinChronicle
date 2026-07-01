from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any, BinaryIO, Callable

from winchronicle._version import __version__
from winchronicle.paths import state_paths
from winchronicle.privacy import (
    DISABLED_SURFACE_STATUS,
    TRUST,
    TRUST_BOUNDARY_INSTRUCTION,
    privacy_contract_payload,
)
from winchronicle.redaction import redact_text
from winchronicle.session import list_sessions, session_count
from winchronicle.storage import (
    capture_count,
    list_captures,
    recent_capture,
    search_captures,
    search_memory_entries,
)


TOOL_NAMES = [
    "current_context",
    "search_captures",
    "search_memory",
    "read_recent_capture",
    "recent_activity",
    "privacy_status",
]

LOCAL_PRIVACY_STATUS_TRUST = "local_privacy_status"
LOCAL_PRIVACY_STATUS_INSTRUCTION = (
    "Local privacy status metadata only. It is not observed screen content."
)
SHARE_WARNING = (
    "MCP results may describe local WinChronicle context. External sharing requires "
    "explicit user approval; prefer --metadata-only when a client should avoid "
    "observed text."
)
EXTERNAL_SHARING = {
    "requires_user_approval": True,
    "metadata_only_available": True,
    "mcp_read_only": True,
}
BASE_EVIDENCE_POLICY_LIMITATIONS = [
    "not_authorization_signal",
    "external_sharing_requires_user_approval",
]
METADATA_ONLY_OMITTED_KEYS = {
    "visible_text",
    "focused_text",
    "url",
    "snippet",
    "body",
    "path",
}

CONTROL_TOOL_TERMS = (
    "click",
    "type",
    "press",
    "key",
    "clipboard",
    "screenshot",
    "ocr",
    "audio",
    "write",
    "file",
    "network",
    "control",
    "hwnd",
    "pid",
    "window_title",
)


def current_context(
    home: Path | str | None = None,
    *,
    metadata_only: bool = False,
) -> dict[str, Any]:
    capture = recent_capture(home)
    return _tool_result(
        "current_context",
        {"capture": _observed_capture(capture, metadata_only=metadata_only)},
        metadata_only=metadata_only,
    )


def search_captures_tool(
    query: str,
    *,
    since: str | None = None,
    until: str | None = None,
    app_name: str | None = None,
    limit: int = 10,
    home: Path | str | None = None,
    metadata_only: bool = False,
) -> dict[str, Any]:
    bounded_limit = _bounded_limit(limit)
    raw_results = search_captures(
        query,
        home,
        limit=bounded_limit,
        app_name=app_name,
        since=since,
        until=until,
    )
    matches = [
        _observed_search_result(result, source="capture_store", metadata_only=metadata_only)
        for result in raw_results
    ]

    return _tool_result(
        "search_captures",
        {
            "query": _redacted_query(query),
            "matches": matches,
        },
        metadata_only=metadata_only,
    )


def search_memory_tool(
    query: str,
    *,
    entry_type: str | None = None,
    limit: int = 10,
    home: Path | str | None = None,
    metadata_only: bool = False,
) -> dict[str, Any]:
    bounded_limit = _bounded_limit(limit)
    raw_results = search_memory_entries(
        query,
        home,
        limit=bounded_limit,
        entry_type=entry_type,
    )
    matches = [
        _observed_search_result(result, source="memory_store", metadata_only=metadata_only)
        for result in raw_results
    ]

    return _tool_result(
        "search_memory",
        {
            "query": _redacted_query(query),
            "entry_type": entry_type,
            "matches": matches,
        },
        metadata_only=metadata_only,
    )


def read_recent_capture(
    *,
    at: str | None = None,
    app_name: str | None = None,
    home: Path | str | None = None,
    metadata_only: bool = False,
) -> dict[str, Any]:
    capture = recent_capture(home, at=at, app_name=app_name)
    return _tool_result(
        "read_recent_capture",
        {"capture": _observed_capture(capture, metadata_only=metadata_only)},
        metadata_only=metadata_only,
    )


def recent_activity(
    *,
    since: str | None = None,
    limit: int = 10,
    home: Path | str | None = None,
    metadata_only: bool = False,
) -> dict[str, Any]:
    captures = list_captures(home, limit=_bounded_limit(limit), since=since)
    return _tool_result(
        "recent_activity",
        {
            "captures": [
                _observed_capture(capture, metadata_only=metadata_only) for capture in captures
            ],
            "sessions": [
                _observed_session(session, metadata_only=metadata_only)
                for session in list_sessions(home, limit=_bounded_limit(limit))
            ],
        },
        metadata_only=metadata_only,
    )


def privacy_status(
    home: Path | str | None = None,
    *,
    metadata_only: bool = False,
) -> dict[str, Any]:
    paths = state_paths(home)
    payload = {
        "home": str(paths["home"]),
        "db_exists": paths["db"].exists(),
        "capture_count": capture_count(paths["home"]),
        "session_count": session_count(paths["home"]),
        **privacy_contract_payload(),
        "tools": TOOL_NAMES,
        "control_tools": [],
        "redaction_enabled": True,
        "mcp_read_only": True,
        "forbidden_surfaces": sorted(DISABLED_SURFACE_STATUS),
    }
    return _tool_result(
        "privacy_status",
        payload,
        trust=LOCAL_PRIVACY_STATUS_TRUST,
        instruction=LOCAL_PRIVACY_STATUS_INSTRUCTION,
        metadata_only=metadata_only,
    )


def tool_definitions() -> list[dict[str, Any]]:
    return [
        {
            "name": "current_context",
            "description": "Return the latest local capture as untrusted observed context.",
            "inputSchema": {"type": "object", "additionalProperties": False, "properties": {}},
        },
        {
            "name": "search_captures",
            "description": "Search local fixture/UIA captures using the SQLite index.",
            "inputSchema": {
                "type": "object",
                "required": ["query"],
                "additionalProperties": False,
                "properties": {
                    "query": {"type": "string"},
                    "since": {"type": "string"},
                    "until": {"type": "string"},
                    "app_name": {"type": "string"},
                    "limit": {"type": "integer", "minimum": 0, "maximum": 50},
                },
            },
        },
        {
            "name": "search_memory",
            "description": "Search deterministic Markdown memory entries using the SQLite index.",
            "inputSchema": {
                "type": "object",
                "required": ["query"],
                "additionalProperties": False,
                "properties": {
                    "query": {"type": "string"},
                    "entry_type": {"type": "string", "enum": ["event", "project", "tool"]},
                    "limit": {"type": "integer", "minimum": 0, "maximum": 50},
                },
            },
        },
        {
            "name": "read_recent_capture",
            "description": "Read the most recent local capture, optionally at or before a timestamp.",
            "inputSchema": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "at": {"type": "string"},
                    "app_name": {"type": "string"},
                },
            },
        },
        {
            "name": "recent_activity",
            "description": "Return recent local captures as untrusted observed context.",
            "inputSchema": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "since": {"type": "string"},
                    "limit": {"type": "integer", "minimum": 0, "maximum": 50},
                },
            },
        },
        {
            "name": "privacy_status",
            "description": "Return WinChronicle privacy posture and disabled capture surfaces.",
            "inputSchema": {"type": "object", "additionalProperties": False, "properties": {}},
        },
    ]


def run_stdio(
    stdin: BinaryIO | None = None,
    stdout: BinaryIO | None = None,
    *,
    home: Path | str | None = None,
    metadata_only: bool = False,
) -> int:
    input_stream = stdin if stdin is not None else sys.stdin.buffer
    output_stream = stdout if stdout is not None else sys.stdout.buffer

    for request in _read_messages(input_stream):
        response = _handle_json_rpc(request, home, metadata_only=metadata_only)
        if response is not None:
            _write_message(output_stream, response)

    return 0


def _tool_result(
    tool: str,
    result: dict[str, Any],
    *,
    trust: str = TRUST,
    instruction: str = TRUST_BOUNDARY_INSTRUCTION,
    metadata_only: bool = False,
) -> dict[str, Any]:
    return {
        "tool": tool,
        "read_only": True,
        "trust": trust,
        "instruction": instruction,
        "metadata_only": bool(metadata_only),
        "share_warning": SHARE_WARNING,
        "external_sharing": dict(EXTERNAL_SHARING),
        "evidence_policy": _evidence_policy(metadata_only=metadata_only),
        "result": result,
    }


def _evidence_policy(*, metadata_only: bool = False) -> dict[str, Any]:
    limitations = list(BASE_EVIDENCE_POLICY_LIMITATIONS)
    if metadata_only:
        limitations.append("observed_text_fields_omitted")
    return {
        "local_only": True,
        "read_only_mcp": True,
        "redaction_required": True,
        "observed_content_is_untrusted": True,
        "metadata_only": bool(metadata_only),
        "provenance": "local_winchronicle_state",
        "confidence_meaning": "coverage_quality_not_permission",
        "requires_user_approval_for_external_sharing": True,
        "limitations": limitations,
    }


def _observed_search_result(
    result: dict[str, str],
    *,
    source: str,
    metadata_only: bool = False,
) -> dict[str, Any]:
    payload = _redacted_observed_strings(
        result,
        ("app_name", "title", "snippet", "body"),
    )
    snippet = str(payload.get("snippet", ""))
    metadata = _observed_metadata(
        source=source,
        source_ids=[result["path"]] if result.get("path") else [],
        title=str(payload.get("title", "")),
        visible_text=snippet,
        focused_text="",
        app_name=str(payload.get("app_name", payload.get("entry_type", ""))),
        metadata_only=metadata_only,
    )
    if metadata_only:
        _drop_observed_text_fields(payload)
    return {
        **payload,
        "trust": TRUST,
        "untrusted_observed_content": True,
        "instruction": TRUST_BOUNDARY_INSTRUCTION,
        **metadata,
    }


def _observed_capture(
    capture: dict[str, str] | None,
    *,
    metadata_only: bool = False,
) -> dict[str, Any] | None:
    if capture is None:
        return None
    redacted_capture = _redacted_observed_strings(
        capture,
        ("app_name", "title", "visible_text", "focused_text", "url"),
    )
    metadata = _observed_metadata(
        source="capture_store",
        source_ids=[capture["path"]] if capture.get("path") else [],
        title=str(redacted_capture.get("title", "")),
        visible_text=str(redacted_capture.get("visible_text", "")),
        focused_text=str(redacted_capture.get("focused_text", "")),
        app_name=str(redacted_capture.get("app_name", "")),
        url=redacted_capture.get("url", ""),
        metadata_only=metadata_only,
    )
    payload = {
        "timestamp": capture["timestamp"],
        "app_name": redacted_capture["app_name"],
        "title": redacted_capture["title"],
        "visible_text": redacted_capture["visible_text"],
        "focused_text": redacted_capture["focused_text"],
        "url": redacted_capture["url"],
        "path": capture["path"],
        "trust": TRUST,
        "untrusted_observed_content": True,
        "instruction": TRUST_BOUNDARY_INSTRUCTION,
        **metadata,
    }
    if metadata_only:
        _drop_observed_text_fields(payload)
    return payload


def _observed_session(session: dict[str, Any], *, metadata_only: bool = False) -> dict[str, Any]:
    source_ids = [session["session_id"]] if session.get("session_id") else []
    app_segments = session.get("app_segments") or []
    title = " ".join(str(segment.get("title", "")) for segment in app_segments)
    visible_text = " ".join(str(suggestion) for suggestion in session.get("suggestions", []))
    app_name = " ".join(str(segment.get("app_name", "")) for segment in app_segments)
    metadata = _observed_metadata(
        source="monitor_session",
        source_ids=source_ids,
        title=title,
        visible_text=visible_text,
        focused_text="",
        app_name=app_name,
        metadata_only=metadata_only,
    )
    if metadata_only:
        return {
            "session_schema_version": session.get("session_schema_version"),
            "session_id": _metadata_session_id(session.get("session_id")),
            "mode": session.get("mode"),
            "started_at": session.get("started_at"),
            "ended_at": session.get("ended_at"),
            "duration_seconds": session.get("duration_seconds"),
            "captures_written": session.get("captures_written"),
            "duplicates_skipped": session.get("duplicates_skipped"),
            "denylisted_skipped": session.get("denylisted_skipped"),
            "excluded_skipped": session.get("excluded_skipped"),
            "heartbeats": session.get("heartbeats"),
            "source_capture_count": len(session.get("source_capture_paths") or []),
            "storage_policy": session.get("storage_policy"),
            "storage_usage": session.get("storage_usage"),
            "error_signals": session.get("error_signals"),
            "trust": TRUST,
            "untrusted_observed_content": True,
            "instruction": TRUST_BOUNDARY_INSTRUCTION,
            **metadata,
        }
    return {
        **session,
        **metadata,
    }


def _observed_metadata(
    *,
    source: str,
    source_ids: list[str],
    title: str,
    visible_text: str,
    focused_text: str,
    app_name: str,
    url: str | None = None,
    metadata_only: bool = False,
) -> dict[str, Any]:
    limitations = _coverage_limitations(
        source_ids=source_ids,
        title=title,
        visible_text=visible_text,
        focused_text=focused_text,
        app_name=app_name,
        url=url,
    )
    if metadata_only:
        limitations = [
            *limitations,
            "metadata_only",
            "observed_text_fields_omitted",
        ]
    return {
        "redacted": True,
        "source": source or "unknown",
        "source_ids": _metadata_source_ids(
            source,
            source_ids,
            metadata_only=metadata_only,
        ),
        "metadata_only": bool(metadata_only),
        "confidence": _coverage_confidence(
            source_ids=source_ids,
            title=title,
            visible_text=visible_text,
            focused_text=focused_text,
            app_name=app_name,
            url=url,
        ),
        "limitations": limitations,
    }


def _metadata_source_ids(
    source: str,
    source_ids: list[str],
    *,
    metadata_only: bool,
) -> list[str]:
    if not metadata_only:
        return source_ids
    prefix = _opaque_source_prefix(source)
    return [_opaque_source_id(prefix, source_id) for source_id in source_ids]


def _metadata_session_id(session_id: Any) -> str | None:
    if session_id is None:
        return None
    return _opaque_source_id("session", str(session_id))


def _opaque_source_prefix(source: str) -> str:
    if source == "capture_store":
        return "capture"
    if source == "memory_store":
        return "memory"
    if source == "monitor_session":
        return "session"
    return "source"


def _opaque_source_id(prefix: str, raw_source_id: str) -> str:
    digest = hashlib.sha256(raw_source_id.encode("utf-8")).hexdigest()[:12]
    return f"{prefix}-{digest}"


def _coverage_confidence(
    *,
    source_ids: list[str],
    title: str,
    visible_text: str,
    focused_text: str,
    app_name: str,
    url: str | None = None,
) -> float:
    visible_len = len(visible_text.strip())
    focused_len = len(focused_text.strip())
    score = 0.0
    if app_name or title or source_ids:
        score = max(score, 0.25)
    if title and visible_len:
        score = max(score, 0.50)
    if title and visible_len and focused_len:
        score = max(score, 0.70)
    if title and visible_len >= 40 and focused_len and source_ids:
        score = max(score, 0.80)
    if title and visible_len >= 120 and focused_len and source_ids and (app_name or url):
        score = max(score, 0.85)
    return min(round(score, 2), 0.85)


def _coverage_limitations(
    *,
    source_ids: list[str],
    title: str,
    visible_text: str,
    focused_text: str,
    app_name: str,
    url: str | None = None,
) -> list[str]:
    limitations: list[str] = []
    if not source_ids:
        limitations.append("source_id_unavailable")
    if not visible_text.strip():
        limitations.append("no_visible_text")
    elif len(visible_text.strip()) < 40:
        limitations.append("low_visible_text")
    if not focused_text.strip():
        limitations.append("no_focused_element")
    if "visual studio code" in app_name.casefold() and not focused_text.strip():
        limitations.append("editor_buffer_not_exposed_by_uia")
    observed_blob = "\n".join(
        value or ""
        for value in (
            title,
            visible_text,
            focused_text,
            app_name,
            url or "",
            "\n".join(source_ids),
        )
    )
    if "[REDACTED:" in observed_blob:
        limitations.append("redaction_applied")
    return limitations


def _bounded_limit(limit: int) -> int:
    return max(0, min(int(limit), 50))


def _redacted_query(query: str) -> str:
    redacted, _ = redact_text(query)
    return redacted or ""


def _redacted_observed_strings(
    payload: dict[str, Any],
    keys: tuple[str, ...],
) -> dict[str, Any]:
    redacted_payload = dict(payload)
    for key in keys:
        value = redacted_payload.get(key)
        if isinstance(value, str):
            redacted, _ = redact_text(value)
            redacted_payload[key] = redacted or ""
    return redacted_payload


def _drop_observed_text_fields(payload: dict[str, Any]) -> None:
    for key in METADATA_ONLY_OMITTED_KEYS:
        payload.pop(key, None)


def _call_tool(
    name: str,
    arguments: dict[str, Any],
    home: Path | str | None,
    *,
    metadata_only: bool = False,
) -> dict[str, Any]:
    dispatch: dict[str, Callable[..., dict[str, Any]]] = {
        "current_context": current_context,
        "search_captures": search_captures_tool,
        "search_memory": search_memory_tool,
        "read_recent_capture": read_recent_capture,
        "recent_activity": recent_activity,
        "privacy_status": privacy_status,
    }
    if any(term in name for term in CONTROL_TOOL_TERMS):
        raise ValueError(f"control-like tool name is not allowed: {name}")
    if name not in dispatch:
        raise ValueError(f"unknown read-only tool: {name}")
    return dispatch[name](home=home, metadata_only=metadata_only, **arguments)


def _handle_json_rpc(
    message: dict[str, Any],
    home: Path | str | None,
    *,
    metadata_only: bool = False,
) -> dict[str, Any] | None:
    request_id = message.get("id")
    if request_id is None:
        return None

    method = message.get("method")
    try:
        if method == "initialize":
            params = message.get("params") or {}
            result = {
                "protocolVersion": params.get("protocolVersion", "2024-11-05"),
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "winchronicle-readonly", "version": __version__},
            }
        elif method == "tools/list":
            result = {"tools": tool_definitions()}
        elif method == "tools/call":
            params = message.get("params") or {}
            tool_result = _call_tool(
                str(params.get("name", "")),
                params.get("arguments") or {},
                home,
                metadata_only=metadata_only,
            )
            result = {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps(tool_result, sort_keys=True),
                    }
                ],
                "isError": False,
            }
        else:
            return _json_rpc_error(request_id, -32601, f"method not found: {method}")
    except Exception as exc:
        return _json_rpc_error(request_id, -32000, str(exc))

    return {"jsonrpc": "2.0", "id": request_id, "result": result}


def _json_rpc_error(request_id: Any, code: int, message: str) -> dict[str, Any]:
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "error": {
            "code": code,
            "message": message,
        },
    }


def _read_messages(stream: BinaryIO):
    while True:
        line = stream.readline()
        if not line:
            break
        if not line.strip():
            continue

        header = line.decode("ascii", errors="ignore").strip()
        if header.lower().startswith("content-length:"):
            length = int(header.split(":", 1)[1].strip())
            while True:
                header_line = stream.readline()
                if not header_line or not header_line.strip():
                    break
            body = stream.read(length)
            yield json.loads(body.decode("utf-8"))
            continue

        yield json.loads(line.decode("utf-8"))


def _write_message(stream: BinaryIO, message: dict[str, Any]) -> None:
    payload = json.dumps(message, separators=(",", ":"), sort_keys=True).encode("utf-8")
    stream.write(f"Content-Length: {len(payload)}\r\n\r\n".encode("ascii"))
    stream.write(payload)
    stream.flush()
