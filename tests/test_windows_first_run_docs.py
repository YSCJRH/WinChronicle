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


def test_windows_first_run_opens_with_workday_summary_boundary():
    doc = (ROOT / "docs" / "windows-first-run.md").read_text(encoding="utf-8")
    intro = doc.split("\n## Install And Check", 1)[0]
    normalized = " ".join(intro.split())

    for expected in (
        "record-only",
        "summary-level evidence",
        "does not send raw observed text",
        "not a telemetry or log-counter report",
        "`summary_boundary`",
    ):
        assert expected in normalized


def test_first_run_and_quick_demo_clarify_mcp_output_is_not_sharing_authorization():
    first_run = " ".join(
        (ROOT / "docs" / "windows-first-run.md").read_text(encoding="utf-8").split()
    )
    quick_demo = " ".join(
        (ROOT / "docs" / "quick-demo.md").read_text(encoding="utf-8").split()
    )

    for doc in (first_run, quick_demo):
        assert (
            "MCP output is local evidence, not permission to publish or share results."
            in doc
        )
        assert "External sharing still requires explicit user approval." in doc

    assert "`metadata-only`" in first_run
