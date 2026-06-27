#!/usr/bin/env python3
"""Shared helpers for lecture pass A (section rails) — interviews + lectures."""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

import yaml

from interview_transcript_sections import (
    PART_I_MARKER,
    common_asr_cleanup,
    find_anchor_pos,
    insert_sections,
    normalize_for_anchor,
    update_fidelity_reviewed_at,
    update_sectioned_frontmatter,
    write_slug_retitle_transcript,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
LECTURES_ROOT = REPO_ROOT / "lectures"
MAPS_ROOT = REPO_ROOT / "data" / "lectures" / "section-maps"
CARDS_PATH = REPO_ROOT / "data" / "cards.jsonl"

SLUG_HEADING_RE = re.compile(r"^### ([a-z][a-z0-9-]*)\s*$", re.M)
ANY_SECTION_RE = re.compile(r"^### (.+)$", re.M)
PIN_CITE_RE = re.compile(
    r"`(?P<file>[a-z0-9-]+-transcript\.md)#(?P<fragment>[a-z0-9-]+)`"
)
GEO_TIMESTAMP_LINE_RE = re.compile(
    r"^-\s*(?P<title>.+?):\s*`[^`]+`",
    re.M,
)


@dataclass
class TranscriptAuditRow:
    source_id: str
    series: str
    path: str
    rail_status: str
    section_count: int
    warn: str = ""


def slug_to_title(slug: str) -> str:
    """Mechanical kebab-slug → Title Case words (preserves GitHub #fragment)."""
    return " ".join(part.capitalize() for part in slug.split("-") if part)


def github_heading_anchor(heading: str) -> str:
    text = heading.strip().lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"\s+", "-", text.strip())
    return text


def is_title_case_heading(heading: str) -> bool:
    heading = heading.strip()
    if SLUG_HEADING_RE.match(f"### {heading}"):
        return False
    if not heading:
        return False
    if heading[0].islower():
        return False
    return True


def split_part_i(doc: str) -> tuple[str, str]:
    if PART_I_MARKER not in doc:
        raise ValueError("missing Part I marker")
    head, body = doc.split(PART_I_MARKER, 1)
    return head, body.lstrip("\n")


def list_transcript_paths(series: str | None = None) -> list[Path]:
    root = LECTURES_ROOT / series if series else LECTURES_ROOT
    paths = sorted(root.rglob("*-transcript.md"))
    return [p for p in paths if p.is_file()]


def load_lecture_card_ids() -> set[str]:
    ids: set[str] = set()
    for line in CARDS_PATH.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        card = json.loads(line)
        path = card.get("source_paths", {}).get("source_chapter_path", "")
        if path.startswith("lectures/"):
            ids.add(card["source_id"])
    return ids


def classify_transcript(path: Path) -> TranscriptAuditRow:
    rel = path.relative_to(REPO_ROOT).as_posix()
    series = path.parts[path.parts.index("lectures") + 1]
    source_id = path.name.replace("-transcript.md", "")
    doc = path.read_text(encoding="utf-8")
    if PART_I_MARKER not in doc:
        return TranscriptAuditRow(source_id, series, rel, "missing_part_i", 0)

    _, body = split_part_i(doc)
    headings = ANY_SECTION_RE.findall(body)
    if not headings:
        return TranscriptAuditRow(source_id, series, rel, "flat", 0, "no sections")

    slug_count = len(SLUG_HEADING_RE.findall(body))
    title_count = sum(1 for h in headings if is_title_case_heading(h))
    if slug_count and slug_count == len(headings):
        status = "slug"
    elif title_count == len(headings):
        status = "title_case"
    else:
        status = "mixed"

    warn = ""
    if status == "title_case" and len(headings) == 1:
        warn = "single_rail"
    return TranscriptAuditRow(
        source_id, series, rel, status, len(headings), warn
    )


def audit_lectures(series: str | None = None) -> list[TranscriptAuditRow]:
    return [classify_transcript(p) for p in list_transcript_paths(series)]


def extract_slug_headings(body: str) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    for match in SLUG_HEADING_RE.finditer(body):
        slug = match.group(1)
        pairs.append((slug, slug_to_title(slug)))
    return pairs


def retitle_slug_transcript(path: Path, *, dry_run: bool = False) -> int:
    doc = path.read_text(encoding="utf-8")
    _, body = split_part_i(doc)
    pairs = extract_slug_headings(body)
    if not pairs:
        print(f"skip {path.name}: no slug headings")
        return 0
    if dry_run:
        print(f"dry-run {path.name}: {len(pairs)} headings")
        return len(pairs)
    write_slug_retitle_transcript(path, pairs, asr_cleanup_fn=common_asr_cleanup)
    return len(pairs)


def parse_geo_timestamp_titles(doc: str) -> list[str]:
    block = doc.split("Source timestamps:", 1)
    if len(block) < 2:
        return []
    tail = block[1].split(PART_I_MARKER, 1)[0]
    titles: list[str] = []
    for match in GEO_TIMESTAMP_LINE_RE.finditer(tail):
        title = match.group("title").strip()
        if title.lower().startswith("opening"):
            titles.append("Opening")
        else:
            titles.append(title[0].upper() + title[1:] if title else title)
    return titles


def anchor_from_title(title: str, body: str, start: int = 0) -> str | None:
    """Find a short anchor phrase from title keywords in body."""
    words = [
        w
        for w in re.findall(r"[a-zA-Z']+", title.lower())
        if len(w) > 3 and w not in {"opening", "closing", "questions", "with", "from", "and", "the"}
    ]
    if not words:
        return None
    hay = normalize_for_anchor(body)
    for n in (4, 3, 2):
        if len(words) < n:
            continue
        phrase = " ".join(words[:n])
        pos = hay.find(phrase, start)
        if pos != -1:
            return body[pos : pos + min(60, len(body) - pos)].split("\n")[0][:60]
    return None


def insert_sections_paragraph_split(body: str, titles: list[str]) -> str:
    paragraphs = [p.strip() for p in re.split(r"\n\n+", body.strip()) if p.strip()]
    n = len(titles)
    if not paragraphs:
        raise ValueError("empty body")
    if n == 1:
        return f"### {titles[0]}\n\n{body.strip()}"

    parts: list[str] = []
    total = len(paragraphs)
    for i, title in enumerate(titles):
        start_idx = (i * total) // n
        end_idx = ((i + 1) * total) // n if i < n - 1 else total
        chunk = "\n\n".join(paragraphs[start_idx:end_idx]).strip()
        parts.append(f"### {title}\n\n{chunk}")
    return "\n\n".join(parts)


def build_anchors_for_titles(titles: list[str], body: str) -> list[str]:
    anchors: list[str] = []
    cursor = 0
    for i, title in enumerate(titles[:-1]):
        if i == 0 and title.lower().startswith("opening"):
            snippet = body.strip()[:50]
            anchors.append(snippet)
            cursor = len(snippet)
            continue
        anchor = anchor_from_title(title, body, cursor)
        if not anchor:
            raise ValueError(f"could not derive anchor for section: {title!r}")
        pos = find_anchor_pos(body, anchor[:40], cursor)
        anchors.append(anchor[:80].strip())
        cursor = pos + 1
    return anchors


def apply_section_map(path: Path, sections: list[dict], *, dry_run: bool = False) -> None:
    doc = path.read_text(encoding="utf-8")
    head, body = split_part_i(doc)
    titles = [s["title"] for s in sections]
    flat = body.strip()

    if sections[0].get("split") == "paragraph":
        new_body = insert_sections_paragraph_split(flat, titles)
    else:
        specified = [s.get("anchor") for s in sections[:-1]]
        try:
            if specified and all(specified):
                anchors = [str(a) for a in specified]
                new_body = insert_sections(
                    flat, titles, anchors, asr_cleanup_fn=common_asr_cleanup
                )
            else:
                anchors = build_anchors_for_titles(titles, flat)
                new_body = insert_sections(
                    flat, titles, anchors, asr_cleanup_fn=common_asr_cleanup
                )
        except ValueError:
            new_body = insert_sections_paragraph_split(flat, titles)

    if dry_run:
        print(f"dry-run apply {path.name}: {len(titles)} sections")
        return

    head = update_sectioned_frontmatter(head)
    out = f"{head}{PART_I_MARKER}\n\n{new_body}\n"
    path.write_text(out, encoding="utf-8", newline="\n")
    print(f"wrote {path} ({len(titles)} sections)")


def load_section_map(source_id: str) -> list[dict]:
    map_path = MAPS_ROOT / f"{source_id}.yaml"
    if not map_path.exists():
        raise FileNotFoundError(map_path)
    data = yaml.safe_load(map_path.read_text(encoding="utf-8"))
    return data["sections"]


def save_section_map(source_id: str, sections: list[dict]) -> Path:
    MAPS_ROOT.mkdir(parents=True, exist_ok=True)
    path = MAPS_ROOT / f"{source_id}.yaml"
    payload = {"source_id": source_id, "sections": sections}
    path.write_text(yaml.safe_dump(payload, sort_keys=False, allow_unicode=True), encoding="utf-8")
    return path


def load_card(source_id: str) -> dict | None:
    for line in CARDS_PATH.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        card = json.loads(line)
        if card.get("source_id") == source_id:
            return card
    return None


def seed_titles_from_card(card: dict) -> list[str]:
    """Derive section title stubs from card pressure points / placement text."""
    sections = card.get("sections") or {}
    titles: list[str] = []
    for key in ("Historical Pressure Points", "Where This Sits"):
        block = sections.get(key, "")
        for line in block.splitlines():
            line = line.strip().lstrip("-").strip()
            if not line or len(line) < 12:
                continue
            # First clause or ~6 words as a rail title stub
            clause = line.split(".")[0].split(":")[0].strip()
            words = clause.split()
            title = " ".join(words[:8]).strip(" ,;")
            if title and title not in titles:
                titles.append(title[0].upper() + title[1:] if title else title)
    if not titles:
        titles = ["Opening", "Core Lecture", "Examples", "Closing"]
    else:
        titles = ["Opening", *titles[:6], "Closing"]
    return titles


def draft_section_map(path: Path, *, template: str | None = None) -> list[dict]:
    """Seed insert-tier YAML from timestamps, card, or series template."""
    source_id = path.name.replace("-transcript.md", "")
    try:
        return draft_geo_map(path)
    except ValueError:
        pass

    if template:
        tpl_path = MAPS_ROOT / "_templates" / f"{template}.yaml"
        if tpl_path.exists():
            return yaml.safe_load(tpl_path.read_text(encoding="utf-8"))["sections"]

    card = load_card(source_id)
    if card:
        titles = seed_titles_from_card(card)
    else:
        titles = ["Opening", "Core Lecture", "Examples", "Closing"]

    return [{"title": t, "split": "paragraph"} for t in titles]


def draft_geo_map(path: Path) -> list[dict]:
    doc = path.read_text(encoding="utf-8")
    titles = parse_geo_timestamp_titles(doc)
    if not titles:
        raise ValueError(f"{path.name}: no Source timestamps block")
    _, body = split_part_i(doc)
    sections: list[dict] = []
    cursor = 0
    for i, title in enumerate(titles):
        entry: dict = {"title": title}
        if i < len(titles) - 1:
            anchor = anchor_from_title(title, body, cursor)
            if anchor:
                entry["anchor"] = anchor[:80].strip()
                cursor = find_anchor_pos(body, entry["anchor"][:40], cursor) + 1
            else:
                entry["anchor_missing"] = True
        sections.append(entry)
    return sections


def transcript_heading_fragments(path: Path) -> set[str]:
    doc = path.read_text(encoding="utf-8")
    if PART_I_MARKER not in doc:
        return set()
    _, body = split_part_i(doc)
    frags: set[str] = set()
    for heading in ANY_SECTION_RE.findall(body):
        frags.add(github_heading_anchor(heading))
    return frags


def verify_pin_cites_for_packet(source_id: str) -> list[str]:
    errors: list[str] = []
    paths = list_transcript_paths()
    transcript_path = next(
        (p for p in paths if p.name == f"{source_id}-transcript.md"), None
    )
    if not transcript_path:
        return [f"{source_id}: transcript not found"]
    commentary_path = transcript_path.with_name(
        transcript_path.name.replace("-transcript.md", "-commentary.md")
    )
    if not commentary_path.exists():
        return []
    fragments = transcript_heading_fragments(transcript_path)
    for match in PIN_CITE_RE.finditer(commentary_path.read_text(encoding="utf-8")):
        frag = match.group("fragment")
        if frag not in fragments:
            errors.append(
                f"{source_id}: pin-cite #{frag} not in transcript headings {sorted(fragments)}"
            )
    return errors
