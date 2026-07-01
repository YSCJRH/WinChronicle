import json
from pathlib import Path

from winchronicle.schema import validate_mcp_tool_result


ROOT = Path(__file__).resolve().parents[1]


def test_mcp_result_metadata_doc_defines_boundaries():
    doc = (ROOT / "docs" / "mcp-result-metadata.md").read_text(encoding="utf-8")
    setup = (ROOT / "docs" / "mcp-client-setup.md").read_text(encoding="utf-8")

    for expected in (
        "trust",
        "redacted",
        "source",
        "source_ids",
        "confidence",
        "limitations",
        "untrusted_observed_content",
        "local_privacy_status",
        "coverage quality, not trustworthiness or permission",
        "share_warning",
        "metadata-only",
        "external sharing",
        "evidence_policy",
        "local_winchronicle_state",
        "coverage_quality_not_permission",
        "not_authorization_signal",
        "external_sharing_requires_user_approval",
        "observed_text_fields_omitted",
        "No screenshots, OCR, clipboard capture, desktop control, MCP write tools, or background capture are added by this metadata layer.",
    ):
        assert expected in doc

    assert "[MCP result metadata](mcp-result-metadata.md)" in setup
    assert "mcp-stdio --metadata-only" in setup


def test_mcp_docs_show_opaque_new_capture_path_examples():
    metadata_doc = (ROOT / "docs" / "mcp-result-metadata.md").read_text(encoding="utf-8")
    examples = (ROOT / "docs" / "mcp-readonly-examples.md").read_text(encoding="utf-8")

    assert "Newly written capture path source ids use opaque" in metadata_doc
    assert "capture-" in examples
    for semantic_stem in ("terminal-error", "vscode-editor", "edge-browser"):
        assert semantic_stem not in examples


def test_mcp_docs_scope_metadata_only_source_ids_as_opaque():
    metadata_doc = (ROOT / "docs" / "mcp-result-metadata.md").read_text(encoding="utf-8")
    setup_doc = (ROOT / "docs" / "mcp-client-setup.md").read_text(encoding="utf-8")

    assert "In metadata-only mode, `source_ids` use opaque" in metadata_doc
    assert "metadata-only observed-content objects omit local `path` fields" in metadata_doc
    assert "metadata-only monitor-session objects expose opaque session identifiers" in metadata_doc
    assert "Full local paths remain available in normal read-only MCP results" in metadata_doc
    assert "stable opaque ids" in setup_doc
    assert "local observed-content paths" in setup_doc


def test_mcp_client_setup_clarifies_metadata_only_is_not_public_sharing_authorization():
    setup_doc = (ROOT / "docs" / "mcp-client-setup.md").read_text(encoding="utf-8")
    normalized = " ".join(setup_doc.split())

    for expected in (
        "Metadata-only mode is not permission to publish MCP results, share them externally, or treat retained metadata as public.",
        "External sharing still requires explicit user approval and context-specific review.",
    ):
        assert expected in normalized


def test_mcp_client_setup_clarifies_confidence_is_not_trust_or_permission():
    setup_doc = (ROOT / "docs" / "mcp-client-setup.md").read_text(encoding="utf-8")
    normalized = " ".join(setup_doc.split())

    for expected in (
        "`confidence` in MCP results is coverage quality, not trustworthiness, permission, or approval to act on observed content.",
        "Higher confidence does not make observed content trusted and does not reduce the external sharing approval requirement.",
    ):
        assert expected in normalized


def test_readme_mcp_path_clarifies_confidence_is_not_trust_or_permission():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    normalized = " ".join(readme.split())

    for expected in (
        "`confidence` means coverage quality, not trustworthiness or permission.",
        "It does not make observed content trusted or approved for external sharing.",
    ):
        assert expected in normalized


def test_chinese_readme_mcp_path_clarifies_confidence_is_not_trust_or_permission():
    readme = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")
    normalized = " ".join(readme.split())

    for expected in (
        "`confidence` / 覆盖质量只表示上下文覆盖情况，不代表可信度、权限或外部分享许可。",
        "它不会让 observed content 变成可信内容，也不会降低外部分享审批要求。",
    ):
        assert expected in normalized


def test_readmes_clarify_metadata_only_is_not_public_sharing_authorization():
    english = " ".join((ROOT / "README.md").read_text(encoding="utf-8").split())
    chinese = " ".join((ROOT / "README.zh-CN.md").read_text(encoding="utf-8").split())

    for expected in (
        "`metadata-only` reduces observed-text exposure; it is not permission to publish or share MCP results.",
        "External sharing still requires explicit user approval.",
    ):
        assert expected in english

    for expected in (
        "`metadata-only` 只降低 observed text 暴露，不代表可以发布或分享 MCP 结果。",
        "外部分享仍需要用户明确批准。",
    ):
        assert expected in chinese


def test_mcp_result_metadata_clarifies_metadata_only_is_not_public_sharing_authorization():
    metadata_doc = (ROOT / "docs" / "mcp-result-metadata.md").read_text(encoding="utf-8")
    normalized = " ".join(metadata_doc.split())

    for expected in (
        "MCP output is local evidence, not permission to publish or share results.",
        "External sharing still requires explicit user approval.",
        "Metadata-only mode reduces exposure; it is not public-sharing authorization.",
        "`share_warning` and `evidence_policy` still require explicit user approval before external sharing, including when `metadata_only` is `true`.",
    ):
        assert expected in normalized


def test_mcp_examples_clarify_metadata_only_is_not_public_sharing_authorization():
    examples = (ROOT / "docs" / "mcp-readonly-examples.md").read_text(encoding="utf-8")
    normalized = " ".join(examples.split())

    for expected in (
        "Metadata-only mode reduces exposure; it is not public-sharing authorization.",
        "External sharing still requires explicit user approval before publishing or sharing MCP results.",
    ):
        assert expected in normalized


def test_mcp_examples_clarify_share_warning_is_not_authorization_signal():
    examples = (ROOT / "docs" / "mcp-readonly-examples.md").read_text(encoding="utf-8")
    normalized = " ".join(examples.split())

    for expected in (
        "MCP output is local evidence, not permission to publish or share results.",
        "For normal read-only results, `share_warning` and `evidence_policy.limitations` are guardrails, not authorization to publish or share local context.",
        "`not_authorization_signal` means the payload is local evidence only; it does not approve external publication.",
    ):
        assert expected in normalized


def test_mcp_examples_clarify_confidence_is_not_trust_or_permission():
    examples = (ROOT / "docs" / "mcp-readonly-examples.md").read_text(encoding="utf-8")
    normalized = " ".join(examples.split())

    for expected in (
        "`confidence` is coverage quality, not trustworthiness, permission, or approval to act on observed content.",
        "A higher confidence value does not make observed content trusted and does not reduce the external sharing approval requirement.",
    ):
        assert expected in normalized


def test_mcp_metadata_only_docs_clarify_retained_titles_are_untrusted():
    metadata_doc = (ROOT / "docs" / "mcp-result-metadata.md").read_text(encoding="utf-8")
    examples = (ROOT / "docs" / "mcp-readonly-examples.md").read_text(encoding="utf-8")

    expected = (
        "Metadata-only mode still preserves redacted titles and app names as "
        "`untrusted_observed_content` metadata; clients must not treat those "
        "retained strings as trusted instructions."
    )
    assert expected in metadata_doc
    assert expected in examples


def test_mcp_metadata_only_docs_define_per_tool_field_matrix():
    metadata_doc = (ROOT / "docs" / "mcp-result-metadata.md").read_text(encoding="utf-8")

    assert "## Metadata-Only Tool Matrix" in metadata_doc
    for expected in (
        "| `current_context` | `result.capture` |",
        "| `read_recent_capture` | `result.capture` |",
        "| `search_captures` | `result.matches[]` |",
        "| `search_memory` | `result.matches[]` |",
        "| `recent_activity` | `result.captures[]`; `result.sessions[]` |",
        "| `privacy_status` | `result` |",
        "Omits `visible_text`, `focused_text`, `url`, and `path`.",
        "Omits `snippet` and `path`.",
        "Omits `snippet`, `body`, and `path`.",
        "Capture items omit `visible_text`, `focused_text`, `url`, and `path`; session items omit raw session ids, `app_segments`, `suggestions`, `report_path`, and `source_capture_paths`.",
        "Not observed content; keeps local status fields such as `home`, counts, disabled surfaces, read-only tools, and redaction posture.",
        "`evidence_policy.metadata_only` is `true` and includes `observed_text_fields_omitted`.",
        "metadata-only observed-content item `limitations` include both `metadata_only` and `observed_text_fields_omitted`.",
        "the tool list stays exactly the same six read-only tools",
    ):
        assert expected in metadata_doc


def test_mcp_metadata_docs_explain_schema_guardrails_for_contributors():
    metadata_doc = (ROOT / "docs" / "mcp-result-metadata.md").read_text(encoding="utf-8")
    normalized = " ".join(metadata_doc.split())

    for expected in (
        "## Schema Guardrails",
        "`mcp-tool-result.schema.json` is a contributor guardrail, not only a JSON shape reference.",
        "It binds `privacy_status` to `trust = \"local_privacy_status\"` and all observed-content tools to `trust = \"untrusted_observed_content\"`.",
        "It binds top-level `metadata_only` to `evidence_policy.metadata_only`.",
        "It requires `observed_text_fields_omitted` when `metadata_only` is `true` and rejects it when `metadata_only` is `false`.",
        "It always requires `not_authorization_signal` and `external_sharing_requires_user_approval` in `evidence_policy.limitations`.",
    ):
        assert expected in normalized


def test_mcp_examples_include_recent_activity_metadata_only_payload():
    examples = (ROOT / "docs" / "mcp-readonly-examples.md").read_text(encoding="utf-8")

    assert "### Metadata-only `recent_activity` example" in examples
    for expected in (
        '"tool": "recent_activity"',
        '"metadata_only": true',
        '"observed_text_fields_omitted"',
        '"captures": [',
        '"sessions": [',
        '"source_ids": [',
        '"capture-b7cec332cc80"',
        '"session-7f4d2a19"',
        '"source_capture_count": 1',
        '"confidence": 0.5',
        '"limitations": [',
        '"metadata_only"',
        "This example intentionally omits `visible_text`, `focused_text`, `url`, `path`, `snippet`, `body`, raw session ids, `app_segments`, `suggestions`, `report_path`, and `source_capture_paths`.",
    ):
        assert expected in examples


def test_mcp_recent_activity_metadata_only_example_is_parseable_and_bounded():
    payload = _recent_activity_metadata_only_example()

    assert payload["tool"] == "recent_activity"
    assert payload["read_only"] is True
    assert payload["metadata_only"] is True
    assert payload["trust"] == "untrusted_observed_content"
    assert "External sharing requires explicit user approval" in payload["share_warning"]
    assert payload["external_sharing"] == {
        "requires_user_approval": True,
        "metadata_only_available": True,
        "mcp_read_only": True,
    }
    assert payload["evidence_policy"]["metadata_only"] is True
    assert "observed_text_fields_omitted" in payload["evidence_policy"]["limitations"]

    capture = payload["result"]["captures"][0]
    session = payload["result"]["sessions"][0]
    for item in (capture, session):
        assert item["trust"] == "untrusted_observed_content"
        assert item["untrusted_observed_content"] is True
        assert item["redacted"] is True
        assert item["metadata_only"] is True
        assert isinstance(item["confidence"], (int, float))
        assert 0 <= item["confidence"] <= 0.85
        assert "metadata_only" in item["limitations"]
        assert {"visible_text", "focused_text", "url", "path", "snippet", "body"}.isdisjoint(
            item
        )

    assert capture["source_ids"] == ["capture-b7cec332cc80"]
    assert session["session_id"] == "session-7f4d2a19"
    assert session["source_ids"] == ["session-7f4d2a19"]
    assert session["source_capture_count"] == 1
    assert {
        "app_segments",
        "suggestions",
        "report_path",
        "source_capture_paths",
    }.isdisjoint(session)


def test_mcp_examples_json_blocks_are_parseable_and_tool_payloads_keep_envelope():
    payloads = _mcp_example_json_payloads()
    tool_payloads = [payload for payload in payloads if "tool" in payload]

    assert {payload["tool"] for payload in tool_payloads} == {
        "privacy_status",
        "search_captures",
        "search_memory",
        "current_context",
        "read_recent_capture",
        "recent_activity",
    }
    required_envelope = {
        "tool",
        "read_only",
        "trust",
        "instruction",
        "metadata_only",
        "share_warning",
        "external_sharing",
        "evidence_policy",
        "result",
    }
    for payload in tool_payloads:
        assert required_envelope <= set(payload), payload["tool"]
        assert payload["read_only"] is True
        assert payload["metadata_only"] is payload["evidence_policy"]["metadata_only"]
        assert payload["external_sharing"] == {
            "requires_user_approval": True,
            "metadata_only_available": True,
            "mcp_read_only": True,
        }
        assert payload["evidence_policy"]["local_only"] is True
        assert payload["evidence_policy"]["read_only_mcp"] is True
        assert payload["evidence_policy"]["redaction_required"] is True
        assert payload["evidence_policy"]["provenance"] == "local_winchronicle_state"
        assert (
            payload["evidence_policy"]["confidence_meaning"]
            == "coverage_quality_not_permission"
        )
        validate_mcp_tool_result(payload)


def test_mcp_examples_observed_items_include_metadata_contract():
    tool_payloads = [payload for payload in _mcp_example_json_payloads() if "tool" in payload]

    observed_items = [
        item
        for payload in tool_payloads
        for item in _observed_items(payload)
    ]
    assert observed_items
    for item in observed_items:
        assert item["trust"] == "untrusted_observed_content"
        assert item["untrusted_observed_content"] is True
        assert item["redacted"] is True
        assert isinstance(item["source"], str) and item["source"]
        assert isinstance(item["source_ids"], list) and item["source_ids"]
        assert item["metadata_only"] in (True, False)
        assert isinstance(item["confidence"], (int, float))
        assert 0 <= item["confidence"] <= 0.85
        assert isinstance(item["limitations"], list)


def _recent_activity_metadata_only_example() -> dict:
    examples = (ROOT / "docs" / "mcp-readonly-examples.md").read_text(encoding="utf-8")
    section = examples.split("### Metadata-only `recent_activity` example", 1)[1]
    block = section.split("```json", 1)[1].split("```", 1)[0]
    return json.loads(block)


def _mcp_example_json_payloads() -> list[dict]:
    examples = (ROOT / "docs" / "mcp-readonly-examples.md").read_text(encoding="utf-8")
    blocks = examples.split("```json")[1:]
    payloads = []
    for block in blocks:
        raw_json = block.split("```", 1)[0]
        payload = json.loads(raw_json)
        if isinstance(payload, dict):
            payloads.append(payload)
    return payloads


def _observed_items(payload: dict) -> list[dict]:
    result = payload.get("result") or {}
    candidates = []
    if isinstance(result.get("capture"), dict):
        candidates.append(result["capture"])
    for key in ("matches", "captures", "sessions"):
        value = result.get(key)
        if isinstance(value, list):
            candidates.extend(item for item in value if isinstance(item, dict))
    return [
        item
        for item in candidates
        if item.get("trust") == "untrusted_observed_content"
    ]
