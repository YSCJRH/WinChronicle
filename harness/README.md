# WinChronicle Harness

The harness contains deterministic contracts, fixtures, scorecards, and scripts
used before real Windows UIA capture is implemented.

Phase 0 covers fixture-only capture, redaction, schema validation, local storage,
and search.

Run the full local harness from the repository root:

```powershell
python harness/scripts/run_harness.py
.\harness\scripts\run_harness.ps1
```

The runner uses a temporary `WINCHRONICLE_HOME` so CLI smoke checks do not write
to the user's normal WinChronicle state directory.
