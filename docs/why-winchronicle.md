# Why WinChronicle

AI agents need local work context to be useful on real developer machines. On
Windows, that context is often trapped inside GUI applications, browser tabs,
terminals, editors, installers, and system dialogs. WinChronicle is a local
memory layer for that environment.

## Product Thesis

Windows agents need memory, but memory should not require default screen
recording, keylogging, clipboard capture, cloud upload, or desktop control.

WinChronicle uses Microsoft UI Automation as the first signal source because it
can expose structured UI context without treating the screen as an image stream.
The project stores that context locally, runs it through deterministic privacy
and redaction gates, indexes it for search, and exposes read-only MCP context to
tool-capable agents.

## What Makes It Different

- Windows-first: built around Microsoft UI Automation rather than macOS
  Accessibility APIs or browser-only instrumentation.
- Local-first: state lives on the user's machine unless a future product phase
  explicitly adds another storage option.
- Harness-first: fixtures, schemas, privacy gates, and deterministic tests are
  part of the product shape, not afterthoughts.
- Read-only MCP first: agents can inspect context, but v0.2 does not expose
  click, type, clipboard, file-write, network, screenshot, OCR, audio, or
  desktop-control tools.
- Privacy boundary first: observed UI text remains untrusted data and carries
  explicit trust metadata.

## Current Use Cases

- Reproduce a local workflow from deterministic UIA fixtures.
- Search recent redacted UI captures with SQLite-backed queries.
- Generate deterministic Markdown memory from already-redacted captures.
- Run a finite monitor session and inspect the resulting local timeline.
- Let an agent read recent local activity through read-only MCP tools.

## Near-Term Product Direction

The most attractive next step is not a broader capture surface. It is a better
human-facing loop around the current safe baseline:

- clearer session summaries,
- better timeline compression,
- app and topic grouping,
- useful local reports,
- improved MCP context for agents,
- compatibility notes for common Windows developer tools.

Any runtime expansion, background capture, LLM summarization, screenshot/OCR
path, or write-capable MCP surface still requires explicit human product
approval.
