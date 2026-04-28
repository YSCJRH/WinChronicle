from __future__ import annotations

import os
from pathlib import Path

from .privacy import DISABLED_SURFACE_STATUS


CONFIG_TEXT = "# WinChronicle local configuration\n" + "".join(
    f"{key} = false\n" for key in DISABLED_SURFACE_STATUS
)


def default_home(environ: dict[str, str] | None = None) -> Path:
    env = environ if environ is not None else os.environ
    override = env.get("WINCHRONICLE_HOME")
    if override:
        return Path(override).expanduser().resolve()

    local_app_data = env.get("LOCALAPPDATA")
    if local_app_data:
        return Path(local_app_data).expanduser() / "WinChronicle"

    return Path.home() / "AppData" / "Local" / "WinChronicle"


def state_paths(home: Path | str | None = None) -> dict[str, Path]:
    root = Path(home).expanduser().resolve() if home is not None else default_home()
    return {
        "home": root,
        "config": root / "config.toml",
        "capture_buffer": root / "capture-buffer",
        "db": root / "index.db",
        "memory": root / "memory",
        "logs": root / "logs",
    }


def ensure_state(home: Path | str | None = None) -> dict[str, Path]:
    paths = state_paths(home)
    paths["home"].mkdir(parents=True, exist_ok=True)
    paths["capture_buffer"].mkdir(parents=True, exist_ok=True)
    paths["memory"].mkdir(parents=True, exist_ok=True)
    paths["logs"].mkdir(parents=True, exist_ok=True)
    if not paths["config"].exists():
        paths["config"].write_text(CONFIG_TEXT, encoding="utf-8")
    return paths
