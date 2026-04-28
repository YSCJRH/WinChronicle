# UIA Helper Quality Matrix

This matrix is the Stage F2 helper-quality contract for v0.1 final readiness.
It summarizes the current helper coverage without expanding the product capture
surface. Manual smoke artifacts may contain observed content; keep them local
and record only pass/fail status, commands, timestamps, environment notes, and
artifact paths.

Product boundary: `python -m winchronicle capture-frontmost` remains
foreground-only through `GetForegroundWindow`. Targeted `--hwnd`, `--pid`, and
title/process capture remain helper-only harness paths gated by both
`--harness` and `WINCHRONICLE_HARNESS=1`. MCP remains read-only and exposes no
targeted capture.

| Gate type | App / scope | Expected signal | Current result | Artifact policy | Privacy risk | Blocking status |
| --- | --- | --- | --- | --- | --- | --- |
| Deterministic helper fixture | Notepad fixture | Helper JSON validates, normalizes to a capture, indexes searchable visible text, records frontmost `capture_target`, and keeps all prohibited capture surfaces false. | Covered by `tests/test_uia_helper_contract.py`; local F2 validation passed. | Fixture JSON is committed because it is synthetic. Generated captures stay under temporary `WINCHRONICLE_HOME`. | Low; synthetic text and schema-only validation. | Hard automated gate. |
| Deterministic helper fixture | Password fixture | Password field values normalize to `[REDACTED:password_field]` and raw password text does not persist. | Covered by helper privacy tests. | Synthetic fixture may be committed; generated capture artifacts stay temporary. | High if regressed; prevents password storage. | Hard automated privacy gate. |
| Deterministic helper fixture | Budget/stale traversal fixture | `uia_stats` records stale skips, exception skips, timeout, node budget, depth budget, char budget, and truncation without crashing. | Covered by helper contract tests. | Synthetic fixture may be committed; no live observed content. | Medium; guards runaway UIA traversal and stale COM failures. | Hard automated contract gate. |
| Deterministic wrapper diagnostics | Fake helper wrapper | Timeout, invalid JSON, empty stdout, and nonzero helper exit return stable diagnostics without echoing observed stdout or stderr. | Covered by CLI/helper wrapper tests. | No raw helper stdout/stderr is committed or printed in failure messages. | Medium; prevents observed-content leakage through diagnostics. | Hard automated gate. |
| Harness boundary guard | Targeted helper path | Targeted capture requires both `--harness` and `WINCHRONICLE_HARNESS=1`; product CLI and MCP expose no targeted HWND/PID/title capture. | Covered by Windows-only helper tests, schema, scorecards, and docs. | No artifact is needed for the rejection path. | High; regression would expand the capture surface. | Hard boundary gate. |
| Harness-only targeted smoke | Notepad | Unique text marker appears in captured visible/focused text; target metadata shows harness-only HWND capture; no activation or desktop control. | Last recorded `v0.1.0-rc.0`: pass. | Local JSON artifact only; record path in manual smoke evidence, do not commit observed content. | Medium; validates simple edit text while preserving no-store artifact policy. | Hard manual release gate. |
| Harness-only targeted smoke | Microsoft Edge | Local HTML body marker appears in browser text; process/title target is harness-only; URL extraction remains best-effort. | Last recorded `v0.1.0-rc.0`: pass. | Local JSON artifact only; record path, do not commit local page contents or capture JSON. | Medium; browser text may contain observed content. | Hard manual release gate. |
| Harness-only targeted smoke | VS Code metadata | `code.cmd` is available, capture resolves VS Code/Code.exe window metadata, and target metadata shows harness-only process/title capture. | Last recorded `v0.1.0-rc.0`: pass with diagnostic warning. | Local JSON artifact only; record path, do not commit editor contents. | Medium; metadata confirms target resolution while avoiding dependence on editor buffer text. | Conditional hard manual release gate when `code.cmd` is available. |
| Harness-only targeted smoke | VS Code strict Monaco marker | Editor marker appears through standard UIA text/value extraction. | Last recorded `v0.1.0-rc.0`: diagnostic failure, consistent with known Monaco/UIA limitation. | Keep diagnostic artifact locally and record path only. | Medium; failure must not trigger screenshot/OCR/keyboard/clipboard/control workarounds. | Diagnostic, non-blocking for v0.1. |
| Manual frontmost smoke | Operator-selected foreground app | Product-shaped `capture-frontmost` captures only the foreground window through caller-provided helper path. | Available as manual smoke; not the app-specific hard gate because focus can be unreliable in agent-hosted desktops. | Temporary state only; do not print or commit observed content. | Medium; validates product path without targeted capture. | Diagnostic/manual confidence gate. |
| Future app coverage | Any additional app | App-specific signal is captured through existing helper contract and privacy pipeline. | Not promoted in v0.1. | Treat artifacts as local observed content. | Unknown until app-specific privacy review. | Diagnostic by default unless a future scorecard promotes it. |

## Release Use

Before `v0.1.0-rc.1` or final, release evidence should cite this matrix and
record:

- Notepad targeted smoke result.
- Edge targeted smoke result.
- VS Code availability and metadata smoke result.
- VS Code strict Monaco result as diagnostic/non-blocking.
- Any diagnostic artifacts by local path only.

Do not use this matrix to justify screenshots, OCR, audio recording, keyboard
capture, clipboard capture, network upload, LLM calls, desktop control, MCP
write tools, or product targeted capture.
