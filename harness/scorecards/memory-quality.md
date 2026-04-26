# Memory Quality Scorecard

Phase 5 memory acceptance criteria:

- Memory generation is deterministic and uses existing redacted captures only.
- `generate-memory` writes inspectable Markdown entries under `memory/`.
- Event entries are named `event-YYYY-MM-DD.md`.
- Markdown entries include source capture paths, app names, time range, and
  `trust: untrusted_observed_content`.
- SQLite creates `entries` and, when FTS5 is available, `entries_fts`.
- `search-memory` searches durable entries without changing raw
  `search-captures` behavior.
- Memory generation must not call LLMs, use network access, read screenshots,
  OCR, audio, keyboard capture, clipboard capture, or desktop control.
- Markdown must not contain unredacted API key, private key, JWT, GitHub token,
  Slack token, or token canaries.
