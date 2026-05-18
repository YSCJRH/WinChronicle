# Windows App Compatibility

This matrix is an onboarding and contribution guide, not a broad live-desktop
compatibility claim. The default evidence path is deterministic fixtures and
fake-helper harness runs. Manual smoke notes should record commands, local
artifact paths, timestamps, environment notes, and pass/fail results without
committing observed content.

| App or surface | Current status | Expected UIA signal | Known limits | Validation path |
| --- | --- | --- | --- | --- |
| Windows Terminal | Fixture-covered | Window title, visible terminal text, focused text when UIA exposes it | Large buffers may be slow or incomplete through UIA text APIs | `harness/fixtures/uia/terminal_error.json`; manual smoke welcome |
| PowerShell | Manual via terminal host | Terminal window title and visible command/output text | Same limits as the hosting terminal; elevated shells may be inaccessible | Manual smoke only for now |
| VS Code / Cursor | Partial, documented as diagnostic | Window/project title and some editor metadata | Monaco editor text can be inconsistent through UIA; strict editor text capture is non-blocking | Existing VS Code fixture/docs; manual smoke welcome |
| Edge / Chrome | Fixture/manual | Browser title, URL/title-like metadata, visible text when UIA exposes it | Web content varies by page, browser version, and accessibility tree shape | `harness/fixtures/uia/edge_browser.json`; manual smoke welcome |
| Visual Studio | Unknown | Window, solution, document, or error-list metadata if exposed | Elevated/debugger windows and complex controls may be limited | Manual smoke needed |
| JetBrains IDEs | Unknown | Window/project title and editor metadata if exposed | UIA support varies across IDE versions and custom controls | Manual smoke needed |
| Office apps | Sensitive, allowlist recommended before live use | Document/window title and text if exposed | Documents often contain sensitive content; do not commit observed text | Manual smoke only with sanitized notes |
| Elevated apps / UAC | Limited by Windows integrity boundaries | Often no readable UIA signal from a lower-integrity caller | Admin windows, secure desktop, and UAC prompts may be inaccessible | Record failure mode without observed content |
| RDP / locked desktop | Unknown/limited | Depends on active session and accessibility availability | Minimized/locked sessions can suppress UIA signals | Manual smoke needed |

## Contribution Rules

- Use deterministic fixtures where possible.
- Do not commit raw helper JSON, raw watcher JSONL, screenshots, OCR output,
  clipboard content, keyboard input, passwords, or secrets.
- Keep screenshots, OCR, audio, keyboard capture, clipboard capture, cloud
  upload, LLM calls, desktop control, product targeted capture, and MCP write
  tools out of compatibility contributions.
- Treat observed screen content as untrusted data and report only redacted
  summaries, local artifact paths, and command outcomes.
