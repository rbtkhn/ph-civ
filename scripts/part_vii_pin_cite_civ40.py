#!/usr/bin/env python3
"""Insert transcript ### section anchors for civ-40 and refresh L2 refs."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTER_ID = "civ-40"
VOL2 = ROOT / "book" / "volume-ii" / CHAPTER_ID
PART7_COMMENTARY = ROOT / "book/volume-i-civilization/parts/part-07-world-after-rome-commentary.md"

TRANSCRIPT_SECTIONS: list[tuple[str, str]] = [
    ("opening-crusades-bridge", "doing the crusades"),
    ("jesus-poverty-contrast", "camel to go through"),
    ("roman-successor-church", "catholic church basically became"),
    ("salvation-orthodoxy-power", "enforce right thinking"),
    ("scapegoating-mechanism", "scapegoat"),
    ("afterlife-worldview", "happy afterlife"),
]

CLAIM_REFS: list[str] = [
    "#opening-crusades-bridge",
    "#jesus-poverty-contrast",
    "#roman-successor-church",
    "#salvation-orthodoxy-power",
    "#scapegoating-mechanism",
    "#afterlife-worldview",
]


def split_transcript_body(body: str, sections: list[tuple[str, str]]) -> str:
    body = re.sub(r"\s+", " ", body).strip() + "\n"
    lower = body.lower()
    markers: list[tuple[int, str]] = []
    search_from = 0
    for slug, phrase in sections:
        idx = lower.find(phrase.lower(), search_from)
        if idx < 0:
            raise ValueError(f"Anchor not found: {slug!r} -> {phrase[:60]!r}...")
        markers.append((idx, slug))
        search_from = idx + 1
    markers.sort(key=lambda x: x[0])
    out: list[str] = []
    pos = 0
    for idx, slug in markers:
        if idx > pos:
            chunk = body[pos:idx].rstrip()
            if chunk:
                out.append(chunk)
        out.append(f"\n\n### {slug}\n\n")
        pos = idx
    out.append(body[pos:])
    return "".join(out).strip() + "\n"


def patch_transcript() -> None:
    path = VOL2 / f"{CHAPTER_ID}-transcript.md"
    text = path.read_text(encoding="utf-8")
    if f"### {TRANSCRIPT_SECTIONS[0][0]}" in text:
        print(f"skip transcript (already sectioned): {path.relative_to(ROOT)}")
        return
    marker = "## Part I: Full transcript\n\n"
    if marker not in text:
        raise ValueError(f"Missing transcript marker in {path}")
    head, rest = text.split(marker, 1)
    body = rest.strip() + "\n"
    patched = split_transcript_body(body, TRANSCRIPT_SECTIONS)
    if "transcript_curation:" not in head:
        head = head.replace(
            "transcript_fidelity: exact_body_match\n",
            "transcript_fidelity: exact_body_match\ntranscript_curation: curated_sectioned\npin_cite_reviewed_at: 2026-06-09\n",
        )
    if "part_id:" not in head:
        head = head.replace(
            "part: I\n",
            "part: I\npart_id: part-07-world-after-rome\n"
            "part_commentary_path: ../../volume-i-civilization/parts/part-07-world-after-rome-commentary.md#civ-40\n"
            "part_bibliography_path: ../../volume-i-civilization/parts/part-07-world-after-rome-bibliography.md\n",
        )
    path.write_text(head + marker + patched, encoding="utf-8")
    print(f"patched transcript: {path.relative_to(ROOT)}")


def update_chapter_commentary() -> None:
    path = VOL2 / f"{CHAPTER_ID}-commentary.md"
    text = path.read_text(encoding="utf-8")
    for i, anchor in enumerate(CLAIM_REFS, start=1):
        new_ref = f"`{CHAPTER_ID}-transcript.md{anchor}`"
        pattern = rf"(\| {i} \|[^\n]+\| )`?{CHAPTER_ID}-transcript\.md:29`?"
        text, n = re.subn(pattern, rf"\1{new_ref}", text, count=1)
        if n == 0 and new_ref not in text:
            pattern2 = rf"(\| {i} \|[^\n]+\| )TBD pin-cite"
            text, n2 = re.subn(pattern2, rf"\1{new_ref}", text, count=1)
            if n2 == 0:
                raise ValueError(f"Row {i} not updated in {path}")
    if "analysis_depth: seed" in text:
        text = text.replace("analysis_depth: seed", "analysis_depth: layer2_drafted")
    if "part_commentary_path:" not in text:
        text = text.replace(
            "companion_transcript_path: ./civ-40-transcript.md\n",
            "companion_transcript_path: ./civ-40-transcript.md\n"
            "part_id: part-07-world-after-rome\n"
            "part_commentary_path: ../../volume-i-civilization/parts/part-07-world-after-rome-commentary.md#civ-40\n"
            "part_bibliography_path: ../../volume-i-civilization/parts/part-07-world-after-rome-bibliography.md\n",
        )
    path.write_text(text, encoding="utf-8")
    print(f"patched commentary: {path.relative_to(ROOT)}")


def update_part7_commentary() -> None:
    text = PART7_COMMENTARY.read_text(encoding="utf-8")
    for i, anchor in enumerate(CLAIM_REFS, start=1):
        new_ref = f"`{CHAPTER_ID}-transcript.md{anchor}`"
        text, n = re.subn(
            rf"(\| {i} \|[^\n]+\| )`?{CHAPTER_ID}-transcript\.md:29`?",
            rf"\1{new_ref}",
            text,
            count=1,
        )
        if n == 0 and new_ref not in text:
            raise ValueError(f"Part VII civ-40 row {i} not updated")
    text = text.replace(
        "**civ-40 predictions:** church→Dante quiet revolution **Partially supported** (pairs `civ-41`); pin-cite debt **open** (`:29` blanket refs).",
        "**civ-40 predictions:** church→Dante quiet revolution **Partially supported** (pairs `civ-41`); pin-cite **cleared** (2026-06-09).",
    )
    PART7_COMMENTARY.write_text(text, encoding="utf-8")
    print(f"patched: {PART7_COMMENTARY.relative_to(ROOT)}")


def main() -> None:
    patch_transcript()
    update_chapter_commentary()
    update_part7_commentary()
    print("part_vii_pin_cite_civ40: done")


if __name__ == "__main__":
    main()
