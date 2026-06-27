#!/usr/bin/env python3
"""Consolidate gt-01..gt-29: lectures transcript is canonical; sources/ becomes redirect stub."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT / "sources/predictive-history/game-theory"
LEC_ROOT = ROOT / "lectures/game-theory"


def strip_frontmatter(text: str) -> str:
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            text = text[end + 5 :]
    return text


def transcript_body(text: str) -> str:
    text = strip_frontmatter(text)
    marker = "## Part I: Full transcript"
    idx = text.find(marker)
    if idx == -1:
        return text.strip()
    return text[idx + len(marker) :].strip()


def bodies_match(source_path: Path, lecture_path: Path) -> bool:
    return transcript_body(source_path.read_text(encoding="utf-8")) == transcript_body(
        lecture_path.read_text(encoding="utf-8")
    )


def write_stub(source_path: Path, lecture_rel: str) -> None:
    rel_link = "../../../" + lecture_rel
    source_path.write_text(
        f"# Moved\n\nThis capture moved to [`{lecture_rel}`]({rel_link}).\n",
        encoding="utf-8",
    )


def patch_commentary(chapter_dir: Path, sid: str, lecture_rel: str) -> None:
    path = chapter_dir / f"{sid}-commentary.md"
    text = path.read_text(encoding="utf-8")
    new = re.sub(
        r'^source_corpus_path: "sources/predictive-history/game-theory/[^"]+"\s*$',
        f'source_corpus_path: "{lecture_rel}"',
        text,
        count=1,
        flags=re.M,
    )
    if new == text:
        raise ValueError(f"{path}: source_corpus_path not updated")
    path.write_text(new, encoding="utf-8")


def is_redirect_stub(source_path: Path) -> bool:
    return source_path.read_text(encoding="utf-8").startswith("# Moved\n")


def patch_readme(chapter_dir: Path, sid: str) -> None:
    path = chapter_dir / "README.md"
    text = path.read_text(encoding="utf-8")
    text = text.replace(
        "read the transcript and public source capture first.",
        "read the transcript first.",
    )
    text = text.replace(
        "read the transcript first; the matching source capture under `sources/` is a provenance mirror.",
        "read the transcript first.",
    )
    text = re.sub(
        r"## Canonical Source Capture\n\n- \[Public source capture\]\(\../../../sources/predictive-history/game-theory/"
        + re.escape(sid)
        + r"\.md\)\n",
        f"## Canonical transcript\n\n- [{sid}-transcript.md]({sid}-transcript.md)\n",
        text,
        count=1,
    )
    text = text.replace(
        "Transcript body is in-folder (aligned with the sources capture).",
        "Transcript body is canonical in this folder.",
    )
    text = text.replace(
        "README first, transcript and source capture second,",
        "README first, transcript second,",
    )
    path.write_text(text, encoding="utf-8")


def consolidate_chapter(sid: str) -> bool:
    source_path = SRC_DIR / f"{sid}.md"
    chapter_dir = LEC_ROOT / sid
    lecture_path = chapter_dir / f"{sid}-transcript.md"
    lecture_rel = f"lectures/game-theory/{sid}/{sid}-transcript.md"
    if not source_path.exists() or not lecture_path.exists():
        raise FileNotFoundError(f"missing paths for {sid}")
    if is_redirect_stub(source_path):
        return False
    if not bodies_match(source_path, lecture_path):
        raise ValueError(f"{sid}: source and lecture bodies differ; skip consolidation")
    write_stub(source_path, lecture_rel)
    patch_commentary(chapter_dir, sid, lecture_rel)
    patch_readme(chapter_dir, sid)
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description="Consolidate GT sources into lecture stubs")
    parser.add_argument("--only", help="Single chapter id, e.g. gt-29")
    args = parser.parse_args()
    if args.only:
        ids = [args.only]
    else:
        ids = [f"gt-{i:02d}" for i in range(1, 30)]
    consolidated = [sid for sid in ids if consolidate_chapter(sid)]
    if consolidated:
        print(f"consolidated {len(consolidated)} chapter(s): {', '.join(consolidated)}")
    else:
        print("no chapters consolidated (already stubbed or missing)")


if __name__ == "__main__":
    main()
