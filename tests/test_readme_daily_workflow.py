from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_readmes_surface_codex_daily_workflow_first_run_path():
    english = (ROOT / "README.md").read_text(encoding="utf-8")
    chinese = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")

    assert "## If You Only Want Codex App To Record Work" in english
    assert english.index("## If You Only Want Codex App To Record Work") < english.index(
        "## Try It In 5 Minutes"
    )
    assert "the fastest path is the local Workday plugin" in english
    assert "| **Workday** | You want Codex App to start, check, stop, and summarize a bounded local work session. | `winchronicle codex setup --dry-run --format text` |" in english
    assert "At the end you should get a short daily review" in english
    assert "## 如果你只想让 Codex App 记录工作" in chinese
    assert chinese.index("## 如果你只想让 Codex App 记录工作") < chinese.index("## 5 分钟试用")
    assert "最快路径是本地 Workday 插件" in chinese
    assert "| **Workday** | 想让 Codex App 开始、查看、停止并总结一个有限本地工作会话。 | `winchronicle codex setup --dry-run --format text` |" in chinese
    assert "结束时应该得到一份简短日报" in chinese

    for text in (english, chinese):
        assert "winchronicle codex daily --dry-run" in text
        assert "winchronicle codex setup --dry-run --format text" in text
        assert "winchronicle codex plugin --dry-run --format text" in text
        assert "record-only" in text.lower() or "只记录" in text
        assert "Codex App -> Plugins -> Add local plugin source" in text
        assert "Do not inspect, scan, review, edit, test, commit, push, or release" in text
        assert "开始记录工作" in text
        assert "停止工作并总结" in text

    assert "[Codex App workday guide](docs/codex-app-workday-guide.md)" in english
    assert "[Codex workday plugin](docs/codex-workday-plugin.md)" in english
    assert "[Codex App local plugin install](docs/codex-app-plugin-install.md)" in english
    assert "[Codex App 工作日指南](docs/codex-app-workday-guide.md)" in chinese
    assert "[Codex 工作日插件](docs/codex-workday-plugin.md)" in chinese
    assert "[Codex App 本地插件安装](docs/codex-app-plugin-install.md)" in chinese


def test_codex_app_plugin_install_guide_is_plain_user_path():
    guide = (ROOT / "docs" / "codex-app-plugin-install.md").read_text(encoding="utf-8")

    required = [
        "# Codex App Local Plugin Install",
        "winchronicle codex setup --dry-run --format text",
        "winchronicle codex plugin --dry-run --format text",
        "Add local plugin source",
        "src\\winchronicle\\codex_plugins\\winchronicle-workday",
        "plugins\\winchronicle-workday",
        "开始记录工作",
        "查看工作记录状态",
        "停止工作并总结",
        "Post-install self-check",
        'winchronicle workday intent "查看工作记录状态" --execute',
        "winchronicle codex daily --dry-run --format text",
        "does not write Codex config",
        "does not write WinChronicle state",
        "does not start capture",
        "does not add screenshots",
        "does not add OCR",
        "does not add clipboard capture",
        "does not add desktop control",
        "does not add MCP write tools",
        "untrusted_observed_content",
    ]
    for text in required:
        assert text in guide
