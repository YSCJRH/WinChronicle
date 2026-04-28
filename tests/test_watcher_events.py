import json
import subprocess
import sys
from pathlib import Path

from winchronicle.cli import main
from winchronicle.events import (
    dispatch_watcher_event_lines,
    dispatch_watcher_events,
    run_watcher_command,
)
from winchronicle.schema import validate_watcher_event
from winchronicle.storage import search_captures


ROOT = Path(__file__).resolve().parents[1]


def test_watcher_event_fixture_dispatches_one_capture_and_heartbeat(tmp_path, monkeypatch):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    event_path = ROOT / "harness" / "fixtures" / "watcher" / "notepad_burst.jsonl"

    for line in event_path.read_text(encoding="utf-8").splitlines():
        validate_watcher_event(json.loads(line))

    result = dispatch_watcher_events(event_path, home)
    results = search_captures("deterministic capture", home)

    assert result.to_json() == {
        "captures_written": 1,
        "duplicates_skipped": 1,
        "denylisted_skipped": 0,
        "heartbeats": 1,
    }
    assert len(results) == 1
    assert results[0]["app_name"] == "Notepad"


def test_watcher_dispatch_counts_heartbeat_only_without_capture(tmp_path, monkeypatch):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))

    result = dispatch_watcher_event_lines(
        [
            json.dumps(
                {
                    "event_schema_version": 1,
                    "source": "win-uia-watcher",
                    "event_id": "heartbeat-only",
                    "event_type": "heartbeat",
                    "timestamp": "2026-04-25T13:30:01+08:00",
                    "heartbeat_id": "heartbeat-only",
                },
                sort_keys=True,
            )
        ],
        home,
    )

    assert result.to_json() == {
        "captures_written": 0,
        "duplicates_skipped": 0,
        "denylisted_skipped": 0,
        "heartbeats": 1,
    }
    assert not (home / "capture-buffer").exists()


def test_watcher_dispatch_skips_duplicate_fingerprint_already_indexed(tmp_path, monkeypatch):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    event_path = ROOT / "harness" / "fixtures" / "watcher" / "notepad_burst.jsonl"

    first = dispatch_watcher_events(event_path, home)
    second = dispatch_watcher_events(event_path, home)
    results = search_captures("deterministic capture", home)

    assert first.to_json() == {
        "captures_written": 1,
        "duplicates_skipped": 1,
        "denylisted_skipped": 0,
        "heartbeats": 1,
    }
    assert second.to_json() == {
        "captures_written": 0,
        "duplicates_skipped": 2,
        "denylisted_skipped": 0,
        "heartbeats": 1,
    }
    assert len(results) == 1


def test_watcher_dispatch_skips_denylisted_lock_app(tmp_path, monkeypatch):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    lock_capture = json.loads(
        (ROOT / "harness" / "fixtures" / "uia-helper" / "lock_app_frontmost.json").read_text(
            encoding="utf-8"
        )
    )
    event_path = tmp_path / "lock_app_event.jsonl"
    event_path.write_text(
        json.dumps(
            {
                "event_schema_version": 1,
                "source": "win-uia-watcher",
                "event_id": "lock-app-foreground",
                "event_type": "foreground_changed",
                "timestamp": "2026-04-25T13:20:00+08:00",
                "capture": lock_capture,
            },
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    result = dispatch_watcher_events(event_path, home)

    assert result.to_json() == {
        "captures_written": 0,
        "duplicates_skipped": 0,
        "denylisted_skipped": 1,
        "heartbeats": 0,
    }
    assert search_captures("Lock screen", home) == []


def test_watch_cli_dispatches_fixture_events(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("WINCHRONICLE_HOME", str(tmp_path / "state"))

    assert main(
        [
            "watch",
            "--events",
            str(ROOT / "harness" / "fixtures" / "watcher" / "notepad_burst.jsonl"),
        ]
    ) == 0
    output = json.loads(capsys.readouterr().out)

    assert output == {
        "captures_written": 1,
        "duplicates_skipped": 1,
        "denylisted_skipped": 0,
        "heartbeats": 1,
    }


def test_watch_cli_runs_fake_watcher_without_raw_event_file(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("WINCHRONICLE_HOME", str(tmp_path / "state"))
    fake_watcher = tmp_path / "fake_watcher.py"
    event_path = ROOT / "harness" / "fixtures" / "watcher" / "notepad_burst.jsonl"
    fake_watcher.write_text(
        "from pathlib import Path\n"
        f"print(Path({str(event_path)!r}).read_text(encoding='utf-8'), end='')\n",
        encoding="utf-8",
    )

    assert main(
        [
            "watch",
            "--watcher",
            sys.executable,
            "--watcher-arg",
            str(fake_watcher),
            "--duration",
            "1",
        ]
    ) == 0
    output = json.loads(capsys.readouterr().out)
    results = search_captures("deterministic capture", tmp_path / "state")

    assert output == {
        "captures_written": 1,
        "duplicates_skipped": 1,
        "denylisted_skipped": 0,
        "heartbeats": 1,
    }
    assert len(results) == 1
    assert results[0]["app_name"] == "Notepad"


def test_watch_cli_suppresses_failed_watcher_stderr(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("WINCHRONICLE_HOME", str(tmp_path / "state"))
    fake_watcher = tmp_path / "fake_failed_watcher.py"
    fake_watcher.write_text(
        "import sys\n"
        "print('Lock screen content must not echo', file=sys.stderr)\n"
        "raise SystemExit(7)\n",
        encoding="utf-8",
    )

    assert main(
        [
            "watch",
            "--watcher",
            sys.executable,
            "--watcher-arg",
            str(fake_watcher),
        ]
    ) == 1
    output = capsys.readouterr().out

    assert output.strip() == "ERROR: watcher failed with exit code 7"
    assert "Lock screen content" not in output


def test_watch_cli_suppresses_helper_failure_observed_content(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("WINCHRONICLE_HOME", str(tmp_path / "state"))
    fake_watcher = tmp_path / "fake_helper_failure_watcher.py"
    fake_watcher.write_text(
        "import sys\n"
        "print('helper stdout observed text must not echo')\n"
        "print('helper stderr observed text must not echo', file=sys.stderr)\n"
        "raise SystemExit(12)\n",
        encoding="utf-8",
    )

    assert main(
        [
            "watch",
            "--watcher",
            sys.executable,
            "--watcher-arg",
            str(fake_watcher),
            "--helper",
            sys.executable,
            "--helper-arg",
            "unused-helper-arg",
        ]
    ) == 1
    output = capsys.readouterr().out

    assert output.strip() == "ERROR: watcher failed with exit code 12"
    assert "helper stdout observed text" not in output
    assert "helper stderr observed text" not in output


def test_watch_cli_reports_malformed_watcher_jsonl(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("WINCHRONICLE_HOME", str(tmp_path / "state"))
    fake_watcher = tmp_path / "fake_malformed_watcher.py"
    fake_watcher.write_text("print('{not json')\n", encoding="utf-8")

    assert main(
        [
            "watch",
            "--watcher",
            sys.executable,
            "--watcher-arg",
            str(fake_watcher),
        ]
    ) == 1
    output = capsys.readouterr().out

    assert output.strip() == "ERROR: watcher JSONL line 1 is malformed"


def test_run_watcher_command_reports_timeout_without_stdout_leak(tmp_path):
    fake_watcher = tmp_path / "fake_slow_watcher.py"
    fake_watcher.write_text(
        "import time\n"
        "print('observed content must not echo')\n"
        "time.sleep(5)\n",
        encoding="utf-8",
    )

    try:
        run_watcher_command(
            [sys.executable, str(fake_watcher)],
            duration_seconds=0,
            timeout_seconds=0.1,
        )
    except RuntimeError as exc:
        assert str(exc) == "watcher timed out"
    else:
        raise AssertionError("watcher timeout did not raise")


def test_watcher_smoke_script_reports_missing_build_without_observed_content(tmp_path):
    missing_dll = tmp_path / "missing-watcher.dll"

    completed = subprocess.run(
        [
            sys.executable,
            "harness/scripts/run_watcher_smoke.py",
            "--watcher-dll",
            str(missing_dll),
        ],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )

    assert completed.returncode == 1
    assert completed.stdout.strip() == "FAIL: watcher DLL does not exist; run dotnet build first"
