from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from winchronicle.privacy import DISABLED_SURFACE_STATUS, TRUST
from winchronicle.schema import validate_mcp_tool_result

EXPECTED_TOOL_NAMES = (
    "current_context",
    "search_captures",
    "search_memory",
    "read_recent_capture",
    "recent_activity",
    "privacy_status",
)
FORBIDDEN_TOOL_TERMS = (
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


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="winchronicle-mcp-smoke-") as temp_dir:
        env = os.environ.copy()
        env["WINCHRONICLE_HOME"] = str(Path(temp_dir) / "state")

        capture = subprocess.run(
            [
                sys.executable,
                "-m",
                "winchronicle",
                "capture-once",
                "--fixture",
                "harness/fixtures/uia/terminal_error.json",
            ],
            cwd=ROOT,
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        if capture.returncode:
            print("FAIL: MCP smoke fixture capture failed")
            return capture.returncode

        memory = subprocess.run(
            [
                sys.executable,
                "-m",
                "winchronicle",
                "generate-memory",
                "--date",
                "2026-04-25",
            ],
            cwd=ROOT,
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        if memory.returncode:
            print("FAIL: MCP smoke memory generation failed")
            return memory.returncode

        completed = subprocess.run(
            [sys.executable, "-m", "winchronicle", "mcp-stdio"],
            cwd=ROOT,
            env=env,
            input=_build_request_stream(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if completed.returncode:
            print("FAIL: MCP stdio command failed")
            return completed.returncode
        if completed.stderr:
            print("FAIL: MCP stdio wrote to stderr")
            return 1

        responses = _parse_response_stream(completed.stdout)
        if len(responses) != 6:
            print("FAIL: MCP stdio did not return the expected response count")
            return 1

        tool_names = [tool["name"] for tool in responses[1]["result"]["tools"]]
        if tool_names != list(EXPECTED_TOOL_NAMES):
            print("FAIL: MCP tools/list returned the wrong tools")
            return 1
        if any(term in name for name in tool_names for term in FORBIDDEN_TOOL_TERMS):
            print("FAIL: MCP tools/list exposed a control-like tool")
            return 1

        privacy = _tool_payload(responses[2])
        validate_mcp_tool_result(privacy)
        if any(privacy["result"].get(key) is not False for key in DISABLED_SURFACE_STATUS):
            print("FAIL: MCP privacy_status reported an enabled prohibited surface")
            return 1
        if privacy["result"].get("observed_content_trust") != TRUST:
            print("FAIL: MCP privacy_status lacked the observed-content trust boundary")
            return 1

        search = _tool_payload(responses[3])
        validate_mcp_tool_result(search)
        matches = search["result"]["matches"]
        if not matches or matches[0]["app_name"] != "Windows Terminal":
            print("FAIL: MCP search_captures did not find the terminal fixture")
            return 1
        if matches[0]["trust"] != TRUST:
            print("FAIL: MCP search result lacked the observed-content trust boundary")
            return 1

        memory_search = _tool_payload(responses[4])
        validate_mcp_tool_result(memory_search)
        memory_matches = memory_search["result"]["matches"]
        if not memory_matches or memory_matches[0]["entry_type"] not in {"event", "project", "tool"}:
            print("FAIL: MCP search_memory did not find deterministic memory")
            return 1
        if memory_matches[0]["trust"] != TRUST:
            print("FAIL: MCP memory search result lacked the trust boundary")
            return 1

        recent = _tool_payload(responses[5])
        validate_mcp_tool_result(recent)
        if "captures" not in recent["result"] or "sessions" not in recent["result"]:
            print("FAIL: MCP recent_activity lacked captures or sessions")
            return 1
        recent_captures = recent["result"]["captures"]
        if not recent_captures or recent_captures[0]["trust"] != TRUST:
            print("FAIL: MCP recent_activity capture lacked the trust boundary")
            return 1
        if not isinstance(recent["result"]["sessions"], list):
            print("FAIL: MCP recent_activity sessions field was not a list")
            return 1

    print("PASS: MCP stdio smoke passed")
    return 0


def _build_request_stream() -> bytes:
    requests = [
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "winchronicle-harness", "version": "0.1.0"},
            },
        },
        {"jsonrpc": "2.0", "method": "notifications/initialized"},
        {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}},
        {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {"name": "privacy_status", "arguments": {}},
        },
        {
            "jsonrpc": "2.0",
            "id": 4,
            "method": "tools/call",
            "params": {
                "name": "search_captures",
                "arguments": {"query": "AssertionError", "limit": 5},
            },
        },
        {
            "jsonrpc": "2.0",
            "id": 5,
            "method": "tools/call",
            "params": {
                "name": "search_memory",
                "arguments": {"query": "AssertionError", "limit": 5},
            },
        },
        {
            "jsonrpc": "2.0",
            "id": 6,
            "method": "tools/call",
            "params": {
                "name": "recent_activity",
                "arguments": {"limit": 5},
            },
        },
    ]
    return b"".join(_encode_message(request) for request in requests)


def _encode_message(message: dict[str, Any]) -> bytes:
    payload = json.dumps(message, separators=(",", ":"), sort_keys=True).encode("utf-8")
    return b"Content-Length: " + str(len(payload)).encode("ascii") + b"\r\n\r\n" + payload


def _parse_response_stream(stream: bytes) -> list[dict[str, Any]]:
    responses: list[dict[str, Any]] = []
    offset = 0
    while offset < len(stream):
        header_end = stream.find(b"\r\n\r\n", offset)
        if header_end == -1:
            raise ValueError("missing MCP response header terminator")
        header = stream[offset:header_end].decode("ascii")
        length = int(header.split(":", 1)[1].strip())
        body_start = header_end + 4
        body_end = body_start + length
        responses.append(json.loads(stream[body_start:body_end].decode("utf-8")))
        offset = body_end
    return responses


def _tool_payload(response: dict[str, Any]) -> dict[str, Any]:
    text = response["result"]["content"][0]["text"]
    return json.loads(text)


if __name__ == "__main__":
    raise SystemExit(main())
