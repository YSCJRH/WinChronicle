from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "harness" / "fixtures" / "uia-helper" / "notepad_frontmost.json"


def main() -> int:
    print(FIXTURE.read_text(encoding="utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
