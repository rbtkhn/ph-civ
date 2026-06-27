from __future__ import annotations

import json
from pathlib import Path

from civ_ph.data import PACKAGE_ROOT, load_cards
from civ_ph.volume_i_parts import load_volume_i_parts_registry

BOOK_PATH_PREFIX = "book/"

FORBIDDEN_TOMBSTONE_PHRASES = (
    "canonical public reader root",
    "canonical two-volume reader",
)

PARTS_PATH_KEYS = (
    "doorway_shelf",
    "spine_ssot",
    "doorway_path",
    "commentary_path",
    "bibliography_path",
)

CATALOG_INDEX_REL = "docs/predictive-history-index.json"
ROUTES_DIR_REL = "data/routes"


def _is_book_repo_path(value: str) -> bool:
    if not value.startswith(BOOK_PATH_PREFIX):
        return False
    rest = value[len(BOOK_PATH_PREFIX) :]
    return bool(rest) and not rest[0].isspace() and ("/" in rest or rest.endswith((".md", ".json", ".yaml", ".yml")))


def _book_path_strings(obj: object) -> list[str]:
    """Collect repo-relative strings that start with book/."""
    found: list[str] = []
    if isinstance(obj, str):
        if _is_book_repo_path(obj):
            found.append(obj)
    elif isinstance(obj, dict):
        for value in obj.values():
            found.extend(_book_path_strings(value))
    elif isinstance(obj, list):
        for item in obj:
            found.extend(_book_path_strings(item))
    return found


def validate_book_tombstone(*, repo_root: Path | None = None) -> list[str]:
    root = repo_root or PACKAGE_ROOT
    errors: list[str] = []
    book_dir = root / "book"
    if not book_dir.exists():
        errors.append("book/ tombstone directory missing")
        return errors

    for path in book_dir.rglob("*"):
        if path.is_dir():
            continue
        rel = path.relative_to(book_dir).as_posix()
        if rel != "README.md":
            errors.append(f"book/ must contain only README.md tombstone; found: book/{rel}")

    readme = book_dir / "README.md"
    if not readme.is_file():
        errors.append("book/README.md tombstone missing")
        return errors

    text = readme.read_text(encoding="utf-8").lower()
    for phrase in FORBIDDEN_TOMBSTONE_PHRASES:
        if phrase in text:
            errors.append(
                f"book/README.md must not claim deprecated canonical status: contains {phrase!r}"
            )
    return errors


def validate_book_namespace(*, repo_root: Path | None = None) -> list[str]:
    root = repo_root or PACKAGE_ROOT
    errors: list[str] = []
    errors.extend(validate_book_tombstone(repo_root=root))

    for card in load_cards():
        source_id = card.get("source_id", "?")
        for key, value in card.get("source_paths", {}).items():
            if isinstance(value, str) and _is_book_repo_path(value):
                errors.append(f"{source_id} source_paths.{key} must not use book/: {value}")

    catalog_path = root / CATALOG_INDEX_REL
    if catalog_path.is_file():
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
        for path in _book_path_strings(catalog):
            errors.append(f"{CATALOG_INDEX_REL} must not reference book/: {path}")

    registry = load_volume_i_parts_registry()
    for key in ("doorway_shelf", "spine_ssot"):
        value = registry.get(key, "")
        if isinstance(value, str) and _is_book_repo_path(value):
            errors.append(f"volume-i-parts.json {key} must not use book/: {value}")
    for part in registry.get("parts", []):
        part_id = part.get("part_id", "?")
        for key in PARTS_PATH_KEYS:
            if key in {"doorway_shelf", "spine_ssot"}:
                continue
            value = part.get(key, "")
            if isinstance(value, str) and _is_book_repo_path(value):
                errors.append(f"volume-i-parts.json {part_id}.{key} must not use book/: {value}")

    routes_dir = root / ROUTES_DIR_REL
    if routes_dir.is_dir():
        for route_file in sorted(routes_dir.glob("*.json")):
            payload = json.loads(route_file.read_text(encoding="utf-8"))
            for path in _book_path_strings(payload):
                rel = route_file.relative_to(root).as_posix()
                errors.append(f"{rel} must not reference book/: {path}")

    return errors
