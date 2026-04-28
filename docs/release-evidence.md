# Release Evidence Guide

Use this guide when preparing maintenance, release-candidate, and final release
evidence. It consolidates what must be recorded for deterministic gates, manual
smoke, and post-publication reconciliation without committing observed-content
artifacts. For the current post-v0.1.1 maintenance cursor, see
[Post-v0.1.1 maintenance plan](next-round-plan-post-v0.1.1.md).

## Evidence Location

Release evidence should live in the release-candidate record, final release
record, GitHub release notes, or PR comment. Do not commit raw helper JSON, raw
watcher JSONL, screenshots, OCR output, observed text, local HTML page
contents, editor buffer contents, passwords, secrets, or token canaries.

Record only:

- command;
- pass/fail result;
- timestamp;
- environment notes;
- commit SHA;
- GitHub Actions run URL;
- local artifact path when an artifact exists.

## Deterministic Evidence

Record the result for each deterministic gate:

```powershell
python -m pytest -q
dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo
dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo
python harness/scripts/run_install_cli_smoke.py
python harness/scripts/run_harness.py
git diff --check
```

Also record the GitHub Actions `Windows Harness` run URL for the PR and for
`main` after merge.

## Post-Publication Reconciliation

After a prerelease or final release is published, reconcile the repository
docs with the published facts:

- release URL;
- tag name and exact tag target SHA;
- publication status;
- PR Windows Harness URL and head SHA;
- post-merge `main` Windows Harness URL and head SHA;
- next active execution cursor.

Do not retag an already published release to reconcile documentation. If a
subsequent product, schema, CLI/MCP JSON shape, or privacy behavior change is
needed, publish a new release candidate instead.

## Manual Evidence

Use [Manual smoke evidence template](manual-smoke-evidence-template.md) for
interactive Windows smoke. Manual evidence must use a temporary
`WINCHRONICLE_HOME` and must not paste observed content.

Hard gates:

- Notepad targeted UIA smoke: marker capture must pass.
- Edge targeted UIA smoke: local HTML body marker capture must pass.

Conditional hard gate:

- VS Code metadata targeted UIA smoke must pass when `code.cmd` exists.

Diagnostic, non-blocking gate:

- VS Code strict Monaco editor marker capture may fail as a known Monaco/UIA
  limitation. If it fails, record the diagnostic artifact path only.

Preview gate:

- Watcher preview smoke should record foreground event behavior, debounce,
  duplicate skip, denylist skip, and diagnostic behavior with temporary state.

## Privacy And Scope Evidence

Before release, confirm the evidence record says:

- screenshots and OCR are absent or disabled by default;
- audio recording is not implemented;
- keyboard capture is not implemented;
- clipboard capture is not implemented;
- network upload is not implemented;
- LLM summarization/classification is not implemented;
- MCP remains read-only;
- daemon/service install and default background capture are not implemented;
- desktop control is not implemented;
- observed content remains marked as `untrusted_observed_content`.

## Release Decision Summary

The release-candidate record should end with:

- deterministic gates passed;
- manual hard gates passed;
- conditional gates skipped and why;
- diagnostic failures and artifact paths;
- privacy/scope confirmation;
- rollback note;
- explicit publication approval status.
