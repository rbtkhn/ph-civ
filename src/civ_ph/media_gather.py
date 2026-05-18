"""Bucket-targeted, deterministic curator prompts aligned with schemas/media-inventory-item.schema.json."""

from __future__ import annotations

import hashlib
import json

BUCKET_ORDER: tuple[str, ...] = (
    "entry_object",
    "context_anchor",
    "primary_object_or_text",
    "comparison_object",
    "pressure_or_structure",
    "limit_or_caution",
)

# Five prompts per bucket per chapter exhibit (chapter-level ph-mus inventory scaffolding).
PROMPTS_PER_EXHIBIT_BUCKET: int = 5

_INTRO = (
    "Media inventory curation (search only). Each bucket matches `schemas/media-inventory-item.schema.json`. "
    "Prefer stable URLs from museums, libraries, archives, or universities."
)

_TEMPLATE_BANK: dict[str, tuple[str, ...]] = {
    "entry_object": (
        'Find one iconic object, artifact, manuscript page, monument, portrait, recording, scan, '
        'or site that signals the lecture opening immediately for a reader who only knows "{title}".',
        "Source a plausible exhibit headline image that could stand beside the caption for this orientation card.",
        "Identify a flagship museum-held item students would recognize quickly as shorthand for "
        "`{pressure_hint}` (without replacing lecture nuance).",
        "Hunt one emblem-grade token: seal, heraldic insignia, state portrait, devotional icon, ceremonial "
        "weapon, pilgrimage badge, cornerstone inscription, treaty seal, coronation relic, founding charter "
        "display, museum-grade coin type, stage prop with documented lineage—whichever crystallizes `{title}`.",
        "Surface a tactile everyday-survivor artifact (dress, inscription tool, devotional object, market weight, "
        "loom weight, stylus/wax tableau, devotional ticket, courthouse docket ledger page) tethered visibly to "
        "`{pressure_hint}` for exhibit threshold legibility.",
    ),
    "context_anchor": (
        "Locate a map, shaded relief atlas plate, geopolitical infographic, archival route map, or "
        "period cartography anchoring geography or regime framing implied around `{pressure_hint}`.",
        "Find timelines, chronological charts, genealogies, dynasty tables, reign lists, broadcast rundowns, "
        "or other temporal anchors grounding `{reading_hook}` in time.",
        "Source contextual reference material (museum wall text, neutral encyclopedic overview, syllabus outline) "
        "that quietly situates `{title}` culturally without overselling causal claims.",
        "Pull trade-route, naval, siege, tariff corridor, migration, pilgrimage, missionary itinerary, or refugee corridor maps (and cadastral survey plats) that ground `{pressure_hint}` spatially.",
        "Find footprints of institutions shaping the lecture: courthouse / basilica / guild hall / agora ruins / fortress plan / synagogue portal / madrasa inscription / arsenal gate—choose imagery whose caption can cite archival provenance tying back to `{reading_hook}`.",
    ),
    "primary_object_or_text": (
        "Find a surviving primary-surrogate object: inscribed stone, archival scan (with stable URL when possible), "
        "museum label page, authoritative legal or military decree image, foundational text spread, treaty "
        "fragment or coin series connected to `{pressure_hint}`.",
        "Identify an artifact or document image that reveals how contemporaries materially encoded legitimacy, "
        "memory, coercion, devotion, commerce, literacy, extraction, mobilization—or another "
        "explicit structural pressure hinted at `{pressure_hint}`.",
        "Pull a pedagogically legible archival photo, excavation image, archaeology release, or excavation "
        "report figure (open-license or institution-hosted) that shows physical evidence—not only secondary "
        "commentary—for `{pressure_hint}`.",
        "Locate a legible manuscript spread, broadsheet, pamphlet woodcut, playbill, petition dossier scan, diplomacy dispatch, cryptographic manual plate—always via ethical archival portals—that shows authority or literacy practices behind `{pressure_hint}`.",
        "Source archaeology-forward evidence: excavation trench photo, pottery typology plate, inscription squeeze, dendro/stratigraphy figure, GPR overlay, conserved metalwork macro—anything primary-adjacent with institution metadata matching `{pressure_hint}`.",
    ),
    "comparison_object": (
        "Find juxtaposition fodder across two regimes, theaters, doctrines, eras, mediums, myths, infrastructures, "
        "or cosmologies hinted by multiple pressure lines in `{title}`.",
        "Source a contrasting artifact pairing (east/west, empire/periphery, elite/popular, archival/or "
        "oral-derived traces) that illuminates divergence without caricature.",
        "Locate a comparison map, split-screen-friendly chart, bifurcated timeline, duel portraits, mirrored "
        "coins, stamps, or monuments stressing tensions related to `{pressure_hint}`.",
        "Surface paired royal portraits spanning dynasties, propaganda poster A/B sets, juxtaposed synagogue and church façade engravings, or dual urban plans contrasting inheritance lines implied inside `{title}`.",
        "Find famine wave, plague curve, diaspora infographic, tariff shock histogram, demographic displacement chart pairings ONLY when `{pressure_hint}` explicitly licenses longitudinal structural comparison.",
    ),
    "pressure_or_structure": (
        "Locate imagery (diagram charts, logistic maps, famine curves, bunker cutaways, propaganda sheet music, "
        "logistics tables) crystallizing systemic pressure hinted by `{pressure_hint}`—avoid "
        "melodrama substitutes.",
        "Find structural depictions—institutions, chains of command, tax flows, siege math, plague curves, "
        "cabling, grain routes, or corridor maps matching `{pressure_hint}` with caveat notes attached.",
        "Surface charters, petitions, labor posters, mobilization notices, satellite views, embargo routes, "
        "or tariff tables (when visibly legible online) aligning with stresses in `{pressure_hint}`; "
        "skip low-trust churn blogs unless no alternative exists.",
        "Locate courtroom sketches, parliamentary chamber engravings, factory inspection photographs, censorship-office exhibits, tribunal photography—museum or archival hosts—whose captions expose institutional coercion arcs implied by `{pressure_hint}`.",
        "Pull chokepoint imagery—submarine cable schematic, continental rail-hub poster, ration queue photograph, or blackout leaflet bundle—and choose one cleanly captioned logistics artifact narrating bottleneck politics tied to `{pressure_hint}` without monocausal doom spreads.",
    ),
    "limit_or_caution": (
        "Find media reinforcing healthy skepticism: contested dating, nationalist mythography, reconstructed "
        "color, sensational exhibits, dubious attributions—or academic debates keyed to `{limit_hint}`.",
        "Locate cautionary parallels (misapplied analogies, overdrawn timelines, monocausal maps) that this "
        "card warns readers to watch for regarding `{pressure_hint}` and `{limit_hint}`.",
        "Source nuanced secondary criticism, museum caveat labels, or peer-reviewed essays clarifying "
        "`{limit_hint}` for cautious students.",
        "Gather restoration before/after photography controversies, iconoclasm aftermath dossiers, deaccessioned provenance hearing PDFs showing how interpreters argue over contested claims surfaced in `{limit_hint}`.",
        "Locate syllabus-grade historiographical explainers—museum wall text debating dating, archaeology blog debunk sequences, encyclopedia caution ribbons—explicitly reinforcing `{limit_hint}` for students prepping exhibit labels.",
    ),
}


def _clip(text: str, max_len: int = 260) -> str:
    text = text.replace("\r", " ").strip()
    if len(text) <= max_len:
        return text or ""
    cut = text[: max_len - 1].rsplit(" ", 1)[0]
    return (cut or text[:max_len]).rstrip(",;:") + "…"


def _squash_orientation_text(section: str, max_len: int = 340) -> str:
    bullets: list[str] = []
    for line in (section or "").splitlines():
        t = line.strip()
        if not t:
            continue
        if t.startswith("- "):
            bullets.append(t[2:].strip())
        elif t.startswith("-") and len(t) > 1:
            bullets.append(t.lstrip("-").strip())
        else:
            bullets.append(t)
    if bullets:
        return _clip("; ".join(bullets), max_len)
    return _clip(section or "", max_len)


def _hints(card: dict) -> dict[str, str]:
    sec = card.get("sections") or {}

    def first_bullet(section: str) -> str:
        for line in (section or "").splitlines():
            t = line.strip()
            if t.startswith("- "):
                return _clip(t[2:])
            if t.startswith("-"):
                return _clip(t.lstrip("-").strip())
        return _clip(section or "")

    pressure = first_bullet(sec.get("Historical Pressure Points", "") or "") or sec.get(
        "Historical Pressure Points",
        "",
    ).strip().split("\n")[0][:220]
    limit_h = first_bullet(sec.get("Limits of the Frame", "") or "")
    reading = first_bullet(sec.get("Reading Posture", "") or "")
    if not pressure:
        pressure = _clip(card.get("title") or "")
    return {
        "title": card.get("title") or "",
        "series": card.get("series") or "",
        "part": card.get("part") or "",
        "placement": card.get("placement_weight") or "",
        "pressure_hint": pressure,
        "limit_hint": limit_h or pressure,
        "reading_hook": reading or pressure,
    }


def _rotate_pool(seed: str, bucket: str, pool: tuple[str, ...]) -> list[str]:
    if not pool:
        return []
    h = hashlib.sha256(f"{seed}:{bucket}:media_gather".encode("utf-8")).digest()
    start = int.from_bytes(h[:4], "big") % len(pool)
    span = min(PROMPTS_PER_EXHIBIT_BUCKET, len(pool))
    return [pool[(start + offset) % len(pool)] for offset in range(span)]


def build_media_gather_prompts(card: dict) -> dict[str, object]:
    sid = card["source_id"]
    hints = _hints(card)
    sec = card.get("sections") or {}
    format_map = {
        "title": hints["title"],
        "pressure_hint": hints["pressure_hint"],
        "limit_hint": hints["limit_hint"],
        "reading_hook": hints["reading_hook"],
    }
    buckets_payload: dict[str, list[str]] = {}
    for bucket in BUCKET_ORDER:
        pool = _TEMPLATE_BANK[bucket]
        chosen = [raw.format(**format_map) for raw in _rotate_pool(sid, bucket, pool)]
        buckets_payload[bucket] = chosen
    return {
        "source_id": sid,
        "title": hints["title"],
        "series": hints["series"],
        "part": hints["part"],
        "placement_weight": hints["placement"],
        "intro": _INTRO,
        "doc_refs": ["docs/media-inventory-guide.md", "docs/media-curator-bounty.md"],
        "buckets": buckets_payload,
        "orientation_snippets": {
            "Historical Pressure Points": _squash_orientation_text(sec.get("Historical Pressure Points", "")),
            "Limits of the Frame": _squash_orientation_text(sec.get("Limits of the Frame", "")),
            "Reading Posture": _squash_orientation_text(sec.get("Reading Posture", "")),
            "Where This Sits": _squash_orientation_text(sec.get("Where This Sits", "")),
        },
    }


def render_media_gather_text(card: dict) -> str:
    payload = build_media_gather_prompts(card)
    lines: list[str] = [
        f"# Media gather prompts • {payload['source_id']} — {payload['title']}",
        "",
        payload["intro"],
        "",
        f"Docs: {', '.join(payload['doc_refs'])}.",
        "",
        "## Orientation excerpts (summarized; cite primary sources externally)",
        "",
    ]
    for key, excerpt in payload["orientation_snippets"].items():
        lines.append(f"- **{key}:** {excerpt}")
    lines.extend(["", f"## Bucket prompts ({PROMPTS_PER_EXHIBIT_BUCKET} angles per bucket; aim for ~15–25 inventory rows)", ""])
    for bucket in BUCKET_ORDER:
        lines.append(f"### {bucket}")
        for idx, prompt in enumerate(payload["buckets"][bucket], start=1):
            lines.append(f"{idx}. {prompt}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def emit_media_gather_json(card: dict) -> str:
    return json.dumps(build_media_gather_prompts(card), indent=2, ensure_ascii=False, sort_keys=True) + "\n"
