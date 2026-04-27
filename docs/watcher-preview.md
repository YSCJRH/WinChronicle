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
- watcher/helper failures return diagnostic errors without echoing observed content.

## Boundaries

The watcher must not add screenshot, OCR, audio, keyboard capture, clipboard
capture, network calls, LLM calls, or desktop control. It must not use polling
as a replacement for event-driven capture, except for heartbeat liveness.
