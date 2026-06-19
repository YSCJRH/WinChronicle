# Contributing

WinChronicle is a harness-first Windows memory project. Start by reading
`AGENTS.md`, `docs/operator-quickstart.md`, `docs/deterministic-demo.md`, and
`docs/roadmap.md`.

For the product-facing entry path, also read `docs/quick-demo.md`,
`docs/why-winchronicle.md`, and `docs/privacy-architecture.md`.

## Good First Contributions

Good first contributions are small, deterministic, and easy to review:

- improve the 5-minute demo or README onboarding;
- add deterministic UIA fixtures with redaction coverage;
- document Windows app compatibility without committing observed content;
- improve read-only MCP examples;
- add privacy regression tests for secret canaries;
- clarify monitor session reports and timeline examples.

## Growth And Trust Starter Tasks

These are good first issues for contributors who want to make the project
easier to understand, try, trust, or share:

- improve the README first screen without adding a long maintenance ledger;
- improve `docs/demo-promotion-kit.md` with clearer fixture-only demo copy;
- improve Codex App Workday plugin docs while keeping the flow record-only;
- add Windows app compatibility notes, but do not commit observed content;
- add deterministic privacy/redaction fixtures using synthetic data only;
- improve `harness/scripts/run_productization_self_eval.py` when onboarding or
  safety promises change.

Before opening a product-facing PR, run:

```powershell
python harness/scripts/run_productization_self_eval.py
```

Use the GitHub issue templates for bug reports, privacy concerns, Windows app
compatibility notes, feature proposals, harness-first tasks, and privacy
boundary reviews.

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

### Harness Timeout Policy

The local harness runners use per-command timeouts to fail closed instead of
hanging release work:

- `python harness/scripts/run_harness.py` defaults to 900 seconds per
  subprocess. Override only for local diagnosis with
  `WINCHRONICLE_HARNESS_COMMAND_TIMEOUT_SECONDS`.
- `python harness/scripts/run_install_cli_smoke.py` defaults to 300 seconds per
  subprocess. Override only for local diagnosis with
  `WINCHRONICLE_INSTALL_CLI_SMOKE_COMMAND_TIMEOUT_SECONDS`.
- GitHub Actions mirrors this with step-level `timeout-minutes` entries for
  install, unit tests, .NET builds, the deterministic harness, and whitespace
  checks.

Timeout handlers print the command and timeout value, but do not print partial
stdout or stderr. A hung command may already have emitted observed content
before it is killed, so timeout diagnostics must stay content-free. Adjusting
timeout values does not authorize new capture surfaces, live UIA capture,
screenshots, OCR, clipboard capture, cloud upload, desktop control, or MCP write
tools.

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
