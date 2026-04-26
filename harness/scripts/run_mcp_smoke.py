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

from winchronicle.mcp.server import CONTROL_TOOL_TERMS, TOOL_NAMES
from winchronicle.schema import validate_mcp_tool_result


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
        if len(responses) != 4:
            print("FAIL: MCP stdio did not return the expected response count")
            return 1

        tool_names = {tool["name"] for tool in responses[1]["result"]["tools"]}
        if tool_names != set(TOOL_NAMES):
            print("FAIL: MCP tools/list returned the wrong tools")
            return 1
        if any(term in name for name in tool_names for term in CONTROL_TOOL_TERMS):
            print("FAIL: MCP tools/list exposed a control-like tool")
            return 1

        privacy = _tool_payload(responses[2])
        validate_mcp_tool_result(privacy)
        if privacy["result"]["screenshots_enabled"] or privacy["result"]["desktop_control_enabled"]:
            print("FAIL: MCP privacy_status reported an enabled prohibited surface")
            return 1

        search = _tool_payload(responses[3])
        validate_mcp_tool_result(search)
        matches = search["result"]["matches"]
        if not matches or matches[0]["app_name"] != "Windows Terminal":
            print("FAIL: MCP search_captures did not find the terminal fixture")
            return 1
        if matches[0]["trust"] != "untrusted_observed_content":
            print("FAIL: MCP search result lacked the observed-content trust boundary")
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
