from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_workday_session_docs_define_natural_language_and_storage_boundaries():
    doc = (ROOT / "docs" / "workday-session.md").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    readme_zh = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")

    for expected in (
        "开始记录工作",
        "开始工作",
        "停止工作并总结",
        "结束工作并总结",
        "winchronicle workday start",
        'winchronicle workday intent "开始记录工作"',
        'winchronicle workday intent "停止工作并总结" --execute',
        "winchronicle workday stop",
        "winchronicle workday status",
        "winchronicle workday status --format text --language zh-CN",
        "winchronicle workday doctor",
        "winchronicle workday summarize",
        "winchronicle workday stop --format text --language zh-CN",
        "--format text",
        "--language zh-CN",
        "工作概览",
        "工作记录状态",
        "explicit finite local monitor session",
        "not a daemon, service, startup task, hidden recorder, or infinite polling loop",
        "12 hours",
        "checkpoint summary every 5",
        "summary_source",
        "checkpoint_updated_at",
        "checkpoint_age_seconds",
        "checkpoint_fresh",
        "--checkpoint-stale-seconds",
        "does not start the watcher, helper, UIA capture, or desktop reading",
        "intent mapping is a local deterministic allowlist",
        "dry-run by default",
        "status text view is read-only",
        "final_result",
        "capture_buffer_recovery",
        "recovered_from_capture_buffer",
        "raw watcher JSONL is not saved",
        "HTML report does not include raw visible text",
        "storage_usage",
        "does not read raw capture visible text",
        "does not call an LLM",
        "error_signals",
        "metadata-only",
        "raw visible text that triggered",
        "rebuilds a bounded summary from persisted",
        "screenshots, OCR, clipboard capture, keylogging, audio recording, cloud upload, desktop control, or MCP write tools",
        "untrusted_observed_content",
    ):
        assert expected in doc

    assert "[Workday session](docs/workday-session.md)" in readme
    assert "[Workday session](docs/workday-session.md)" in readme_zh


def test_codex_app_workday_guide_keeps_user_flow_record_only():
    doc = (ROOT / "docs" / "codex-app-workday-guide.md").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    readme_zh = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")

    for expected in (
        "Codex App Workday Guide",
        "ordinary user",
        "开始工作",
        "结束工作并总结",
        "开始记录工作",
        "停止工作并总结",
        "winchronicle codex install --dry-run",
        "winchronicle workday status --format text --language zh-CN",
        "Only call WinChronicle workday commands",
        "Only paste a summary into chat after the user explicitly asks for chat output",
        "Do not inspect, scan, review, edit, test, commit, push, or release repository files",
        "explicit finite local monitor session",
        "not a daemon, service, startup task, hidden recorder, or infinite polling loop",
        "untrusted_observed_content",
    ):
        assert expected in doc

    for forbidden in (
        "screenshot fallback",
        "OCR fallback",
        "clipboard capture",
        "keylogging",
        "desktop control",
        "MCP write tools",
        "cloud upload",
    ):
        assert forbidden in doc

    assert "[Codex App workday guide](docs/codex-app-workday-guide.md)" in readme
    assert "[Codex App 工作日指南](docs/codex-app-workday-guide.md)" in readme_zh
