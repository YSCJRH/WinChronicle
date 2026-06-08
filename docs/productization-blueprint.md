# WinChronicle Productization Blueprint

This blueprint keeps the v0.2 productization lane finite. It is not a new
maintenance loop and it does not authorize capture-surface expansion.

## Product Identity

WinChronicle is a Windows-first, UIA structured context first, local storage
first, deterministic pipeline first, read-only MCP first, privacy/redaction
first AI agent context memory layer. It is independent and not affiliated with
OpenAI.

## Non-Goals

The productization lane must not add or imply default screenshots, OCR,
keyboard logging, clipboard capture, audio recording, cloud upload, desktop
control, background daemons or services, infinite polling, MCP write tools,
arbitrary file reads, network upload, or product-targeted capture behavior.
Observed UI or screen content remains `untrusted_observed_content`.

## Finite Phases

| Phase | Goal | Primary surfaces | Release |
| --- | --- | --- | --- |
| 0 | Automation guardrails | `AGENTS.md`, `.github/`, this blueprint | Patch tag/release after merge |
| 1 | README hero and social visual | README files, `docs/assets/`, project presentation | Patch tag/release after merge |
| 2 | Three-path onboarding | README files, first-run, Workday, MCP docs | Patch tag/release after merge |
| 3 | Workday summary examples | README files, Workday docs, synthetic examples | Patch tag/release after merge |
| 4 | Codex App / CLI / MCP usage card | README files, Codex and MCP docs, plugin skill docs if needed | Patch tag/release after merge |
| 5 | Docs navigation polish | README files, maintenance index, project presentation | Final productization patch tag/release |

Stop after Phase 5. Do not start a new release-readiness path or propose
capture-surface expansion as a follow-up.

## Required Gates

Every phase should run:

```powershell
python -m pip install -e ".[dev]"
python -m pytest -q
python harness/scripts/run_mcp_smoke.py
python -m winchronicle codex install --dry-run
git diff --check
```

The GitHub productization workflow also checks phase-scoped file changes,
generated/local artifact patterns, and required docs or asset paths for each
phase.

Patch releases must keep release tags and runtime version metadata aligned.
Version metadata changes are allowed in every productization phase only for:

- `pyproject.toml`
- `plugins/winchronicle-workday/.codex-plugin/plugin.json`
- `src/winchronicle/codex_plugins/winchronicle-workday/.codex-plugin/plugin.json`
- `src/winchronicle/_version.py`
- `tests/test_version_identity.py`

Those files must not be used for product behavior changes in this lane.

## Review Contract

Each phase should receive isolated read-only review from:

- Privacy Boundary Reviewer
- Product Clarity Reviewer
- Release Gate Reviewer

Blockers must be fixed before merge. Normal branch protection and status checks
must be used. Do not force-push `main`, do not use admin override merges, and do
not retag existing releases.
