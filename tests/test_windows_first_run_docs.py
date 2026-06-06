from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_windows_first_run_docs_link_bootstrap_without_expanding_capture_surface():
    doc = (ROOT / "docs" / "windows-first-run.md").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    readme_zh = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")

    for expected in (
        "Windows First Run",
        "winchronicle bootstrap --dry-run --format text",
        "python -m pip install -e \".[dev]\"",
        "dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo",
        "dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo",
        "winchronicle init",
        "winchronicle doctor",
        "winchronicle codex setup --dry-run --format text",
        "winchronicle codex plugin --dry-run --format text",
        "winchronicle workday intent \"开始工作\" --execute",
        "winchronicle workday status --format text --language zh-CN",
        "winchronicle workday intent \"结束工作并总结\" --execute --wait-seconds 60",
        "does not write state",
        "does not start UIA",
        "does not start capture",
        "untrusted_observed_content",
        "record-only",
    ):
        assert expected in doc

    for forbidden in (
        "screenshots",
        "OCR",
        "clipboard",
        "keylogging",
        "cloud upload",
        "desktop control",
        "MCP write tools",
        "background daemon",
    ):
        assert forbidden in doc

    assert "[Windows first run](docs/windows-first-run.md)" in readme
    assert "[Windows 首次运行](docs/windows-first-run.md)" in readme_zh
