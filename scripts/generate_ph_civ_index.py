#!/usr/bin/env python3
"""Generate docs/predictive-history-index.md from data/cards.jsonl (all ph-civ + ph-apo chapters)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from civ_ph.data import load_cards  # noqa: E402
from civ_ph.ph_civ_index import ensure_ph_civ_index  # noqa: E402


def main() -> int:
    cards = load_cards()
    md_path, json_path, written = ensure_ph_civ_index(cards, repo_root=ROOT, force=True)
    action = "wrote" if written else "unchanged"
    print(
        f"{action} {md_path.relative_to(ROOT)} and {json_path.relative_to(ROOT)} ({len(cards)} chapters)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
