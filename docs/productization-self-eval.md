# Productization Self-Eval

`harness/scripts/run_productization_self_eval.py` is a deterministic check for
the public product surface. It scores whether a first-time visitor can
understand, try, trust, share, and contribute to WinChronicle without expanding
the capture surface.

## Run It

```powershell
python harness/scripts/run_productization_self_eval.py
python harness/scripts/run_productization_self_eval.py --format json
```

The passing threshold is 90/100. The script exits non-zero when required
public-facing promises are missing or when obvious overclaiming phrases appear.

## What It Checks

- README first-screen clarity: product promise, hero image, Demo / Workday / MCP
  paths, and first commands.
- Privacy boundary: independent project, redaction-first wording,
  `untrusted_observed_content`, and no screenshots/OCR/desktop-control/MCP-write
  promises.
- Fixture demo: `run_quick_demo.py`, fake-helper wording, and no live desktop
  dependency.
- Codex entry: Workday plugin guide, record-only mode, and read-only MCP setup.
- Contributor entry: safe good-first tasks, growth/trust starter tasks, and
  no observed-content commits.
- Overclaim risk: obvious claims such as official affiliation, recording
  everything, desktop control, screenshot defaults, or cloud desktop upload.

## Boundary

The self-eval reads repository docs and static metadata only. It does not start
live UIA, read the desktop, inspect user windows, start a monitor session,
capture observed content, call an LLM, upload data, or change local state.

It is a growth and trust check, not a release checklist. Keep it lightweight and
update it only when a user-facing onboarding promise changes.
