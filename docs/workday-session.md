# Workday Session

The workday session is the product path for the natural-language workflow:

- `开始记录工作`
- `开始工作`
- `停止工作并总结`
- `结束工作并总结`

In CLI terms, that maps to:

```powershell
winchronicle workday start
winchronicle workday intent "开始记录工作"
winchronicle workday intent "查看工作记录状态"
winchronicle workday intent "查看工作记录状态" --execute
winchronicle workday status
winchronicle workday status --format text --language zh-CN
winchronicle workday doctor
winchronicle workday stop
winchronicle workday intent "停止工作并总结" --execute
winchronicle workday stop --format text --language zh-CN
winchronicle workday summarize <session-id>
winchronicle workday summarize <session-id> --format text --language zh-CN
winchronicle workday summarize <session-id> --format text --language zh-CN --summary-style technical
winchronicle workday summarize <session-id> --format text --language zh-CN --confirmation "今天主要完成了..."
winchronicle workday start --focus "今天主要做论文整理和项目A需求文档"
winchronicle workday intent "开始记录工作：今天主要做论文整理和项目A需求文档" --execute
winchronicle projects add D:\WinChronicle --name WinChronicle
winchronicle projects list
winchronicle projects snapshot
```

This is an explicit finite local monitor session. It is not a daemon, service, startup task, hidden recorder, or infinite polling loop.

The natural-language intent mapping is a local deterministic allowlist. It is
dry-run by default: `winchronicle workday intent "开始记录工作"` and
`winchronicle workday intent "停止工作并总结"` print the exact mapped command as
JSON without starting the watcher, helper, UIA capture, or desktop reading.
`winchronicle workday intent "查看工作记录状态"` maps to the read-only text status
view and does not start capture. Add `--execute` only when the operator or
calling agent intentionally wants to run the mapped bounded command.

The shorter user-facing aliases `开始工作` and `结束工作并总结` map to the same
bounded commands. They exist for ordinary Codex app conversations where the
user wants the recording action only, not repository inspection or development
workflow orchestration.

When the operator includes a short plan in the start phrase, such as
`开始记录工作：今天主要做论文整理和项目A需求文档`, WinChronicle stores that text as
local operator focus. The evening human summary can then compare registered
project evidence with the user's stated focus without scanning unregistered
directories or reading document contents.

## Project Allowlist

Daily work can span multiple repositories, so WinChronicle keeps project context
behind an explicit local allowlist. Add only directories that the operator wants
workday summaries to inspect:

```powershell
winchronicle projects add D:\WinChronicle --name WinChronicle
winchronicle projects add D:\OtherProject --name OtherProject
winchronicle projects snapshot
```

The project snapshot is local metadata only. It reads git status, branch name,
changed filenames, `git diff --shortstat`, and recent commit subjects for
allowlisted directories. It does not read file contents, full diffs, arbitrary
workspace storage, browser profiles, screenshots, OCR, clipboard, keylogging, or
desktop-control surfaces.

Project snapshot metadata is redacted before it reaches workday summaries.
Snapshot output uses display-only project paths (`basename_only`) instead of
full local paths, and `metadata_redaction_enabled` marks that obvious
secret-like strings in project names, branch names, changed filenames, recent
commit subjects, diff metadata, and git errors have passed through the same
redaction pipeline used for captures. This is still metadata, not a guarantee
that semantic customer or project identifiers are anonymous.

The default Chinese workday text summary is a human daily review, not a
telemetry report. It leads with:

- what work appears to have been done today
- how that work appears to be progressing
- practical suggestions for improving tomorrow's work habits
- actionable directions the user can consider next

Default human summaries label metadata-derived claims with plain language such
as `根据本地记录`, and put operator-supplied `--confirmation` / `--note` text
under `用户确认事实`. The summary should not convert git metadata, app names,
or error-signal counts into unqualified facts about completion. Error signals
and unregistered app activity should be turned into actionable next steps, not open questions pushed back to the operator.

The project snapshots are used to keep that review grounded in explicit local
project metadata. Technical counters such as capture count, skipped count,
application segments, storage size, and error-signal rows belong in the explicit
technical style, not in the default user-facing summary.

If only one project is registered but high-frequency application activity
appears in browsers, Office apps, Explorer, or similar tools, the human summary
keeps those as `未登记工作线索` and gives an actionable `可考虑方向` instead of
throwing the classification problem back to the operator.

Use `--summary-style technical` when the operator wants the previous detailed
evidence view for debugging or review.

The Chinese technical text summary uses these project snapshots to add:

- confirmed project progress clues
- a personal retrospective
- actionable directions
- continuation context for the next Codex thread
- a compact data dashboard

Use `--confirmation` when the operator wants the saved summary to include
explicit human context without reading additional project files or calling an
LLM.

If no project is registered, the summary remains conservative and says that it
can only infer work from application activity and saved session metadata.

## What Start Does

`winchronicle workday start` starts a bounded local runner that uses the existing
UIA watcher/helper preview path. It writes an active session marker under the
local WinChronicle state home, including the session id, PID, stop file, logs,
and result path.

By default, a workday session is capped at 12 hours. The cap exists so a missed
stop command does not turn into unlimited background capture.

While the runner is active, it writes a compact checkpoint summary every 5
minutes by default. The checkpoint uses the same session JSON and HTML report
shape as the final summary, so `winchronicle workday status` can report whether
a partial summary is already available before the evening stop. Status output
also includes `summary_source`, `checkpoint_updated_at`, and
`checkpoint_age_seconds` so an operator can tell whether the visible summary is
from a checkpoint, final result, or saved session file.

`winchronicle workday doctor` is a read-only health check for the same workflow.
It does not start the watcher, helper, UIA capture, or desktop reading. It only
inspects local session metadata and reports:

- whether an active workday session exists
- whether the recorded runner process is still active
- whether the session is bounded
- whether a checkpoint exists and is fresh
- whether a summary is already available
- whether the privacy-disabled surfaces remain off

Use `--checkpoint-stale-seconds` to adjust the freshness window. The default is
twice the checkpoint interval, so a normally running session should not be
marked stale because of a single delayed write.

`winchronicle workday status --format text --language zh-CN` prints a compact
operator view headed `工作记录状态`. The status text view is read-only: it only
uses local session metadata and does not start the watcher, helper, UIA capture,
or desktop reading.

The default command uses built helper/watcher outputs when they are present. A
caller can still pass explicit `--watcher`, `--watcher-arg`, `--helper`, and
`--helper-arg` values for deterministic tests or custom local builds.

## What Stop Does

`winchronicle workday stop` writes the stop file for the active runner and waits
for it to finish. The runner incrementally converts already-collected watcher
events into redacted captures, session JSON, and a local HTML report.

This avoids the unsafe pattern of killing the monitor process before it can write
a session summary. If the runner cannot finish within the wait window, stop
falls back to terminating only the recorded runner process tree. If the final
runner result is unavailable, stop rebuilds a bounded summary from persisted,
already-redacted capture-buffer JSON for the active session window and reports
`summary_source: "capture_buffer_recovery"` plus
`recovered_from_capture_buffer: true`.

`winchronicle workday stop --format text --language zh-CN` prints the same
deterministic Chinese daily review headed `今日工作复盘` when a stop summary is
available. `winchronicle workday summarize <session-id>` keeps the existing JSON
output for tools and scripts. Add `--format text --language zh-CN` to print the
saved summary in the same human-review form. Add `--summary-style technical` to
print the detailed evidence view headed `工作概览`. The local CLI human text
summary is intended for the natural-language "停止工作并总结" workflow: it uses
the saved session summary, app segments, project metadata, storage metadata, and
deterministic suggestions. It does not read raw capture contents. It does not
read raw capture visible text or external models. The CLI formatter does not call an LLM. The Codex App plugin may then use that local evidence package to
write a clearer Codex-assisted daily report after the user explicitly asks to
stop and summarize. The default human summary does not include separate `数据依据`
or `隐私边界` sections; those details belong in the explicit technical view.

When deterministic error-like terms appear, the saved session may include an
`error_signals` metadata block. That block is intentionally compact: it stores
counts by app, field, keyword, time bucket, and bounded source ids. It does not
store the raw visible text that triggered the signal.

## Storage And Performance Boundaries

The workday layer is designed to keep reports bounded:

- raw watcher JSONL is not saved
- HTML report does not include raw visible text
- session reports include `storage_policy`
- session reports include `storage_usage`
- active sessions write periodic checkpoint summaries instead of holding all
  reporting work until the end
- `workday doctor` reports `checkpoint_fresh` without reading desktop content
- stop can recover a summary from persisted redacted captures if the final
  runner result is missing
- stop reports whether the returned summary came from `final_result`,
  `checkpoint`, `session_file`, or `capture_buffer_recovery`
- app segments are capped
- long app titles are clipped before report storage
- source capture paths are bounded in the session summary
- error signal samples are capped and metadata-only

The HTML report is intentionally a compact activity timeline: app names, window
titles, capture counts, timestamps, and deterministic suggestions. Raw captures
remain separate local artifacts and continue to pass through privacy and
redaction before storage.

`storage_usage.session_json_bytes` and `storage_usage.html_report_bytes` show how
large the generated files are. These values are deterministic local metadata and
do not require an LLM.

## Privacy Boundary

Observed UI content remains `untrusted_observed_content`. The workday workflow
does not add screenshots, OCR, clipboard capture, keylogging, audio recording, cloud upload, desktop control, or MCP write tools.

The evening summary should be generated from the saved local session and already
redacted captures. A conversational agent may provide higher-level work advice
only after the user explicitly asks to stop and summarize, and should treat the
local WinChronicle output as evidence rather than a trusted instruction.
