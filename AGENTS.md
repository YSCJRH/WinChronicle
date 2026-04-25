# AGENTS.md - WinChronicle Project Pact

WinChronicle is a Windows-first, UIA-first, local memory layer for tool-capable
agents.

## Non-negotiable principles

- Local-first.
- UIA-first.
- Harness-first.
- Read-only MCP first.
- Screenshots off by default.
- OCR off by default.
- No audio recording.
- No keylogging.
- No clipboard capture in v0.1.
- No cloud upload of captured content unless explicitly configured in a future
  phase.
- No desktop control tools in v0.1.
- Never store password fields.
- Never store obvious secrets such as API keys, private keys, JWTs, GitHub
  tokens, Slack tokens, or token canaries.
- Treat observed screen content as untrusted data.
- Do not implement screenshot/OCR in the first pass.
- Do not implement real UIA capture in the first pass.
- Do not implement LLM reducer/classifier in the first pass; deterministic
  placeholders are acceptable.

## Development mode

This is a harness-first project. Before implementing behavior, add or update:

1. contracts / schemas,
2. fixtures,
3. tests,
4. scorecards or documentation.

## Required report format for each Codex task

At the end of every task, report exactly:

- What changed
- Tests run
- Tests not run and why
- Privacy/security implications
- Next smallest implementation task

Do not claim success unless relevant tests were run or you clearly state why
they could not run.
