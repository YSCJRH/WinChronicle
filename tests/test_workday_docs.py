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
        'winchronicle workday intent "查看工作记录状态"',
        'winchronicle workday intent "停止工作并总结" --execute',
        "winchronicle workday stop",
        "winchronicle workday status",
        'winchronicle workday intent "查看工作记录状态" --execute',
        "winchronicle workday doctor",
        "winchronicle workday summarize",
        "winchronicle workday stop --format text --language zh-CN",
        "--summary-style technical",
        "--focus",
        "--note",
        "--format text",
        "--language zh-CN",
        "开始记录工作：今天主要做",
        "今日工作复盘",
        "human daily review",
        "not a telemetry or log-counter report",
        "复盘来源: 本地阶段性记录",
        "来源说明: 最终结果暂不可用，本次复盘使用已保存的本地阶段性记录。",
        "来源说明: 本次复盘使用已保存的本地工作记录。",
        "来源说明: 最终结果不可用，本次复盘由已脱敏的本地记录恢复生成。",
        "operator focus",
        "operator focus after obvious-secret redaction",
        "未登记工作线索",
        "工作概览",
        "工作记录状态",
        "Project snapshot metadata is redacted",
        "basename_only",
        "metadata_redaction_enabled",
        "redaction pipeline used for captures",
        "根据本地记录",
        "用户确认事实",
        "not open questions pushed back",
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
        "本地记录状态信息",
        "状态边界: 这里只查看本地记录状态",
        "不会启动 watcher/helper/UIA capture",
        "也不会读取桌面内容",
        "阶段性复盘: 尚未生成",
        "结束时会基于当时已保存的本地记录保守复盘",
        "阶段性复盘: 已有本地阶段性记录",
        "结束时会基于已保存记录生成保守总结",
        "复盘边界: 可从本地阶段性记录继续查看",
        "未保存或未登记的工作会保持保守表达",
        "final_result",
        "capture_buffer_recovery",
        "recovered_from_capture_buffer",
        "raw watcher JSONL is not saved",
        "HTML report does not include raw visible text",
        "storage_usage",
        "read raw capture visible text",
        "CLI formatter does not call an LLM",
        "Codex-assisted daily report",
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
        "not a telemetry or log-counter report",
        "开始工作",
        "结束工作并总结",
        "开始记录工作",
        "查看工作记录状态",
        "停止工作并总结",
        "winchronicle codex install --dry-run",
        "winchronicle codex setup --dry-run --format text",
        "winchronicle codex daily --dry-run --format text",
        "what_to_say_next",
        "first_prompt_to_try",
        'winchronicle workday intent "查看工作记录状态" --execute',
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


def test_chinese_workday_summary_example_sets_local_record_coverage_expectation():
    text = (ROOT / "docs" / "examples" / "workday-summary.zh-CN.md").read_text(
        encoding="utf-8"
    )

    assert "本次复盘基于约 2 小时的本地记录" in text
    assert "保持保守表达" in text

    for forbidden in (
        "36 条",
        "captures_written",
        "source_capture_paths",
        "capture-a",
    ):
        assert forbidden not in text


def test_workday_summary_examples_keep_assistant_review_shape_not_counter_report():
    english = (ROOT / "docs" / "examples" / "workday-summary.en.md").read_text(
        encoding="utf-8"
    )
    chinese = (ROOT / "docs" / "examples" / "workday-summary.zh-CN.md").read_text(
        encoding="utf-8"
    )
    english_normalized = " ".join(english.split())
    chinese_normalized = " ".join(chinese.split())

    for expected in (
        "The default review should read like a work assistant summary, not a telemetry or log-counter report.",
        "Do not turn capture counts, skipped counts, storage sizes, or error-signal counts into the main narrative.",
        "Those counters belong only in the explicit technical style.",
        "The default review should stay focused on outcomes, progress, tomorrow's next steps, and confirmation directions.",
    ):
        assert expected in english_normalized

    for expected in (
        "默认复盘应读起来像工作助理式复盘，不是遥测或日志计数报告。",
        "不要把 capture 数、skipped 数、storage 大小或 error-signal 计数写成主线。",
        "这些计数只属于显式 technical style。",
        "默认复盘应围绕产出、进展、明天行动和可确认方向。",
    ):
        assert expected in chinese_normalized


def test_agents_report_format_exempts_recording_only_workday_turns():
    text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")

    assert "Recording-only WinChronicle Workday turns are not development tasks" in text
    assert "Do not use the required report format" in text
    assert "paste the local workday summary or Codex-assisted daily report directly" in text
