import json
import sqlite3
import subprocess
import sys
from pathlib import Path

from winchronicle.cli import main
from winchronicle.events import (
    dispatch_watcher_event_lines,
    dispatch_watcher_events,
    run_watcher_command,
)
from winchronicle.memory import generate_memory_entries
from winchronicle.mcp.server import search_memory_tool
from winchronicle.schema import validate_capture, validate_watcher_event
from winchronicle.storage import search_captures, search_memory_entries
from harness.scripts import run_watcher_smoke


ROOT = Path(__file__).resolve().parents[1]


def _raw_watcher_jsonl_files(home: Path) -> list[Path]:
    return sorted(home.rglob("*.jsonl")) if home.exists() else []


def _read_capture_files(home: Path) -> list[dict]:
    return [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted((home / "capture-buffer").glob("*.json"))
    ]


def _helper_output_from_privacy_fixture(fixture_name: str) -> dict:
    fixture_path = ROOT / "harness" / "fixtures" / "privacy" / f"{fixture_name}.json"
    output = json.loads(fixture_path.read_text(encoding="utf-8"))
    output.pop("fixture_name", None)
    output["helper_schema_version"] = 1
    output["source"] = "win-uia-helper"
    output["command"] = "capture-frontmost"
    visible_text = output.get("visible_text", "")
    node_count = 1 + len(output.get("uia_tree", {}).get("children", []))
    output["limits"] = {
        "depth": 80,
        "max_nodes": 5000,
        "max_text_chars": 20000,
        "node_count": node_count,
    }
    output["uia_stats"] = {
        "nodes_visited": node_count,
        "nodes_skipped": 0,
        "stale_nodes_skipped": 0,
        "exceptions_skipped": 0,
        "chars_collected": len(visible_text),
        "elapsed_ms": 10,
        "max_depth_observed": 1,
        "time_budget_ms": 3000,
        "time_budget_exceeded": False,
        "max_nodes_reached": False,
        "max_depth_reached": False,
        "max_chars_reached": False,
    }
    output["capture_target"] = {
        "kind": "frontmost",
        "hwnd": output["window"]["hwnd"],
        "requested_pid": None,
        "resolved_pid": output["window"]["pid"],
        "frontmost_at_capture": True,
        "harness_only": True,
    }
    output["truncated"] = False
    output["capture_surfaces"] = {
        "screenshots": False,
        "ocr": False,
        "audio": False,
        "keyboard": False,
        "clipboard": False,
        "desktop_control": False,
    }
    return output


def _title_denylisted_helper_output() -> dict:
    output = _helper_output_from_privacy_fixture("prompt_injection_visible_text")
    output["timestamp"] = "2026-04-25T13:40:03+08:00"
    output["window"]["process_name"] = "notepad.exe"
    output["window"]["exe_path"] = "C:\\Windows\\System32\\notepad.exe"
    output["window"]["app_name"] = "Notepad"
    output["window"]["title"] = "Secret recovery phrase - Notepad"
    output["focused_element"]["text"] = "title-denylisted observed text must not persist"
    output["visible_text"] = "title-denylisted observed text must not persist"
    output["url"] = None
    output["uia_stats"]["chars_collected"] = len(output["visible_text"])
    return output


def _watcher_event(
    event_id: str,
    event_type: str,
    timestamp: str,
    capture: dict,
) -> dict:
    return {
        "event_schema_version": 1,
        "source": "win-uia-watcher",
        "event_id": event_id,
        "event_type": event_type,
        "timestamp": timestamp,
        "capture": capture,
    }


def _write_privacy_parity_events(tmp_path: Path) -> Path:
    events = [
        _watcher_event(
            "privacy-password-field",
            "foreground_changed",
            "2026-04-25T13:40:00+08:00",
            _helper_output_from_privacy_fixture("password_field"),
        ),
        _watcher_event(
            "privacy-secret-canaries",
            "value_changed",
            "2026-04-25T13:40:01+08:00",
            _helper_output_from_privacy_fixture("secrets_visible_text"),
        ),
        _watcher_event(
            "privacy-prompt-injection",
            "name_changed",
            "2026-04-25T13:40:02+08:00",
            _helper_output_from_privacy_fixture("prompt_injection_visible_text"),
        ),
        _watcher_event(
            "privacy-denylisted-app",
            "foreground_changed",
            "2026-04-25T13:40:03+08:00",
            _helper_output_from_privacy_fixture("denylisted_app"),
        ),
        _watcher_event(
            "privacy-title-denylist",
            "foreground_changed",
            "2026-04-25T13:40:04+08:00",
            _title_denylisted_helper_output(),
        ),
        {
            "event_schema_version": 1,
            "source": "win-uia-watcher",
            "event_id": "privacy-heartbeat",
            "event_type": "heartbeat",
            "timestamp": "2026-04-25T13:40:05+08:00",
            "heartbeat_id": "privacy-heartbeat",
        },
    ]
    event_path = tmp_path / "privacy_parity.jsonl"
    event_path.write_text(
        "\n".join(json.dumps(event, sort_keys=True) for event in events) + "\n",
        encoding="utf-8",
    )
    return event_path


def _sqlite_text_payload(home: Path) -> str:
    db_path = home / "index.db"
    if not db_path.exists():
        return ""

    tables = ("captures", "captures_fts", "entries", "entries_fts")
    payload: list[str] = []
    with sqlite3.connect(db_path) as conn:
        for table in tables:
            exists = conn.execute(
                "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = ?",
                (table,),
            ).fetchone()
            if not exists:
                continue
            for row in conn.execute(f"SELECT * FROM {table}"):
                payload.append(json.dumps([str(value) for value in row], sort_keys=True))
    return "\n".join(payload)


def _assert_raw_terms_not_indexed(home: Path, raw_terms: tuple[str, ...]) -> None:
    capture_payload = "\n".join(
        path.read_text(encoding="utf-8")
        for path in sorted((home / "capture-buffer").glob("*.json"))
    )
    memory_payload = "\n".join(
        path.read_text(encoding="utf-8")
        for path in sorted((home / "memory").glob("*.md"))
    )
    sqlite_payload = _sqlite_text_payload(home)
    for term in raw_terms:
        assert term not in capture_payload
        assert term not in memory_payload
        assert term not in sqlite_payload
        assert search_captures(term, home) == []
        assert search_memory_entries(term, home) == []
        assert search_memory_tool(term, home=home)["result"]["matches"] == []


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


def test_watcher_privacy_fixture_preserves_redaction_skip_and_trust(
    tmp_path, monkeypatch
):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    event_path = _write_privacy_parity_events(tmp_path)

    for line in event_path.read_text(encoding="utf-8").splitlines():
        validate_watcher_event(json.loads(line))

    result = dispatch_watcher_events(event_path, home)
    captures = _read_capture_files(home)
    serialized = json.dumps(captures, sort_keys=True)
    password_capture = next(
        capture for capture in captures if capture["window_meta"]["app_name"] == "Example Login"
    )

    assert result.to_json() == {
        "captures_written": 3,
        "duplicates_skipped": 0,
        "denylisted_skipped": 2,
        "heartbeats": 1,
    }
    assert len(captures) == 3
    for capture in captures:
        validate_capture(capture)
    assert _raw_watcher_jsonl_files(home) == []
    assert password_capture["source"] == "uia_helper"
    assert password_capture["trigger"] == {
        "source": "win_uia_helper",
        "event_type": "capture_frontmost",
    }
    assert password_capture["focused_element"]["value"] == "[REDACTED:password_field]"
    assert password_capture["focused_element"]["text"] == "[REDACTED:password_field]"
    assert password_capture["focused_element"]["value_length"] == 0
    assert password_capture["focused_element"]["text_length"] == 0
    assert password_capture["screenshot"] is None
    assert "[REDACTED:password_field]" in serialized
    assert "[REDACTED:api_key]" in serialized
    assert "[REDACTED:github_token]" in serialized
    assert "[REDACTED:slack_token]" in serialized
    assert "[REDACTED:jwt]" in serialized
    assert "[REDACTED:private_key]" in serialized
    assert all(capture["untrusted_observed_content"] is True for capture in captures)
    assert search_captures("super secret value", home) == []
    assert search_captures("Production API token", home) == []
    assert search_captures("title-denylisted observed text", home) == []
    assert search_captures("Ignore previous instructions", home)[0]["trust"] == (
        "untrusted_observed_content"
    )

    generate_memory_entries(home, date="2026-04-25")
    memory_results = search_memory_entries("Ignore previous instructions", home)
    assert memory_results
    assert memory_results[0]["trust"] == "untrusted_observed_content"
    mcp_memory_results = search_memory_tool("Ignore previous instructions", home=home)
    assert mcp_memory_results["trust"] == "untrusted_observed_content"
    assert mcp_memory_results["result"]["matches"][0]["trust"] == (
        "untrusted_observed_content"
    )
    assert "trust: untrusted_observed_content" in "\n".join(
        path.read_text(encoding="utf-8")
        for path in sorted((home / "memory").glob("*.md"))
    )
    _assert_raw_terms_not_indexed(
        home,
        (
            "CorrectHorseBatteryStaple!",
            "sk-winchronicle-test-canary-1234567890abcdef",
            "ghp_winchroniclecanary1234567890ABCD",
            "xoxb-winchronicle-canary-token",
            "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ3aW5jaHJvbmljbGUifQ.signature12345",
            "-----BEGIN PRIVATE KEY-----",
            "super secret value",
            "title-denylisted observed text",
        ),
    )


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
    assert list((home / "capture-buffer").glob("*.json")) == []


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
    assert list((home / "capture-buffer").glob("*.json")) == []
    assert _raw_watcher_jsonl_files(home) == []


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


def test_watch_cli_dispatches_privacy_fixture_without_raw_jsonl(tmp_path, monkeypatch, capsys):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    event_path = _write_privacy_parity_events(tmp_path)

    assert main(
        [
            "watch",
            "--events",
            str(event_path),
        ]
    ) == 0
    output = json.loads(capsys.readouterr().out)

    assert output == {
        "captures_written": 3,
        "duplicates_skipped": 0,
        "denylisted_skipped": 2,
        "heartbeats": 1,
    }
    assert _raw_watcher_jsonl_files(home) == []
    assert search_captures("CorrectHorseBatteryStaple!", home) == []
    assert search_captures("super secret value", home) == []
    assert search_captures("title-denylisted observed text", home) == []


def test_watch_events_cli_suppresses_invalid_helper_payload_observed_content(
    tmp_path, monkeypatch, capsys
):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    canary = "OBSERVED_SECRET_SHOULD_NOT_ECHO"
    helper_output = json.loads(
        (ROOT / "harness" / "fixtures" / "uia-helper" / "notepad_frontmost.json").read_text(
            encoding="utf-8"
        )
    )
    helper_output["source"] = "unexpected-helper"
    helper_output["visible_text"] = canary
    event_path = tmp_path / "invalid_helper_event.jsonl"
    event_path.write_text(
        json.dumps(
            {
                "event_schema_version": 1,
                "source": "win-uia-watcher",
                "event_id": "invalid-helper-payload",
                "event_type": "foreground_changed",
                "timestamp": "2026-04-25T13:20:00+08:00",
                "capture": helper_output,
            },
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    assert main(["watch", "--events", str(event_path)]) == 1
    output = capsys.readouterr().out

    assert output.strip() == "ERROR: watcher output could not be captured safely"
    assert canary not in output
    assert list((home / "capture-buffer").glob("*.json")) == []
    assert _raw_watcher_jsonl_files(home) == []
    assert search_captures(canary, home) == []


def test_watch_cli_runs_fake_watcher_without_raw_event_file(tmp_path, monkeypatch, capsys):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
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
    assert _raw_watcher_jsonl_files(home) == []


def test_watch_cli_fake_watcher_privacy_stdout_without_raw_event_file(
    tmp_path, monkeypatch, capsys
):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    event_path = _write_privacy_parity_events(tmp_path)
    fake_watcher = tmp_path / "fake_privacy_watcher.py"
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

    assert output == {
        "captures_written": 3,
        "duplicates_skipped": 0,
        "denylisted_skipped": 2,
        "heartbeats": 1,
    }
    assert _raw_watcher_jsonl_files(home) == []
    _assert_raw_terms_not_indexed(
        home,
        (
            "CorrectHorseBatteryStaple!",
            "sk-winchronicle-test-canary-1234567890abcdef",
            "super secret value",
            "title-denylisted observed text",
        ),
    )


def test_watch_cli_counts_heartbeat_only_without_capture_or_raw_jsonl(
    tmp_path, monkeypatch, capsys
):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    fake_watcher = tmp_path / "fake_heartbeat_watcher.py"
    fake_watcher.write_text(
        "import json\n"
        "print(json.dumps({\n"
        "  'event_schema_version': 1,\n"
        "  'source': 'win-uia-watcher',\n"
        "  'event_id': 'heartbeat-only-cli',\n"
        "  'event_type': 'heartbeat',\n"
        "  'timestamp': '2026-04-25T13:30:01+08:00',\n"
        "  'heartbeat_id': 'heartbeat-only-cli',\n"
        "}, sort_keys=True))\n",
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

    assert output == {
        "captures_written": 0,
        "duplicates_skipped": 0,
        "denylisted_skipped": 0,
        "heartbeats": 1,
    }
    assert list((home / "capture-buffer").glob("*.json")) == []
    assert _raw_watcher_jsonl_files(home) == []


def test_watch_cli_suppresses_failed_watcher_stdout_and_stderr(
    tmp_path, monkeypatch, capsys
):
    monkeypatch.setenv("WINCHRONICLE_HOME", str(tmp_path / "state"))
    fake_watcher = tmp_path / "fake_failed_watcher.py"
    fake_watcher.write_text(
        "import sys\n"
        "print('Watcher stdout observed text must not echo')\n"
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
    assert "Watcher stdout observed text" not in output
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
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
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
    assert _raw_watcher_jsonl_files(home) == []


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


def test_watch_cli_reports_timeout_without_stdout_leak(
    tmp_path, monkeypatch, capsys
):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))

    def fake_timeout(*_args, **_kwargs):
        raise RuntimeError("watcher timed out")

    monkeypatch.setattr("winchronicle.cli.run_watcher_command", fake_timeout)

    assert main(["watch", "--watcher", sys.executable]) == 1
    output = capsys.readouterr().out

    assert output.strip() == "ERROR: watcher timed out"
    assert "observed content" not in output
    assert _raw_watcher_jsonl_files(home) == []


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


def test_watcher_smoke_default_allows_capture_startup_before_heartbeat():
    args = run_watcher_smoke.build_parser().parse_args([])

    assert args.duration_ms >= 3000
    assert args.heartbeat_ms == 250


def test_watcher_smoke_accepts_capture_startup_without_heartbeat():
    assert run_watcher_smoke._has_capture_smoke_signal(
        {
            "captures_written": 1,
            "duplicates_skipped": 0,
            "denylisted_skipped": 0,
            "heartbeats": 0,
        }
    )


def test_watcher_smoke_rejects_heartbeat_only_without_capture():
    assert not run_watcher_smoke._has_capture_smoke_signal(
        {
            "captures_written": 0,
            "duplicates_skipped": 0,
            "denylisted_skipped": 0,
            "heartbeats": 1,
        }
    )


def test_watcher_preview_docs_cover_reliability_modes_and_boundaries():
    docs = (ROOT / "docs" / "watcher-preview.md").read_text(encoding="utf-8")

    for reliability_mode in (
        "Watcher exits nonzero",
        "Helper failure surfaced by watcher",
        "Malformed watcher JSONL",
        "Invalid embedded helper payload",
        "Watcher timeout",
        "Heartbeat-only run",
        "Denylisted app or lock screen",
        "Duplicate content fingerprint",
        "Watcher privacy fixture parity",
        "Raw watcher JSONL persistence",
        "Harness smoke may stage fake-helper watcher JSONL",
    ):
        assert reliability_mode in docs

    for boundary in (
        "does not save raw watcher JSONL",
        "redaction, denylist, trust-boundary, MCP/memory-search parity",
        "explicit, time-bounded, and operator-started",
        "must not add screenshot, OCR, audio, keyboard capture, clipboard",
        "daemon, service installer, startup task",
    ):
        assert boundary in docs
