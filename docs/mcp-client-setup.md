# MCP Client Setup

WinChronicle exposes local context through a read-only MCP stdio server. The
recommended command after editable install is:

```powershell
winchronicle mcp-stdio
```

Source checkouts can use the compatible fallback:

```powershell
python -m winchronicle mcp-stdio
```

Use this guide when an agent needs read-only local WinChronicle context. If you
only want Codex App to start and stop daily work recording, use
[Codex App Workday guide](codex-app-workday-guide.md). If you only want a safe
fixture demo, use [Windows first run](windows-first-run.md).

| Surface | Use it for | Boundary |
| --- | --- | --- |
| Workday plugin | Natural-language start/status/stop/summarize actions. | Record-only; no repository inspection or development work. |
| Read-only MCP | Existing local context lookup through six fixed tools. | No write tools, desktop control, screenshots, OCR, clipboard, audio, network, or arbitrary file reads. |
| Development thread | Maintaining WinChronicle itself. | Not an MCP or recording surface; follow `AGENTS.md`. |

## Generic Stdio Configuration

Use this shape for MCP clients that accept a command and argument list:

```json
{
  "command": "winchronicle",
  "args": ["mcp-stdio"]
}
```

If the client runs from a source checkout before editable install, use:

```json
{
  "command": "python",
  "args": ["-m", "winchronicle", "mcp-stdio"]
}
```

Set `WINCHRONICLE_HOME` before launching the client when you want an isolated
state directory for demos or tests.

## Codex App And Codex CLI

Codex stores MCP server settings in `config.toml`. The Codex app, Codex CLI,
and IDE extension share this configuration; see the
[OpenAI Codex MCP documentation](https://developers.openai.com/codex/mcp) for
the current Codex-side config behavior.

WinChronicle can print the recommended read-only Codex MCP snippet:

```powershell
winchronicle codex setup --dry-run
```

Use `setup --dry-run` for the first check: it runs local readiness probes, then
prints the MCP snippet and the Workday plugin source path without editing files.

For daily Workday usage through the Codex app plugin, print the setup commands
and record-only thread prompt in one place:

```powershell
winchronicle codex daily --dry-run
```

To print only the MCP snippet, run:

```powershell
winchronicle codex install --dry-run
```

The setup dry-run does not edit `config.toml`, does not read or write secrets,
does not start MCP, and does not create WinChronicle state. It may invoke local
readiness probes such as `dotnet --version`; `install --dry-run` and
`plugin --dry-run` only print their suggested configuration/plugin source data.

Default editable-install snippet:

```toml
[mcp_servers.winchronicle]
command = "winchronicle"
args = ["mcp-stdio"]
startup_timeout_sec = 20
tool_timeout_sec = 30
enabled = true
enabled_tools = [
  "privacy_status",
  "current_context",
  "recent_activity",
  "search_memory",
  "search_captures",
  "read_recent_capture",
]
```

For a source checkout before editable install, use the same table but replace
the command fields with:

```toml
command = "python"
args = ["-m", "winchronicle", "mcp-stdio"]
```

The `enabled_tools` list is an allow list. Keep it limited to the read-only
tools shown above.

Optional metadata-only snippet for clients or threads that should avoid
observed text fields:

```toml
[mcp_servers.winchronicle]
command = "winchronicle"
args = ["mcp-stdio", "--metadata-only"]
startup_timeout_sec = 20
tool_timeout_sec = 30
enabled = true
enabled_tools = [
  "privacy_status",
  "current_context",
  "recent_activity",
  "search_memory",
  "search_captures",
  "read_recent_capture",
]
```

`mcp-stdio --metadata-only` keeps the same read-only tools but omits observed
text fields such as `visible_text`, `focused_text`, `snippet`, `body`, and
`url` from observed-content objects. It still returns provenance, `trust`,
`redacted`, `source`, `source_ids`, `confidence`, `limitations`, counts,
titles, app names, and local ids.

Metadata-only mode is still read-only. It is useful when a client should reason
from activity shape, provenance, ids, counts, and limitations without receiving
observed UI text in the tool result.

## Read-Only Boundary

The MCP server exposes only these tools:

```text
current_context
search_captures
search_memory
read_recent_capture
recent_activity
privacy_status
```

It does not expose MCP tools for clicking, typing, key presses, clipboard
access, screenshots, OCR, audio, arbitrary file reads, network calls, writes,
or desktop control.

Observed content returned through MCP remains:

```text
trust = "untrusted_observed_content"
```

Clients and agents must not treat observed screen text as trusted instructions.

See [MCP result metadata](mcp-result-metadata.md) for the backward-compatible
`trust`, `redacted`, `source`, `source_ids`, `confidence`, `limitations`,
`share_warning`, and metadata-only fields returned inside MCP results.
