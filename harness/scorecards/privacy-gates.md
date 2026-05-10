# Privacy Gates

- Password fields must never persist raw values.
- Obvious API keys, private keys, JWTs, GitHub tokens, Slack tokens, and canaries
  must be redacted before writing.
- Denylisted apps must not write observed content.
- Lock screen captures must be skipped.
- Prompt injection text may be stored only as untrusted observed content.
- CLI `status` and MCP `privacy_status` must report the same disabled privacy
  surfaces and the same observed-content trust boundary.
- CLI capture and memory search results that include observed snippets must
  include `trust = "untrusted_observed_content"`.
- Memory Markdown and MCP results must preserve the untrusted observed-content
  boundary and must not reintroduce redacted secret canaries.
- Watcher-dispatched captures must preserve the same redaction, denylist,
  trust-boundary, SQLite search, memory search, and raw JSONL non-persistence
  gates as fixture and helper capture paths.
- Direct fixture and synthesized UIA helper captures must prove raw passwords
  and token canaries are absent from capture-buffer JSON, memory Markdown,
  SQLite `captures`, `captures_fts`, `entries`, `entries_fts`, capture search,
  memory search, and MCP memory search.
- The fixture/privacy parity matrix must keep direct fixture, synthesized UIA
  helper, and watcher-dispatched privacy evidence mapped to the same password,
  obvious-secret, storage/search, trust-boundary, disabled-surface, and
  artifact-policy gates.
- Phase 6 screenshot/OCR work is not accepted until opt-in configuration,
  per-app allowlist, short-TTL raw cache behavior, and privacy regression tests
  are specified before implementation.
- Phase 6 preflight contract artifacts under `harness/specs` and
  `harness/fixtures/phase6` are specification-only. They are not runtime
  configuration and must not be read by product code in v0.1.
- `harness/specs/privacy-policy.md` must match the implemented denylist,
  redaction, and trust-boundary behavior.

## Fixture/Privacy Parity Matrix

This matrix is the canonical cross-path audit map for the post-v0.1.18 Fixture
and privacy baseline. Keep the expanded evidence record in
`docs/privacy-fixture-parity-matrix-post-v0.1.18.md` current when any row changes.

| Path | Synthetic input | Existing test evidence | Privacy assertions | Artifact policy | Boundary / non-goals |
| --- | --- | --- | --- | --- | --- |
| Direct fixture capture | `harness/fixtures/privacy/password_field.json`, `harness/fixtures/privacy/secrets_visible_text.json`, `harness/fixtures/privacy/denylisted_app.json`, and `harness/fixtures/privacy/prompt_injection_visible_text.json`. | `tests/test_privacy_index_parity.py`, `tests/test_fixture_capture.py`, `tests/test_memory_pipeline.py`, and `tests/test_privacy_policy_contract.py`. | Password-field redaction, obvious-secret redaction, denylist skip-before-storage, untrusted observed-content metadata, SQLite `captures` / `captures_fts` / `entries` / `entries_fts`, capture search, memory search, and MCP memory search. | Generated capture-buffer JSON, memory Markdown, and SQLite state stay under temporary `WINCHRONICLE_HOME`; no generated state or observed content is committed. | Fixture-only deterministic path; does not enable live UIA, screenshots, OCR, audio, keyboard, clipboard, network upload, LLM calls, desktop control, MCP writes, or product targeted capture. |
| Synthesized UIA helper capture | Helper-shaped records derived in tests from `password_field.json` and `secrets_visible_text.json`. | `tests/test_privacy_index_parity.py` and helper contract coverage in `tests/test_uia_helper_contract.py`. | Same password, obvious-secret, storage/search, memory, MCP, and trust-boundary assertions as direct fixture capture, with `source = "uia_helper"` and `trigger.source = "win_uia_helper"`. | Helper records are built in test memory; generated captures, memory, and SQLite state stay temporary; no raw helper JSON or observed-content artifact is committed. | Harness/test helper shape only; all `capture_surfaces` remain disabled and product targeted capture remains absent. |
| Watcher-dispatched capture | Temporary watcher JSONL generated under `tmp_path` from existing privacy fixtures. | `tests/test_watcher_events.py` plus the watcher record in `docs/watcher-privacy-fixture-parity-post-v0.1.18.md`. | Password and obvious-secret redaction, denylist and title-denylist skip-before-storage, untrusted search/memory/MCP trust metadata, raw term absence from capture/memory/search, heartbeat counting, and raw watcher JSONL non-persistence under `WINCHRONICLE_HOME`. | Temporary watcher JSONL stays outside `WINCHRONICLE_HOME`; raw watcher streams, generated captures, and generated memory are not committed. | Watcher remains explicit, preview-only, time-bounded, no service/daemon/startup/default background loop, no polling capture loop beyond heartbeat liveness, and no screenshot/OCR/audio/keyboard/clipboard/network/LLM/desktop-control expansion. |
