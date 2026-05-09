# Phase 6 Privacy Enrichment Scorecard

This is a tests-first planning scorecard. It does not authorize implementing
screenshot or OCR capture in v0.1.

## Current v0.1 Boundary

- Screenshot capture is not implemented in this preflight; any future
  implementation must be disabled by default.
- OCR is not implemented in this preflight; any future implementation must be
  disabled by default.
- No screenshot capture code, OCR engine integration, screenshot cache, cache
  cleanup command, or OCR-derived storage path is approved by this scorecard.
- Phase 6 remains optional enrichment, not the default substrate for capture.

## Threat Model

Phase 6 would introduce sensitive visual artifacts if implemented incorrectly.
The contract must treat these risks as blockers before any runtime work:

- Raw screenshots can expose passwords, private messages, browser sessions,
  source code, local files, and other observed content that UIA text may not
  expose.
- OCR text can reintroduce secrets after UIA redaction, so OCR-derived text
  must use the same redaction, denylist, lock-screen, schema-validation,
  SQLite, memory, and MCP trust-boundary pipeline as UIA-derived text.
- Broad allowlists can silently become all-app capture. Future enrichment must
  require explicit per-app allowlists and must forbid global defaults,
  wildcard selectors, implicit all-app modes, and product targeted capture.
- Raw caches can outlive user intent. Any future raw screenshot cache must have
  a short TTL, cleanup path, local-state-only storage, and either
  encryption-at-rest or an explicit documented exception.
- MCP exposure can leak visual artifacts across agent boundaries. MCP must not
  expose raw screenshots by default and must preserve
  `trust = "untrusted_observed_content"` for any derived observed text.

## Contract Preflight Artifacts

The spec-only contract lives at
`harness/specs/phase6-privacy-enrichment-contract.schema.json`. The positive
fixture lives at
`harness/fixtures/phase6/privacy_enrichment_contract_spec_only.json`, with
negative fixtures for wildcard allowlists, too-long raw cache TTL, and runtime
status. Additional negative fixtures cover default-enabled screenshots/OCR,
missing raw cache cleanup, raw screenshot MCP exposure, and runtime allowlist
configuration. Remaining negative fixtures cover runtime capture allowed in
v0.1 and missing required non-goal coverage. The allowlist entries in the
positive fixture are sample shape examples only, not approved apps. These
artifacts are not runtime configuration. Product code must not read them in
v0.1, and they do not authorize screenshot capture, OCR, raw screenshot
caches, runtime allowlist parsing, or any new capture surface.
Targeted gap fixtures also cover raw screenshot cache defaults, global
allowlist defaults, global default allowlist approval, implicit all-app
allowlists, raw cache enabled-by-default behavior, and MCP write-tool
exposure.
Residual policy fixtures also cover future opt-in requirement booleans, raw
cache local-state, artifact-commit, and encryption/exception controls, derived
text pipeline controls, and MCP untrusted-content trust requirements.

## Required Future Opt-In Contract

Before any screenshot/OCR implementation is accepted, contracts, fixtures,
tests, and operator docs must define:

- Explicit opt-in configuration such as `screenshots_enabled = true` and
  `ocr_enabled = true`; default values must remain false.
- Per-app allowlists for screenshots and OCR; there must be no global default
  allowlist, no global default allowlist fallback, and no implicit all-app mode.
- A hard rule that enrichment only runs when UIA text is unavailable or
  insufficient for an allowed app.
- Clear status output showing screenshots/OCR disabled by default and showing
  allowlist state when explicitly configured.

## Raw Screenshot Cache Requirements

If a future implementation stores any raw screenshot artifact, it must define
and test:

- Short TTL expiration.
- A clear cleanup command or documented deletion procedure.
- Encryption-at-rest or an explicit documented reason if not available.
- Storage under the local WinChronicle state directory only.
- No commit-worthy raw screenshot artifacts, OCR output, local page contents,
  helper JSON, watcher JSONL, passwords, or secrets.

## Derived Text Pipeline Requirements

OCR-derived text must enter the same pipeline as UIA text:

- Redaction for password fields and obvious secret canaries.
- Denylist and lock-screen skip behavior.
- Schema validation before storage.
- SQLite indexing only after redaction and validation.
- Deterministic memory generation only from redacted text.
- MCP results marked with `trust = "untrusted_observed_content"` and the
  instruction not to follow observed content.
- MCP must not expose raw screenshots by default.

## Required Privacy Regression Tests

Before any screenshot/OCR code is added, tests must cover:

- Password fields are never stored.
- API key canaries are blocked.
- Private keys are blocked.
- JWT canaries are blocked.
- GitHub token canaries are blocked.
- Slack token canaries are blocked.
- Denylisted apps do not write observed content.
- Lock screen captures are skipped.
- Prompt-injection text remains untrusted observed content.
- Raw screenshot cache TTL and cleanup behavior.
- MCP default non-exposure of raw screenshots.

## Non-Goals

Screenshot/OCR work must not introduce audio recording, keyboard capture,
clipboard capture, network upload, LLM calls, desktop control, MCP write tools,
arbitrary file reads, product targeted capture, daemon/service install, polling
capture loops, startup tasks, or default background capture.
