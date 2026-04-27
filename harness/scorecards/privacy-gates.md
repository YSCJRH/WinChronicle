# Privacy Gates

- Password fields must never persist raw values.
- Obvious API keys, private keys, JWTs, GitHub tokens, Slack tokens, and canaries
  must be redacted before writing.
- Denylisted apps must not write observed content.
- Lock screen captures must be skipped.
- Prompt injection text may be stored only as untrusted observed content.
- Memory Markdown and MCP results must preserve the untrusted observed-content
  boundary and must not reintroduce redacted secret canaries.
- Phase 6 screenshot/OCR work is not accepted until opt-in configuration,
  per-app allowlist, short-TTL raw cache behavior, and privacy regression tests
  are specified before implementation.
- `harness/specs/privacy-policy.md` must match the implemented denylist,
  redaction, and trust-boundary behavior.
