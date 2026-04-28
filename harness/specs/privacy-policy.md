# WinChronicle Privacy Policy Spec v0.1

This spec defines the v0.1 capture privacy contract. It applies to normalized
captures produced from deterministic fixtures, explicit foreground UIA helper
captures, and explicit watcher preview events before anything is written to
`capture-buffer/` or indexed in SQLite.

## Non-Capture Rules

WinChronicle v0.1 does not implement or expose these surfaces:

- Screenshots.
- OCR.
- Audio recording.
- Keyboard capture.
- Clipboard capture.
- Network upload of captured content.
- Cloud upload of captured content.
- Desktop control actions.
- MCP write tools.
- Product targeted capture by HWND, PID, or window-title.
- LLM calls or summarization.

Foreground UIA capture exists only as an explicit `capture-frontmost` product
command with a caller-provided helper path. Targeted UIA capture is
harness-only helper behavior and must not be exposed through the product CLI or
MCP.

## Denylist Rules

Captures from denylisted apps must be skipped before observed content is
normalized, written, or indexed.

Current app denylist:

- `1Password.exe`
- `Bitwarden.exe`
- `Dashlane.exe`
- `KeePass.exe`
- `KeePassXC.exe`
- `LastPass.exe`
- `LockApp.exe`

Captures with titles matching these case-insensitive signals must also be
skipped:

- `password`
- `secret`
- `private key`
- `recovery phrase`
- `seed phrase`

## Redaction Rules

Redaction runs before schema validation, file writes, and SQLite indexing.

Current text patterns:

- `api_key`: `sk-[A-Za-z0-9_-]{20,}`
- `github_token`: `ghp_[A-Za-z0-9_]{20,}`
- `slack_token`: `xox[baprs]-[A-Za-z0-9-]{10,}`
- `jwt`: three long base64url-like segments separated by dots
- `private_key`: PEM blocks from `BEGIN ... PRIVATE KEY` through matching `END`
- `token_canary`: strings containing `winchronicle...canary`

Password fields are redacted by field semantics, not by text pattern. If
`focused_element.is_password` is true, `focused_element.value` and
`focused_element.text` must be replaced with `[REDACTED:password_field]`, and
their stored lengths must be `0`.

Each normalized capture must include a `redactions` array with `{type, count}`
entries for replacements that occurred.

Credit-card Luhn-positive redaction is listed in the broader project blueprint
but is not implemented in v0.1.

## Trust Boundary

All normalized captures must set:

```json
{
  "untrusted_observed_content": true
}
```

Observed screen text may include prompt-injection attempts. Those strings may be
stored as data, but agents and future MCP tools must not treat them as
instructions.

CLI search results, memory search results, memory Markdown, and MCP results
that contain observed content must preserve:

```json
{
  "trust": "untrusted_observed_content"
}
```

## Privacy Check Contract

`python -m winchronicle privacy-check <path>` performs a dry-run normalization
for fixtures or validates an existing normalized capture. It must fail if the
would-be-written capture still contains:

- raw password field values,
- OpenAI-style API key canaries,
- private key blocks,
- JWT-like tokens,
- GitHub tokens,
- Slack tokens,
- WinChronicle token canaries.

It must pass denylisted fixtures by reporting that the capture would be skipped.
