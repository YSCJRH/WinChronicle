# Phase 6 Privacy Enrichment Scorecard

This is a tests-first planning scorecard. It does not authorize implementing
screenshot or OCR capture in v0.1.

- Screenshots and OCR must remain disabled by default.
- Screenshot/OCR enrichment must require explicit opt-in configuration.
- Enrichment must require a per-app allowlist; no global default allowlist.
- Raw screenshot cache must have a short TTL and a clear command or documented
  procedure for deletion before implementation is accepted.
- OCR-derived text must pass through the same redaction, denylist, schema,
  storage, memory, and MCP trust-boundary pipeline as UIA text.
- MCP must not expose raw screenshots by default.
- Privacy regression tests must cover password fields, API keys, private keys,
  JWTs, GitHub tokens, Slack tokens, denylisted apps, lock screen captures, and
  prompt-injection trust boundaries before any screenshot/OCR code is added.
- Screenshot/OCR work must not introduce audio, keyboard capture, clipboard
  capture, network upload, LLM calls, or desktop control.
