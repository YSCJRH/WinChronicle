from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

from jsonschema import validate


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def capture_schema_path() -> Path:
    return repo_root() / "harness" / "specs" / "capture.schema.json"


def uia_helper_output_schema_path() -> Path:
    return repo_root() / "harness" / "specs" / "uia-helper-output.schema.json"


def watcher_event_schema_path() -> Path:
    return repo_root() / "harness" / "specs" / "watcher-event.schema.json"


def mcp_tool_result_schema_path() -> Path:
    return repo_root() / "harness" / "specs" / "mcp-tool-result.schema.json"


def memory_entry_schema_path() -> Path:
    return repo_root() / "harness" / "specs" / "memory-entry.schema.json"


@lru_cache(maxsize=1)
def load_capture_schema() -> dict[str, Any]:
    return json.loads(capture_schema_path().read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def load_uia_helper_output_schema() -> dict[str, Any]:
    return json.loads(uia_helper_output_schema_path().read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def load_watcher_event_schema() -> dict[str, Any]:
    return json.loads(watcher_event_schema_path().read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def load_mcp_tool_result_schema() -> dict[str, Any]:
    return json.loads(mcp_tool_result_schema_path().read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def load_memory_entry_schema() -> dict[str, Any]:
    return json.loads(memory_entry_schema_path().read_text(encoding="utf-8"))


def validate_capture(capture: dict[str, Any]) -> None:
    validate(instance=capture, schema=load_capture_schema())


def validate_uia_helper_output(output: dict[str, Any]) -> None:
    validate(instance=output, schema=load_uia_helper_output_schema())


def validate_watcher_event(event: dict[str, Any]) -> None:
    validate(instance=event, schema=load_watcher_event_schema())


def validate_mcp_tool_result(result: dict[str, Any]) -> None:
    validate(instance=result, schema=load_mcp_tool_result_schema())


def validate_memory_entry(entry: dict[str, Any]) -> None:
    validate(instance=entry, schema=load_memory_entry_schema())
