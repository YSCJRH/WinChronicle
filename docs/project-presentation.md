# Project Presentation Checklist

Use this checklist when updating the GitHub repository page, launch posts, or
community descriptions. It is not a release checklist.

## Repository Description

Suggested short description:

```text
Local-first Windows UI Automation memory for AI agents
```

## Topics

Suggested GitHub topics:

```text
windows
uia
mcp
ai-agents
local-first
privacy
sqlite
developer-tools
workflow-memory
python
dotnet
```

## Social Preview

Suggested social preview copy:

```text
WinChronicle
Local-first memory for Windows AI agents
UIA context -> privacy gates -> local search -> read-only MCP
No screenshots. No keylogging. No cloud upload.
```

GitHub social preview images should be at least `640x320` pixels, with
`1280x640` preferred for sharper rendering.

The committed social preview asset is:

```text
docs/assets/winchronicle-social-preview.png
```

The committed README hero asset is:

```text
docs/assets/winchronicle-hero.png
```

Regenerate or review both assets against
[the hero prompt contract](assets/winchronicle-hero.prompt.md). The images must
not include third-party logos, real desktop screenshots, OCR/screen-recording
visuals, cloud-upload imagery, surveillance metaphors, desktop-control cues, or
official-brand implications.

## Positioning Against Codex Chronicle

Use this when a launch post or repository description needs the comparison
without putting a long table on the README first screen.

WinChronicle is independent from OpenAI. Official Codex Chronicle is a
Codex-native macOS research preview. WinChronicle is a Windows-first,
UIA-first, local-first, auditable, read-only MCP layer for agent context.

| Area | Official Codex Chronicle | WinChronicle |
| --- | --- | --- |
| Platform | Codex App research preview on macOS. | Windows-first open-source project. |
| Context source | Recent screen context. | Microsoft UI Automation metadata and explicit finite sessions. |
| Memory integration | Codex-native memories. | Local captures, SQLite search, deterministic reports, and read-only MCP. |
| Screenshots/OCR | Official docs describe selected screenshots and OCR as possible inputs. | Not implemented as the default baseline; remains off by default. |
| Local storage | Official docs describe temporary local captures and generated local memories. | Local state under `%LOCALAPPDATA%\WinChronicle` by default, or `WINCHRONICLE_HOME` for isolated demos/tests. |
| MCP interface | Not positioned as the primary Chronicle interface. | Fixed read-only MCP tool list for local context. |
| Desktop control | Not positioned as a desktop-control API. | No click/type/key/clipboard/screenshot/OCR/audio/cloud/MCP-write tools. |
| Privacy stance | Opt-in preview with sensitive-content warnings. | Redaction-first; observed content is untrusted; capture expansion needs human approval. |

## First-Time Visitor Path

Point new users to:

1. [README](../README.md)
2. [5-minute demo](quick-demo.md)
3. [Why WinChronicle](why-winchronicle.md)
4. [Privacy architecture](privacy-architecture.md)
5. [Contributing](../CONTRIBUTING.md)

## Productization Completion Note

For the final productization patch release, say:

```text
This release completes the finite v0.2 productization pass: guardrails, README
hero assets, three-path onboarding, synthetic workday examples, Codex usage
surface clarity, and compact docs navigation are now in place. It does not add
new capture surfaces or start a new maintenance loop.
```

## Good First Issue Themes

- Add deterministic UIA fixtures.
- Improve docs for common Windows developer tools.
- Add app compatibility notes without committing observed content.
- Improve fixture-only examples and MCP examples.
- Add privacy regression tests for redaction canaries.
