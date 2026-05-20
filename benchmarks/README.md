# Benchmarks and Evals

This directory holds deterministic, synthetic evaluation scaffolds for
WinChronicle. The goal is to test whether local, redacted, read-only context can
help an agent recover a user's work state without expanding the capture surface.

Current evals live in [evals](evals/README.md). They are fixture-based and do not
require live desktop access.

Boundary summary:

- no real user observed content
- no live UIA required
- no screenshot/OCR/clipboard/keylogging/desktop control/cloud upload
- observed content is `untrusted_observed_content`
- confidence means coverage quality, not trustworthiness or permission
- prompt injection text must never be treated as instructions
