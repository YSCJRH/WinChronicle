# Watcher Preview

The v0.1 watcher is an explicit preview path. It is not installed as a service,
does not start by default, and does not save raw watcher JSONL streams.

## Product Shape

The supported preview command is:

```powershell
python -m winchronicle watch --watcher path\to\win-uia-watcher.exe --helper path\to\win-uia-helper.exe --duration 30
```

The watcher emits JSONL events in memory. Python dispatches those events through
the same normalize, privacy, redaction, schema, and SQLite pipeline used by
fixture and frontmost captures.

## Manual Smoke

Run manual watcher smoke with a temporary `WINCHRONICLE_HOME`.

Expected observations:

- foreground window changes emit capture events;
- short typing bursts are debounced into fewer captures;
- duplicate content fingerprints are skipped;
- denylisted apps and lock-screen captures do not write observed content;
- heartbeat-only runs report liveness without writing captures;
- watcher/helper failures return diagnostic errors without echoing observed content.

## Operator-Facing Diagnostics

The preview path is designed to fail closed and report a stable diagnostic
without printing observed content. Operators should record the command, exit
code, diagnostic line, and artifact path in the manual smoke evidence template,
and track freshness in the manual smoke evidence ledger, but should not paste
raw watcher JSONL or helper capture output into release notes.

Expected diagnostics:

| Scenario | Expected operator signal | Content handling |
| --- | --- | --- |
| Watcher exits nonzero | `ERROR: watcher failed with exit code <code>` | Suppress watcher stderr/stdout so observed content is not echoed. |
| Helper failure surfaced by watcher | The watcher exits nonzero and Python reports the watcher exit code. | Treat helper stderr/stdout as observed-adjacent; do not copy it into evidence. |
| Malformed watcher JSONL | `ERROR: watcher JSONL line <n> is malformed` | Do not save or paste the malformed raw line. |
| Invalid embedded helper payload | `ERROR: watcher output could not be captured safely` | Do not paste schema validation output or invalid helper payloads; they may contain observed content. |
| Watcher timeout | `ERROR: watcher timed out` from the CLI. | Do not print partial stdout; rerun with a temporary state directory and shorter repro notes. |
| Heartbeat-only run | JSON counts show `captures_written = 0` and `heartbeats > 0`. | Do not create a capture artifact or save raw watcher JSONL; investigate helper/window conditions from the diagnostic only. |
| Denylisted app or lock screen | JSON counts show `denylisted_skipped` incrementing and `captures_written` unchanged. | No observed content should be written, searched, or echoed in diagnostics. |
| Duplicate content fingerprint | JSON counts show `duplicates_skipped` incrementing. | Duplicate captures should not be written again. |
| Raw watcher JSONL persistence | No `.jsonl` event stream is written under `WINCHRONICLE_HOME` by `watch --watcher`. | Treat live watcher JSONL as transient observed-adjacent data consumed in memory only. |

Harness smoke may stage fake-helper watcher JSONL in a temporary file outside
`WINCHRONICLE_HOME` only to feed the deterministic `watch --events` path. That
temporary file is not live observed UI content, is not committed, and is deleted
with the temporary smoke directory.

Deterministic coverage exists for these failure and skip modes in the watcher
tests and harness fixtures. Live watcher smoke remains manual because it depends
on an interactive Windows desktop.

## Deterministic Coverage

The post-v0.1 reliability contract is covered without starting a live desktop
watcher:

| Mode | Deterministic coverage |
| --- | --- |
| Heartbeat-only run | CLI fake-watcher test asserts `captures_written = 0`, `heartbeats > 0`, no capture buffer, and no raw watcher JSONL under temporary state. |
| Duplicate content fingerprint | Fixture dispatch test replays the same watcher events and asserts duplicate skips without extra captures. |
| Watcher privacy fixture parity | Focused tests generate deterministic watcher JSONL under `tmp_path` from existing privacy fixtures and assert redaction, denylist, trust-boundary, MCP/memory-search parity, and no raw watcher JSONL under `WINCHRONICLE_HOME`; [Fixture/privacy parity matrix after v0.1.18](privacy-fixture-parity-matrix-post-v0.1.18.md) maps this against direct fixture and synthesized helper evidence. |
| Denylisted app or lock screen | Lock-screen helper fixture dispatch asserts `denylisted_skipped`, no capture artifact, no raw watcher JSONL under state, and no searchable observed content. |
| Watcher exits nonzero | Fake watcher exits with a code; CLI reports only the stable exit-code diagnostic. |
| Helper failure surfaced by watcher | Fake watcher emits helper-adjacent stdout/stderr and exits; CLI suppresses observed-adjacent output. |
| Malformed watcher JSONL | Fake watcher emits malformed JSONL; CLI reports the line number and does not persist raw JSONL. |
| Invalid embedded helper payload | Fixture-events CLI test injects an invalid helper payload with an observed-content canary; CLI reports only a stable error and writes no capture or raw JSONL under state. |
| Watcher timeout | Slow fake watcher times out; wrapper reports `watcher timed out` without printing partial stdout. |
| Raw watcher JSONL persistence | Fake watcher tests assert no raw `.jsonl` stream is persisted under `WINCHRONICLE_HOME`. |

## Boundaries

The watcher must not add screenshot, OCR, audio, keyboard capture, clipboard
capture, network calls, LLM calls, or desktop control. It must not use polling
as a replacement for event-driven capture, except for heartbeat liveness.

Do not add a daemon, service installer, startup task, always-on background
worker, or default capture loop for v0.1. Every live watcher run must stay
explicit, time-bounded, and operator-started.
