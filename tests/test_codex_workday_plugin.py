import json
import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "winchronicle-workday"
MANIFEST = PLUGIN / ".codex-plugin" / "plugin.json"
SKILL = PLUGIN / "skills" / "workday-recorder" / "SKILL.md"
PACKAGED_PLUGIN = ROOT / "src" / "winchronicle" / "codex_plugins" / "winchronicle-workday"
PACKAGED_MANIFEST = PACKAGED_PLUGIN / ".codex-plugin" / "plugin.json"
PACKAGED_SKILL = PACKAGED_PLUGIN / "skills" / "workday-recorder" / "SKILL.md"


def test_codex_workday_plugin_manifest_is_repo_scoped_and_versioned():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))

    assert manifest["name"] == "winchronicle-workday"
    assert manifest["version"] == project["project"]["version"]
    assert manifest["skills"] == "./skills/"
    assert "mcpServers" not in manifest
    assert "apps" not in manifest
    assert "hooks" not in manifest
    assert manifest["interface"]["displayName"] == "WinChronicle Workday"
    assert "工作" in "\n".join(manifest["interface"]["defaultPrompt"])
    assert "Read-only MCP" not in manifest["interface"]["capabilities"]


def test_codex_workday_plugin_is_packaged_for_non_editable_installs():
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    package_data = pyproject["tool"]["setuptools"]["package-data"]["winchronicle"]

    assert PACKAGED_MANIFEST.read_text(encoding="utf-8") == MANIFEST.read_text(encoding="utf-8")
    assert PACKAGED_SKILL.read_text(encoding="utf-8") == SKILL.read_text(encoding="utf-8")
    assert "codex_plugins/winchronicle-workday/.codex-plugin/plugin.json" in package_data
    assert "codex_plugins/winchronicle-workday/skills/workday-recorder/SKILL.md" in package_data


def test_codex_workday_plugin_skill_is_a_thin_existing_cli_wrapper():
    text = SKILL.read_text(encoding="utf-8")

    required_commands = [
        'winchronicle workday intent "开始工作" --execute',
        'winchronicle workday intent "结束工作并总结" --execute --wait-seconds 60',
        "winchronicle workday status --format text --language zh-CN",
    ]
    for command in required_commands:
        assert command in text

    assert "python -m winchronicle" in text
    assert "untrusted_observed_content" in text
    assert "explicit finite local monitor session" in text
    assert "read-only MCP" in text
    assert "Do not inspect, scan, review, edit, test, commit, push, or release repository files." in text


def test_codex_workday_plugin_doc_warns_before_chat_output():
    text = (ROOT / "docs" / "codex-workday-plugin.md").read_text(encoding="utf-8")

    assert "Codex chat" in text
    assert "conversation service" in text
    assert "only paste" in text.lower()
    assert "winchronicle codex plugin --dry-run" in text


def test_codex_workday_plugin_does_not_expand_capture_or_mcp_surface():
    text = SKILL.read_text(encoding="utf-8").lower()
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    forbidden_boundaries = [
        "no screenshot",
        "no ocr",
        "no clipboard",
        "no keylogging",
        "no audio",
        "no cloud upload",
        "no desktop control",
        "no mcp write tools",
    ]
    for boundary in forbidden_boundaries:
        assert boundary in text

    assert not (PLUGIN / ".mcp.json").exists()
    assert not (PLUGIN / ".app.json").exists()
    assert "mcpServers" not in manifest
    assert "apps" not in manifest
