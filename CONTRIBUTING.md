# Contributing

WinChronicle is a harness-first Windows memory project. Start by reading
`AGENTS.md`, `docs/operator-quickstart.md`, `docs/deterministic-demo.md`, and
`docs/roadmap.md`.

## Safe Contribution Shape

Prefer small changes that fit one roadmap lane:

- deterministic fixtures, schemas, tests, scorecards, or docs;
- privacy/redaction and denylist regression coverage;
- UIA helper contract diagnostics without expanding product capture targets;
- watcher preview diagnostics without daemon, service, polling, or default
  background capture;
- read-only MCP compatibility examples and exact tool-list tests;
- deterministic memory goldens and idempotence evidence;
- release evidence, manual smoke templates, and operator docs.

## Harness-first Workflow

Before changing behavior, update the relevant contracts, fixtures, tests,
scorecards, or documentation. Keep changes scoped to the smallest verifiable
surface.

Run the standard deterministic validation set when applicable:

```powershell
python -m pytest -q
dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo
dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo
python harness/scripts/run_install_cli_smoke.py
python harness/scripts/run_harness.py
git diff --check
```

## Privacy And Scope Boundaries

Do not add screenshot capture, OCR, audio recording, keyboard capture, clipboard
capture, network upload, LLM reducer/classifier calls, desktop control,
daemon/service install, polling capture loops, default background capture, MCP
write tools, arbitrary file read tools, or product targeted capture.

Do not commit local state, raw helper JSON, raw watcher JSONL, generated
captures, generated memory, screenshots, OCR output, secrets, passwords, or
observed-content diagnostics. Observed content must remain marked as
`trust = "untrusted_observed_content"`.

If a proposal may affect capture surfaces, privacy behavior, schema shape,
CLI/MCP JSON shape, helper/watcher behavior, storage, memory output, or release
evidence, open a privacy boundary review issue before implementation.
