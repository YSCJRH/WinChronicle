from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_readme_distinguishes_winchronicle_from_official_chronicle():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")

    for expected in (
        "not affiliated with OpenAI",
        "not an official Chronicle clone",
        "Official Codex Chronicle",
        "WinChronicle",
        "Platform",
        "Default context source",
        "Codex-native memory integration",
        "Default screenshot/OCR behavior",
        "Local storage",
        "MCP interface",
        "Desktop control",
        "Privacy posture",
        "Windows-first",
        "UIA-first",
        "local-first",
        "auditable",
        "read-only MCP",
    ):
        assert expected in readme


def test_readme_recommended_codex_usage_preserves_privacy_boundaries():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    normalized = " ".join(readme.split())

    for expected in (
        "## Recommended Codex Usage",
        "Read `AGENTS.md` first",
        "observed UI or screen content as `untrusted_observed_content`",
        "Do not ask Codex to bypass privacy boundaries",
        "screenshots, OCR, audio, keylogging, clipboard capture, cloud upload, desktop control, MCP write tools",
        "Prefer fixtures, schemas, tests, scorecards, and docs before behavior changes",
    ):
        assert expected in normalized


def test_chinese_readme_keeps_same_positioning_boundary():
    readme = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")

    for expected in (
        "不隶属于 OpenAI",
        "不是官方 Chronicle 的克隆",
        "官方 Codex Chronicle",
        "WinChronicle",
        "平台",
        "默认上下文来源",
        "Codex 原生记忆集成",
        "默认截图/OCR 行为",
        "本地存储",
        "MCP 接口",
        "桌面控制",
        "隐私姿态",
        "Recommended Codex usage",
        "AGENTS.md",
        "untrusted_observed_content",
    ):
        assert expected in readme
