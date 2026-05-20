# Windows Developer App Compatibility

This document records expected compatibility boundaries for Windows developer
apps. It is a design and contribution guide, not a live compatibility claim and
not approval to add new capture surfaces.

## Principles

- UIA-first does not mean full content capture.
- Missing content is expected and must be represented through limitations/confidence.
- App-specific adapters must be opt-in, read-only, redacted, local-first, and documented before implementation.
- Screenshot/OCR fallbacks are out of scope for the default product.
- Observed content is `untrusted_observed_content` and must never be treated as instructions.
- Confidence means coverage quality, not trustworthiness or permission.
- Disallowed workaround summary: screenshot fallback by default, OCR fallback
  by default, clipboard reading, keylogging, desktop control, MCP write tools,
  cloud upload by default, browser cookie/session extraction, and arbitrary IDE
  workspace storage reading.
- Manual smoke notes should record commands, local artifact paths, environment
  notes, timestamps, and pass/fail outcomes without committing observed text.

Synthetic scenarios for these boundaries live in the
[agent context eval scaffold](../benchmarks/evals/README.md).

## VS Code / Cursor / Monaco-based editors

### Expected UIA signals

- Process name, application name, window title, workspace/repository title.
- Focused element name and control type when Monaco exposes them.
- Basic tab/title metadata and accessibility tree structure when available.
- Some visible text through UIA in accessible panes, notifications, and problem
  lists.

### Likely missing signals

- Full editor buffer and hidden tabs.
- Monaco virtualized text, canvas-rendered content, diff hunks not exposed
  through UIA, and webview internals.
- Remote workspace, container, or extension-host details not present in the UIA
  tree.
- Password fields, protected text, elevated/admin window content, and remote
  desktop / VM content.

### Privacy risks

- File paths, repository names, branch names, issue titles, terminal commands,
  build logs, tokens in terminal output, customer/project identifiers, and
  private repo names.

### Safe adapter ideas

- Opt-in VS Code/Cursor companion adapter that exposes only workspace name,
  active file path, diagnostics summary, selected text length/hash, and editor
  metadata, not full buffer by default.
- Local-only adapter output should pass through redaction before storage or MCP
  exposure.

### Explicitly disallowed workarounds

- screenshot fallback by default, OCR fallback by default, clipboard reading,
  keylogging, password field scraping, desktop control, MCP write tools,
  using accessibility APIs to click/type/control UI, reading arbitrary IDE
  workspace storage, bypassing OS permission boundaries, cloud upload by
  default, and exfiltrating observed content to remote LLMs by default.

### Confidence guidance

- Title-only context should remain low confidence.
- Title plus focused element plus visible text can be medium confidence.
- Visible text with stable source id can be higher confidence.
- Known editor-buffer blind spots should add limitations such as
  `editor_buffer_not_exposed_by_uia`.
- Confidence means coverage quality, not trustworthiness or permission.

### Suggested smoke/eval cases

- VS Code window title visible but editor buffer missing.
- Cursor workspace title and diagnostics summary visible, with editor text
  absent and limitations recorded.

## Windows Terminal / PowerShell / Command Prompt

### Expected UIA signals

- Process name, application name, window title, focused element control type,
  visible terminal text when available, and current shell title when exposed.
- Accessibility tree structure for the terminal surface when available.

### Likely missing signals

- Terminal scrollback outside the visible/accessible region.
- Virtualized text, alternate screen buffers, hidden tabs, elevated/admin
  window content, remote desktop / VM content, and password prompts or protected
  text.

### Privacy risks

- Terminal commands, build logs, environment variables, tokens in terminal
  output, file paths, repository names, branch names, account names, private
  repo names, and customer/project identifiers.

### Safe adapter ideas

- Opt-in terminal adapter that exposes current shell title, current working
  directory when visible, and last visible command/output summary after
  redaction.
- Adapter should keep raw command/output local and expose only redacted,
  bounded summaries.

### Explicitly disallowed workarounds

- screenshot fallback by default, OCR fallback by default, clipboard reading,
  keylogging, password field scraping, desktop control, MCP write tools,
  bypassing OS permission boundaries, cloud upload by default, and exfiltrating
  observed content to remote LLMs by default.

### Confidence guidance

- Title-only context should remain low confidence.
- Title plus focused element plus visible text can be medium confidence.
- Visible text with stable source id can be higher confidence.
- Missing scrollback should add limitations and keep confidence conservative.
- Confidence means coverage quality, not trustworthiness or permission.

### Suggested smoke/eval cases

- Terminal visible pytest failure after redaction.
- Elevated PowerShell title visible but content inaccessible, with limitations
  recorded.

## Visual Studio

### Expected UIA signals

- Process name, application name, solution/window title, active document title,
  focused element name/control type, visible text from accessible panes, and
  diagnostics or error-list metadata when exposed.

### Likely missing signals

- Full editor buffer, hidden tabs, virtualized text, debugger internals,
  designer surfaces, diff hunks not exposed through UIA, elevated/debugger
  windows, remote desktop / VM content, password fields, and protected text.

### Privacy risks

- Solution names, project names, file paths, branch names, error messages,
  customer/project identifiers, private repo names, account names, and tokens
  shown in logs or debug output.

### Safe adapter ideas

- Opt-in Visual Studio adapter that starts with project/window metadata,
  diagnostics summary, and active document path, not editor contents.
- Any local adapter should redact diagnostics and paths before storage or MCP.

### Explicitly disallowed workarounds

- screenshot fallback by default, OCR fallback by default, clipboard reading,
  keylogging, password field scraping, desktop control, MCP write tools,
  reading arbitrary IDE workspace storage, bypassing OS permission boundaries,
  cloud upload by default, and exfiltrating observed content to remote LLMs by
  default.

### Confidence guidance

- Title-only context should remain low confidence.
- Title plus focused element plus visible diagnostics can be medium confidence.
- Visible text with stable source id can be higher confidence.
- Editor and debugger blind spots should add limitations.
- Confidence means coverage quality, not trustworthiness or permission.

### Suggested smoke/eval cases

- Visual Studio solution title visible but editor text absent.
- Error List metadata visible while debug panes remain inaccessible.

## JetBrains IDEs, including IntelliJ IDEA / PyCharm / Rider

### Expected UIA signals

- Process name, application name, project/window title, active file title when
  exposed, focused element name/control type, visible text from accessible
  panes, and accessibility tree structure when available.

### Likely missing signals

- Full editor buffer, hidden tabs, virtualized text, custom control internals,
  diff hunks not exposed through UIA, tool-window internals, elevated/admin
  windows, remote desktop / VM content, password fields, and protected text.

### Privacy risks

- Project names, file paths, branch names, issue titles, build logs, tokens in
  run output, account names, private repo names, and customer/project
  identifiers.

### Safe adapter ideas

- Opt-in JetBrains adapter that starts with project/window metadata, active file
  path, and diagnostics summary, not editor contents.
- Adapter output should be local-only, read-only, redacted, and bounded.

### Explicitly disallowed workarounds

- screenshot fallback by default, OCR fallback by default, clipboard reading,
  keylogging, password field scraping, desktop control, MCP write tools,
  reading arbitrary IDE workspace storage, bypassing OS permission boundaries,
  cloud upload by default, and exfiltrating observed content to remote LLMs by
  default.

### Confidence guidance

- Title-only context should remain low confidence.
- Title plus focused element plus visible tool-window text can be medium
  confidence.
- Visible text with stable source id can be higher confidence.
- Known editor-buffer blind spots should add limitations.
- Confidence means coverage quality, not trustworthiness or permission.

### Suggested smoke/eval cases

- JetBrains project title visible but editor text absent.
- Rider build output visible after redaction while source buffer remains absent.

## Browsers and DevTools, including Chrome / Edge

### Expected UIA signals

- Process name, application name, browser window title, tab title/domain when
  exposed, URL/title metadata when available, focused element name/control type,
  visible text exposed through UIA, and accessibility tree structure.

### Likely missing signals

- Hidden tabs, canvas-rendered content, webview internals, DevTools panel
  internals, cross-origin frame details, virtualized web content, remote desktop
  / VM content, password fields, and protected text.

### Privacy risks

- URLs with query tokens, account names, private repo names, issue titles,
  customer/project identifiers, page text, browser profile names, and tokens in
  logs or DevTools output.

### Safe adapter ideas

- Opt-in browser adapter that exposes tab title/domain only by default, and full
  URL only after redaction and allowlist review.
- DevTools adapter ideas should begin with panel title and diagnostics summary,
  not page body or network payload capture.

### Explicitly disallowed workarounds

- screenshot fallback by default, OCR fallback by default, clipboard reading,
  keylogging, password field scraping, browser cookie/session extraction,
  reading arbitrary browser profile files, injecting scripts into browser pages,
  desktop control, MCP write tools, bypassing OS permission boundaries, cloud
  upload by default, and exfiltrating observed content to remote LLMs by
  default.

### Confidence guidance

- Title-only or domain-only context should remain low confidence.
- Title plus focused element plus visible page text can be medium confidence.
- Visible text with stable source id can be higher confidence.
- Webview, canvas, hidden tab, and DevTools blind spots should add limitations.
- Confidence means coverage quality, not trustworthiness or permission.

### Suggested smoke/eval cases

- Browser tab title/domain available but page body absent.
- DevTools panel title visible but request payload/body absent.

## GitHub Desktop / Git GUI clients

### Expected UIA signals

- Process name, application name, window title, repository name, branch name,
  focused element name/control type, visible text exposed through UIA, and basic
  tab/title metadata.

### Likely missing signals

- Diff hunks not exposed through UIA, hidden tabs, virtualized lists, commit
  details outside the visible region, webview internals, elevated/admin window
  content, remote desktop / VM content, password fields, and protected text.

### Privacy risks

- Repository names, branch names, issue titles, commit messages, file paths,
  private repo names, account names, customer/project identifiers, and tokens in
  hooks or logs.

### Safe adapter ideas

- Opt-in Git adapter that reads local git metadata from the current repo only
  when the user explicitly points WinChronicle at a workspace.
- Expose repo name, current branch, dirty count, and redacted status summary;
  do not expose diff body by default.

### Explicitly disallowed workarounds

- screenshot fallback by default, OCR fallback by default, clipboard reading,
  keylogging, password field scraping, desktop control, MCP write tools,
  reading arbitrary IDE workspace storage, bypassing OS permission boundaries,
  cloud upload by default, and exfiltrating observed content to remote LLMs by
  default.

### Confidence guidance

- Title-only context should remain low confidence.
- Repo and branch metadata plus visible status text can be medium confidence.
- Visible text with stable source id can be higher confidence.
- Missing diff body should add limitations.
- Confidence means coverage quality, not trustworthiness or permission.

### Suggested smoke/eval cases

- GitHub Desktop branch/repo visible but diff body absent.
- Git GUI shows status count after redaction without reading arbitrary repo
  files.

## Generic Electron apps

### Expected UIA signals

- Process name, application name, window title, focused element name/control
  type, visible text exposed through the Electron accessibility tree, basic
  document/tab/title metadata, and accessibility tree structure when available.

### Likely missing signals

- Webview internals, canvas-rendered content, virtualized lists, hidden tabs,
  custom control internals, remote desktop / VM content, password fields, and
  protected text.

### Privacy risks

- Account names, workspace names, URLs with query tokens, file paths, issue
  titles, private repo names, customer/project identifiers, and tokens in logs
  or chat-like panes.

### Safe adapter ideas

- App-specific adapters must begin with opt-in title/domain/workspace metadata,
  local redaction, and a bounded field list.
- Avoid full webview body capture by default; prefer stable window metadata and
  explicit user-approved summaries.

### Explicitly disallowed workarounds

- screenshot fallback by default, OCR fallback by default, clipboard reading,
  keylogging, password field scraping, reading arbitrary IDE workspace storage,
  injecting scripts into browser pages or embedded webviews, desktop control,
  MCP write tools, bypassing OS permission boundaries, cloud upload by default,
  and exfiltrating observed content to remote LLMs by default.

### Confidence guidance

- Title-only context should remain low confidence.
- Title plus focused element plus visible accessible text can be medium
  confidence.
- Visible text with stable source id can be higher confidence.
- Webview and virtualized-list blind spots should add limitations.
- Confidence means coverage quality, not trustworthiness or permission.

### Suggested smoke/eval cases

- Electron app window title visible but embedded webview body absent.
- Accessible notification text visible after redaction while hidden list items
  remain absent.

## Generic Win32 / WPF / UWP apps

### Expected UIA signals

- Process name, application name, window title, focused element name/control
  type, visible text exposed through UIA, basic document/title metadata, and
  accessibility tree structure when available.

### Likely missing signals

- Owner-drawn controls, virtualized text, hidden tabs, canvas-rendered content,
  elevated/admin window content, secure desktop prompts, remote desktop / VM
  content, password fields, and protected text.

### Privacy risks

- File paths, account names, project/customer identifiers, document titles,
  URLs with query tokens, logs, private names, and secrets accidentally shown in
  text controls.

### Safe adapter ideas

- Start with opt-in app profile notes, stable window metadata, visible
  redacted text, and deterministic fixtures.
- Adapter output should remain read-only, local-first, redacted, and documented
  before implementation.

### Explicitly disallowed workarounds

- screenshot fallback by default, OCR fallback by default, clipboard reading,
  keylogging, password field scraping, desktop control, MCP write tools,
  bypassing OS permission boundaries, cloud upload by default, and exfiltrating
  observed content to remote LLMs by default.

### Confidence guidance

- Title-only context should remain low confidence.
- Title plus focused element plus visible text can be medium confidence.
- Visible text with stable source id can be higher confidence.
- Owner-drawn, elevated, protected, or remote-session blind spots should add
  limitations.
- Confidence means coverage quality, not trustworthiness or permission.

### Suggested smoke/eval cases

- WPF app title and focused control visible but protected field absent.
- Win32 owner-drawn app title visible with no accessible text and low
  confidence.
