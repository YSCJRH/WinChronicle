# Watcher Privacy Fixture Parity After v0.1.18

This record starts the Fixture and privacy baseline lane selected by
`docs/next-blueprint-lane-selection-post-v0.1.18.md`.

## Scope

The task adds deterministic watcher JSONL coverage for the existing watcher
dispatch path. It does not authorize live UIA capture changes, screenshot/OCR
implementation, helper/watcher behavior changes, CLI output shape changes,
MCP output changes, schema expansion, version changes, daemon/service install,
default background capture, polling loops, clipboard capture, keyboard capture,
audio recording, desktop control, network/cloud upload, or LLM calls.

## Fixture

The focused tests generate deterministic watcher JSONL under `tmp_path` from
the existing synthetic privacy fixtures in `harness/fixtures/privacy`. This
avoids committing a second raw watcher JSONL stream with password and token
canaries while still exercising:

- password-field redaction,
- obvious API key, private key, JWT, GitHub token, Slack token, and canary
  redaction,
- prompt-injection text stored only as untrusted observed content,
- denylisted app skipping before storage and indexing,
- heartbeat counting without capture writes.

The generated watcher JSONL is temporary test input only. It is not committed,
copied into `WINCHRONICLE_HOME`, release notes, manual smoke evidence,
generated captures, generated memory, or runtime state.

## Acceptance

Watcher privacy fixture parity is complete when deterministic tests prove:

- watcher-dispatched captures preserve normalized redaction markers and
  `redactions` metadata before capture storage and SQLite indexing,
- denylisted watcher events increment `denylisted_skipped` and leave no
  capture artifact or searchable observed content,
- watcher-dispatched prompt-injection text remains searchable only with
  `trust = "untrusted_observed_content"`,
- generated memory from watcher captures preserves the untrusted boundary,
- raw password values, token canaries, private key text, JWT text, and
  denylisted observed text are absent from capture files, memory files,
  capture search, memory search, and MCP memory search,
- raw watcher JSONL is not persisted under `WINCHRONICLE_HOME`, including when
  `watch --watcher` consumes watcher stdout.

## Validation

Local validation for this parity record:

```powershell
python -m pytest tests/test_watcher_events.py tests/test_privacy_check.py tests/test_redaction.py -q
python -m pytest tests/test_compatibility_evidence_docs.py tests/test_operator_diagnostics_docs.py tests/test_version_identity.py -q
python -m pytest -q
git diff --check
git diff --name-only v0.1.18..HEAD -- pyproject.toml src\winchronicle\_version.py src\winchronicle\mcp\server.py resources
python harness/scripts/run_harness.py
```

Result: passed locally before PR review. Focused watcher/privacy/redaction
validation reported 31 tests, focused docs/version validation reported
93 tests, full pytest reported 218 tests, `git diff --check` passed, the
version/MCP/resources product diff printed no files, the stale AH7/old
committed watcher privacy fixture wording scan returned no matches, and the
full deterministic harness passed, including 218 pytest tests, helper/watcher
builds with 0 warnings and 0 errors, watcher smoke, MCP smoke, install CLI
smoke, privacy check, fixture capture/search/memory, deterministic watcher
fixture, and watcher fake-helper smoke.

## Privacy And Security

This task strengthens deterministic privacy evidence for the watcher preview
path. It reuses existing synthetic harness canaries from `harness/fixtures`
through temporary watcher JSONL so tests can prove redaction and non-indexing.
It does not add a new capture surface, does not persist raw watcher streams
under local state, and does not commit generated captures, generated memory,
screenshots, OCR output, or live observed content.
