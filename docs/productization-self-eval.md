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
- Contributor entry: safe good-first tasks, growth/trust starter tasks,
  Workday entrypoint consistency guidance, and no observed-content commits.
- Overclaim risk: obvious claims such as official affiliation, recording
  everything, desktop control, screenshot defaults, or cloud desktop upload.

The `contributor_entry` category also guards both README contributor
entrypoints. `README.md` must point contributors to `CONTRIBUTING.md` and
`docs/productization-self-eval.md`. `README.zh-CN.md` must point contributors
to `CONTRIBUTING.md` and the `Task Classification` / `中文速览` labels.

## Contributor Required Intake Checks

The `contributor_entry` category guards the Required Intake sentence in
`.github/pull_request_template.md`,
`.github/ISSUE_TEMPLATE/harness_first_task.yml`,
`.github/ISSUE_TEMPLATE/feature_proposal.yml`, and
`.github/ISSUE_TEMPLATE/privacy_boundary_review.yml`.

The guarded sentence is:

```text
Before implementation, read `AGENTS.md`, `docs/roadmap.md`, `README.md`, `docs/codex-long-term-goal.md`, and the files, tests, fixtures, schemas, scorecards, or docs affected by the task.
```

The checks live in `CONTRIBUTOR_TEMPLATE_INTAKE_CHECKS` as
`PR required intake`, `Harness issue required intake`,
`Feature proposal required intake`, and `Privacy review required intake`.

The same category guards the long-term-goal authorization boundary in
`CONTRIBUTING.md`, `.github/pull_request_template.md`,
`.github/ISSUE_TEMPLATE/harness_first_task.yml`,
`.github/ISSUE_TEMPLATE/feature_proposal.yml`, and
`.github/ISSUE_TEMPLATE/privacy_boundary_review.yml`.

```text
Reading `docs/codex-long-term-goal.md` gives direction only; it is not release authorization, not automatic maintenance authorization, and not approval for broad evidence sweeps, release or publish actions, or capture-surface expansion.
```

Those checks live in `CONTRIBUTOR_LONG_TERM_GOAL_BOUNDARY_CHECKS`.

This is a static docs and metadata check; it does not run live UIA, read the
desktop, or capture observed content.

## Codex Workday Entrypoint Consistency

Keep the Workday path consistent across the public Codex entrypoints:

- `README.md`
- `docs/windows-first-run.md`
- `docs/codex-app-plugin-install.md`
- `docs/codex-app-workday-guide.md`
- `docs/codex-workday-plugin.md`

`README.zh-CN.md` is the localized README mirror and shares the same Workday
boundary guard.

When `README.md` or `README.zh-CN.md` changes, run
`python -m pytest tests/test_readme_daily_workflow.py -q` with the self-eval
JSON gate.

When one changes, confirm the affected entrypoints still say the Workday flow
is record-only, the stopped summary uses summary-level evidence, and it does
not send raw observed text. They should keep the `summary_boundary` field or
visible `Summary boundary:` output tied to the same promise: the default daily
review is not a telemetry or log-counter report, and technical counters belong
only in the explicit technical/debugging view. The localized Chinese README must
preserve the equivalent phrase `不是遥测或日志计数报告`. Recording-only entrypoints
should also preserve the repository boundary:
`Do not inspect, scan, review, edit, test, commit, push, or release repository files.`

The self-eval also checks `CONTRIBUTING.md` so contributors see this rule before
changing a Codex Workday entrypoint.

Use `python harness/scripts/run_productization_self_eval.py --format json` plus
the focused docs tests for the edited entrypoints before closing the task.

## Review Entry Checks

Use this section when README, demo, Codex entry, contribution path, or safety
claims change.

- Feature proposal: use for product-facing ideas or developer-experience ideas
  before implementation; it classifies the idea but does not approve
  implementation.
- Harness-first task: use for deterministic docs, fixtures, tests, scorecards,
  CI, or compatible metadata inside the current baseline; include expected
  validation commands.
- Privacy-boundary review: use before implementation when work touches capture
  surfaces, observed content, storage, MCP output, memory output, redaction, or
  release evidence; include MCP output impact when relevant.
- Pull request template: use at PR time to confirm validation, Product CLI/MCP
  shape changes, prohibited surfaces, observed-content artifacts, and MCP
  schema guardrails.

If the correct entry is unclear, choose the stricter review path before
changing runtime behavior.

## Stable Text Output

The text output is a reader-facing contract for contributors and release notes.
Keep the section order stable so reviewers can compare local runs without
unrelated diff noise.

`Categories:` uses this canonical order: `codex_entry`, `contributor_entry`,
`first_screen`, `fixture_demo`, `overclaim_risk`, `privacy_boundary`.
Unknown future categories append after the known order so new checks do not
reorder existing report lines.

`Boundary:` uses this canonical order: `does_not_run_live_uia`,
`does_not_read_desktop`, `does_not_capture_observed_content`,
`checks_public_docs_and_static_metadata_only`.

When adding a category or boundary flag, update the canonical order constants
and focused text-output tests before changing report wording.

## JSON Contract

`--format json` is a local automation contract for the self-eval scorecard.
The current payload uses `schema_version = 1`.

Keep these top-level keys stable: `schema_version`, `name`, `score`,
`threshold`, `passed`, `categories`, `failed_items`, `next_actions`,
`provenance`, and `boundary`.

When changing the JSON payload shape, change the schema version and focused JSON
contract tests before renaming or removing fields.

## JSON Failure Contract

Failure JSON keeps the same `schema_version`, `provenance`, and `boundary`
fields as passing JSON. A failed run changes `passed`, category scores,
`failed_items`, and `next_actions`, not the automation envelope.

`failed_items` identifies the missing or overclaiming check, while
`next_actions` keeps the next local repair step machine-readable.

Do not snapshot absolute `checked_root` paths in tests or docs. Assert local
paths dynamically so contributors do not commit machine-specific evidence.

## Failed Item Format

`failed_items` entries use `category: name (path: reason)`.

The format is intentionally compact so automation can split the category, check
name, source path, and reason without reading free-form prose.

When changing this string, update `FAILED_ITEM_FORMAT` and focused failed-item
format tests before changing output code.

## Next Actions Contract

`next_actions` is a small stable action vocabulary for local automation.

Passing runs use the three `PASSING_NEXT_ACTIONS` entries.
Missing-file failures prepend `MISSING_FILE_NEXT_ACTION` before
`GENERIC_FAILURE_NEXT_ACTIONS`. Other failures return only
`GENERIC_FAILURE_NEXT_ACTIONS`.

When changing this vocabulary, update `PASSING_NEXT_ACTIONS`,
`MISSING_FILE_NEXT_ACTION`, `GENERIC_FAILURE_NEXT_ACTIONS`, and focused
next-actions tests before changing output code.

## Score Contract

`score` and category scores use `round(100 * passed / total)`.

The numerator is passed checks and the denominator is total checks at the same
scope. Overall score uses all checks; category scores use only checks in that
category.

When changing score semantics, update `SCORE_FORMULA`, `_percentage_score`, and
focused score contract tests before changing output code.

## Pass Contract

`passed` is true only when `score >= threshold` and `failed_items` is empty.

A high score with any failed item still fails the gate, and a clean run below
threshold also fails.

When changing pass semantics, update `PASS_CONDITION`, `_passes_gate`, and
focused pass contract tests before changing output code.

## Threshold Contract

`DEFAULT_THRESHOLD` is 90.

`threshold` is an integer percentage from 0 to 100. Programmatic callers must
pass a real `int`; `bool`, `float`, `str`, and `None` are rejected. CLI
`--threshold` rejects values outside this range before evaluation.

`CLI_ERROR_EXIT_CODE` is 2. CLI threshold errors use
`CLI_THRESHOLD_RANGE_ERROR` or `CLI_THRESHOLD_INTEGER_ERROR`.

CLI threshold errors do not emit a JSON payload or traceback.

When changing threshold semantics, update `THRESHOLD_RANGE`,
`CLI_ERROR_EXIT_CODE`, `CLI_THRESHOLD_RANGE_ERROR`,
`CLI_THRESHOLD_INTEGER_ERROR`, `_validate_threshold`, `_parse_threshold`, and
focused threshold contract tests before changing output code.

## Root Argument Contract

`--root` is a hidden local test override.

`ROOT_ARGUMENT_CONTRACT` is `existing directory used as local self-eval root`.
CLI root errors use `CLI_ROOT_PATH_ERROR`.

Invalid root paths do not emit a JSON payload or traceback.

Existing roots with missing checked paths are self-eval failures, not CLI
argument errors.

When changing root semantics, update `ROOT_ARGUMENT_CONTRACT`,
`CLI_ROOT_PATH_ERROR`, `_parse_root`, and focused root argument tests before
changing output code.

## JSON Provenance

`--format json` includes `provenance.checked_root` and
`provenance.checked_paths` so local runs can be audited without guessing which
checkout was evaluated.

`provenance.checked_root` is a local audit pointer to the repository root
passed to the self-eval. It may reveal a local filesystem path, so do not treat
JSON output as permission to publish or externally share local evidence.

`provenance.checked_paths` lists the fixed repository-relative docs and static
metadata paths checked by the scorecard. It is not an arbitrary file inventory,
and it does not authorize live UIA, desktop reads, observed content capture, LLM
calls, upload, or local state changes.

## Boundary

The self-eval reads repository docs and static metadata only. It does not start
live UIA, read the desktop, inspect user windows, start a monitor session,
capture observed content, call an LLM, upload data, or change local state.

It is a growth and trust check, not a release checklist. Keep it lightweight and
update it only when a user-facing onboarding promise changes.
