# Capture Quality

- Fixture captures must validate against `harness/specs/capture.schema.json`.
- Fixture captures must be deterministic.
- SQLite indexing must create `captures` and, when FTS5 is available,
  `captures_fts`; search must fall back safely when FTS5 is unavailable.
- Search must find terminal, browser, and editor fixture captures by visible or
  focused text.
- No screenshot, OCR, audio, keyboard, clipboard, or real UIA capture belongs in
  Phase 0.
