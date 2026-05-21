# Workday Session

The workday session is the product path for the natural-language workflow:

- `开始记录工作`
- `停止工作并总结`

In CLI terms, that maps to:

```powershell
winchronicle workday start
winchronicle workday status
winchronicle workday stop
winchronicle workday summarize <session-id>
```

This is an explicit finite local monitor session. It is not a daemon, service, startup task, hidden recorder, or infinite polling loop.

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

## Storage And Performance Boundaries

The workday layer is designed to keep reports bounded:

- raw watcher JSONL is not saved
- HTML report does not include raw visible text
- session reports include `storage_policy`
- session reports include `storage_usage`
- active sessions write periodic checkpoint summaries instead of holding all
  reporting work until the end
- stop can recover a summary from persisted redacted captures if the final
  runner result is missing
- stop reports whether the returned summary came from `final_result`,
  `checkpoint`, `session_file`, or `capture_buffer_recovery`
- app segments are capped
- long app titles are clipped before report storage
- source capture paths are bounded in the session summary

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
only after the user explicitly asks to stop and summarize.
