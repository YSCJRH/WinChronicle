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
- Phase 6 screenshot/OCR work is not accepted until opt-in configuration,
  per-app allowlist, short-TTL raw cache behavior, and privacy regression tests
  are specified before implementation.
- Phase 6 preflight contract artifacts under `harness/specs` and
  `harness/fixtures/phase6` are specification-only. They are not runtime
  configuration and must not be read by product code in v0.1.
- `harness/specs/privacy-policy.md` must match the implemented denylist,
  redaction, and trust-boundary behavior.
