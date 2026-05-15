# Media Inventory Guide

The media inventory is a corpus-scale search and curation project. Curators collect candidate public references for every civ-ph card. Maintainers and agents later normalize, caption, validate, and render final media packs.

## Scope

- Civilization: `civ-01` through `civ-60`
- Great Books: routed `gb-*` entries
- Geo-Strategy: `geo-01` through `geo-20`
- Game Theory: `gt-01` through `gt-22`
- Secret History: `sh-01` through `sh-28`

Current scope: 140 civ-ph entries.

## Per-Entry Inventory Target

Collect 15-25 candidate items per source ID. Final media packs may use fewer.

Buckets:

- `entry_object`
- `context_anchor`
- `primary_object_or_text`
- `comparison_object`
- `pressure_or_structure`
- `limit_or_caution`

## Required Fields

See `schemas/media-inventory-item.schema.json` and `data/media-inventory/template.csv`.

## Quality Standard

Good items are not merely related. They help a student notice a pattern: inheritance, pressure, transformation, analogy, rupture, geography, institution, technology, imagination, limit, or return path.
