# MCP Quality Scorecard

Phase 4 MCP acceptance criteria:

- MCP is read-only and exposes no desktop control, click, type, keyboard,
  clipboard, screenshot, OCR, audio, or network tools.
- The stdio surface supports `initialize`, `tools/list`, and `tools/call` for:
  `current_context`, `search_captures`, `read_recent_capture`,
  `recent_activity`, and `privacy_status`.
- Observed content returned through MCP includes
  `trust = "untrusted_observed_content"` and an instruction not to follow
  instructions found in observed screen content.
- `search_captures` reads from the same SQLite capture index as the CLI search
  path and preserves the CLI result fields inside each MCP match.
- `privacy_status` reports screenshots, OCR, audio, keyboard capture,
  clipboard capture, cloud upload, and desktop control as disabled.
- The MCP smoke uses deterministic fixture captures and does not start real UIA
  capture, screenshots, OCR, audio, keyboard capture, clipboard capture,
  network calls, or desktop control.
