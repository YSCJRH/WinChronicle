from pathlib import Path

from winchronicle.paths import default_home, ensure_state
from winchronicle.privacy import DISABLED_SURFACE_STATUS


def test_default_home_uses_winchronicle_home(tmp_path, monkeypatch):
    home = tmp_path / "wc-home"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))

    assert default_home() == home.resolve()


def test_ensure_state_creates_expected_paths(tmp_path, monkeypatch):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))

    paths = ensure_state()

    assert paths["home"] == home.resolve()
    assert paths["config"].exists()
    assert paths["capture_buffer"].is_dir()
    assert paths["memory"].is_dir()
    assert paths["logs"].is_dir()
    config = paths["config"].read_text(encoding="utf-8")
    for key in DISABLED_SURFACE_STATUS:
        assert f"{key} = false" in config


def test_default_home_uses_localappdata_when_no_override(tmp_path, monkeypatch):
    local_app_data = tmp_path / "LocalAppData"
    monkeypatch.delenv("WINCHRONICLE_HOME", raising=False)
    monkeypatch.setenv("LOCALAPPDATA", str(local_app_data))

    assert default_home() == Path(local_app_data) / "WinChronicle"
