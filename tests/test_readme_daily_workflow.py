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
    assert "## 如果你只想让 Codex App 记录工作" in chinese
    assert chinese.index("## 如果你只想让 Codex App 记录工作") < chinese.index("## 5 分钟试用")
    assert "最快路径是本地 Workday 插件" in chinese

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
    assert "[Codex App 工作日指南](docs/codex-app-workday-guide.md)" in chinese
    assert "[Codex 工作日插件](docs/codex-workday-plugin.md)" in chinese
