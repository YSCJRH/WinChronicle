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


@lru_cache(maxsize=1)
def load_capture_schema() -> dict[str, Any]:
    return json.loads(capture_schema_path().read_text(encoding="utf-8"))


def validate_capture(capture: dict[str, Any]) -> None:
    validate(instance=capture, schema=load_capture_schema())
