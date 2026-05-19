from __future__ import annotations

import argparse
import json
import random
import sys
from collections import Counter

from .data import (
    DATA_ROOT,
    card_markdown,
    get_card,
    get_pattern,
    get_route,
    load_cards,
    load_choreography,
    load_course_architecture,
    load_growth_goals,
    load_llm_experience,
    load_museum_index,
    load_patterns,
    load_route_seed,
    load_spine,
    load_surfaces,
    pattern_markdown,
    patterns_for_source,
)

EXPECTED_SOURCE_REPO = "rbtkhn/ph-workshop"

PROMPT_MODES = {
    "study": "Create a study plan that helps me understand this ph-civ orientation card without treating it as a substitute for the source lecture.",
    "seminar": "Write seminar questions that test the card's framing, pressure points, and limits.",
    "creative": "Generate creative project prompts inspired by this card, preserving the card's limits and avoiding unsupported claims.",
    "counter-reading": "Develop counter-readings and skeptical questions that keep the card grounded in its stated limits.",
}

SURFACES = load_surfaces()["surfaces"]

VOLUME_ALIASES = {
    "volume-i": "volume_i",
    "volume-ii": "volume_ii",
    "volume_i": "volume_i",
    "volume_ii": "volume_ii",
}

COMMENTARY_CANVAS_FIELDS = {
    "canvas_status": "open",
    "analysis_depth": "seed",
    "scaffold_version": "ph_civ_commentary_canvas_v1",
}

COMMENTARY_CANVAS_HEADINGS = [
    "## Project Canvas",
    "### Project Leverage",
    "### Laws / Patterns Exposed",
    "### Volume Role",
    "### Museum Hooks",
    "### Strategy / Present-Day Application",
    "### Counter-Readings",
    "### Open Questions",
    "### Build Notes / Future Enhancements",
]

PUBLIC_BOUNDARY_SCAN_PATHS = [
    "AGENTS.md",
    "README.md",
    "START-HERE.md",
    "llms.txt",
    "llms-full.txt",
    "book",
    "data",
    "docs",
    "ph-civ",
    "ph-apo",
    "ph-mus",
    "prompts",
    "schemas",
]

PUBLIC_BOUNDARY_SCAN_EXCLUDES = {
    "docs/strategy-codex-bridge.md",
}

PUBLIC_BOUNDARY_FORBIDDEN_MARKERS = [
    "strategy_codex",
    "strategy-codex",
    "Strategy-Codex",
    "transfer_lecture_path",
    "strategy_codex_lecture_path",
    "strategy_codex_analysis_path",
    "strategy_codex_evidence_pack_path",
    "exported_from_strategy_codex_at",
    "raw-input",
    "recursion-gate",
    "self-memory",
    "session-log",
    "C:\\",
    "C:/",
]

ALLOWED_ROUTE_TYPES = {"spine", "paired_close_reading", "application", "coda"}


def card_surface(card: dict) -> str:
    return "ph-civ" if card["part"] == "civilization" else "ph-apo"


def bridge_support_ids() -> set[str]:
    return set(load_course_architecture()["bridge_support_nodes"])


def conceptual_volume_ids(card: dict) -> list[str]:
    volumes: list[str] = []
    if card["part"] == "civilization" or card["source_id"] in bridge_support_ids():
        volumes.append("volume_i")
    if card["part"] == "world-war":
        volumes.append("volume_ii")
    return volumes


def conceptual_bridge_role(card: dict) -> str | None:
    if card["source_id"] in bridge_support_ids():
        return "volume_i_bridge_support"
    return None


def cards_for_volume(volume_id: str) -> list[dict]:
    canonical = VOLUME_ALIASES.get(volume_id)
    if not canonical:
        raise KeyError(volume_id)
    return [card for card in load_cards() if canonical in conceptual_volume_ids(card)]


def markdown_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}
    fields: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" not in line or line.startswith(" "):
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip().strip('"')
    return fields


def validate_commentary_canvas(source_id: str, commentary_path) -> list[str]:
    text = commentary_path.read_text(encoding="utf-8").replace("\r\n", "\n")
    frontmatter = markdown_frontmatter(text)
    errors: list[str] = []
    if "commentary_status" not in frontmatter:
        errors.append(f"{source_id} missing commentary_status")
    for key, expected in COMMENTARY_CANVAS_FIELDS.items():
        if frontmatter.get(key) != expected:
            errors.append(f"{source_id} invalid {key}: {frontmatter.get(key)}")
    for heading in COMMENTARY_CANVAS_HEADINGS:
        if heading not in text:
            errors.append(f"{source_id} missing commentary canvas heading: {heading}")
    return errors


def validate_public_boundary() -> list[str]:
    root = DATA_ROOT.parent
    errors: list[str] = []
    for relative_root in PUBLIC_BOUNDARY_SCAN_PATHS:
        scan_root = root / relative_root
        if not scan_root.exists():
            continue
        paths = [scan_root] if scan_root.is_file() else scan_root.rglob("*")
        for path in paths:
            if not path.is_file():
                continue
            relative_path = path.relative_to(root).as_posix()
            if relative_path in PUBLIC_BOUNDARY_SCAN_EXCLUDES:
                continue
            if path.suffix not in {".json", ".jsonl", ".md", ".py", ".txt", ".yaml", ".yml"}:
                continue
            text = path.read_text(encoding="utf-8")
            for marker in PUBLIC_BOUNDARY_FORBIDDEN_MARKERS:
                if marker in text:
                    errors.append(
                        f"public boundary leak: {relative_path} contains {marker}"
                    )
    return errors


def visible_cards(surface_scope: str | None = None, include_all: bool = False) -> list[dict]:
    cards = load_cards()
    if include_all or surface_scope is None:
        return cards
    if surface_scope == "ph-civ":
        return [card for card in cards if card["part"] == "civilization"]
    if surface_scope == "ph-apo":
        return [card for card in cards if card["part"] == "world-war"]
    return cards


def route_public_payload(route: dict) -> dict:
    card = get_card(route["source_id"])
    return {
        "source_id": route["source_id"],
        "title": card["title"],
        "surface": route["surface"],
        "part": card["part"],
        "series": card["series"],
        "conceptual_volumes": conceptual_volume_ids(card),
        "bridge_role": conceptual_bridge_role(card),
        "route_type": route["route_type"],
        "caveat": route.get("caveat", ""),
        "what_changes_here": route["what_changes_here"],
        "card": {
            "path": route["card_path"],
            "transcript_path": route["transcript_path"],
            "commentary_path": route["commentary_path"],
        },
        "museum": {
            "status": route["museum_status"],
            "exhibit_path": route.get("museum_exhibit_path"),
        },
        "pressure_echoes": route.get("pressure_echoes", []),
        "civilization_roots": route.get("civilization_roots", []),
    }


def emit_json(data) -> int:
    print(json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True))
    return 0


def cmd_list(args) -> int:
    cards = visible_cards(getattr(args, "surface_scope", None), getattr(args, "all", False))
    if args.series:
        cards = [card for card in cards if card["series"] == args.series]
    if args.part:
        cards = [card for card in cards if card["part"] == args.part]
    if args.spine:
        ids = {sid for node in load_spine()["sequence"] for sid in node["source_ids"]}
        cards = [card for card in cards if card["source_id"] in ids]
    rows = [{"source_id": card["source_id"], "title": card["title"], "series": card["series"], "part": card["part"]} for card in cards]
    if args.json:
        return emit_json(rows)
    for row in rows:
        print(f"{row['source_id']}\t{row['series']}\t{row['part']}\t{row['title']}")
    return 0


def cmd_show(args) -> int:
    try:
        card = get_card(args.source_id)
        scope = getattr(args, "surface_scope", None)
        if scope in {"ph-civ", "ph-apo"} and card_surface(card) != scope:
            print(f"{args.source_id} is not available through {scope}", file=sys.stderr)
            return 2
        if args.format == "json":
            return emit_json(card)
        print(card_markdown(args.source_id), end="")
        return 0
    except KeyError:
        print(f"Unknown source_id: {args.source_id}", file=sys.stderr)
        return 2


def cmd_search(args) -> int:
    q = args.query.casefold()
    matches = []
    for card in visible_cards(getattr(args, "surface_scope", None), getattr(args, "all", False)):
        haystack = "\n".join([card["source_id"], card["title"], json.dumps(card["sections"], ensure_ascii=False)]).casefold()
        if q in haystack and (not args.series or card["series"] == args.series):
            matches.append({"source_id": card["source_id"], "title": card["title"], "series": card["series"], "part": card["part"]})
    if args.json:
        return emit_json(matches)
    for match in matches:
        print(f"{match['source_id']}\t{match['series']}\t{match['title']}")
    return 0


def cmd_route(args) -> int:
    try:
        route = get_route(args.source_id)
    except KeyError:
        print(f"No public route for source_id: {args.source_id}", file=sys.stderr)
        return 2

    scope = getattr(args, "surface_scope", None)
    if (
        scope in {"ph-civ", "ph-apo"}
        and route["surface"] != scope
        and not (scope == "ph-civ" and route["source_id"] in bridge_support_ids())
    ):
        print(f"{args.source_id} is routed through {route['surface']}, not {scope}", file=sys.stderr)
        return 2
    payload = route_public_payload(route)
    if args.json:
        return emit_json(payload)
    print(f"{payload['source_id']}\t{payload['surface']}\t{payload['title']}")
    print(f"route_type: {payload['route_type']}")
    print(f"museum: {payload['museum']['status']}\t{payload['museum']['exhibit_path']}")
    if payload.get("caveat"):
        print(f"caveat: {payload['caveat']}")
    print(f"what changes here: {payload['what_changes_here']}")
    return 0


def cmd_patterns(args) -> int:
    patterns = load_patterns()
    rows = [
        {
            "pattern_id": pattern["pattern_id"],
            "title": pattern["title"],
            "source_ids": pattern["source_ids"],
            "public_status": pattern["public_status"],
        }
        for pattern in patterns
    ]
    if args.json:
        return emit_json(rows)
    for row in rows:
        print(
            f"{row['pattern_id']}\t{row['public_status']}\t"
            f"{','.join(row['source_ids'])}\t{row['title']}"
        )
    return 0


def cmd_pattern(args) -> int:
    try:
        pattern = get_pattern(args.pattern_id)
        if args.format == "json":
            return emit_json(pattern)
        print(pattern_markdown(args.pattern_id), end="")
        return 0
    except KeyError:
        print(f"Unknown pattern_id: {args.pattern_id}", file=sys.stderr)
        return 2


def cmd_bridge(args) -> int:
    try:
        card = get_card(args.source_id)
    except KeyError:
        print(f"Unknown source_id: {args.source_id}", file=sys.stderr)
        return 2
    payload = {
        "source_id": card["source_id"],
        "title": card["title"],
        "patterns": patterns_for_source(card["source_id"]),
    }
    output_format = "json" if args.json else args.format
    if output_format == "json":
        return emit_json(payload)
    print(f"# {payload['source_id']} - {payload['title']}")
    print()
    print("Public bridge patterns:")
    for pattern in payload["patterns"]:
        print(f"- `{pattern['pattern_id']}` - {pattern['title']}")
    if not payload["patterns"]:
        print("- No public bridge patterns currently cite this source.")
    return 0


def cmd_museum_list(args) -> int:
    exhibits = load_museum_index()
    if args.json:
        return emit_json(exhibits)
    for exhibit in exhibits:
        print(f"{exhibit['source_id']}\t{exhibit['surface']}\t{exhibit['museum_status']}\t{exhibit['title']}")
    return 0


def cmd_museum_show(args) -> int:
    for exhibit in load_museum_index():
        if exhibit["source_id"] == args.source_id:
            if args.json:
                return emit_json(exhibit)
            print(f"{exhibit['source_id']}\t{exhibit['surface']}\t{exhibit['title']}")
            print(f"status: {exhibit['museum_status']}")
            print(f"exhibit: {exhibit['museum_exhibit_path']}")
            return 0
    print(f"No museum exhibit for source_id: {args.source_id}", file=sys.stderr)
    return 2


def cmd_prompt(args) -> int:
    try:
        card = get_card(args.source_id)
    except KeyError:
        print(f"Unknown source_id: {args.source_id}", file=sys.stderr)
        return 2
    print(
        f"{PROMPT_MODES[args.mode]}\n\n"
        f"Source ID: {card['source_id']}\n"
        f"Title: {card['title']}\n"
        f"Placement weight: {card['placement_weight']}\n\n"
        f"Where this sits:\n{card['sections']['Where This Sits']}\n\n"
        f"Limits:\n{card['sections']['Limits of the Frame']}"
    )
    return 0


def cmd_spark(args) -> int:
    try:
        card = get_card(args.source_id)
    except KeyError:
        print(f"Unknown source_id: {args.source_id}", file=sys.stderr)
        return 2
    seeds = [
        "What pattern becomes visible here?",
        "What would change if the lecture's main analogy were weaker?",
        "Which pressure point deserves a diagram?",
        "What should a reader verify before quoting this?",
        "What does this card make easier to return to later?",
        "What object, map, or document would make this lecture legible at a glance?",
    ]
    random.seed(card["source_id"])
    for index, prompt in enumerate(random.sample(seeds, k=min(args.count, len(seeds))), start=1):
        print(f"{index}. {prompt}")
    return 0


def cmd_spine(args) -> int:
    spine = load_spine(args.spine_id)
    if args.json:
        return emit_json(spine)
    print(f"# {spine['title']}\n")
    print(spine["description"])
    if spine.get("guardrail"):
        print("")
        print(f"guardrail: {spine['guardrail']}")
    if spine.get("launch_readiness"):
        print(f"launch_readiness: {spine['launch_readiness']}")
    if spine.get("first_reader_gap"):
        print(f"first_reader_gap: {spine['first_reader_gap']}")
    print("")
    for index, node in enumerate(spine["sequence"], start=1):
        print(f"{index}. {node['author']}: {', '.join(node['source_ids'])}")
        if node.get("note"):
            print(f"   {node['note']}")
    return 0


def cmd_path(args) -> int:
    if args.path_id != "homer-to-tolstoy":
        print(f"Unknown path: {args.path_id}", file=sys.stderr)
        return 2
    return cmd_spine(argparse.Namespace(spine_id=args.path_id, json=args.json))


def cmd_validate(args) -> int:
    cards = load_cards()
    errors = []
    ids = set()
    required = ["Where This Sits", "Reading Posture", "Historical Pressure Points", "Limits of the Frame", "Return Path"]
    for card in cards:
        source_id = card.get("source_id")
        if not source_id:
            errors.append("card missing source_id")
            continue
        if source_id in ids:
            errors.append(f"duplicate source_id: {source_id}")
        ids.add(source_id)
        for section in required:
            if not card.get("sections", {}).get(section):
                errors.append(f"{source_id} missing section: {section}")
        if card.get("placement_weight") not in {"strong", "medium", "light"}:
            errors.append(f"{source_id} invalid placement_weight: {card.get('placement_weight')}")
        source_repo = card.get("source_snapshot", {}).get("repo")
        if source_repo != EXPECTED_SOURCE_REPO:
            errors.append(f"{source_id} invalid source repo: {source_repo}")
        source_paths = card.get("source_paths", {})
        transcript_path = source_paths.get("source_chapter_path")
        commentary_path = source_paths.get("commentary_path")
        for label, relative_path in [
            ("transcript", transcript_path),
            ("commentary", commentary_path),
        ]:
            if not relative_path:
                errors.append(f"{source_id} missing {label} path")
                continue
            chapter_path = DATA_ROOT.parent / relative_path
            if not chapter_path.exists():
                errors.append(f"{source_id} missing {label} file: {relative_path}")
            elif label == "commentary":
                errors.extend(validate_commentary_canvas(source_id, chapter_path))
    for metadata_path in [
        DATA_ROOT / "index.json",
        DATA_ROOT / "surfaces.json",
        DATA_ROOT / "routes" / "choreography.json",
    ]:
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        source_repo = metadata.get("source_snapshot", {}).get("repo")
        if source_repo != EXPECTED_SOURCE_REPO:
            errors.append(f"{metadata_path.relative_to(DATA_ROOT)} invalid source repo: {source_repo}")
    choreography = load_choreography()
    route_ids = [route.get("source_id") for route in choreography]
    if len(choreography) != 10:
        errors.append(f"choreography route count must be 10: {len(choreography)}")
    if len(set(route_ids)) != len(route_ids):
        errors.append("choreography route IDs must be unique")
    for route in choreography:
        source_id = route.get("source_id")
        route_type = route.get("route_type")
        if route_type not in ALLOWED_ROUTE_TYPES:
            errors.append(f"{source_id} invalid route_type: {route_type}")
        if not route.get("caveat"):
            errors.append(f"{source_id} missing route caveat")
    route_seed = load_route_seed()
    seed_route_ids = route_seed.get("route_ids", [])
    if route_seed.get("seed_id") != "ten_route_spine_seed":
        errors.append("route seed must be ten_route_spine_seed")
    if seed_route_ids != route_ids:
        errors.append("route seed IDs must match choreography route IDs in order")
    llm_experience = load_llm_experience()
    if not (DATA_ROOT.parent / "START-HERE.md").exists():
        errors.append("START-HERE.md must exist as the LLM bootloader")
    if llm_experience.get("start_here") != "START-HERE.md":
        errors.append("llm-experience.json must point to START-HERE.md")
    full_context = llm_experience.get("full_context", {})
    if full_context.get("path") != "llms-full.txt":
        errors.append("llm-experience.json must point to llms-full.txt")
    full_context_path = DATA_ROOT.parent / "llms-full.txt"
    if not full_context_path.exists():
        errors.append("llms-full.txt must exist as the full LLM context packet")
    else:
        full_context_text = full_context_path.read_text(encoding="utf-8")
        for marker in [
            "full one-shot LLM context packet",
            "First Response Contract",
            "Do not stop at a generic repository summary",
            "Default mode: `first_tour`",
            "Homer to Tolstoy is the Volume I literary spine",
            "ph-mus` is not a third volume",
        ]:
            if marker not in full_context_text:
                errors.append(f"llms-full.txt missing marker: {marker}")
    if llm_experience.get("primary_artifact") != "two_volume_ph_civ":
        errors.append("llm-experience.json invalid primary_artifact")
    first_response = llm_experience.get("first_response_contract", {})
    if first_response.get("default_mode") != "first_tour":
        errors.append("llm-experience first response must default to first_tour")
    if "generic repository summary" not in first_response.get("anti_pattern", ""):
        errors.append("llm-experience must forbid summary-only pasted-URL responses")
    if first_response.get("required_opening_files") != [
        "START-HERE.md",
        "llms.txt",
        "llms-full.txt",
    ]:
        errors.append("llm-experience first response must cite all opening files")
    if first_response.get("opening_route") != "civ-07":
        errors.append("llm-experience first response must open at civ-07")
    if first_response.get("opening_path") != "homer-to-tolstoy":
        errors.append("llm-experience first response must open Homer-to-Tolstoy")
    if not any("Choose one:" in line for line in first_response.get("template", [])):
        errors.append("llm-experience first response template must offer reader choices")
    if llm_experience.get("first_seed", {}).get("route_ids") != seed_route_ids:
        errors.append("llm-experience route IDs must match route seed")
    llm_surfaces = llm_experience.get("public_surfaces", {})
    if llm_surfaces.get("volume_i", {}).get("surface") != "ph-civ":
        errors.append("llm-experience volume_i must use ph-civ")
    if llm_surfaces.get("volume_ii", {}).get("surface") != "ph-apo":
        errors.append("llm-experience volume_ii must use ph-apo")
    if llm_surfaces.get("museum", {}).get("surface") != "ph-mus":
        errors.append("llm-experience museum must use ph-mus")
    if llm_surfaces.get("museum", {}).get("not_a_volume") is not True:
        errors.append("llm-experience must mark ph-mus as not a volume")
    guardrails = "\n".join(llm_experience.get("guardrails", []))
    for marker in [
        "Homer to Tolstoy",
        "Anna Karenina coda",
        "ph-mus is not a third volume",
    ]:
        if marker not in guardrails:
            errors.append(f"llm-experience missing guardrail: {marker}")
    museum_ids = [exhibit.get("source_id") for exhibit in load_museum_index()]
    if set(museum_ids) != set(seed_route_ids):
        errors.append("museum index must contain the same route IDs as the seed")
    sh16_route = next((route for route in choreography if route.get("source_id") == "sh-16"), None)
    if not sh16_route:
        errors.append("choreography must include sh-16")
    else:
        if sh16_route.get("surface") != "ph-apo":
            errors.append("sh-16 route must remain on ph-apo")
        if sh16_route.get("route_type") != "coda":
            errors.append("sh-16 route must use coda route_type")
        caveat = sh16_route.get("caveat", "")
        if "Anna Karenina coda" not in caveat or "not a dedicated Tolstoy lecture" not in caveat:
            errors.append("sh-16 route must preserve the Tolstoy caveat")
    architecture = load_course_architecture()
    if architecture.get("repo_identity") != "ph-civ":
        errors.append("surfaces.json invalid repo_identity")
    if architecture.get("primary_artifact") != "two_volume_ph_civ":
        errors.append("surfaces.json invalid primary_artifact")
    if architecture.get("volumes", {}).get("volume_i", {}).get("surface") != "ph-civ":
        errors.append("volume_i must route through ph-civ")
    if architecture.get("volumes", {}).get("volume_i", {}).get("role") != "law_discovery":
        errors.append("volume_i must use law_discovery role")
    if architecture.get("volumes", {}).get("volume_ii", {}).get("surface") != "ph-apo":
        errors.append("volume_ii must route through ph-apo")
    if architecture.get("volumes", {}).get("volume_ii", {}).get("role") != "law_application":
        errors.append("volume_ii must use law_application role")
    if architecture.get("museum", {}).get("surface") != "ph-mus":
        errors.append("museum layer must route through ph-mus")
    if architecture.get("museum", {}).get("role") != "chapter_exhibit_layer":
        errors.append("museum layer must use chapter_exhibit_layer role")
    if architecture.get("bridge_support_nodes") != ["sh-11", "sh-16", "sh-17", "sh-18"]:
        errors.append("bridge_support_nodes invariant changed")
    literary_spine = load_spine("homer-to-tolstoy")
    if literary_spine.get("launch_readiness") != "defined_not_launch_ready":
        errors.append("homer-to-tolstoy spine must preserve launch readiness tension")
    if "first public reader" not in literary_spine.get("first_reader_gap", ""):
        errors.append("homer-to-tolstoy spine must name the first-reader gap")
    growth_goals = load_growth_goals()
    policy = growth_goals.get("agent_goal_policy", {})
    if growth_goals.get("goal_system") != "ph_civ_public_growth":
        errors.append("growth-goals.json invalid goal_system")
    if policy.get("must_translate_outcome_to_machinery") is not True:
        errors.append("growth goals must translate outcome goals into machinery")
    required_outputs = {
        "README and public contract explain the two-volume ph-civ artifact within one screen",
        "analytics plan defines what counts as a view across GitHub, web, video, social, and document surfaces",
        "distribution calendar converts the target into weekly and monthly milestones",
    }
    campaigns = growth_goals.get("campaigns", [])
    if not campaigns:
        errors.append("growth-goals.json must define at least one campaign")
    for campaign in campaigns:
        if "source-disciplined educational trust" not in campaign.get("unresolved_tension", ""):
            errors.append(f"{campaign.get('campaign_id')} must preserve the growth-vs-trust tension")
        if campaign.get("success_requires_external_audience_behavior") is not True:
            errors.append(f"{campaign.get('campaign_id')} must mark external audience dependency")
        wedge = campaign.get("first_live_wedge", {})
        if wedge.get("wedge_id") != "launch_volume_i_spine":
            errors.append(f"{campaign.get('campaign_id')} must name the first live publishing wedge")
        if wedge.get("launch_readiness") != "defined_not_launch_ready":
            errors.append(f"{campaign.get('campaign_id')} must distinguish defined wedge from launch readiness")
        if "without claiming views have already been earned" not in wedge.get("done_when", ""):
            errors.append(f"{campaign.get('campaign_id')} must forbid fake reach completion")
        outputs = set(campaign.get("measurable_agent_outputs", []))
        if not required_outputs <= outputs:
            errors.append(f"{campaign.get('campaign_id')} missing measurable growth outputs")
    errors.extend(validate_patterns(load_patterns(), cards))
    errors.extend(validate_public_boundary())
    series = Counter(card["series"] for card in cards)
    result = {"status": "valid" if not errors else "invalid", "card_count": len(cards), "series_counts": dict(sorted(series.items())), "errors": errors}
    if args.json:
        emit_json(result)
        return 1 if errors else 0
    print(f"status: {result['status']}")
    print(f"card_count: {len(cards)}")
    for key, value in result["series_counts"].items():
        print(f"{key}: {value}")
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


def validate_patterns(patterns: list[dict], cards: list[dict]) -> list[str]:
    errors: list[str] = []
    pattern_ids: set[str] = set()
    source_ids = {card["source_id"] for card in cards}
    required = {
        "pattern_id",
        "title",
        "summary",
        "strategy_use",
        "source_ids",
        "tags",
        "limits",
        "public_status",
    }
    allowed_status = {"seed", "in_review", "stable"}
    for pattern in patterns:
        pattern_id = pattern.get("pattern_id")
        if not pattern_id:
            errors.append("pattern missing pattern_id")
            continue
        if pattern_id in pattern_ids:
            errors.append(f"duplicate pattern_id: {pattern_id}")
        pattern_ids.add(pattern_id)
        for field in sorted(required):
            if field not in pattern or pattern.get(field) in ("", [], None):
                errors.append(f"{pattern_id} missing field: {field}")
        status = pattern.get("public_status")
        if status not in allowed_status:
            errors.append(f"{pattern_id} invalid public_status: {status}")
        for source_id in pattern.get("source_ids", []):
            if source_id not in source_ids:
                errors.append(f"{pattern_id} unknown source_id: {source_id}")
    return errors


def cmd_surface(args) -> int:
    surface = SURFACES[args.surface]
    if args.json:
        return emit_json({"surface": args.surface, **surface})
    print(f"{args.surface}: {surface['title']}")
    print(f"status: {surface['status']}")
    print(surface["description"])
    return 0


def cmd_status(args) -> int:
    architecture = load_course_architecture()
    if args.json:
        return emit_json(
            {
                "repo_identity": architecture["repo_identity"],
                "primary_artifact": architecture["primary_artifact"],
                "volumes": architecture["volumes"],
                "museum": architecture["museum"],
                "surfaces": SURFACES,
                "unique_card_count": len(load_cards()),
            }
        )
    print("ph-civ: two-volume public Predictive History artifact")
    print(f"primary_artifact: {architecture['primary_artifact']}")
    print(
        "Volume I / ph-civ / Civilization: "
        f"{architecture['volumes']['volume_i']['role']}"
    )
    print(
        "Volume II / ph-apo / Apocalypse: "
        f"{architecture['volumes']['volume_ii']['role']}"
    )
    print("ph-mus: chapter_exhibit_layer for both volumes")
    return 0


def volume_payload(volume_id: str, include_cards: bool = False) -> dict:
    canonical = VOLUME_ALIASES[volume_id]
    architecture = load_course_architecture()
    volume = architecture["volumes"][canonical]
    cards = cards_for_volume(canonical)
    payload = {
        "volume_id": canonical,
        "surface": volume["surface"],
        "title": volume["title"],
        "role": volume["role"],
        "description": volume["description"],
        "card_count": len(cards),
        "bridge_support_nodes": architecture["bridge_support_nodes"]
        if canonical == "volume_i"
        else [],
    }
    if include_cards:
        payload["cards"] = [
            {
                "source_id": card["source_id"],
                "title": card["title"],
                "series": card["series"],
                "part": card["part"],
                "bridge_role": conceptual_bridge_role(card),
            }
            for card in cards
        ]
    return payload


def cmd_volumes(args) -> int:
    architecture = load_course_architecture()
    payload = {
        "repo_identity": architecture["repo_identity"],
        "primary_artifact": architecture["primary_artifact"],
        "volumes": {
            "volume_i": volume_payload("volume_i"),
            "volume_ii": volume_payload("volume_ii"),
        },
        "museum": architecture["museum"],
        "unique_card_count": len(load_cards()),
    }
    if args.json:
        return emit_json(payload)
    for volume in payload["volumes"].values():
        print(f"{volume['volume_id']}\t{volume['surface']}\t{volume['role']}\t{volume['card_count']}")
    print(f"ph-mus\t{payload['museum']['role']}\t{payload['museum']['description']}")
    print(f"unique_card_count\t{payload['unique_card_count']}")
    return 0


def cmd_volume(args) -> int:
    try:
        payload = volume_payload(args.volume_id, include_cards=True)
    except KeyError:
        print(f"Unknown volume: {args.volume_id}", file=sys.stderr)
        return 2
    if args.json:
        return emit_json(payload)
    print(f"# {payload['title']} ({payload['volume_id']})")
    print(f"surface: {payload['surface']}")
    print(f"role: {payload['role']}")
    print(f"card_count: {payload['card_count']}")
    for card in payload["cards"]:
        bridge = f"\t{card['bridge_role']}" if card["bridge_role"] else ""
        print(f"{card['source_id']}\t{card['series']}\t{card['title']}{bridge}")
    return 0


def cmd_growth(args) -> int:
    growth_goals = load_growth_goals()
    if args.json:
        return emit_json(growth_goals)
    print("ph-civ public growth")
    print(growth_goals["principle"])
    print("")
    print("Agent goal rule:")
    print(f"- {growth_goals['agent_goal_policy']['forbidden_completion_claim']}")
    print("- Translate reach ambitions into repo quality, assets, cadence, metrics, and human-approved distribution.")
    print("")
    for campaign in growth_goals["campaigns"]:
        print(f"{campaign['campaign_id']}: {campaign['title']}")
        print(f"status: {campaign['status']}")
        print(f"target: {campaign['target_count']} {campaign['target_metric']} by {campaign['target_date']}")
        print(f"tension: {campaign['unresolved_tension']}")
        print(f"agent work: {campaign['agent_executable_translation']}")
        wedge = campaign.get("first_live_wedge")
        if wedge:
            print(f"first wedge: {wedge['wedge_id']} - {wedge['title']}")
            print(f"readiness: {wedge['launch_readiness']}")
    return 0


def cmd_start(args) -> int:
    experience = load_llm_experience()
    if args.json:
        return emit_json(experience)
    print("ph-civ: LLM-native two-volume Predictive History bootloader")
    print(f"github_url: {experience['github_url']}")
    print(f"start_here: {experience['start_here']}")
    if experience.get("full_context"):
        print(f"full_context: {experience['full_context']['path']}")
    if experience.get("first_response_contract"):
        print(f"default_mode: {experience['first_response_contract']['default_mode']}")
        print(f"opening_path: {experience['first_response_contract']['opening_path']}")
    print(f"primary_artifact: {experience['primary_artifact']}")
    print("surfaces:")
    for key, surface in experience["public_surfaces"].items():
        print(f"- {key}: {surface['surface']} - {surface['role']}")
    print("first_seed:")
    print(f"- {experience['first_seed']['seed_id']}: {', '.join(experience['first_seed']['route_ids'])}")
    print("modes:")
    for mode in experience["modes"]:
        print(f"- {mode['mode']}: {mode['instruction']}")
    print("guardrails:")
    for guardrail in experience["guardrails"]:
        print(f"- {guardrail}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ph-civ", description="Provider-neutral Predictive History study cards and prompts.")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("list", help="List cards.")
    p.add_argument("--series", choices=["civilization", "great-books", "geo-strategy", "game-theory", "secret-history"])
    p.add_argument("--part", choices=["civilization", "world-war"])
    p.add_argument("--spine", action="store_true", help="Limit to Homer-to-Tolstoy spine cards.")
    p.add_argument("--all", action="store_true", help="Include cards outside the current public surface.")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_list)

    p = sub.add_parser("show", help="Show one card.")
    p.add_argument("source_id")
    p.add_argument("--format", choices=["markdown", "json"], default="markdown")
    p.set_defaults(func=cmd_show)

    p = sub.add_parser("search", help="Search cards.")
    p.add_argument("query")
    p.add_argument("--series", choices=["civilization", "great-books", "geo-strategy", "game-theory", "secret-history"])
    p.add_argument("--all", action="store_true", help="Include cards outside the current public surface.")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_search)

    p = sub.add_parser("route", help="Show the public choreography route for one source ID.")
    p.add_argument("source_id")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_route)

    p = sub.add_parser("patterns", help="List downstream strategy-facing public pattern IDs.")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_patterns)

    p = sub.add_parser("pattern", help="Show one public pattern card.")
    p.add_argument("pattern_id")
    p.add_argument("--format", choices=["markdown", "json"], default="markdown")
    p.set_defaults(func=cmd_pattern)

    p = sub.add_parser("bridge", help="Show public patterns attached to one source ID.")
    p.add_argument("source_id")
    p.add_argument("--format", choices=["markdown", "json"], default="markdown")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_bridge)

    p = sub.add_parser("prompt", help="Render a provider-neutral prompt template for one card.")
    p.add_argument("source_id")
    p.add_argument("--mode", choices=sorted(PROMPT_MODES), default="study")
    p.set_defaults(func=cmd_prompt)

    p = sub.add_parser("spark", help="Generate deterministic study sparks for one card.")
    p.add_argument("source_id")
    p.add_argument("--count", type=int, default=3)
    p.set_defaults(func=cmd_spark)

    p = sub.add_parser("spine", help="Show a spine.")
    p.add_argument("spine_id", nargs="?", default="homer-to-tolstoy")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_spine)

    p = sub.add_parser("path", help="Show a named path.")
    p.add_argument("path_id")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_path)

    p = sub.add_parser("validate", help="Validate packaged cards.")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_validate)

    p = sub.add_parser("status", help="Show the current public surface status.")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_status)

    p = sub.add_parser("start", help="Show the LLM-native start-here bootloader.")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_start)

    p = sub.add_parser("volumes", help="Show the two-volume ph-civ architecture.")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_volumes)

    p = sub.add_parser("volume", help="Show cards for one conceptual volume.")
    p.add_argument("volume_id", choices=sorted(VOLUME_ALIASES))
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_volume)

    p = sub.add_parser("growth", help="Show public-growth goals and agent-executable translation rules.")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_growth)

    p = sub.add_parser("surface", help="Show public surface metadata.")
    p.add_argument("surface", choices=sorted(SURFACES), nargs="?", default="ph-civ")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_surface)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    args.surface_scope = "ph-civ"
    return args.func(args)


def apo_main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv or ["list"])
    args.surface_scope = "ph-apo"
    return args.func(args)


def build_museum_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ph-mus", description="Predictive History Museum public manifest routes.")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("status", help="Show ph-mus status.")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=lambda args: cmd_surface(argparse.Namespace(surface="ph-mus", json=args.json)))

    p = sub.add_parser("list", help="List published public museum exhibit manifests.")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_museum_list)

    p = sub.add_parser("show", help="Show one museum exhibit manifest.")
    p.add_argument("source_id")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_museum_show)

    p = sub.add_parser("route", help="Show the public route for one museum exhibit.")
    p.add_argument("source_id")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_route)
    return parser


def mus_main(argv: list[str] | None = None) -> int:
    args = build_museum_parser().parse_args(argv or ["list"])
    args.surface_scope = "ph-mus"
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
