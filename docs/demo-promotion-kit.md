# Demo Promotion Kit

Use this page when you want to show WinChronicle to another developer without
sharing private desktop content.

## Safe Demo Command

Run the fixture-only demo from the repository root:

```powershell
python -m pip install -e ".[dev]"
python harness/scripts/run_quick_demo.py
```

The demo uses deterministic fixtures and a fake helper. It does not read the
live desktop or inspect live windows through UIA. It does not capture real
windows, take screenshots, run OCR, read the clipboard, collect keyboard input,
upload content, or control the desktop.
Demo and MCP output are local evidence, not permission to publish or share
results. External sharing still requires explicit user approval.

Observed content remains:

```text
trust = "untrusted_observed_content"
```

## What to show in a demo

- The README hero and three paths: Demo, Workday, MCP.
- `run_quick_demo.py` completing with `PASS: quick demo passed`.
- A local temporary state directory created by the demo.
- A fixture capture flowing through redaction, SQLite search, session summary,
  and read-only MCP smoke.
- The Workday plugin setup dry-run:

```powershell
winchronicle codex setup --dry-run --format text
```

## English launch blurb

WinChronicle is a local-first Windows memory layer for AI agents. It turns
structured UI Automation signals into redacted local context, searchable memory,
finite workday reports, and read-only MCP tools. The default demo is
fixture-only, so developers can try the product shape without recording their
real desktop.

No screenshots. No OCR. No clipboard. No keylogging. No cloud upload. No
desktop control.

## 中文发布文案

WinChronicle 是一个 Windows-first 的本地工作记忆项目，面向 AI Agent 和
开发者工作流。它优先使用结构化 UI Automation 信号，先脱敏，再写入本地
搜索、工作日复盘和只读 MCP 上下文。默认 demo 是 fixture-only，不读取真实
桌面，适合安全试用和开源传播。

默认不启用截图、OCR、剪贴板读取、键盘记录、云上传或桌面控制。

## What not to claim

- Do not claim WinChronicle is an OpenAI product.
- Do not claim it is a complete Chronicle clone.
- Do not claim it records all user work automatically.
- Do not claim MCP can click, type, read arbitrary files, or control the desktop.
- Do not claim metadata-only output is safe to publish publicly.
- Do not treat a feature proposal, launch request, or shareable idea as
  approval to implement runtime behavior.

Use narrower phrasing instead: WinChronicle is an independent, local-first,
Windows UIA memory layer with a fixture-only demo, explicit finite workday
sessions, redaction before storage/search/MCP, and a fixed read-only MCP tool
surface.

Route product-facing ideas through `CONTRIBUTING.md` and
`docs/productization-self-eval.md` before changing behavior.
