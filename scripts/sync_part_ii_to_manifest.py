#!/usr/bin/env python3
"""Merge Part II (civ-07..13) pin-cite SSOT into volume-i-anchors.yaml."""

from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "pin-cite" / "volume-i-anchors.yaml"
VOL2 = ROOT / "book" / "volume-ii"
PART_ID = "part-02-hellenic-world"

# SSOT: part_ii_tier_b_uplift.py + part_ii_iii_pin_cite_sweep.py
from part_ii_tier_b_uplift import (  # noqa: E402
    CHAPTER_CLAIM_REFS as TIER_B_CLAIMS,
    TRANSCRIPT_SECTIONS as TIER_B_SECTIONS,
)
from part_ii_iii_pin_cite_sweep import (  # noqa: E402
    CHAPTER_CLAIM_REFS as SWEEP_CLAIMS,
    TRANSCRIPT_SECTIONS as SWEEP_SECTIONS,
)

PART_II_CHAPTERS = [
    "civ-07",
    "civ-08",
    "civ-09",
    "civ-10",
    "civ-11",
    "civ-12",
    "civ-13",
]

L2_REF_RE = re.compile(
    r"^\|\s*\d+\s*\|[^\n]+\|\s*`[^`]*#([a-z0-9-]+)`",
    re.MULTILINE,
)


def sections_for(chapter_id: str) -> list[dict[str, str]]:
    pairs = TIER_B_SECTIONS.get(chapter_id) or SWEEP_SECTIONS.get(chapter_id)
    if not pairs:
        raise KeyError(f"no TRANSCRIPT_SECTIONS for {chapter_id}")
    return [{"slug": slug, "phrase": phrase} for slug, phrase in pairs]


def claim_refs_from_commentary(chapter_id: str) -> list[str]:
    path = VOL2 / chapter_id / f"{chapter_id}-commentary.md"
    text = path.read_text(encoding="utf-8")
    start = text.find("### Major Claims")
    if start < 0:
        raise ValueError(f"no Major Claims in {path}")
    block = text[start:]
    end = block.find("### Core Concepts")
    if end >= 0:
        block = block[:end]
    refs = [f"#{m.group(1)}" for m in L2_REF_RE.finditer(block)]
    if refs:
        return refs
    fallback = TIER_B_CLAIMS.get(chapter_id) or SWEEP_CLAIMS.get(chapter_id)
    if fallback:
        return fallback
    raise ValueError(f"no claim refs for {chapter_id}")


def build_entry(chapter_id: str) -> dict:
    sections = sections_for(chapter_id)
    claim_refs = claim_refs_from_commentary(chapter_id)
    slugs = {row["slug"] for row in sections}
    for ref in claim_refs:
        slug = ref.lstrip("#")
        if slug not in slugs:
            raise ValueError(f"{chapter_id}: claim ref {ref} not in section slugs")
    return {
        "part_id": PART_ID,
        "sections": sections,
        "claim_refs": claim_refs,
    }


def ordered_chapters(chapters: dict) -> dict:
    """Keep civ-01..06, insert Part II, then remaining keys sorted."""
    keys = list(chapters.keys())
    part_ii = PART_II_CHAPTERS
    before = [k for k in keys if k < "civ-07" and k not in part_ii]
    after = [k for k in keys if k not in before and k not in part_ii]
    ordered_keys = before + part_ii + sorted(after)
    return {k: chapters[k] for k in ordered_keys if k in chapters}


def main() -> int:
    if yaml is None:
        print("PyYAML required", file=sys.stderr)
        return 1
    data = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    chapters = data.setdefault("chapters", {})
    for cid in PART_II_CHAPTERS:
        chapters[cid] = build_entry(cid)
        print(f"synced {cid}: {len(chapters[cid]['sections'])} sections, "
              f"{len(chapters[cid]['claim_refs'])} claim_refs")
    data["chapters"] = ordered_chapters(chapters)
    MANIFEST.write_text(
        yaml.dump(data, sort_keys=False, allow_unicode=True, default_flow_style=False),
        encoding="utf-8",
        newline="\n",
    )
    print(f"sync_part_ii_to_manifest: wrote {MANIFEST.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
