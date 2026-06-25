from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from .commentary_v2 import commentary_metadata
from .data import PACKAGE_ROOT, load_cards

INDEX_MD_REL = "docs/predictive-history-index.md"
INDEX_JSON_REL = "data/predictive-history-index.json"
DEPRECATED_SOURCE_VIDEO_INDEX_REL = "docs/source-video-index.md"
FINGERPRINT_MARKER = "<!-- predictive-history-index-fingerprint:"
SCHEMA_VERSION = 2

PART_SECTIONS: dict[str, list[tuple[str, str]]] = {
    "civilization": [
        ("civilization", "Civilization"),
        ("great-books", "Great Books"),
        ("game-theory", "Game Theory (Volume I lane)"),
    ],
    "world-war": [
        ("geo-strategy", "Geo-Strategy"),
        ("game-theory", "Game Theory"),
        ("secret-history", "Secret History"),
        ("essays", "Essays"),
    ],
}

PART_META = {
    "civilization": ("ph-civ", "Volume I — Civilization (law discovery)"),
    "world-war": ("ph-apo", "Volume II — Apocalypse (law application)"),
}


def index_markdown_path(repo_root: Path | None = None) -> Path:
    root = repo_root or PACKAGE_ROOT
    return root / INDEX_MD_REL


def index_json_path(repo_root: Path | None = None) -> Path:
    root = repo_root or PACKAGE_ROOT
    return root / INDEX_JSON_REL


def markdown_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}
    block = text[4:end]
    fields: dict[str, str] = {}
    for line in block.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip().strip('"')
    return fields


def markdown_body(text: str) -> str:
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            return text[end + 5 :]
    return text


def count_transcript_words(text: str) -> int:
    body = markdown_body(text)
    return len(re.findall(r"\b[\w']+\b", body, flags=re.UNICODE))


def transcript_word_count(card: dict, repo_root: Path) -> int:
    transcript_rel = card.get("source_paths", {}).get("source_chapter_path", "")
    if not transcript_rel:
        return 0
    transcript_path = repo_root / transcript_rel
    if not transcript_path.exists():
        return 0
    return count_transcript_words(transcript_path.read_text(encoding="utf-8"))


def source_video_url(card: dict, repo_root: Path) -> str:
    transcript_rel = card.get("source_paths", {}).get("source_chapter_path", "")
    if not transcript_rel:
        return ""
    transcript_path = repo_root / transcript_rel
    if not transcript_path.exists():
        return ""
    frontmatter = markdown_frontmatter(transcript_path.read_text(encoding="utf-8"))
    return frontmatter.get("source_url", "") or frontmatter.get("canonical_url", "")


def chapter_folder_rel(card: dict, repo_root: Path) -> str:
    transcript_rel = card.get("source_paths", {}).get("source_chapter_path", "")
    commentary_rel = card.get("source_paths", {}).get("commentary_path", "")
    if not transcript_rel or not commentary_rel:
        return ""
    folder = "/".join(transcript_rel.split("/")[:-1])
    if not folder.endswith(f"/{card['source_id']}"):
        return ""
    if not commentary_rel.startswith(f"{folder}/"):
        return ""
    readme = repo_root / folder / "README.md"
    return folder if readme.exists() else ""


def chapter_entry(card: dict, repo_root: Path) -> dict:
    paths = card.get("source_paths", {})
    transcript = paths.get("source_chapter_path", "")
    commentary = paths.get("commentary_path", "")
    folder = chapter_folder_rel(card, repo_root)
    surface, volume_label = PART_META[card["part"]]
    entry = {
        "source_id": card["source_id"],
        "title": card["title"],
        "part": card["part"],
        "surface": surface,
        "volume_label": volume_label,
        "series": card["series"],
        "review_status": card.get("review_status", ""),
        "placement_weight": card.get("placement_weight", ""),
        "paths": {
            "transcript": transcript,
            "commentary": commentary,
        },
        "transcript_word_count": transcript_word_count(card, repo_root),
    }
    if folder:
        entry["paths"]["folder"] = folder
        entry["paths"]["folder_readme"] = f"{folder}/README.md"
    video = source_video_url(card, repo_root)
    if video:
        entry["source_video_url"] = video
    commentary_path = repo_root / commentary if commentary else None
    if commentary_path and commentary_path.exists():
        meta = commentary_metadata(commentary_path)
        entry["commentary_maturity"] = meta["commentary_maturity"]
        entry["scaffold_version"] = meta["scaffold_version"]
        if meta["migration_source"]:
            entry["migration_source"] = meta["migration_source"]
        entry["deprecated_part_routing"] = meta["deprecated_part_routing"]
    return entry


def render_index_payload(cards: list[dict], repo_root: Path) -> dict:
    chapters = [
        chapter_entry(card, repo_root)
        for card in sorted(cards, key=lambda row: row["source_id"])
    ]
    by_surface: dict[str, dict] = {}
    for surface in ("ph-civ", "ph-apo"):
        part = "civilization" if surface == "ph-civ" else "world-war"
        surface_chapters = [entry for entry in chapters if entry["surface"] == surface]
        series_counts: dict[str, int] = {}
        for entry in surface_chapters:
            series_counts[entry["series"]] = series_counts.get(entry["series"], 0) + 1
        _, volume_label = PART_META[part]
        by_surface[surface] = {
            "part": part,
            "volume_label": volume_label,
            "chapter_count": len(surface_chapters),
            "series_counts": dict(sorted(series_counts.items())),
            "transcript_word_total": sum(
                entry.get("transcript_word_count", 0) for entry in surface_chapters
            ),
        }

    fingerprint = index_payload_fingerprint(chapters)
    transcript_word_total = sum(entry.get("transcript_word_count", 0) for entry in chapters)
    return {
        "schema_version": SCHEMA_VERSION,
        "fingerprint": fingerprint,
        "card_count": len(cards),
        "transcript_word_total": transcript_word_total,
        "ssot": "data/cards.jsonl",
        "markdown_index": INDEX_MD_REL,
        "surfaces": {
            "ph-civ": {
                "part": "civilization",
                "label": PART_META["civilization"][1],
            },
            "ph-apo": {
                "part": "world-war",
                "label": PART_META["world-war"][1],
            },
        },
        "series_order": {
            part: [{"series": series, "label": label} for series, label in sections]
            for part, sections in PART_SECTIONS.items()
        },
        "by_surface": by_surface,
        "chapters": chapters,
    }


def index_payload_fingerprint(chapters: list[dict]) -> str:
    blob = json.dumps(chapters, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    digest = hashlib.sha256(blob.encode("utf-8")).hexdigest()
    return digest[:16]


def md_link(label: str, rel_from_docs: str) -> str:
    if not rel_from_docs:
        return ""
    return f"[{label}](../{rel_from_docs})"


def render_table(cards: list[dict], repo_root: Path) -> list[str]:
    header = "| Source ID | Title | Review | Words | Transcript | Commentary | Folder | Video |"
    sep = "| --- | --- | --- | ---: | --- | --- | --- | --- |"
    rows = [header, sep]
    for card in sorted(cards, key=lambda row: row["source_id"]):
        entry = chapter_entry(card, repo_root)
        paths = entry["paths"]
        transcript = paths.get("transcript", "")
        commentary = paths.get("commentary", "")
        folder = paths.get("folder", "")
        video = entry.get("source_video_url", "")
        words = entry.get("transcript_word_count", 0)
        rows.append(
            "| "
            + " | ".join(
                [
                    f"`{entry['source_id']}`",
                    entry["title"].replace("|", "\\|"),
                    f"`{entry['review_status']}`",
                    f"{words:,}" if words else "—",
                    md_link("transcript", transcript) if transcript else "",
                    md_link("commentary", commentary) if commentary else "",
                    md_link("folder", paths.get("folder_readme", "")) if folder else "",
                    f"[video]({video})" if video else "",
                ]
            )
            + " |"
        )
    return rows


def render_index_body(cards: list[dict], repo_root: Path) -> str:
    by_part: dict[str, dict[str, list[dict]]] = {
        "civilization": {},
        "world-war": {},
    }
    for card in cards:
        part = card["part"]
        series = card["series"]
        by_part.setdefault(part, {}).setdefault(series, []).append(card)

    lines = [
        "# Predictive History Chapter Index",
        "",
        "Canonical catalog of every public Predictive History lecture chapter in this repository.",
        "",
        f"- **Card count:** {len(cards)}",
        f"- **Transcript words (total):** {sum(transcript_word_count(card, repo_root) for card in cards):,}",
        f"- **SSOT:** [`data/cards.jsonl`](../data/cards.jsonl) · [`data/predictive-history-index.json`](../data/predictive-history-index.json) · [`data/index.json`](../data/index.json)",
        "- **Regenerate:** `ph-civ index` · `python scripts/generate_ph_civ_index.py` · auto-sync during `ph-civ validate` and publish",
        "",
        "Surfaces:",
        "",
        "- **ph-civ** — Volume I / Civilization (`part: civilization`)",
        "- **ph-apo** — Volume II / Apocalypse (`part: world-war`)",
        "",
        "Bridge support nodes (`sh-11`, `sh-16`, `sh-17`, `sh-18`) appear in Volume I membership but carry cross-volume routing; check each card's `part` and folder.",
        "",
        "YouTube and Substack source URLs appear in the **Video** column below and in "
        "[`data/predictive-history-index.json`](../data/predictive-history-index.json) (`source_video_url`). "
        "**Words** counts transcript body text only (YAML frontmatter excluded). "
        "Legacy [`source-video-index.md`](source-video-index.md) redirects here.",
        "",
    ]

    for part in ("civilization", "world-war"):
        surface, heading = PART_META[part]
        part_cards = [c for c in cards if c["part"] == part]
        lines.extend(
            [
                f"## {heading}",
                "",
                f"**Surface:** `{surface}` · **Chapters:** {len(part_cards)}",
                "",
            ]
        )
        for series_key, series_label in PART_SECTIONS[part]:
            series_cards = by_part.get(part, {}).get(series_key, [])
            if not series_cards:
                continue
            lines.append(f"### {series_label}")
            lines.append("")
            lines.extend(render_table(series_cards, repo_root))
            lines.append("")

    lines.append("## Full alphabetical index")
    lines.append("")
    lines.extend(render_table(cards, repo_root))
    lines.append("")
    return lines


def render_index_markdown(cards: list[dict], repo_root: Path, *, fingerprint: str) -> str:
    body_lines = render_index_body(cards, repo_root)
    body = "\n".join(body_lines)
    return f"{FINGERPRINT_MARKER} {fingerprint} -->\n{body}"


def render_index_json(cards: list[dict], repo_root: Path) -> str:
    payload = render_index_payload(cards, repo_root)
    return json.dumps(payload, indent=2, ensure_ascii=False) + "\n"


def read_index_fingerprint(path: Path) -> str | None:
    if not path.exists():
        return None
    if path.suffix == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        value = data.get("fingerprint")
        return value if isinstance(value, str) else None
    first_line = path.read_text(encoding="utf-8").splitlines()[0:1]
    if not first_line:
        return None
    match = re.match(r"<!-- predictive-history-index-fingerprint: ([0-9a-f]+) -->", first_line[0])
    return match.group(1) if match else None


def expected_index_fingerprint(cards: list[dict], repo_root: Path) -> str:
    chapters = [
        chapter_entry(card, repo_root)
        for card in sorted(cards, key=lambda row: row["source_id"])
    ]
    return index_payload_fingerprint(chapters)


def ensure_ph_civ_index(
    cards: list[dict] | None = None,
    *,
    repo_root: Path | None = None,
    force: bool = False,
) -> tuple[Path, Path, bool]:
    root = repo_root or PACKAGE_ROOT
    cards = cards if cards is not None else load_cards()
    md_path = index_markdown_path(root)
    json_path = index_json_path(root)
    fingerprint = expected_index_fingerprint(cards, root)
    if not force and md_path.exists() and json_path.exists():
        if (
            read_index_fingerprint(md_path) == fingerprint
            and read_index_fingerprint(json_path) == fingerprint
        ):
            return md_path, json_path, False

    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text(render_index_markdown(cards, root, fingerprint=fingerprint), encoding="utf-8")
    json_path.write_text(render_index_json(cards, root), encoding="utf-8")
    return md_path, json_path, True


def validate_ph_civ_index(cards: list[dict] | None = None, *, repo_root: Path | None = None) -> list[str]:
    root = repo_root or PACKAGE_ROOT
    cards = cards if cards is not None else load_cards()
    md_path = index_markdown_path(root)
    json_path = index_json_path(root)
    expected_fp = expected_index_fingerprint(cards, root)
    errors: list[str] = []

    if not md_path.exists():
        errors.append(f"missing chapter index: {INDEX_MD_REL}")
    elif read_index_fingerprint(md_path) != expected_fp:
        errors.append(
            f"stale chapter index: {INDEX_MD_REL} (run `ph-civ index` or `ph-civ validate` to refresh)"
        )

    if not json_path.exists():
        errors.append(f"missing chapter index: {INDEX_JSON_REL}")
    else:
        json_fp = read_index_fingerprint(json_path)
        if json_fp != expected_fp:
            errors.append(
                f"stale chapter index: {INDEX_JSON_REL} (run `ph-civ index` or `ph-civ validate` to refresh)"
            )
        payload = json.loads(json_path.read_text(encoding="utf-8"))
        if payload.get("card_count") != len(cards):
            errors.append(f"chapter index card_count mismatch in {INDEX_JSON_REL}")

    md_fp = read_index_fingerprint(md_path) if md_path.exists() else None
    json_fp = read_index_fingerprint(json_path) if json_path.exists() else None
    if md_fp and json_fp and md_fp != json_fp:
        errors.append("chapter index fingerprint mismatch between markdown and JSON exports")

    return errors


DEPRECATED_SOURCE_VIDEO_INDEX_MARKERS = [
    "deprecated",
    "predictive-history-index.md",
    "source_video_url",
]


def validate_deprecated_source_video_index(*, repo_root: Path | None = None) -> list[str]:
    root = repo_root or PACKAGE_ROOT
    path = root / DEPRECATED_SOURCE_VIDEO_INDEX_REL
    errors: list[str] = []
    if not path.exists():
        errors.append(f"missing deprecated redirect stub: {DEPRECATED_SOURCE_VIDEO_INDEX_REL}")
        return errors
    text = path.read_text(encoding="utf-8")
    lowered = text.lower()
    for marker in DEPRECATED_SOURCE_VIDEO_INDEX_MARKERS:
        if marker.lower() not in lowered:
            errors.append(f"{DEPRECATED_SOURCE_VIDEO_INDEX_REL} missing marker: {marker}")
    return errors


DEPRECATED_PH_CIV_INDEX_MD_REL = "docs/ph-civ-index.md"
DEPRECATED_PH_CIV_INDEX_JSON_REL = "data/ph-civ-index.json"

DEPRECATED_PH_CIV_INDEX_MARKERS = [
    "deprecated",
    "predictive-history-index.md",
    "predictive-history-index.json",
]


def validate_deprecated_ph_civ_index(*, repo_root: Path | None = None) -> list[str]:
    root = repo_root or PACKAGE_ROOT
    errors: list[str] = []
    md_path = root / DEPRECATED_PH_CIV_INDEX_MD_REL
    if not md_path.exists():
        errors.append(f"missing deprecated redirect stub: {DEPRECATED_PH_CIV_INDEX_MD_REL}")
    else:
        lowered = md_path.read_text(encoding="utf-8").lower()
        for marker in DEPRECATED_PH_CIV_INDEX_MARKERS:
            if marker.lower() not in lowered:
                errors.append(f"{DEPRECATED_PH_CIV_INDEX_MD_REL} missing marker: {marker}")

    json_path = root / DEPRECATED_PH_CIV_INDEX_JSON_REL
    if not json_path.exists():
        errors.append(f"missing deprecated redirect stub: {DEPRECATED_PH_CIV_INDEX_JSON_REL}")
    else:
        payload = json.loads(json_path.read_text(encoding="utf-8"))
        if payload.get("_deprecated") != "Moved to data/predictive-history-index.json":
            errors.append(f"{DEPRECATED_PH_CIV_INDEX_JSON_REL} missing _deprecated marker")
        if payload.get("redirect") != "data/predictive-history-index.json":
            errors.append(f"{DEPRECATED_PH_CIV_INDEX_JSON_REL} redirect must point to canonical index")
    return errors
