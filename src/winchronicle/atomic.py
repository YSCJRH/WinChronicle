from __future__ import annotations

from contextlib import suppress
import os
import threading
import time
from pathlib import Path


def atomic_write_text(path: Path, text: str, *, encoding: str = "utf-8") -> None:
    atomic_write_bytes(path, text.encode(encoding))


def atomic_write_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.with_name(
        f".{path.name}.{os.getpid()}.{threading.get_ident()}.{time.monotonic_ns()}.tmp"
    )
    try:
        with temp_path.open("wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        temp_path.replace(path)
    except Exception:
        with suppress(OSError):
            temp_path.unlink(missing_ok=True)
        raise


def restore_or_remove(path: Path, previous_bytes: bytes | None) -> None:
    if previous_bytes is None:
        with suppress(OSError):
            path.unlink(missing_ok=True)
        return

    atomic_write_bytes(path, previous_bytes)
