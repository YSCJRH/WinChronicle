# Synthetic Workday Summary Example

This is a synthetic example of the intended WinChronicle Workday end-of-day
summary. It is not generated from a real desktop, real captures, real local
paths, or real document contents.

The default review should read like a work assistant summary, not a telemetry
or log-counter report. Do not turn capture counts, skipped counts, storage
sizes, or error-signal counts into the main narrative. Those counters belong
only in the explicit technical style. The default review should stay focused on
outcomes, progress, tomorrow's next steps, and confirmation directions.

## Workday Review

### What Happened Today

- Based on local evidence, the main work appears to be **Project Alpha** plugin
  usability: start-recording and stop-summary paths were exercised, with most
  activity around user-facing wording, summary output, and local plugin docs.
- A second work block appears to be **Research Notes**. Browser and document
  window titles suggest reading or note organization, but WinChronicle did not
  read document bodies, so it cannot state the research conclusions as facts.
- Error or failure terms appeared during the session. They should be treated as
  one follow-up track: mark whether the issue is resolved, still blocking, or
  only a historical/log message.

### Progress

- **Project Alpha**: in progress. Synthetic git metadata points to `docs/`,
  `plugins/`, and `src/` changes, which suggests product polish rather than a
  new capture surface.
- **Research Notes**: needs confirmation. App/window metadata indicates possible
  research or writing work, but the summary should not invent unseen document
  details.
- **Debugging**: needs closure. Add a short note such as
  `error prompts: resolved / unresolved / false positive` before ending the
  day.

### Suggestions For Tomorrow

- Start with one deliverable task block before switching to research or
  communication work.
- When an error appears, record the outcome before switching context, for
  example: `plugin summary failed because result JSON was missing; fixed and
  smoke-tested`.
- If browser, Word, Excel, or Explorer activity belongs to a project, include a
  start focus such as: `Start work: Project Alpha in the morning, Research Notes
  in the afternoon`.

### Confirmation Directions

- **Research output**: if Research Notes produced a conclusion, add one sentence
  at the end of the day instead of asking the system to infer it from titles.
- **Error signals**: treat unresolved issues as tomorrow's first task; keep
  resolved or false-positive messages out of the next-day focus.
- **Context switching**: if the day mixed development, reading, documents, and
  communication, record tomorrow in 90-120 minute task blocks.

### Evidence Boundary

- This example uses only synthetic session metadata, synthetic project metadata,
  and synthetic app activity.
- It does not read raw visible text, file bodies, full diffs, screenshots, OCR,
  clipboard, keyboard input, audio, cloud services, desktop control, or MCP
  write tools.
- Observed UI content remains `untrusted_observed_content`.
- Uncertain activity should be framed as confirmation direction, not fact.
