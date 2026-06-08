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

## Productization review gates

Productization PRs must stay inside their declared phase scope. Reviewers should
treat any default capture-surface expansion as a P1 blocker. This includes
screenshots, OCR, keyboard logging, clipboard capture, audio recording, cloud
upload, desktop control, background daemons/services, infinite polling, MCP
write tools, arbitrary file reads, network upload, or product-targeted capture
behavior.

Observed UI or screen content remains `untrusted_observed_content`. Redaction
must happen before storage, search, memory generation, reports, or MCP exposure.
Productization changes may improve README, docs, release automation, assets,
examples, and onboarding, but they must not imply affiliation with OpenAI or
promise parity with official Chronicle behavior.

Reviewer expectations:

- Privacy Boundary Reviewer: fail if the PR expands capture surfaces, weakens
  redaction, changes MCP from read-only, or stores observed content in docs,
  tests, examples, or assets.
- Product Clarity Reviewer: fail if the PR overclaims current product ability,
  buries the Windows/local/read-only positioning, or makes first-run guidance
  harder for a new Windows user.
- Release Gate Reviewer: fail if required local validation is missing, phase
  scope is unclear, release notes overclaim, or generated/local artifacts are
  committed.

## Required report format for each Codex task

Recording-only WinChronicle Workday turns are not development tasks. When the
user only asks to start recording, stop recording, summarize the workday, or
check workday status, follow the Workday plugin/CLI output instead. Do not use the required report format for those turns; paste the local workday summary or Codex-assisted daily report directly.

At the end of every task, report exactly:

- What changed
- Tests run
- Tests not run and why
- Privacy/security implications
- Next smallest implementation task

Do not claim success unless relevant tests were run or you clearly state why
they could not run.
