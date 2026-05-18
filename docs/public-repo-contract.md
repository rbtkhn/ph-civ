# Public Repository Contract

This repository is the public-facing distribution layer for the two-volume PH-CIV artifact: `ph-civ`, `ph-apo`, and `ph-mus`.

## Public Surfaces

- `ph-civ`: **Volume I / Predictive History: Civilization** public orientation cards, paths, prompts, and study navigation for discovering the laws of history.
- `ph-apo`: **Volume II / Predictive History: Apocalypse** public orientation cards, paths, prompts, and study navigation for applying the laws of history.
- `ph-mus`: **Predictive History Museum** public exhibit manifests, artifact metadata, schemas, validation rules, and generated reader-facing exhibit pages for both volumes.

`ph-mus` is not a third volume. It is the chapter exhibit layer corresponding to chapters across Volume I and Volume II.

## Source Of Truth Boundary

This repo publishes public-facing material, including chapter transcripts, chapter commentaries, public cards, routes, prompts, schemas, and manifests. It is not a private notes workspace and not the large artifact archive.

The current chapter corpus was imported from the maintained Predictive History workspace and keeps that snapshot as provenance. Physical source series and folder labels are provenance metadata; the public reader architecture is the two-volume PH-CIV rollup.

Each public chapter consists of:

- lecture transcript
- companion commentary
- public orientation/navigation metadata

## Museum Storage Boundary

Museum artifacts must not be represented by URLs alone.

Every accepted museum artifact needs:

- a local file in the museum vault
- a mirrored file in the shared document cloud workspace
- provenance URL or citation
- rights status
- exhibit and room assignment
- curator note
- limit or caution

Git should track manifests, metadata, schemas, small generated pages, and validation rules. Git should not be used as the primary storage system for large image, audio, video, PDF, scan, or derivative archives.

## Chapter Exhibit Model

The primary museum unit is the chapter exhibit.

Each exhibit should map to one chapter in `ph-civ` or `ph-apo`. Every chapter should eventually have a corresponding `ph-mus` exhibit. A useful exhibit contains a small curated set of artifacts arranged into rooms:

- `entrance_artifact`
- `context_room`
- `primary_artifacts_and_texts`
- `comparison_artifacts`
- `pressure_systems`
- `caution_room`

Flat item inventories may be useful as imports or review exports, but they are not the museum source of truth.

The current public choreography export is `data/routes/choreography.json`; the public museum exhibit index is `data/museum/index.json`. These files expose only safe routing metadata and manifest pointers, not artifact binaries.

## Human Curator Role

Human curators provide judgment that cannot be automated away: selection taste, cultural and historical balance, rights prudence, emotional calibration, representative caution, and final responsibility for why an artifact belongs in a chapter exhibit.
