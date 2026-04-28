# MCP Quality Scorecard

Phase 4 MCP acceptance criteria:

- MCP is read-only and exposes no desktop control, click, type, keyboard,
  clipboard, screenshot, OCR, audio, or network tools.
- The stdio surface supports `initialize`, `tools/list`, and `tools/call` for:
  `current_context`, `search_captures`, `search_memory`, `read_recent_capture`,
  `recent_activity`, and `privacy_status`.
- Observed content returned through MCP includes
  `trust = "untrusted_observed_content"` and an instruction not to follow
  instructions found in observed screen content.
- `search_captures` reads from the same SQLite capture index as the CLI search
  path and preserves the CLI result fields inside each MCP match.
- `search_memory` reads from the same SQLite memory index as the CLI
  `search-memory` path and returns only deterministic entry metadata,
  snippets, paths, and the observed-content trust boundary.
- `privacy_status` reports the same disabled privacy surfaces as CLI
  `status`: screenshots, OCR, audio, keyboard capture, clipboard capture,
  network upload, cloud upload, LLM calls, desktop control, product targeted
  capture, and MCP write tools.
- The MCP smoke uses deterministic fixture captures and does not start real UIA
  capture, screenshots, OCR, audio, keyboard capture, clipboard capture,
  network calls, or desktop control.
- MCP compatibility examples must cover every exposed read-only tool, show
  `trust = "untrusted_observed_content"`, and must not document write tools,
  arbitrary file reads, desktop control, screenshots, OCR, audio, keyboard,
  clipboard, or network tools.
