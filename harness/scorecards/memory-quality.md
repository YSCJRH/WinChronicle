# Memory Quality Scorecard

Phase 5 memory acceptance criteria:

- Memory generation is deterministic and uses existing redacted captures only.
- `generate-memory` writes inspectable Markdown entries under `memory/`.
- Event entries are named `event-YYYY-MM-DD.md`.
- Project entries are named `project-*.md` and are built from deterministic
  local title/URL hints, not LLM classification.
- Tool entries are named `tool-*.md` and group captures by app name.
- Markdown entries include source capture paths, app names, time range, and
  `trust: untrusted_observed_content`.
- Memory generation must be idempotent: rerunning the reducer over the same
  captures must leave the same Markdown bodies and entry count.
- Event Markdown must have golden fixture coverage for the terminal, editor,
  and browser deterministic timeline.
- Memory generation must have manifest golden coverage for entry ordering,
  entry types, titles, time ranges, paths, and capture counts.
- SQLite creates `entries` and, when FTS5 is available, `entries_fts`.
- `search-memory` searches durable entries without changing raw
  `search-captures` behavior.
- MCP `search_memory` must match CLI memory search semantics and remain
  read-only.
- Memory generation must not call LLMs, use network access, read screenshots,
  OCR, audio, keyboard capture, clipboard capture, or desktop control.
- Markdown must not contain unredacted API key, private key, JWT, GitHub token,
  Slack token, or token canaries.
