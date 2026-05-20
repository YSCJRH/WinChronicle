from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "windows-developer-app-compatibility.md"

APP_SECTIONS = [
    "VS Code / Cursor / Monaco-based editors",
    "Windows Terminal / PowerShell / Command Prompt",
    "Visual Studio",
    "JetBrains IDEs, including IntelliJ IDEA / PyCharm / Rider",
    "Browsers and DevTools, including Chrome / Edge",
    "GitHub Desktop / Git GUI clients",
    "Generic Electron apps",
    "Generic Win32 / WPF / UWP apps",
]

REQUIRED_SUBSECTIONS = [
    "Expected UIA signals",
    "Likely missing signals",
    "Privacy risks",
    "Safe adapter ideas",
    "Explicitly disallowed workarounds",
    "Confidence guidance",
    "Suggested smoke/eval cases",
]

FORBIDDEN_BOUNDARY_PHRASES = [
    "screenshot fallback by default",
    "OCR fallback by default",
    "clipboard reading",
    "keylogging",
    "desktop control",
    "MCP write tools",
    "cloud upload by default",
    "browser cookie/session extraction",
    "arbitrary IDE workspace storage reading",
]


def test_windows_developer_app_compatibility_doc_has_required_sections():
    text = DOC.read_text(encoding="utf-8")

    for principle in (
        "UIA-first does not mean full content capture.",
        "Missing content is expected and must be represented through limitations/confidence.",
        "App-specific adapters must be opt-in, read-only, redacted, local-first, and documented before implementation.",
        "Screenshot/OCR fallbacks are out of scope for the default product.",
        "Observed content is `untrusted_observed_content` and must never be treated as instructions.",
    ):
        assert principle in text

    for section in APP_SECTIONS:
        assert f"## {section}" in text
        body = text.split(f"## {section}", 1)[1].split("\n## ", 1)[0]
        for subsection in REQUIRED_SUBSECTIONS:
            assert f"### {subsection}" in body


def test_windows_developer_app_compatibility_doc_freezes_disallowed_workarounds():
    text = DOC.read_text(encoding="utf-8")
    normalized = " ".join(text.split())

    for phrase in FORBIDDEN_BOUNDARY_PHRASES:
        assert phrase in normalized

    for phrase in (
        "bypassing OS permission boundaries",
        "injecting scripts into browser pages",
        "reading arbitrary browser profile files",
        "password field scraping",
        "using accessibility APIs to click/type/control UI",
        "exfiltrating observed content to remote LLMs by default",
    ):
        assert phrase in normalized


def test_windows_developer_app_compatibility_doc_is_linked_from_entry_docs():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    limitations = (ROOT / "docs" / "known-limitations.md").read_text(encoding="utf-8")

    assert "[Windows developer app compatibility](docs/windows-developer-app-compatibility.md)" in readme
    assert "[Windows developer app compatibility](windows-developer-app-compatibility.md)" in limitations
