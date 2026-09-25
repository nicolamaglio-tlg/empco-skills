#!/usr/bin/env python3
"""Copy files from shared/ into each skill's references/, so every skill installs standalone.

  python3 scripts/sync_shared.py          write the copies
  python3 scripts/sync_shared.py --check  exit 1 if any copy is missing or out of date (used in CI)
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

TARGETS = {
    "empco-screening.md": ["empco-screener", "empco-claim-writer"],
}


def expected(name: str) -> str:
    header = f"<!-- Synced from shared/{name} by scripts/sync_shared.py. Edit the shared copy, not this one. -->\n\n"
    return header + (ROOT / "shared" / name).read_text(encoding="utf-8")


def main() -> int:
    check = "--check" in sys.argv[1:]
    stale = []
    for name, skills in TARGETS.items():
        content = expected(name)
        for skill in skills:
            dest = ROOT / skill / "references" / name
            if dest.exists() and dest.read_text(encoding="utf-8") == content:
                continue
            if check:
                stale.append(dest.relative_to(ROOT))
            else:
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_text(content, encoding="utf-8")
                print(f"synced {dest.relative_to(ROOT)}")
    if stale:
        print("Out of sync with shared/ — run `python3 scripts/sync_shared.py`:", file=sys.stderr)
        for p in stale:
            print(f"  {p}", file=sys.stderr)
        return 1
    if check:
        print("All shared copies up to date.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
