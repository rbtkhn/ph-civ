from __future__ import annotations

import argparse
import json
import random
import sys
from collections import Counter

from .data import card_markdown, get_card, load_cards, load_spine

PROMPT_MODES = {
    "study": "Create a study plan that helps me understand this ph-civ orientation card without treating it as a substitute for the source lecture.",
    "seminar": "Write seminar questions that test the card's framing, pressure points, and limits.",
    "creative": "Generate creative project prompts inspired by this card, preserving the card's limits and avoiding unsupported claims.",
    "counter-reading": "Develop counter-readings and skeptical questions that keep the card grounded in its stated limits.",
}

SURFACES = {
    "ph-civ": {
        "title": "Predictive History: Civilization",
        "status": "active",
        "description": "Public orientation cards, study prompts, paths, and card validation.",
    },
    "ph-apo": {
        "title": "Predictive History: Apocalypse",
        "status": "reserved",
        "description": "Public Apocalypse cards and paths are reserved here and will be populated from reviewed exports.",
    },
    "ph-mus": {
        "title": "Predictive History Museum",
        "status": "reserved",
        "description": "Public exhibit manifests, artifact metadata, schemas, and generated museum pages. Large artifact files live outside Git.",
    },
}


def emit_json(data) -> int:
    print(json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True))
    return 0


def cmd_list(args) -> int:
    cards = load_cards()
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
        if args.format == "json":
            return emit_json(get_card(args.source_id))
        print(card_markdown(args.source_id), end="")
        return 0
    except KeyError:
        print(f"Unknown source_id: {args.source_id}", file=sys.stderr)
        return 2


def cmd_search(args) -> int:
    q = args.query.casefold()
    matches = []
    for card in load_cards():
        haystack = "\n".join([card["source_id"], card["title"], json.dumps(card["sections"], ensure_ascii=False)]).casefold()
        if q in haystack and (not args.series or card["series"] == args.series):
            matches.append({"source_id": card["source_id"], "title": card["title"], "series": card["series"], "part": card["part"]})
    if args.json:
        return emit_json(matches)
    for match in matches:
        print(f"{match['source_id']}\t{match['series']}\t{match['title']}")
    return 0


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


def cmd_surface(args) -> int:
    surface = SURFACES[args.surface]
    if args.json:
        return emit_json({"surface": args.surface, **surface})
    print(f"{args.surface}: {surface['title']}")
    print(f"status: {surface['status']}")
    print(surface["description"])
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ph-civ", description="Provider-neutral Predictive History study cards and prompts.")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("list", help="List cards.")
    p.add_argument("--series", choices=["civilization", "great-books", "geo-strategy", "game-theory", "secret-history"])
    p.add_argument("--part", choices=["civilization", "world-war"])
    p.add_argument("--spine", action="store_true", help="Limit to Homer-to-Tolstoy spine cards.")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_list)

    p = sub.add_parser("show", help="Show one card.")
    p.add_argument("source_id")
    p.add_argument("--format", choices=["markdown", "json"], default="markdown")
    p.set_defaults(func=cmd_show)

    p = sub.add_parser("search", help="Search cards.")
    p.add_argument("query")
    p.add_argument("--series", choices=["civilization", "great-books", "geo-strategy", "game-theory", "secret-history"])
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_search)

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

    p = sub.add_parser("surface", help="Show public surface metadata.")
    p.add_argument("surface", choices=sorted(SURFACES), nargs="?", default="ph-civ")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_surface)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)

def compat_main(argv: list[str] | None = None) -> int:
    return main(argv)


def reserved_surface_main(surface: str, argv: list[str] | None = None) -> int:
    args = list(argv or sys.argv[1:])
    if args in ([], ["status"]):
        return cmd_surface(argparse.Namespace(surface=surface, json=False))
    if args == ["--json"] or args == ["status", "--json"]:
        return cmd_surface(argparse.Namespace(surface=surface, json=True))
    print(f"{surface} currently supports: status [--json]", file=sys.stderr)
    return 2


def apo_main(argv: list[str] | None = None) -> int:
    return reserved_surface_main("ph-apo", argv)


def mus_main(argv: list[str] | None = None) -> int:
    return reserved_surface_main("ph-mus", argv)


if __name__ == "__main__":
    raise SystemExit(main())
