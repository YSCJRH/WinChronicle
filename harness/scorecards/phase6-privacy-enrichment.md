# Phase 6 Privacy Enrichment Scorecard

This is a tests-first planning scorecard. It does not authorize implementing
screenshot or OCR capture in v0.1.

## Current v0.1 Boundary

- Screenshot capture is absent or disabled by default.
- OCR is absent or disabled by default.
- No screenshot capture code, OCR engine integration, screenshot cache, cache
  cleanup command, or OCR-derived storage path is approved by this scorecard.
- Phase 6 remains optional enrichment, not the default substrate for capture.

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
