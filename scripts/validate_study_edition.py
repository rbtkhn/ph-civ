#!/usr/bin/env python3
"""Validate study-edition bundles: anchor integrity and required outputs."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE_DATA = ROOT / "site" / "_data" / "chapters"
SITE_DIST = ROOT / "site" / "dist" / "study"


def validate_bundle(path: Path) -> list[str]:
    errors: list[str] = []
    bundle = json.loads(path.read_text(encoding="utf-8"))
    source_id = bundle.get("source_id", path.stem)
    sections = {row["slug"] for row in bundle.get("sections", [])}
    for claim in bundle.get("claims", []):
        anchor = claim.get("anchor")
        if anchor not in sections:
            errors.append(f"{source_id}: claim {claim.get('n')} missing section #{anchor}")
    html_path = SITE_DIST / source_id / "index.html"
    if not html_path.is_file():
        errors.append(f"{source_id}: missing HTML output {html_path.relative_to(ROOT)}")
    else:
        html = html_path.read_text(encoding="utf-8")
        for slug in sections:
            if f'id="{slug}"' not in html:
                errors.append(f"{source_id}: HTML missing section id={slug}")
        for claim in bundle.get("claims", []):
            n = claim.get("n")
            if f'id="claim-{n}"' not in html:
                errors.append(f"{source_id}: HTML missing claim-{n}")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate study-edition outputs.")
    parser.add_argument("--chapter", default="civ-07")
    args = parser.parse_args(argv)
    json_path = SITE_DATA / f"{args.chapter}.json"
    if not json_path.is_file():
        print(f"validate_study_edition: missing bundle {json_path.relative_to(ROOT)}", file=sys.stderr)
        return 1
    errors = validate_bundle(json_path)
    if errors:
        for err in errors:
            print(err, file=sys.stderr)
        print(f"validate_study_edition: {len(errors)} error(s)", file=sys.stderr)
        return 1
    print(f"validate_study_edition: ok ({args.chapter})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
