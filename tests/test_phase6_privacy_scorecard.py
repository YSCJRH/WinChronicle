import re
import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCORECARD = ROOT / "harness" / "scorecards" / "phase6-privacy-enrichment.md"
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
