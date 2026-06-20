import json
import subprocess
import sys
from copy import deepcopy
from pathlib import Path

import pytest

from winchronicle.cli import main
from winchronicle.mcp.server import recent_activity, search_captures_tool
from winchronicle.paths import ensure_state
from winchronicle.redaction import scan_for_unredacted_secrets
from winchronicle.schema import validate_session_report, validate_watcher_event
from winchronicle.session import (
    _build_session_report,
    _error_signals,
    _write_session,
    create_monitor_session_state,
    monitor_events,
    read_session,
    run_monitor_watcher_command,
    write_monitor_session_state,
)
from test_watcher_events import _assert_raw_terms_not_indexed, _write_privacy_parity_events


ROOT = Path(__file__).resolve().parents[1]
WATCHER_FIXTURE = ROOT / "harness" / "fixtures" / "watcher" / "notepad_burst.jsonl"


def test_monitor_events_creates_session_summary_and_html_report(tmp_path, monkeypatch):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))

    for line in WATCHER_FIXTURE.read_text(encoding="utf-8").splitlines():
        validate_watcher_event(json.loads(line))

    result = monitor_events(WATCHER_FIXTURE, home, session_id="dev-loop")
    summary = result.to_json()

    validate_session_report(result.session)
    assert summary["session_id"] == "dev-loop"
    assert summary["mode"] == "events"
    assert summary["captures_written"] == 1
    assert summary["duplicates_skipped"] == 1
    assert summary["heartbeats"] == 1
    assert summary["trust"] == "untrusted_observed_content"
    assert summary["untrusted_observed_content"] is True
    assert summary["app_segments"] == [
        {
            "app_name": "Notepad",
            "title": "watcher-notes.txt - Notepad",
            "start_timestamp": "2026-04-25T13:30:00+08:00",
            "end_timestamp": "2026-04-25T13:30:00+08:00",
            "capture_count": 1,
        }
    ]
    assert "Repeated UI state was observed" in " ".join(summary["suggestions"])
    assert Path(summary["path"]).is_file()
    assert Path(summary["report_path"]).is_file()
    assert summary["storage_policy"]["raw_watcher_jsonl_saved"] is False
    assert summary["storage_policy"]["html_report_contains_visible_text"] is False
    assert summary["storage_policy"]["max_app_segments"] >= len(summary["app_segments"])
    assert summary["storage_usage"]["html_report_bytes"] > 0
    assert summary["storage_usage"]["session_json_bytes"] > 0
    assert summary["storage_usage"]["html_report_bytes"] == Path(summary["report_path"]).stat().st_size
    assert summary["storage_usage"]["session_json_bytes"] == Path(summary["path"]).stat().st_size
    assert "Watcher burst should write one deterministic capture" not in Path(
        summary["report_path"]
    ).read_text(encoding="utf-8")
    assert list(home.rglob("*.jsonl")) == []


def test_monitor_session_preserves_previous_files_when_report_replace_fails(
    tmp_path, monkeypatch
):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    old_result = write_monitor_session_state(
        home,
        session_id="daily",
        mode="workday",
        state=create_monitor_session_state(),
        operator_focus=["old focus"],
    )
    old_session_text = old_result.path.read_text(encoding="utf-8")
    old_report_text = old_result.report_path.read_text(encoding="utf-8")
    original_replace = Path.replace

    def fail_report_replace(self: Path, target_path: Path) -> Path:
        if target_path == old_result.report_path:
            raise OSError("simulated report replace failure")
        return original_replace(self, target_path)

    monkeypatch.setattr(Path, "replace", fail_report_replace)

    try:
        write_monitor_session_state(
            home,
            session_id="daily",
            mode="workday",
            state=create_monitor_session_state(),
            operator_focus=["new focus"],
        )
    except OSError:
        pass
    else:
        raise AssertionError("expected simulated report replace failure")

    assert old_result.path.read_text(encoding="utf-8") == old_session_text
    assert old_result.report_path.read_text(encoding="utf-8") == old_report_text
    assert list(home.rglob("*.tmp")) == []


def test_monitor_session_restores_previous_report_when_session_replace_fails(
    tmp_path, monkeypatch
):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    old_result = write_monitor_session_state(
        home,
        session_id="daily",
        mode="workday",
        state=create_monitor_session_state(),
        extra_suggestions=["old suggestion"],
    )
    old_session_text = old_result.path.read_text(encoding="utf-8")
    old_report_text = old_result.report_path.read_text(encoding="utf-8")
    original_replace = Path.replace

    def fail_session_replace(self: Path, target_path: Path) -> Path:
        if target_path == old_result.path:
            raise OSError("simulated session replace failure")
        return original_replace(self, target_path)

    monkeypatch.setattr(Path, "replace", fail_session_replace)

    try:
        write_monitor_session_state(
            home,
            session_id="daily",
            mode="workday",
            state=create_monitor_session_state(),
            extra_suggestions=["new suggestion"],
        )
    except OSError:
        pass
    else:
        raise AssertionError("expected simulated session replace failure")

    assert old_result.path.read_text(encoding="utf-8") == old_session_text
    assert old_result.report_path.read_text(encoding="utf-8") == old_report_text
    assert "new suggestion" not in old_result.report_path.read_text(encoding="utf-8")
    assert list(home.rglob("*.tmp")) == []


def test_monitor_session_write_failure_does_not_mutate_input_session(
    tmp_path, monkeypatch
):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    paths = ensure_state(home)
    state = create_monitor_session_state()
    session = _build_session_report(
        paths,
        session_id="daily",
        mode="workday",
        timestamps=list(state.timestamps),
        timeline=list(state.timeline),
        counts=dict(state.counts),
    )
    original_session = deepcopy(session)
    report_path = Path(session["report_path"])
    original_replace = Path.replace

    def fail_report_replace(self: Path, target_path: Path) -> Path:
        if target_path == report_path:
            raise OSError("simulated report replace failure")
        return original_replace(self, target_path)

    monkeypatch.setattr(Path, "replace", fail_report_replace)

    try:
        _write_session(paths, session)
    except OSError:
        pass
    else:
        raise AssertionError("expected simulated report replace failure")

    assert session == original_session
    assert list(home.rglob("*.tmp")) == []


def test_monitor_session_redacts_secret_like_operator_focus_before_storage(
    tmp_path, monkeypatch
):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    secret_focus = "handoff ACCESS_TOKEN=winchroniclecanary0123456789abcd"

    result = write_monitor_session_state(
        home,
        session_id="secret-focus",
        mode="workday",
        state=create_monitor_session_state(),
        operator_focus=[secret_focus],
    )
    session_text = result.path.read_text(encoding="utf-8")
    report_text = result.report_path.read_text(encoding="utf-8")

    assert "winchroniclecanary0123456789abcd" not in session_text
    assert "winchroniclecanary0123456789abcd" not in report_text
    assert "[REDACTED:api_key]" in session_text
    assert scan_for_unredacted_secrets(session_text) == []
    assert scan_for_unredacted_secrets(report_text) == []


def test_monitor_session_records_metadata_only_error_signals(tmp_path, monkeypatch):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    base_event = json.loads(WATCHER_FIXTURE.read_text(encoding="utf-8").splitlines()[0])
    event = deepcopy(base_event)
    raw_observed = (
        "pytest failed in test_payment_flow with AssertionError and "
        "ghp_winchroniclecanary1234567890ABCD"
    )
    event["event_id"] = "signal-1"
    event["timestamp"] = "2026-04-25T13:45:00+08:00"
    event["capture"]["timestamp"] = "2026-04-25T13:45:00+08:00"
    event["capture"]["visible_text"] = raw_observed
    event["capture"]["focused_element"]["text"] = "Failure panel"
    event["capture"]["uia_stats"]["chars_collected"] = len(raw_observed)
    event["capture"]["capture_target"]["hwnd"] = "0x0000000000120666"

    event_path = tmp_path / "error-events.jsonl"
    event_path.write_text(json.dumps(event) + "\n", encoding="utf-8")

    result = monitor_events(event_path, home, session_id="error-signal")
    session_text = result.path.read_text(encoding="utf-8")
    report_text = result.report_path.read_text(encoding="utf-8")

    validate_session_report(result.session)
    signals = result.session["error_signals"]
    assert signals["trust"] == "untrusted_observed_content"
    assert signals["contains_observed_text"] is False
    assert signals["total_count"] == 1
    assert signals["by_field"] == [
        {"field": "visible_text", "count": 1},
        {"field": "focused_text", "count": 1},
    ]
    assert {"keyword": "failed", "count": 1} in signals["by_keyword"]
    assert {"keyword": "failure", "count": 1} in signals["by_keyword"]
    assert signals["by_app"] == [{"app_name": "Notepad", "count": 1}]
    assert signals["time_buckets"] == [
        {"bucket_start": "2026-04-25T13:45+08:00", "count": 1}
    ]
    assert len(signals["samples"]) == 1
    sample = signals["samples"][0]
    assert sample["timestamp"] == "2026-04-25T13:45:00+08:00"
    assert sample["time_bucket"] == "2026-04-25T13:45+08:00"
    assert sample["app_name"] == "Notepad"
    assert sample["fields"] == ["visible_text", "focused_text"]
    assert sample["keywords"] == ["error", "failed", "failure"]
    assert sample["source_id"].startswith("capture-")
    assert "signal-1" not in sample["source_id"]
    assert "\\" not in sample["source_id"]
    assert "/" not in sample["source_id"]

    serialized_signals = json.dumps(signals, sort_keys=True)
    for raw_term in (
        raw_observed,
        "test_payment_flow",
        "AssertionError",
        "ghp_winchroniclecanary1234567890ABCD",
    ):
        assert raw_term not in serialized_signals
        assert raw_term not in session_text
        assert raw_term not in report_text


def test_monitor_session_does_not_leak_secret_event_id_into_paths_or_mcp(tmp_path, monkeypatch):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    base_event = json.loads(WATCHER_FIXTURE.read_text(encoding="utf-8").splitlines()[0])
    event = deepcopy(base_event)
    canary = "ghp_winchroniclecanary1234567890ABCD"
    event["event_id"] = canary
    event["timestamp"] = "2026-04-25T13:55:00+08:00"
    event["capture"]["timestamp"] = "2026-04-25T13:55:00+08:00"
    event["capture"]["visible_text"] = "event id privacy regression deterministic capture"
    event["capture"]["uia_stats"]["chars_collected"] = len(event["capture"]["visible_text"])
    event_path = tmp_path / "event-id-canary.jsonl"
    event_path.write_text(json.dumps(event) + "\n", encoding="utf-8")

    result = monitor_events(event_path, home, session_id="event-id-canary")
    capture_paths = sorted((home / "capture-buffer").glob("*.json"))
    capture_search = search_captures_tool(
        "deterministic capture",
        home=home,
        metadata_only=True,
    )
    serialized = json.dumps(
        {
            "session": result.session,
            "capture_paths": [str(path) for path in capture_paths],
            "capture_search": capture_search,
        },
        sort_keys=True,
    )

    validate_session_report(result.session)
    assert result.session["captures_written"] == 1
    assert capture_paths
    assert canary not in serialized
    assert "winchroniclecanary" not in serialized.lower()
    assert "github_token" not in serialized
    assert all(canary not in path.name for path in capture_paths)


def test_monitor_session_caps_error_signal_aggregate_rows(tmp_path, monkeypatch):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    base_event = json.loads(WATCHER_FIXTURE.read_text(encoding="utf-8").splitlines()[0])
    lines = []
    for index in range(30):
        event = deepcopy(base_event)
        hour = 8 + (index // 4)
        minute = (index % 4) * 15
        timestamp = f"2026-04-25T{hour:02d}:{minute:02d}:00+08:00"
        app_name = f"App{index:02d}"
        event["event_id"] = f"signal-{index:02d}"
        event["timestamp"] = timestamp
        event["capture"]["timestamp"] = timestamp
        event["capture"]["window"]["app_name"] = app_name
        event["capture"]["window"]["process_name"] = f"{app_name}.exe"
        event["capture"]["window"]["title"] = f"{app_name} build"
        event["capture"]["visible_text"] = f"pytest failed with error marker {index:02d}"
        event["capture"]["focused_element"]["text"] = ""
        event["capture"]["uia_stats"]["chars_collected"] = len(event["capture"]["visible_text"])
        event["capture"]["capture_target"]["hwnd"] = f"0x{index + 4096:016X}"
        lines.append(json.dumps(event))

    event_path = tmp_path / "many-error-events.jsonl"
    event_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    result = monitor_events(event_path, home, session_id="many-error-signals")
    signals = result.session["error_signals"]

    assert signals["total_count"] == 30
    assert len(signals["samples"]) == 25
    assert len(signals["by_app"]) == 25
    assert len(signals["time_buckets"]) == 25
    assert signals["sample_limit"] == 25


def test_error_signal_metadata_bounds_strings_without_raw_path_or_bad_timestamp():
    long_app = "CustomerProject" * 40
    long_timestamp = "not-a-timestamp-" + ("x" * 500)
    raw_path = "C:/state/capture-buffer/" + ("secret-project-" * 40) + ".json"

    signals = _error_signals(
        [
            {
                "timestamp": long_timestamp,
                "app_name": long_app,
                "title": "",
                "visible_text": "error while running test",
                "focused_text": "",
                "path": raw_path,
            }
        ]
    )
    serialized = json.dumps(signals, sort_keys=True)

    assert signals["total_count"] == 1
    assert len(signals["by_app"][0]["app_name"]) <= 120
    assert signals["samples"][0]["timestamp"] == ""
    assert signals["samples"][0]["time_bucket"] == ""
    assert signals["samples"][0]["source_id"] == ""
    assert long_app not in serialized
    assert long_timestamp not in serialized
    assert raw_path not in serialized


def test_monitor_cli_and_summarize_session_round_trip(tmp_path, monkeypatch, capsys):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))

    assert main(["monitor", "--events", str(WATCHER_FIXTURE), "--session-id", "dev-loop"]) == 0
    monitor_output = json.loads(capsys.readouterr().out)
    assert monitor_output["session_id"] == "dev-loop"
    assert monitor_output["captures_written"] == 1
    assert Path(monitor_output["report_path"]).is_file()

    assert main(["summarize-session", "dev-loop"]) == 0
    summary_output = json.loads(capsys.readouterr().out)
    assert summary_output["session_id"] == "dev-loop"
    assert summary_output["source_capture_paths"] == monitor_output["source_capture_paths"]

    assert main(["status"]) == 0
    status = json.loads(capsys.readouterr().out)
    assert status["session_count"] == 1


def test_monitor_cli_exclude_app_skips_operator_excluded_observed_content(
    tmp_path, monkeypatch, capsys
):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))

    assert main(
        [
            "monitor",
            "--events",
            str(WATCHER_FIXTURE),
            "--session-id",
            "excluded-notepad",
            "--exclude-app",
            "Notepad",
        ]
    ) == 0
    output = json.loads(capsys.readouterr().out)

    assert output["captures_written"] == 0
    assert output["excluded_skipped"] == 2
    assert output["heartbeats"] == 1
    assert output["source_capture_paths"] == []
    assert list((home / "capture-buffer").glob("*.json")) == []
    assert "Some windows were intentionally skipped" in " ".join(output["suggestions"])
    assert list(home.rglob("*.jsonl")) == []


def test_monitor_privacy_fixture_does_not_leak_to_session_report_or_mcp(
    tmp_path, monkeypatch
):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    event_path = _write_privacy_parity_events(tmp_path)

    result = monitor_events(event_path, home, session_id="privacy-session")
    serialized_captures = "\n".join(
        path.read_text(encoding="utf-8")
        for path in sorted((home / "capture-buffer").glob("*.json"))
    )
    session_text = result.path.read_text(encoding="utf-8")
    report_text = result.report_path.read_text(encoding="utf-8")
    activity_text = json.dumps(recent_activity(home=home, limit=5), sort_keys=True)

    assert result.session["captures_written"] == 3
    assert result.session["denylisted_skipped"] == 2
    assert result.session["heartbeats"] == 1
    assert result.session["trust"] == "untrusted_observed_content"
    assert result.session["untrusted_observed_content"] is True
    assert "[REDACTED:password_field]" in serialized_captures
    assert "[REDACTED:api_key]" in serialized_captures
    assert "[REDACTED:github_token]" in serialized_captures
    assert "Some windows were intentionally skipped" in " ".join(result.session["suggestions"])
    assert list(home.rglob("*.jsonl")) == []

    for raw_term in (
        "CorrectHorseBatteryStaple!",
        "sk-winchronicle-test-canary-1234567890abcdef",
        "ghp_winchroniclecanary1234567890ABCD",
        "xoxb-winchronicle-canary-token",
        "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ3aW5jaHJvbmljbGUifQ.signature12345",
        "-----BEGIN PRIVATE KEY-----",
        "super secret value",
        "title-denylisted observed text",
    ):
        assert raw_term not in serialized_captures
        assert raw_term not in session_text
        assert raw_term not in report_text
        assert raw_term not in activity_text

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


def test_monitor_cli_watcher_command_creates_session_without_raw_jsonl(
    tmp_path, monkeypatch, capsys
):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    fake_watcher = tmp_path / "fake_watcher.py"
    fake_watcher.write_text(
        "\n".join(
            [
                "from pathlib import Path",
                f"print(Path({str(WATCHER_FIXTURE)!r}).read_text(encoding='utf-8'), end='')",
            ]
        ),
        encoding="utf-8",
    )

    assert (
        main(
            [
                "monitor",
                "--watcher",
                sys.executable,
                "--watcher-arg",
                str(fake_watcher),
                "--duration",
                "0",
                "--heartbeat-ms",
                "250",
                "--session-id",
                "fake-watch",
            ]
        )
        == 0
    )
    output = json.loads(capsys.readouterr().out)

    assert output["session_id"] == "fake-watch"
    assert output["mode"] == "watcher"
    assert output["captures_written"] == 1
    assert output["duplicates_skipped"] == 1
    assert output["heartbeats"] == 1
    assert list(home.rglob("*.jsonl")) == []


def test_monitor_cli_watcher_failure_does_not_echo_raw_output(
    tmp_path, monkeypatch, capsys
):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    fake_watcher = tmp_path / "bad_watcher.py"
    fake_watcher.write_text("print('api_key=WINCHRONICLE_SECRET_CANARY')\n", encoding="utf-8")

    assert (
        main(
            [
                "monitor",
                "--watcher",
                sys.executable,
                "--watcher-arg",
                str(fake_watcher),
                "--duration",
                "0",
                "--session-id",
                "bad-watch",
            ]
        )
        == 1
    )
    output = capsys.readouterr().out

    assert "ERROR:" in output
    assert "api_key" not in output
    assert "WINCHRONICLE_SECRET_CANARY" not in output


def test_monitor_cli_real_watcher_slow_helper_writes_session_without_leak(
    tmp_path, monkeypatch, capsys
):
    watcher_dll = (
        ROOT
        / "resources"
        / "win-uia-watcher"
        / "bin"
        / "Debug"
        / "net8.0-windows"
        / "win-uia-watcher.dll"
    )
    if not watcher_dll.exists():
        pytest.skip("watcher DLL does not exist; run dotnet build first")

    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    canary = "SLOW_HELPER_OBSERVED_CONTENT_MUST_NOT_ECHO"
    slow_helper = tmp_path / "slow_helper.py"
    slow_helper.write_text(
        "import sys, time\n"
        "time.sleep(10)\n"
        f"print({canary!r})\n"
        f"print({canary!r}, file=sys.stderr)\n",
        encoding="utf-8",
    )

    assert (
        main(
            [
                "monitor",
                "--watcher",
                "dotnet",
                "--watcher-arg",
                str(watcher_dll),
                "--helper",
                sys.executable,
                "--helper-arg",
                str(slow_helper),
                "--duration",
                "1",
                "--heartbeat-ms",
                "250",
                "--capture-on-start",
                "--session-id",
                "slow-helper",
            ]
        )
        == 0
    )
    output_text = capsys.readouterr().out
    output = json.loads(output_text)
    session_text = Path(output["path"]).read_text(encoding="utf-8")
    report_text = Path(output["report_path"]).read_text(encoding="utf-8")

    assert output["session_id"] == "slow-helper"
    assert output["mode"] == "watcher"
    assert output["captures_written"] == 0
    assert output["source_capture_paths"] == []
    assert Path(output["path"]).is_file()
    assert Path(output["report_path"]).is_file()
    assert list(home.rglob("*.jsonl")) == []
    assert canary not in output_text
    assert canary not in session_text
    assert canary not in report_text
    assert list((home / "capture-buffer").glob("*.json")) == []


def test_run_monitor_watcher_command_formats_windows_status_without_output_leak(monkeypatch):
    def fake_run(command, **_kwargs):
        return subprocess.CompletedProcess(
            command,
            3221226505,
            stdout="monitor stdout observed text must not echo",
            stderr="monitor stderr observed text must not echo",
        )

    monkeypatch.setattr("winchronicle.session.subprocess.run", fake_run)

    try:
        run_monitor_watcher_command([sys.executable])
    except RuntimeError as exc:
        message = str(exc)
    else:
        raise AssertionError("monitor watcher status failure did not raise")

    assert message == "watcher failed with exit code 3221226505 (windows_status=0xC0000409)"
    assert "monitor stdout observed text" not in message
    assert "monitor stderr observed text" not in message


def test_read_session_accepts_session_id_only(tmp_path, monkeypatch):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    result = monitor_events(WATCHER_FIXTURE, home, session_id="path-check")

    by_id = read_session("path-check", home)

    assert by_id == result.session
    assert main(["summarize-session", str(result.path)]) == 1
