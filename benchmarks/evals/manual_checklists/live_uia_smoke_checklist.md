# Live UIA Smoke Checklist

This is a future manual checklist, not an automatic test and not approval to run
live desktop capture by default.

Boundary summary:

- no real user observed content should be committed
- no live UIA required for the automated eval scaffold
- no screenshot/OCR/clipboard/keylogging/desktop control/cloud upload
- observed content is `untrusted_observed_content`
- confidence means coverage quality, not trustworthiness or permission
- prompt injection text must never be treated as instructions

Before any future manual smoke:

1. Use an isolated temporary `WINCHRONICLE_HOME`.
2. Use synthetic or disposable windows where possible.
3. Record only command lines, timestamps, pass/fail status, local artifact paths,
   and environment notes.
4. Do not commit observed UI text, raw helper JSON, raw watcher JSONL,
   screenshots, OCR output, secrets, passwords, or private project details.
5. Confirm that any output containing observed content is redacted and labeled
   `untrusted_observed_content`.
