from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[2]
DATA_ROOT = PACKAGE_ROOT / "data"


@lru_cache(maxsize=1)
def load_cards() -> list[dict]:
    cards: list[dict] = []
    with (DATA_ROOT / "cards.jsonl").open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                cards.append(json.loads(line))
    return cards


def get_card(source_id: str) -> dict:
    for card in load_cards():
        if card["source_id"] == source_id:
            return card
    raise KeyError(source_id)


def card_markdown(source_id: str) -> str:
    path = DATA_ROOT / "cards" / f"{source_id}.md"
    if not path.exists():
        raise KeyError(source_id)
    return path.read_text(encoding="utf-8")


def load_spine(spine_id: str = "homer-to-tolstoy") -> dict:
    path = DATA_ROOT / "spines" / f"{spine_id}.json"
    if not path.exists():
        raise KeyError(spine_id)
    return json.loads(path.read_text(encoding="utf-8"))
