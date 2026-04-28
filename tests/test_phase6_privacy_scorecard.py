from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCORECARD = ROOT / "harness" / "scorecards" / "phase6-privacy-enrichment.md"


def test_phase6_privacy_scorecard_remains_spec_only():
    text = SCORECARD.read_text(encoding="utf-8")

    required_phrases = (
        "does not authorize implementing",
        "Screenshot capture is absent or disabled by default.",
        "OCR is absent or disabled by default.",
        "No screenshot capture code, OCR engine integration, screenshot cache",
        "Phase 6 remains optional enrichment, not the default substrate",
    )
    for phrase in required_phrases:
        assert phrase in text


def test_phase6_privacy_scorecard_requires_opt_in_allowlists_and_cache_controls():
    text = SCORECARD.read_text(encoding="utf-8")

    required_phrases = (
        "Explicit opt-in configuration",
        "`screenshots_enabled = true`",
        "`ocr_enabled = true`",
        "default values must remain false",
        "Per-app allowlists",
        "no global default allowlist",
        "Short TTL expiration",
        "cleanup command or documented deletion procedure",
        "Encryption-at-rest",
        "local WinChronicle state directory only",
    )
    for phrase in required_phrases:
        assert phrase in text


def test_phase6_privacy_scorecard_keeps_derived_text_in_existing_privacy_pipeline():
    text = SCORECARD.read_text(encoding="utf-8")

    required_phrases = (
        "OCR-derived text must enter the same pipeline as UIA text",
        "Redaction for password fields and obvious secret canaries",
        "Denylist and lock-screen skip behavior",
        "Schema validation before storage",
        "SQLite indexing only after redaction and validation",
        "Deterministic memory generation only from redacted text",
        '`trust = "untrusted_observed_content"`',
        "MCP must not expose raw screenshots by default",
    )
    for phrase in required_phrases:
        assert phrase in text


def test_phase6_privacy_scorecard_lists_required_regressions_and_non_goals():
    text = SCORECARD.read_text(encoding="utf-8")

    required_phrases = (
        "Password fields are never stored.",
        "API key canaries are blocked.",
        "Private keys are blocked.",
        "JWT canaries are blocked.",
        "GitHub token canaries are blocked.",
        "Slack token canaries are blocked.",
        "Denylisted apps do not write observed content.",
        "Lock screen captures are skipped.",
        "Prompt-injection text remains untrusted observed content.",
        "Raw screenshot cache TTL and cleanup behavior.",
        "MCP default non-exposure of raw screenshots.",
        "must not introduce audio recording, keyboard capture",
        "clipboard capture, network upload, LLM calls, desktop control",
        "MCP write tools",
        "arbitrary file reads",
        "product targeted capture",
        "daemon/service install",
        "default background capture",
    )
    for phrase in required_phrases:
        assert phrase in text
