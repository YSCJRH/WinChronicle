import json
import tomllib
from pathlib import Path

from winchronicle.cli import main


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "winchronicle-workday"
MANIFEST = PLUGIN / ".codex-plugin" / "plugin.json"
SKILL = PLUGIN / "skills" / "workday-recorder" / "SKILL.md"
PACKAGED_PLUGIN = ROOT / "src" / "winchronicle" / "codex_plugins" / "winchronicle-workday"
PACKAGED_MANIFEST = PACKAGED_PLUGIN / ".codex-plugin" / "plugin.json"
PACKAGED_SKILL = PACKAGED_PLUGIN / "skills" / "workday-recorder" / "SKILL.md"
ENTRYPOINT_CONTRACT = ROOT / "harness" / "fixtures" / "workday" / "plugin_entrypoint_contract.json"


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
    assert "开始记录工作" in manifest["interface"]["defaultPrompt"]
    assert "停止工作并总结" in manifest["interface"]["defaultPrompt"]
    assert "Read-only MCP" not in manifest["interface"]["capabilities"]


def test_codex_workday_plugin_default_prompts_are_daily_user_actions():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    assert manifest["interface"]["defaultPrompt"] == [
        "开始记录工作",
        "停止工作并总结",
        "查看工作记录状态",
    ]
    assert len(manifest["interface"]["defaultPrompt"]) <= 3
    assert "record-only" in manifest["interface"]["longDescription"]
    assert "repository scanning" in manifest["interface"]["longDescription"]


def test_codex_workday_plugin_entrypoints_match_fixture_contract(
    tmp_path, monkeypatch, capsys
):
    contract = json.loads(ENTRYPOINT_CONTRACT.read_text(encoding="utf-8"))
    manifests = [
        json.loads(MANIFEST.read_text(encoding="utf-8")),
        json.loads(PACKAGED_MANIFEST.read_text(encoding="utf-8")),
    ]
    skill_texts = [
        SKILL.read_text(encoding="utf-8"),
        PACKAGED_SKILL.read_text(encoding="utf-8"),
    ]

    for manifest in manifests:
        interface = manifest["interface"]
        visible_copy = " ".join(
            [
                interface["shortDescription"],
                interface["longDescription"],
                *interface["defaultPrompt"],
            ]
        )
        assert interface["defaultPrompt"] == contract["visible_default_prompts"]
        for expected in contract["manifest_must_contain"]:
            assert expected in visible_copy
        for forbidden in contract["manifest_forbidden_substrings"]:
            assert forbidden not in visible_copy

    for text in skill_texts:
        normalized = " ".join(text.split())
        for expected in contract["skill_must_contain"]:
            assert " ".join(expected.split()) in normalized
        for forbidden in contract["skill_forbidden_substrings"]:
            assert forbidden not in normalized

    monkeypatch.setenv("WINCHRONICLE_HOME", str(tmp_path / "state"))
    for case in contract["intent_cases"]:
        assert main(["workday", "intent", case["phrase"]]) == 0
        plan = json.loads(capsys.readouterr().out)
        assert plan["matched"] is True
        assert plan["execute"] is False
        assert plan["intent"] == case["intent"]
        assert plan["command"] == case["command"]
        assert plan["bounded"] is True
        assert plan["capture_surface"] == case["capture_surface"]
        assert plan["trust"] == "local_workday_intent_mapping"
        assert plan["dry_run_by_default"] is True
        assert plan.get("operator_focus", []) == case.get("operator_focus", [])

    assert not (tmp_path / "state" / "workday-active.json").exists()


def test_codex_workday_plugin_manifest_visible_copy_names_summary_boundary():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    packaged_manifest = json.loads(PACKAGED_MANIFEST.read_text(encoding="utf-8"))

    for current_manifest in (manifest, packaged_manifest):
        interface = current_manifest["interface"]
        visible_copy = " ".join(
            [
                interface["shortDescription"],
                interface["longDescription"],
                *interface["defaultPrompt"],
            ]
        )
        normalized = " ".join(visible_copy.split())

        for expected in (
            "record-only",
            "summary-level evidence",
            "does not send raw observed text",
            "without repository scanning",
        ):
            assert expected in normalized


def test_codex_workday_plugin_is_packaged_for_non_editable_installs():
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    package_data = pyproject["tool"]["setuptools"]["package-data"]["winchronicle"]

    assert PACKAGED_MANIFEST.read_text(encoding="utf-8") == MANIFEST.read_text(encoding="utf-8")
    assert PACKAGED_SKILL.read_text(encoding="utf-8") == SKILL.read_text(encoding="utf-8")
    assert "codex_plugins/winchronicle-workday/.codex-plugin/plugin.json" in package_data
    assert "codex_plugins/winchronicle-workday/skills/workday-recorder/SKILL.md" in package_data


def test_codex_workday_plugin_skill_is_a_thin_existing_cli_wrapper():
    text = SKILL.read_text(encoding="utf-8")
    packaged_text = PACKAGED_SKILL.read_text(encoding="utf-8")
    normalized_text = " ".join(text.split())
    normalized_packaged_text = " ".join(packaged_text.split())

    required_commands = [
        'winchronicle workday intent "开始工作" --execute',
        'winchronicle workday intent "结束工作并总结" --execute --wait-seconds 60',
        'winchronicle workday intent "查看工作记录状态" --execute',
        "winchronicle workday summarize <session-id> --format text --language zh-CN",
    ]
    for command in required_commands:
        assert command in text
        assert command in packaged_text

    for expected in (
        "python -m winchronicle",
        "untrusted_observed_content",
        "explicit finite local monitor session",
        "read-only MCP",
        "Do not inspect, scan, review, edit, test, commit, push, or release repository files.",
        "Use the local CLI output as evidence, then write a Codex-assisted Chinese daily report",
        "Use only summary-level evidence",
        "Do not paste telemetry counters as the main answer",
        "Technical counters belong only in the explicit technical/debugging view, not in the default daily report.",
        "Do not show capture counts, skipped counts, raw JSON, source ids, storage policy, privacy boundary paragraphs, allowlist, metadata, or capture surface terminology in the default report body.",
        "human daily review, not a telemetry or log-counter report",
        "今日完成了什么",
        "进展如何",
        "明天怎样更高效",
        "今天主要做了什么",
        "值得留意的地方",
        "明天怎么更顺手",
        "今日工作复盘",
        "今日工作结论",
        "工作进行情况",
        "明天改进建议",
        "可考虑方向",
        "--summary-style technical",
        "winchronicle projects add <path> --name <name>",
        "Do not auto-register or scan projects during a recording-only turn",
        "pass the full user phrase",
        "今天主要做",
        "operator focus",
        "obvious-secret redaction",
        "prefer actionable directions",
        "Do not send raw visible_text, raw focused_text, file contents, full diffs, URL query strings, screenshots, OCR output, clipboard content, keyboard input, or audio content to Codex chat.",
        "Do not add a new CLI command, MCP tool, capture source, or evidence schema for this behavior.",
    ):
        normalized_expected = " ".join(expected.split())
        assert normalized_expected in normalized_text
        assert normalized_expected in normalized_packaged_text

    for removed_default_section in ("待确认问题", "数据依据"):
        assert removed_default_section not in text
        assert removed_default_section not in packaged_text

    for forbidden in (
        "desktop-observation",
        "paste the CLI text summary directly into chat",
        "Do not compress it into a one-paragraph agent summary",
    ):
        assert forbidden not in text
        assert forbidden not in packaged_text


def test_codex_workday_plugin_skill_frontmatter_names_recording_triggers():
    text = SKILL.read_text(encoding="utf-8")
    frontmatter = text.split("---", 2)[1]

    for phrase in [
        "开始记录工作",
        "开始记录今天的工作",
        "停止工作并总结",
        "开始工作",
        "结束工作并总结",
        "结束今天的工作并总结",
    ]:
        assert phrase in frontmatter
    assert "查看工作记录状态" in frontmatter
    assert "repository scanning" in frontmatter


def test_codex_workday_plugin_recording_mode_blocks_repo_preflight():
    text = SKILL.read_text(encoding="utf-8")
    doc_text = (ROOT / "docs" / "codex-app-workday-guide.md").read_text(encoding="utf-8")

    assert "## Recording Mode" in text
    assert "Do not run preliminary repository discovery commands" in text
    for command_name in ["git status", "rg", "Get-ChildItem", "Get-Content", "ls"]:
        assert command_name in text
    assert "Do not read AGENTS.md only to start recording" in text
    assert "Do not use the repository task report format" in text
    assert "If the user only says a workday recording phrase, execute the matching command first" in text

    assert "Record-only mode" in doc_text
    assert "do not run repository preflight commands" in doc_text


def test_codex_workday_plugin_doc_warns_before_chat_output():
    text = (ROOT / "docs" / "codex-workday-plugin.md").read_text(encoding="utf-8")
    normalized = " ".join(text.split())

    for phrase in [
        "开始工作",
        "开始记录工作",
        "开始记录今天的工作",
        "结束工作并总结",
        "结束今天的工作并总结",
        "停止工作并总结",
    ]:
        assert phrase in text
    assert "Starter Prompts" in text
    assert "first three" in text
    assert "copyable plugin-source instruction" in text
    assert "raw JSON" in text
    assert "repository task report" in text
    assert "Codex App -> Plugins -> Add local plugin source" in text
    assert "Fastest Codex App Setup" in text
    assert "winchronicle codex setup --dry-run --format text" in text
    assert "winchronicle codex plugin --dry-run --format text" in text
    assert "does not write Codex config" in text
    assert "does not write WinChronicle state" in text
    assert "does not start capture" in text
    assert "Codex chat" in text
    assert "conversation service" in text
    assert "only paste" in text.lower()
    assert "winchronicle codex daily --dry-run" in text
    assert "winchronicle codex setup --dry-run" in text
    assert "winchronicle codex plugin --dry-run" in text
    assert "winchronicle codex plugin --dry-run --format text" in text
    assert "`summary_boundary`" in text
    assert "not a telemetry or log-counter report" in text
    assert "Codex-assisted report" in text
    assert "local evidence package" in text
    assert "not a telemetry or log-counter report" in normalized
    assert "summary-level evidence" in normalized
    assert "does not send raw observed text" in normalized
    assert "does not read file contents" in normalized
    assert "does not add a CLI command" in normalized
    assert "今天主要做了什么" in text
    assert "进展如何" in text
    assert "值得留意的地方" in text
    assert "明天怎么更顺手" in text
    assert "capture counts" in text
    assert "metadata" in text
    assert "does not add screenshot" in text
    assert "开始记录工作：今天主要做" in text
    assert "operator focus" in text
    assert "obvious-secret redaction" in text
    assert "电脑观察补充" not in text


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


def test_codex_app_guide_documents_assisted_summary_boundary():
    text = (ROOT / "docs" / "codex-app-workday-guide.md").read_text(encoding="utf-8")
    normalized = " ".join(text.split())

    for expected in (
        "Codex-assisted daily review",
        "summary-level evidence",
        "does not send raw observed text",
        "`summary_boundary`",
        "not a telemetry or log-counter report",
        "does not read file contents",
        "does not add a new CLI command",
        "does not add MCP tools",
        "今天主要做了什么",
        "进展如何",
        "值得留意的地方",
        "明天怎么更顺手",
    ):
        assert " ".join(expected.split()) in normalized
