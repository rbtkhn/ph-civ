#!/usr/bin/env python3
"""Build Phase 0 study-edition bundles and static HTML from chapter packets."""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VOL2 = ROOT / "book" / "volume-ii"
PARTS_JSON = ROOT / "data" / "parts" / "volume-i-parts.json"
SPINE_JSON = ROOT / "data" / "spines" / "homer-to-tolstoy.json"
SITE_DATA = ROOT / "site" / "_data" / "chapters"
SITE_DIST = ROOT / "site" / "dist"
ASSETS = ROOT / "site" / "assets"

TRANSCRIPT_MARKER = "## Part I: Full transcript\n\n"
SOURCE_ID_RE = re.compile(r"^civ-\d{2}$")
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
SECTION_RE = re.compile(r"^### ([a-z0-9-]+)\s*$", re.MULTILINE)
L2_ROW_RE = re.compile(
    r"^\|\s*(\d+)\s*\|\s*(.+?)\s*\|\s*`[^`]*#([a-z0-9-]+)`\s*\|\s*([^|]+)\|\s*([^|]+)\|",
    re.MULTILINE,
)
CONCEPT_RE = re.compile(
    r"^- \*\*([^*]+)\*\*:\s*(.+?)\s*`[^`]*#([a-z0-9-]+)`",
    re.MULTILINE,
)


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}, text
    meta: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip().strip('"')
    return meta, text[match.end() :]


def slug_label(slug: str) -> str:
    return slug.replace("-", " ").title()


def transcript_body(text: str) -> str:
    if TRANSCRIPT_MARKER not in text:
        raise ValueError("transcript missing Part I marker")
    return text.split(TRANSCRIPT_MARKER, 1)[1]


def parse_sections(body: str) -> tuple[str, list[dict[str, str]]]:
    parts = SECTION_RE.split(body)
    if len(parts) < 2:
        raise ValueError("transcript has no ### section rails")
    opening = parts[0].strip()
    sections: list[dict[str, str]] = []
    i = 1
    while i < len(parts):
        slug = parts[i].strip()
        content = parts[i + 1].strip() if i + 1 < len(parts) else ""
        sections.append({"slug": slug, "body": content})
        i += 2
    return opening, sections


def parse_layer1(commentary: str) -> str:
    marker = "## Layer 1 - Neutral Summary\n\n"
    if marker not in commentary:
        return ""
    chunk = commentary.split(marker, 1)[1]
    end = chunk.find("\n---\n")
    if end >= 0:
        chunk = chunk[:end]
    return chunk.strip()


def parse_claims(commentary: str) -> list[dict[str, str]]:
    block = commentary
    start = block.find("### Major Claims")
    if start < 0:
        return []
    block = block[start:]
    end = block.find("### Core Concepts")
    if end >= 0:
        block = block[:end]
    claims: list[dict[str, str]] = []
    for match in L2_ROW_RE.finditer(block):
        claims.append(
            {
                "n": int(match.group(1)),
                "claim": match.group(2).strip(),
                "anchor": match.group(3).strip(),
                "strength": match.group(4).strip(),
                "confidence": match.group(5).strip(),
            }
        )
    return claims


def parse_concepts(commentary: str) -> list[dict[str, str]]:
    start = commentary.find("### Core Concepts Defined")
    if start < 0:
        return []
    block = commentary[start:]
    end = block.find("\n---\n")
    if end >= 0:
        block = block[:end]
    concepts: list[dict[str, str]] = []
    for match in CONCEPT_RE.finditer(block):
        concepts.append(
            {
                "term": match.group(1).strip(),
                "definition": match.group(2).strip(),
                "anchor": match.group(3).strip(),
            }
        )
    return concepts


def load_part_meta(part_id: str) -> dict[str, str]:
    data = json.loads(PARTS_JSON.read_text(encoding="utf-8"))
    for part in data.get("parts", []):
        if part.get("part_id") == part_id:
            return {
                "part_id": part_id,
                "display_title": part.get("display_title", part_id),
                "title": part.get("title", part_id),
            }
    return {"part_id": part_id, "display_title": part_id, "title": part_id}


def route_context(source_id: str) -> dict[str, object] | None:
    if not SPINE_JSON.is_file():
        return None
    spine = json.loads(SPINE_JSON.read_text(encoding="utf-8"))
    for idx, step in enumerate(spine.get("sequence", []), start=1):
        ids = step.get("source_ids", [])
        if source_id in ids:
            return {
                "spine_id": spine.get("spine_id"),
                "title": spine.get("title"),
                "step": idx,
                "author": step.get("author"),
                "source_ids": ids,
            }
    return None


def resolve_chapter(source_id: str) -> Path:
    if not SOURCE_ID_RE.match(source_id):
        raise ValueError(f"unsupported source_id for Phase 0: {source_id}")
    folder = VOL2 / source_id
    if not folder.is_dir():
        raise FileNotFoundError(f"missing chapter folder: {folder.relative_to(ROOT)}")
    return folder


def build_bundle(source_id: str) -> dict[str, object]:
    folder = resolve_chapter(source_id)
    transcript_path = folder / f"{source_id}-transcript.md"
    commentary_path = folder / f"{source_id}-commentary.md"
    t_meta, t_rest = parse_frontmatter(transcript_path.read_text(encoding="utf-8"))
    c_meta, c_rest = parse_frontmatter(commentary_path.read_text(encoding="utf-8"))
    opening, sections = parse_sections(transcript_body(t_rest))
    claims = parse_claims(c_rest)
    concepts = parse_concepts(c_rest)
    part_id = t_meta.get("part_id") or c_meta.get("part_id", "")
    part = load_part_meta(part_id) if part_id else {}
    anchors = {row["slug"] for row in sections}
    for claim in claims:
        if claim["anchor"] not in anchors:
            raise ValueError(
                f"{source_id}: claim {claim['n']} anchor #{claim['anchor']} missing in transcript"
            )
    claims_by_anchor: dict[str, list[int]] = {}
    for claim in claims:
        claims_by_anchor.setdefault(claim["anchor"], []).append(claim["n"])
    return {
        "source_id": source_id,
        "title": t_meta.get("title") or c_meta.get("title", source_id),
        "part_id": part_id,
        "part": part,
        "review_status": t_meta.get("review_status", "unknown"),
        "transcript_status": t_meta.get("transcript_status", ""),
        "source_video": t_meta.get("canonical_url", ""),
        "route": route_context(source_id),
        "opening": opening,
        "sections": [
            {
                "slug": row["slug"],
                "label": slug_label(row["slug"]),
                "body": row["body"],
                "claim_numbers": claims_by_anchor.get(row["slug"], []),
            }
            for row in sections
        ],
        "claims": claims,
        "concepts": concepts,
        "layer1_summary": parse_layer1(c_rest),
        "paths": {
            "transcript": str(transcript_path.relative_to(ROOT)).replace("\\", "/"),
            "commentary": str(commentary_path.relative_to(ROOT)).replace("\\", "/"),
            "part_commentary": t_meta.get("part_commentary_path", ""),
            "part_bibliography": t_meta.get("part_bibliography_path", ""),
        },
    }


def render_html(bundle: dict[str, object]) -> str:
    title = html.escape(str(bundle["title"]))
    source_id = html.escape(str(bundle["source_id"]))
    part = bundle.get("part") or {}
    part_title = html.escape(str(part.get("display_title", "")))
    review = html.escape(str(bundle.get("review_status", "")))
    transcript_status = html.escape(str(bundle.get("transcript_status", "")))
    video = str(bundle.get("source_video") or "")
    route = bundle.get("route") or {}
    route_line = ""
    if route:
        route_line = (
            f"Homer-to-Tolstoy · step {route.get('step')} · {html.escape(str(route.get('author', '')))}"
        )

    outline_items = []
    for section in bundle["sections"]:  # type: ignore[union-attr]
        slug = section["slug"]
        label = html.escape(section["label"])
        nums = section.get("claim_numbers") or []
        badge = ""
        if nums:
            badge = f'<span class="claim-badge">{",".join(str(n) for n in nums)}</span>'
        outline_items.append(
            f'<li><button type="button" class="outline-btn" data-slug="{html.escape(slug)}">'
            f"{label}{badge}</button></li>"
        )

    floor_parts = []
    opening = str(bundle.get("opening") or "").strip()
    if opening:
        floor_parts.append(
            f'<section class="transcript-section opening" id="opening">'
            f"<p>{html.escape(opening)}</p></section>"
        )
    for section in bundle["sections"]:  # type: ignore[union-attr]
        slug = html.escape(section["slug"])
        body = html.escape(section["body"])
        nums = section.get("claim_numbers") or []
        markers = "".join(
            f'<button type="button" class="claim-marker" data-claim="{n}">[{n}]</button>'
            for n in nums
        )
        floor_parts.append(
            f'<section class="transcript-section" id="{slug}" data-slug="{slug}">'
            f'<header class="section-head"><h3>{html.escape(section["label"])}</h3>{markers}</header>'
            f"<p>{body}</p></section>"
        )

    claim_items = []
    for claim in bundle["claims"]:  # type: ignore[union-attr]
        claim_items.append(
            f'<article class="claim-card" id="claim-{claim["n"]}" data-claim="{claim["n"]}" '
            f'data-anchor="{html.escape(claim["anchor"])}">'
            f'<div class="claim-head"><span class="claim-n">{claim["n"]}</span>'
            f'<button type="button" class="claim-jump" data-anchor="{html.escape(claim["anchor"])}">'
            f"↗ passage</button></div>"
            f'<p class="claim-text">{html.escape(claim["claim"])}</p>'
            f'<p class="claim-meta">{html.escape(claim["strength"])} · {html.escape(claim["confidence"])}</p>'
            f"</article>"
        )

    concept_items = []
    for concept in bundle.get("concepts") or []:
        concept_items.append(
            f'<article class="concept-card" data-anchor="{html.escape(concept["anchor"])}">'
            f"<strong>{html.escape(concept['term'])}</strong> "
            f"{html.escape(concept['definition'])}</article>"
        )

    summary = html.escape(str(bundle.get("layer1_summary") or ""))
    video_link = ""
    if video:
        video_link = (
            f'<a class="status-link" href="{html.escape(video)}" target="_blank" rel="noopener">'
            "Source video</a>"
        )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} · ph-civ study edition</title>
  <link rel="stylesheet" href="../../assets/study-edition.css">
</head>
<body>
  <header class="top-bar">
    <div class="brand">ph-civ study edition</div>
    <div class="meta">
      <span class="chip">{source_id}</span>
      <span class="chip warn">{review}</span>
      {f'<span class="chip">{route_line}</span>' if route_line else ''}
      {video_link}
    </div>
  </header>
  <main class="study-grid" data-chapter="{source_id}">
    <aside class="panel outline-panel" aria-label="Outline">
      <h2>{part_title}</h2>
      <p class="panel-sub">{title}</p>
      <nav>
        <ol class="outline-list">
          {''.join(outline_items)}
        </ol>
      </nav>
    </aside>
    <article class="panel floor-panel" aria-label="Transcript">
      <div class="status-ribbon">
        Transcript floor · {transcript_status or 'verbatim lecture'} · not quotation-grade until review complete
      </div>
      {''.join(floor_parts)}
    </article>
    <aside class="panel notes-panel" aria-label="Study notes">
      <details class="summary-block" open>
        <summary>Layer 1 summary</summary>
        <p>{summary}</p>
      </details>
      <h3>Layer 2 claims</h3>
      <div class="claims-list">
        {''.join(claim_items)}
      </div>
      <h3>Core concepts</h3>
      <div class="concepts-list">
        {''.join(concept_items)}
      </div>
      <footer class="notes-footer">
        <p>Part apparatus and bibliography remain in repo markdown for Phase 0.</p>
      </footer>
    </aside>
  </main>
  <script src="../../assets/study-edition.js"></script>
</body>
</html>
"""


def write_outputs(source_id: str, bundle: dict[str, object], *, write_json: bool = True) -> Path:
    html_path = SITE_DIST / "study" / source_id / "index.html"
    html_path.parent.mkdir(parents=True, exist_ok=True)
    html_path.write_text(render_html(bundle), encoding="utf-8", newline="\n")
    if write_json:
        json_path = SITE_DATA / f"{source_id}.json"
        json_path.parent.mkdir(parents=True, exist_ok=True)
        json_path.write_text(
            json.dumps(bundle, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
            newline="\n",
        )
    return html_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build study-edition static pages.")
    parser.add_argument("--chapter", default="civ-07", help="source_id (Phase 0: civ-NN)")
    parser.add_argument("--no-json", action="store_true", help="skip site/_data JSON bundle")
    args = parser.parse_args(argv)
    try:
        bundle = build_bundle(args.chapter)
        out = write_outputs(args.chapter, bundle, write_json=not args.no_json)
    except (ValueError, FileNotFoundError) as exc:
        print(f"build_study_edition: {exc}", file=sys.stderr)
        return 1
    claims = len(bundle["claims"])  # type: ignore[arg-type]
    sections = len(bundle["sections"])  # type: ignore[arg-type]
    print(
        f"build_study_edition: ok {args.chapter} "
        f"({sections} sections, {claims} claims) -> {out.relative_to(ROOT)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
