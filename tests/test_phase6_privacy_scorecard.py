import copy
import json
import re
import tomllib
from pathlib import Path

import pytest
from jsonschema import ValidationError, validate


ROOT = Path(__file__).resolve().parents[1]
SCORECARD = ROOT / "harness" / "scorecards" / "phase6-privacy-enrichment.md"
PRIVACY_GATES = ROOT / "harness" / "scorecards" / "privacy-gates.md"
PHASE6_CONTRACT_SCHEMA = (
    ROOT / "harness" / "specs" / "phase6-privacy-enrichment-contract.schema.json"
)
PHASE6_CONTRACT_FIXTURE = (
    ROOT / "harness" / "fixtures" / "phase6" / "privacy_enrichment_contract_spec_only.json"
)
PHASE6_INVALID_FIXTURES = (
    ROOT
    / "harness"
    / "fixtures"
    / "phase6"
    / "privacy_enrichment_contract_invalid_global_allowlist.json",
    ROOT
    / "harness"
    / "fixtures"
    / "phase6"
    / "privacy_enrichment_contract_invalid_raw_cache_ttl.json",
    ROOT
    / "harness"
    / "fixtures"
    / "phase6"
    / "privacy_enrichment_contract_invalid_runtime_status.json",
)
PYPROJECT = ROOT / "pyproject.toml"
PRODUCTION_ROOTS = (ROOT / "src" / "winchronicle", ROOT / "resources")
SOURCE_SUFFIXES = {".py", ".cs", ".csproj", ".ps1"}
ALLOWED_PHASE6_SOURCE_SENTINELS = {
    "src/winchronicle/capture.py": {'"screenshot": None,'},
    "src/winchronicle/privacy.py": {
        '"screenshots_enabled": False,',
        '"ocr_enabled": False,',
    },
    "src/winchronicle/mcp/server.py": {
        '"screenshot",',
        '"ocr",',
    },
    "src/winchronicle/cli.py": {
        '"--screenshot",',
        '"--ocr",',
    },
    "resources/win-uia-helper/Program.cs": {
        '["screenshots"] = false,',
        '["ocr"] = false,',
    },
}
FORBIDDEN_PHASE6_ENGINE_PATTERNS = tuple(
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"\bImageGrab\b",
        r"\bmss\b",
        r"\bpyscreenshot\b",
        r"\bpyautogui\b",
        r"\bpytesseract\b",
        r"\beasyocr\b",
        r"\bpaddleocr\b",
        r"\bWindows\.Graphics\.Capture\b",
        r"\bCopyFromScreen\b",
        r"\bBitBlt\b",
        r"\bPrintWindow\b",
        r"\bTesseract\b",
    )
)


def test_phase6_privacy_scorecard_remains_spec_only():
    text = SCORECARD.read_text(encoding="utf-8")
    normalized = _normalize_markdown(text)

    required_phrases = (
        "does not authorize implementing",
        "Screenshot capture is not implemented in this preflight",
        "OCR is not implemented in this preflight",
        "future implementation must be disabled by default",
        "No screenshot capture code, OCR engine integration, screenshot cache",
        "Phase 6 remains optional enrichment, not the default substrate",
        "These artifacts are not runtime configuration",
        "Product code must not read them in v0.1",
    )
    for phrase in required_phrases:
        assert phrase in normalized


def test_phase6_privacy_scorecard_records_threat_model_and_preflight_artifacts():
    text = SCORECARD.read_text(encoding="utf-8")
    privacy_gates = PRIVACY_GATES.read_text(encoding="utf-8")
    normalized = _normalize_markdown(text)
    normalized_privacy_gates = _normalize_markdown(privacy_gates)

    required_phrases = (
        "Threat Model",
        "Raw screenshots can expose passwords",
        "OCR text can reintroduce secrets after UIA redaction",
        "Broad allowlists can silently become all-app capture",
        "Raw caches can outlive user intent",
        "MCP exposure can leak visual artifacts across agent boundaries",
        "phase6-privacy-enrichment-contract.schema.json",
        "privacy_enrichment_contract_spec_only.json",
        "negative fixtures for wildcard allowlists",
        "too-long raw cache TTL",
        "runtime status",
        "sample shape examples only, not approved apps",
        "do not authorize screenshot capture, OCR, raw screenshot caches",
    )
    for phrase in required_phrases:
        assert phrase in normalized

    for phrase in (
        "Phase 6 preflight contract artifacts",
        "specification-only",
        "not runtime configuration",
        "must not be read by product code in v0.1",
    ):
        assert phrase in normalized_privacy_gates


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


def test_phase6_privacy_enrichment_contract_fixture_validates_as_spec_only():
    schema = _load_json(PHASE6_CONTRACT_SCHEMA)
    contract = _load_json(PHASE6_CONTRACT_FIXTURE)

    validate(instance=contract, schema=schema)

    assert contract["status"] == "spec_only"
    assert contract["defaults"] == {
        "screenshots_enabled": False,
        "ocr_enabled": False,
        "raw_screenshot_cache_enabled": False,
        "global_allowlist_enabled": False,
    }
    assert contract["future_opt_in_requirements"]["allows_runtime_capture_in_v0_1"] is False
    assert contract["allowlist_policy"]["sample_allowlist_entries_only"] is True
    assert contract["allowlist_policy"]["runtime_allowlist_config_allowed"] is False
    assert contract["allowlist_policy"]["global_default_allowlist_allowed"] is False
    assert contract["allowlist_policy"]["implicit_all_apps_allowed"] is False
    assert contract["raw_cache_policy"]["ttl_seconds_max"] <= 3600
    assert contract["raw_cache_policy"]["cleanup_required"] is True
    assert contract["mcp_policy"]["raw_screenshot_exposure_default"] is False
    assert contract["mcp_policy"]["mcp_write_tools_allowed"] is False
    assert "desktop control" in contract["non_goals"]


def test_phase6_privacy_enrichment_contract_rejects_committed_negative_fixtures():
    schema = _load_json(PHASE6_CONTRACT_SCHEMA)

    for fixture in PHASE6_INVALID_FIXTURES:
        with pytest.raises(ValidationError):
            validate(instance=_load_json(fixture), schema=schema)


def test_phase6_privacy_enrichment_contract_rejects_unsafe_in_memory_variants():
    schema = _load_json(PHASE6_CONTRACT_SCHEMA)
    baseline = _load_json(PHASE6_CONTRACT_FIXTURE)

    unsafe_variants = []

    screenshots_enabled = copy.deepcopy(baseline)
    screenshots_enabled["defaults"]["screenshots_enabled"] = True
    unsafe_variants.append(screenshots_enabled)

    ocr_enabled = copy.deepcopy(baseline)
    ocr_enabled["defaults"]["ocr_enabled"] = True
    unsafe_variants.append(ocr_enabled)

    missing_cleanup = copy.deepcopy(baseline)
    missing_cleanup["raw_cache_policy"]["cleanup_required"] = False
    unsafe_variants.append(missing_cleanup)

    raw_screenshot_mcp = copy.deepcopy(baseline)
    raw_screenshot_mcp["mcp_policy"]["raw_screenshot_exposure_default"] = True
    unsafe_variants.append(raw_screenshot_mcp)

    runtime_allowlist = copy.deepcopy(baseline)
    runtime_allowlist["allowlist_policy"]["runtime_allowlist_config_allowed"] = True
    unsafe_variants.append(runtime_allowlist)

    allows_runtime_capture = copy.deepcopy(baseline)
    allows_runtime_capture["future_opt_in_requirements"]["allows_runtime_capture_in_v0_1"] = True
    unsafe_variants.append(allows_runtime_capture)

    missing_non_goal = copy.deepcopy(baseline)
    missing_non_goal["non_goals"].remove("arbitrary file reads")
    unsafe_variants.append(missing_non_goal)

    for variant in unsafe_variants:
        with pytest.raises(ValidationError):
            validate(instance=variant, schema=schema)


def test_phase6_has_no_source_surface_implementation_artifacts():
    unexpected_surface_mentions = []
    unexpected_engine_mentions = []

    for path in _production_source_files():
        relative = path.relative_to(ROOT).as_posix()
        allowed_lines = ALLOWED_PHASE6_SOURCE_SENTINELS.get(relative, set())
        text = path.read_text(encoding="utf-8")
        for line_number, line in enumerate(text.splitlines(), start=1):
            stripped = line.strip()
            if re.search(r"screenshot|ocr", line, re.IGNORECASE) and stripped not in allowed_lines:
                unexpected_surface_mentions.append(f"{relative}:{line_number}: {stripped}")
            for pattern in FORBIDDEN_PHASE6_ENGINE_PATTERNS:
                if pattern.search(line):
                    unexpected_engine_mentions.append(f"{relative}:{line_number}: {stripped}")

    assert unexpected_surface_mentions == []
    assert unexpected_engine_mentions == []


def test_phase6_contract_artifacts_are_not_runtime_configuration():
    forbidden_runtime_references = (
        "phase6-privacy-enrichment-contract",
        "privacy_enrichment_contract",
        "harness/fixtures/phase6",
        "harness\\fixtures\\phase6",
    )

    references = []
    for path in _production_source_files():
        relative = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8").lower()
        for reference in forbidden_runtime_references:
            if reference.lower() in text:
                references.append(f"{relative}: {reference}")

    assert references == []


def test_phase6_has_no_direct_dependency_surface_implementation_artifacts():
    package_metadata = tomllib.loads(PYPROJECT.read_text(encoding="utf-8"))
    dependencies = set(package_metadata["project"].get("dependencies", []))
    for extra_dependencies in package_metadata["project"].get(
        "optional-dependencies", {}
    ).values():
        dependencies.update(extra_dependencies)

    normalized_names = {_normalize_dependency_name(dependency) for dependency in dependencies}
    forbidden_direct_dependencies = {
        "aiohttp",
        "comtypes",
        "easyocr",
        "httpx",
        "keyboard",
        "mss",
        "openai",
        "opencv-contrib-python",
        "opencv-python",
        "paddleocr",
        "pillow",
        "pyaudio",
        "pyautogui",
        "pynput",
        "pyperclip",
        "pyscreenshot",
        "pytesseract",
        "pywin32",
        "pywinauto",
        "requests",
        "sounddevice",
        "uiautomation",
        "whisper",
    }
    normalized_forbidden = {
        _normalize_dependency_name(dependency)
        for dependency in forbidden_direct_dependencies
    }

    assert normalized_names.isdisjoint(normalized_forbidden)


def _production_source_files() -> list[Path]:
    return sorted(
        path
        for root in PRODUCTION_ROOTS
        for path in root.rglob("*")
        if path.is_file()
        and path.suffix in SOURCE_SUFFIXES
        and not {"bin", "obj"}.intersection(path.relative_to(root).parts)
    )


def _normalize_dependency_name(dependency: str) -> str:
    name = re.split(r"\s*(?:[<>=!~]=?|;|\[)", dependency, maxsplit=1)[0]
    return re.sub(r"[-_.]+", "-", name).lower()


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _normalize_markdown(text: str) -> str:
    return " ".join(text.split())
