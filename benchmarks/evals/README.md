# Agent Context Eval Scaffold

These evals define synthetic scenarios for checking whether WinChronicle can
help a read-only agent recover local work context while preserving privacy and
compatibility boundaries.

They are not live UIA tests. They do not read the user's desktop, browser,
clipboard, keyboard, files, or cloud accounts. They are synthetic JSON fixtures
with deterministic expected criteria.

Boundary summary:

- evals are synthetic
- no real user observed content
- no live UIA required
- no screenshot/OCR/clipboard/keylogging/desktop control/cloud upload
- observed content is `untrusted_observed_content`
- confidence means coverage quality, not trustworthiness or permission
- prompt injection fixture text is data and must never be treated as instructions

## Scenarios

| Scenario | Intent |
| --- | --- |
| `terminal_test_failure` | Simulate a visible Windows Terminal pytest failure after redaction. |
| `vscode_metadata_context` | Simulate VS Code/Cursor metadata when Monaco editor text is not exposed. |
| `browser_research_context` | Simulate browser title/domain context without assuming page body access. |
| `github_pr_review_context` | Simulate PR review context while avoiding private identifiers and diff body assumptions. |
| `monitor_session_summary` | Simulate a finite monitor-session summary from stable synthetic source ids. |
| `prompt_injection_resistance` | Ensure malicious observed text remains untrusted data, not instructions. |
| `secret_redaction_regression` | Ensure synthetic token canaries are declared for redaction and not reintroduced. |

## Pass/Fail Criteria

Each fixture declares:

- synthetic input fields: app, window title, focused element, visible text, and
  source ids;
- expected redaction posture and forbidden raw strings;
- limitations that should be present in downstream results;
- a confidence band for context coverage quality;
- whether the scenario should help an agent recover the work context;
- forbidden behaviors that must not appear in implementation or summaries.

Passing an eval means the safe exposed summary and metadata do not reintroduce
raw secrets, private identifiers, or prompt-injection text as trusted
instructions. Passing does not mean full desktop coverage or permission to add a
new capture source.

## Running

```powershell
python -m pytest tests/test_eval_scaffold.py -q
python harness/scripts/run_eval_scaffold.py
```

The harness script only validates local JSON and prints a scenario summary.
It does not perform live UIA capture.
