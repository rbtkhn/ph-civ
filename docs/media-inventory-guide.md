# Predictive History Museum Exhibit Guide

The Predictive History Museum is a chapter-exhibit project. Curators assemble stored artifacts, metadata, and visitor paths for chapters in Predictive History: Civilization and Predictive History: Apocalypse.

Flat inventories can be useful as temporary imports, exports, or review checklists. They are not the museum source of truth.

## Scope

- Predictive History: Civilization chapter exhibits
- Predictive History: Apocalypse chapter exhibits
- Public museum manifests and generated exhibit pages

Each chapter should have one exhibit.

## Exhibit Target

Each finished exhibit should contain a curated set of artifacts, usually 5-15, arranged into rooms.

Rooms:

- `entrance_artifact`
- `context_room`
- `primary_artifacts_and_texts`
- `comparison_artifacts`
- `pressure_systems`
- `caution_room`

## Required Fields

See `schemas/museum-exhibit.schema.json` and `schemas/museum-artifact.schema.json`.

Every accepted artifact needs:

- stable artifact ID
- chapter ID
- room
- title
- artifact type
- local vault path
- shared cloud path
- provenance URL or citation
- source name
- rights status
- what to notice
- lecture connection
- limit or caution
- curator note

URLs are provenance, not storage.

## Quality Standard

Good artifacts are not merely related. They help a visitor notice a pattern: inheritance, pressure, transformation, analogy, rupture, geography, institution, technology, imagination, limit, or return path.

The best exhibit has a clear path: an opening object, context, primary evidence, comparison, pressure systems, and a caution that prevents overclaiming.
