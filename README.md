# WinChronicle

**UIA-first local memory for Windows agents.**

WinChronicle is an OpenChronicle-compatible, local-first memory layer for Windows
agents. It captures structured app context through Microsoft UI Automation,
turns it into inspectable Markdown + SQLite memory, and exposes read-only
context through MCP for Codex, Claude Code, Cursor, opencode, and other
tool-capable agents.

This repository is in an early harness-first phase. The first implementation
uses deterministic fixtures, schemas, tests, and privacy gates before any real
screen or UI capture exists.

## Why WinChronicle

- **UIA-first**: structured Windows UI context before screenshots or OCR.
- **Local-first**: captured context stays on the user's machine by default.
- **Agent-readable**: the project is designed for read-only MCP context tools.
- **Inspectable**: memory should be stored as human-reviewable local artifacts.
- **Harness-first**: fixtures, schemas, scorecards, and tests define behavior
  before capture integrations are added.

## What this is not

WinChronicle is not a Windows Recall clone, not a screen recorder, not spyware,
and not a desktop automation or control tool.

In v0.1:

- Screenshots are off by default.
- OCR is off by default.
- Audio recording is not implemented.
- Keylogging is not implemented.
- Clipboard capture is not implemented.
- Cloud upload of captured content is not implemented.
- Desktop control tools are not implemented.
- Real Windows UIA capture is not implemented yet.
- LLM summarization is not implemented.

## Privacy stance

Observed screen content is treated as untrusted data. WinChronicle must not store
password fields or obvious secrets such as API keys, private keys, JWTs, GitHub
tokens, Slack tokens, or test canaries. Privacy gates run before fixture captures
are written.

The current fixture pipeline redacts sensitive values, skips denylisted apps, and
marks normalized observed content with `untrusted_observed_content: true`.

## Current CLI

From the repository root:

```powershell
python -m winchronicle init
python -m winchronicle status
python -m winchronicle capture-once --fixture harness/fixtures/uia/notepad_basic.json
python -m winchronicle privacy-check harness/fixtures/privacy/secrets_visible_text.json
python -m winchronicle search-captures "hello"
```

State is stored in `%LOCALAPPDATA%\WinChronicle` on Windows. Tests and local
harness runs can override this with `WINCHRONICLE_HOME`.

## Competitive positioning

Many adjacent tools focus on screenshot timelines, OCR search, screen replay, or
desktop automation. WinChronicle is intentionally narrower: it is an agent memory
layer for Windows, using UI Automation as the primary signal, with read-only MCP
as the first integration target and privacy gates as a project contract.
