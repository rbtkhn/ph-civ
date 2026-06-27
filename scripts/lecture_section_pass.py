#!/usr/bin/env python3
"""Lecture pass A CLI — audit, slug retitle, geo maps, apply section maps."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

from lecture_rails_lib import (
    MAPS_ROOT,
    apply_section_map,
    audit_lectures,
    classify_transcript,
    draft_geo_map,
    draft_section_map,
    list_transcript_paths,
    load_lecture_card_ids,
    retitle_slug_transcript,
    save_section_map,
)

REPO_ROOT = Path(__file__).resolve().parents[1]


def cmd_audit(args: argparse.Namespace) -> int:
    rows = audit_lectures(args.series)
    card_ids = load_lecture_card_ids()
    transcript_ids = {r.source_id for r in rows}
    orphans = sorted(transcript_ids - card_ids)

    counts: dict[str, int] = {}
    for row in rows:
        counts[row.rail_status] = counts.get(row.rail_status, 0) + 1

    print(f"lectures audited: {len(rows)}")
    print(f"status: {counts}")
    if orphans:
        print(f"orphan transcripts (no card): {orphans}")

    for row in rows:
        warn = f" [{row.warn}]" if row.warn else ""
        print(f"{row.source_id}\t{row.rail_status}\t{row.section_count}{warn}")

    if args.strict:
        bad = [r for r in rows if r.rail_status != "title_case"]
        if bad:
            print(f"strict fail: {len(bad)} packets not title_case", file=sys.stderr)
            return 1
    return 0


def _paths_for_source_or_series(args: argparse.Namespace) -> list[Path]:
    if args.source_id:
        return [
            p
            for p in list_transcript_paths()
            if p.name == f"{args.source_id}-transcript.md"
        ]
    return list_transcript_paths(args.series)


def cmd_slug_retitle(args: argparse.Namespace) -> int:
    paths = _paths_for_source_or_series(args)
    changed = 0
    for path in paths:
        row = classify_transcript(path)
        if row.rail_status not in {"slug", "mixed"}:
            continue
        n = retitle_slug_transcript(path, dry_run=args.dry_run)
        changed += 1 if n else 0
    print(f"slug-retitle touched: {changed}")
    return 0


def cmd_draft_map(args: argparse.Namespace) -> int:
    paths = _paths_for_source_or_series(args)
    drafted = 0
    for path in paths:
        row = classify_transcript(path)
        if row.rail_status == "title_case" and row.section_count >= 2:
            continue
        source_id = path.name.replace("-transcript.md", "")
        sections = draft_section_map(path, template=args.template)
        if args.dry_run:
            print(f"dry-run {source_id}: {len(sections)} sections")
        else:
            save_section_map(source_id, sections)
            print(f"drafted {source_id}.yaml ({len(sections)} sections)")
        drafted += 1
    print(f"draft-map drafted: {drafted}")
    return 0


def cmd_geo_from_timestamps(args: argparse.Namespace) -> int:
    paths = list_transcript_paths(args.series or "geo-strategy")
    drafted = 0
    for path in paths:
        try:
            sections = draft_geo_map(path)
        except ValueError as exc:
            print(f"skip {path.name}: {exc}")
            continue
        if not sections:
            continue
        source_id = path.name.replace("-transcript.md", "")
        if args.dry_run:
            print(f"dry-run {source_id}: {len(sections)} sections")
        else:
            save_section_map(source_id, sections)
            print(f"drafted {source_id}.yaml ({len(sections)} sections)")
        drafted += 1
    print(f"geo maps drafted: {drafted}")
    return 0


def cmd_apply(args: argparse.Namespace) -> int:
    if args.source_id:
        ids = [args.source_id]
    elif args.series:
        ids = [
            p.name.replace("-transcript.md", "")
            for p in list_transcript_paths(args.series)
        ]
    else:
        print("specify --source-id or --series", file=sys.stderr)
        return 1

    applied = 0
    for source_id in ids:
        map_path = MAPS_ROOT / f"{source_id}.yaml"
        if not map_path.exists():
            if args.auto_paragraph:
                tpl_path = MAPS_ROOT / "_templates" / f"{args.template}.yaml"
                if not tpl_path.exists():
                    print(f"skip {source_id}: no map and no template", file=sys.stderr)
                    continue
                sections = yaml.safe_load(tpl_path.read_text(encoding="utf-8"))["sections"]
            else:
                print(f"skip {source_id}: no map at {map_path}")
                continue
        else:
            sections = yaml.safe_load(map_path.read_text(encoding="utf-8"))["sections"]

        path = next(
            p for p in list_transcript_paths() if p.name == f"{source_id}-transcript.md"
        )
        row = classify_transcript(path)
        if row.rail_status == "title_case" and row.section_count >= 2 and not args.force:
            print(f"skip {source_id}: already sectioned ({row.section_count} rails)")
            continue
        apply_section_map(path, sections, dry_run=args.dry_run)
        applied += 1
    print(f"applied: {applied}")
    return 0


def cmd_auto_section(args: argparse.Namespace) -> int:
    tpl_path = MAPS_ROOT / "_templates" / f"{args.template}.yaml"
    sections = yaml.safe_load(tpl_path.read_text(encoding="utf-8"))["sections"]
    paths = list_transcript_paths(args.series)
    applied = 0
    for path in paths:
        row = classify_transcript(path)
        if row.rail_status == "title_case" and row.section_count >= 2:
            continue
        if row.rail_status == "slug" or row.rail_status == "mixed":
            continue
        apply_section_map(path, sections, dry_run=args.dry_run)
        applied += 1
    print(f"auto-section applied: {applied}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Lecture pass A section rails")
    sub = parser.add_subparsers(dest="command", required=True)

    p_audit = sub.add_parser("audit", help="audit lecture transcript rails")
    p_audit.add_argument("--series")
    p_audit.add_argument("--strict", action="store_true")
    p_audit.set_defaults(func=cmd_audit)

    p_slug = sub.add_parser("slug-retitle", help="T1 slug to Title Case retitle")
    p_slug.add_argument("--series")
    p_slug.add_argument("--source-id")
    p_slug.add_argument("--dry-run", action="store_true")
    p_slug.set_defaults(func=cmd_slug_retitle)

    p_draft = sub.add_parser("draft-map", help="seed insert-tier YAML from card/timestamps/template")
    p_draft.add_argument("--series")
    p_draft.add_argument("--source-id")
    p_draft.add_argument("--template")
    p_draft.add_argument("--dry-run", action="store_true")
    p_draft.set_defaults(func=cmd_draft_map)

    p_geo = sub.add_parser("geo-from-timestamps", help="draft geo YAML from preface")
    p_geo.add_argument("--series", default="geo-strategy")
    p_geo.add_argument("--dry-run", action="store_true")
    p_geo.set_defaults(func=cmd_geo_from_timestamps)

    p_apply = sub.add_parser("apply", help="apply section map YAML")
    p_apply.add_argument("--source-id")
    p_apply.add_argument("--series")
    p_apply.add_argument("--dry-run", action="store_true")
    p_apply.add_argument("--force", action="store_true")
    p_apply.add_argument("--auto-paragraph", action="store_true")
    p_apply.add_argument("--template", default="gt-monologue")
    p_apply.set_defaults(func=cmd_apply)

    p_auto = sub.add_parser("auto-section", help="template paragraph split on flat series")
    p_auto.add_argument("--series", required=True)
    p_auto.add_argument("--template", required=True)
    p_auto.add_argument("--dry-run", action="store_true")
    p_auto.set_defaults(func=cmd_auto_section)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
