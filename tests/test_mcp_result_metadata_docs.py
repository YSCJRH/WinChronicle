from pathlib import Path


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
