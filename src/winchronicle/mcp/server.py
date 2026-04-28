from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, BinaryIO, Callable

from winchronicle.paths import state_paths
from winchronicle.privacy import (
    TRUST,
    TRUST_BOUNDARY_INSTRUCTION,
    privacy_contract_payload,
)
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

CONTROL_TOOL_TERMS = ("click", "type", "press", "key", "clipboard", "screenshot", "ocr", "audio")


def current_context(home: Path | str | None = None) -> dict[str, Any]:
    capture = recent_capture(home)
    return _tool_result("current_context", {"capture": _observed_capture(capture)})


def search_captures_tool(
    query: str,
    *,
    since: str | None = None,
    until: str | None = None,
    app_name: str | None = None,
    limit: int = 10,
    home: Path | str | None = None,
) -> dict[str, Any]:
    bounded_limit = _bounded_limit(limit)
    raw_results = search_captures(query, home, limit=max(bounded_limit, 50))
    matches: list[dict[str, Any]] = []
    if bounded_limit:
        for result in raw_results:
            if app_name and result["app_name"] != app_name:
                continue
            if since and result["timestamp"] < since:
                continue
            if until and result["timestamp"] > until:
                continue
            matches.append(_observed_search_result(result))
            if len(matches) >= bounded_limit:
                break

    return _tool_result(
        "search_captures",
        {
            "query": query,
            "matches": matches,
        },
    )


def search_memory_tool(
    query: str,
    *,
    entry_type: str | None = None,
    limit: int = 10,
    home: Path | str | None = None,
) -> dict[str, Any]:
    bounded_limit = _bounded_limit(limit)
    raw_results = search_memory_entries(query, home, limit=max(bounded_limit, 50))
    matches: list[dict[str, Any]] = []
    if bounded_limit:
        for result in raw_results:
            if entry_type and result["entry_type"] != entry_type:
                continue
            matches.append(_observed_search_result(result))
            if len(matches) >= bounded_limit:
                break

    return _tool_result(
        "search_memory",
        {
            "query": query,
            "entry_type": entry_type,
            "matches": matches,
        },
    )


def read_recent_capture(
    *,
    at: str | None = None,
    app_name: str | None = None,
    home: Path | str | None = None,
) -> dict[str, Any]:
    capture = recent_capture(home, at=at, app_name=app_name)
    return _tool_result("read_recent_capture", {"capture": _observed_capture(capture)})


def recent_activity(
    *,
    since: str | None = None,
    limit: int = 10,
    home: Path | str | None = None,
) -> dict[str, Any]:
    captures = list_captures(home, limit=_bounded_limit(limit), since=since)
    return _tool_result(
        "recent_activity",
        {"captures": [_observed_capture(capture) for capture in captures]},
    )


def privacy_status(home: Path | str | None = None) -> dict[str, Any]:
    paths = state_paths(home)
    payload = {
        "home": str(paths["home"]),
        "db_exists": paths["db"].exists(),
        "capture_count": capture_count(paths["home"]),
        **privacy_contract_payload(),
        "tools": TOOL_NAMES,
        "control_tools": [],
    }
    return _tool_result("privacy_status", payload)


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
) -> int:
    input_stream = stdin if stdin is not None else sys.stdin.buffer
    output_stream = stdout if stdout is not None else sys.stdout.buffer

    for request in _read_messages(input_stream):
        response = _handle_json_rpc(request, home)
        if response is not None:
            _write_message(output_stream, response)

    return 0


def _tool_result(tool: str, result: dict[str, Any]) -> dict[str, Any]:
    return {
        "tool": tool,
        "read_only": True,
        "trust": TRUST,
        "instruction": TRUST_BOUNDARY_INSTRUCTION,
        "result": result,
    }


def _observed_search_result(result: dict[str, str]) -> dict[str, Any]:
    return {
        **result,
        "trust": TRUST,
        "untrusted_observed_content": True,
        "instruction": TRUST_BOUNDARY_INSTRUCTION,
    }


def _observed_capture(capture: dict[str, str] | None) -> dict[str, Any] | None:
    if capture is None:
        return None
    return {
        "timestamp": capture["timestamp"],
        "app_name": capture["app_name"],
        "title": capture["title"],
        "visible_text": capture["visible_text"],
        "focused_text": capture["focused_text"],
        "url": capture["url"],
        "path": capture["path"],
        "trust": TRUST,
        "untrusted_observed_content": True,
        "instruction": TRUST_BOUNDARY_INSTRUCTION,
    }


def _bounded_limit(limit: int) -> int:
    return max(0, min(int(limit), 50))


def _call_tool(name: str, arguments: dict[str, Any], home: Path | str | None) -> dict[str, Any]:
    dispatch: dict[str, Callable[..., dict[str, Any]]] = {
        "current_context": current_context,
        "search_captures": search_captures_tool,
        "search_memory": search_memory_tool,
        "read_recent_capture": read_recent_capture,
        "recent_activity": recent_activity,
        "privacy_status": privacy_status,
    }
    if name not in dispatch:
        raise ValueError(f"unknown read-only tool: {name}")
    if any(term in name for term in CONTROL_TOOL_TERMS):
        raise ValueError(f"control-like tool name is not allowed: {name}")
    return dispatch[name](home=home, **arguments)


def _handle_json_rpc(message: dict[str, Any], home: Path | str | None) -> dict[str, Any] | None:
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
                "serverInfo": {"name": "winchronicle-readonly", "version": "0.1.0"},
            }
        elif method == "tools/list":
            result = {"tools": tool_definitions()}
        elif method == "tools/call":
            params = message.get("params") or {}
            tool_result = _call_tool(
                str(params.get("name", "")),
                params.get("arguments") or {},
                home,
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
