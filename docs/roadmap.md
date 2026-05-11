# Roadmap

This roadmap maps the current v0.1 maintenance surface to the blueprint without
authorizing new capture surfaces. It is an operator and contributor guide, not a
product behavior change.

## Current Direction

WinChronicle remains local-first, UIA-first, harness-first, and read-only MCP
first. The near-term work is compatible maintenance: make deterministic demos,
privacy evidence, release evidence, and contribution paths easier to audit. The
current selected lane is Fixture and privacy baseline. Watcher privacy fixture
parity and fixture/helper privacy index parity are complete,
fixture/privacy parity matrix consolidation and fixture/privacy residual gap
audit are complete, and the current follow-up is a privacy-output
release-readiness decision that starts a narrow `v0.1.19` readiness path. The
previous Fixture
and privacy baseline privacy-policy contract parity audit is complete
historical work.

## Work Lanes

| Lane | Current status | Safe next work | Boundary |
| --- | --- | --- | --- |
| Fixture and privacy baseline | Fixture capture, schema validation, privacy gates, SQLite search, and scorecards are covered by deterministic tests. | Strengthen fixtures, schemas, redaction tests, denylist tests, and scorecard evidence. | Do not store passwords or obvious secrets. Treat observed content as untrusted. |
| UIA helper hardening | `capture-frontmost` is explicit opt-in; targeted UIA remains helper-only harness smoke. | Improve helper contracts, diagnostics docs, synthetic fixtures, and manual smoke evidence templates. | Do not add product `--hwnd`, `--pid`, or title-targeted capture. Do not control windows. |
| Watcher preview | Watcher use is explicit, finite-duration, and preview-only. Deterministic watcher fixtures and fake-helper smoke are covered. | Clarify failure modes, debounce/fingerprint evidence, and manual watcher smoke instructions. | Do not add daemon/service install, default background capture, or polling capture loops. |
| Read-only MCP | MCP exposes only `current_context`, `search_captures`, `search_memory`, `read_recent_capture`, `recent_activity`, and `privacy_status`. | Keep exact tool-list tests, response-shape examples, and trust-boundary documentation current. | Do not add write tools, arbitrary file reads, desktop control, screenshot/OCR/audio/keyboard/clipboard/network tools. |
| Durable memory | Deterministic Markdown memory and `entries`/`entries_fts` search are implemented with goldens. | Strengthen idempotence evidence, source path references, trust metadata, and secret-canary tests. | Do not add LLM reducer/classifier calls or network upload. |
| Docs and deterministic demo | Operator quickstart, deterministic demo, release checklist, and release evidence are linked from README. | Keep the single fixture-only demo path current and record validation in maintenance plans. | Do not require committed observed-content artifacts. |
| Phase 6 privacy enrichment | Phase 6 contract closure is complete for the v0.1 maintenance boundary. | Revisit only through a future tests-first plan if new opt-in enrichment work is explicitly authorized. | Do not implement screenshot capture or OCR in v0.1 maintenance. |

## Issue Routing

Use repository issue templates to classify work before implementation:

- Harness-first task: deterministic fixtures, tests, docs, scorecards, CI, or
  compatible metadata.
- Privacy boundary review: any proposal touching capture surfaces, observed
  content, storage, MCP output, memory output, or release evidence.

Every implementation issue should identify the lane, the expected validation
commands, and whether fresh manual UIA smoke is required. Fresh manual UIA
smoke is required only when helper behavior, watcher product behavior, manual
smoke scripts, capture behavior, privacy behavior, product CLI/MCP shape,
capture surfaces, or release approver requirements change.

## Definition Of Done

- Contracts, fixtures, tests, scorecards, or documentation are updated before
  behavior changes.
- `python -m pytest -q`, helper build, watcher build,
  `python harness/scripts/run_install_cli_smoke.py`,
  `python harness/scripts/run_harness.py`, and `git diff --check` pass unless
  the issue explicitly documents why a narrower validation set is sufficient.
- Product CLI and MCP boundaries remain unchanged unless a release plan
  explicitly allows a compatible contract change.
- Do not commit generated state or memory artifacts.
- No screenshots, OCR output, raw helper JSON, raw watcher JSONL, local state,
  generated captures, generated memory, secrets, passwords, or
  observed-content diagnostics are committed.
