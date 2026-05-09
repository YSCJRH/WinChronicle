import json
import tomllib
from io import BytesIO
from pathlib import Path

import winchronicle
from winchronicle.mcp.server import run_stdio


ROOT = Path(__file__).resolve().parents[1]


def test_project_runtime_and_mcp_versions_match(tmp_path):
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    project_version = pyproject["project"]["version"]

    assert project_version == "0.1.18"
    assert winchronicle.__version__ == project_version
    assert _mcp_server_version(tmp_path / "state") == project_version


def _mcp_server_version(home: Path) -> str:
    stdin = BytesIO(
        _encode(
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {"protocolVersion": "2024-11-05"},
            }
        )
    )
    stdout = BytesIO()

    assert run_stdio(stdin, stdout, home=home) == 0

    response = _decode_stream(stdout.getvalue())[0]
    return response["result"]["serverInfo"]["version"]


def _encode(message):
    payload = json.dumps(message, separators=(",", ":"), sort_keys=True).encode("utf-8")
    return b"Content-Length: " + str(len(payload)).encode("ascii") + b"\r\n\r\n" + payload


def _decode_stream(stream):
    header_end = stream.find(b"\r\n\r\n")
    header = stream[:header_end].decode("ascii")
    length = int(header.split(":", 1)[1].strip())
    start = header_end + 4
    end = start + length
    return [json.loads(stream[start:end].decode("utf-8"))]
