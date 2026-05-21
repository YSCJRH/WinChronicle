from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_workday_session_docs_define_natural_language_and_storage_boundaries():
    doc = (ROOT / "docs" / "workday-session.md").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    readme_zh = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")

    for expected in (
        "开始记录工作",
        "停止工作并总结",
        "winchronicle workday start",
        "winchronicle workday stop",
        "winchronicle workday status",
        "winchronicle workday summarize",
        "explicit finite local monitor session",
        "not a daemon, service, startup task, hidden recorder, or infinite polling loop",
        "12 hours",
        "raw watcher JSONL is not saved",
        "HTML report does not include raw visible text",
        "storage_usage",
        "screenshots, OCR, clipboard capture, keylogging, audio recording, cloud upload, desktop control, or MCP write tools",
        "untrusted_observed_content",
    ):
        assert expected in doc

    assert "[Workday session](docs/workday-session.md)" in readme
    assert "[Workday session](docs/workday-session.md)" in readme_zh
