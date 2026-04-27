# Capture Quality

- Fixture captures must validate against `harness/specs/capture.schema.json`.
- Fixture captures must be deterministic.
- SQLite indexing must create `captures` and, when FTS5 is available,
  `captures_fts`; search must fall back safely when FTS5 is unavailable.
- CLI and harness smoke tests must find terminal, browser, and editor fixture
  captures by visible or focused text, returning only `timestamp`, `app_name`,
  `title`, `snippet`, and `path`.
- UIA helper work must start with a JSON output contract and helper-like
  fixtures; the contract must keep screenshots, OCR, audio, keyboard,
  clipboard, and desktop control disabled and bounded.
- UIA helper tree extraction may use UIA raw view to surface editor/browser
  text, but depth, node count, and text length limits must remain enforced.
- Helper targeted capture is harness-only: it must require both `--harness`
  and `WINCHRONICLE_HARNESS=1`, write only stdout/artifacts, and must not
  activate, click, type, move, resize, or control windows.
- Phase 2 targeted smoke release gates:
  - Notepad targeted smoke is a hard gate and must capture its text marker.
  - Edge targeted smoke is a hard gate and must capture its local HTML body
    marker; URL extraction is best-effort.
  - VS Code metadata smoke is a hard gate when `code.cmd` is available.
  - VS Code strict Monaco editor marker capture is diagnostic and
    non-blocking; strict failure must produce a diagnostic artifact.
- Real foreground capture must be explicit opt-in through `capture-frontmost`
  with a caller-provided helper path; tests use fake-helper output by default.
- Manual UIA helper smoke scripts must use temporary state and must not print
  observed content.
- Watcher work must start with deterministic JSONL event fixtures; `watch
  --events` must dedupe repeated captures, count heartbeats, and skip
  denylisted apps without starting a real WinEvent hook.
- The experimental WinEvent watcher scaffold may be compiled in harness, but
  live watcher runs must remain manual and temporary-state only.
- Watcher smoke may run with `--capture-on-start` only when using a fake helper
  and temporary state, so no live observed UI content is read.
- `watch --watcher` must consume watcher JSONL in memory and must not save raw
  event streams by default.
- No screenshot, OCR, audio, keyboard, clipboard, or real UIA capture belongs in
  Phase 0.
