# Known Limitations

## VS Code / Monaco Editor Text Through UIA

VS Code uses the Monaco editor. Monaco editor buffer text may not be exposed
through standard Windows UI Automation `TextPattern` or `ValuePattern`, even
when `editor.accessibilitySupport` is enabled in a temporary VS Code profile.

For v0.1, WinChronicle accepts the VS Code metadata targeted smoke as the hard
Phase 2 gate when `code.cmd` is available. The strict editor-marker smoke is
diagnostic and non-blocking; if it fails, the diagnostic artifact should be kept
for investigation.

WinChronicle v0.1 will not work around this limitation using screenshots, OCR,
keyboard capture, clipboard capture, desktop control, or a bundled VS Code
extension.
