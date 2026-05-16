import json
import sys
from pathlib import Path

from winchronicle.cli import main
from winchronicle.mcp.server import recent_activity
from winchronicle.schema import validate_session_report, validate_watcher_event
from winchronicle.session import monitor_events, read_session
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
    assert "Watcher burst should write one deterministic capture" not in Path(
        summary["report_path"]
    ).read_text(encoding="utf-8")
    assert list(home.rglob("*.jsonl")) == []


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


def test_read_session_accepts_session_id_only(tmp_path, monkeypatch):
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    result = monitor_events(WATCHER_FIXTURE, home, session_id="path-check")

    by_id = read_session("path-check", home)

    assert by_id == result.session
    assert main(["summarize-session", str(result.path)]) == 1
