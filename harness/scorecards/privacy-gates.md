# Privacy Gates

- Password fields must never persist raw values.
- Obvious API keys, private keys, JWTs, GitHub tokens, Slack tokens, and canaries
  must be redacted before writing.
- Denylisted apps must not write observed content.
- Prompt injection text may be stored only as untrusted observed content.
- `harness/specs/privacy-policy.md` must match the implemented denylist,
  redaction, and trust-boundary behavior.
