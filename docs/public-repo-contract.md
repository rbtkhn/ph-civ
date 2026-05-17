# Public Repository Contract

This repository is the public-facing distribution layer for Predictive History: Civilization, Predictive History: Apocalypse, and the Predictive History Museum.

## Public Surfaces

- **Predictive History: Civilization**: public orientation cards, paths, prompts, and study navigation.
- **Predictive History: Apocalypse**: public orientation cards, paths, prompts, and study navigation as that surface is prepared.
- **Predictive History Museum**: public exhibit manifests, artifact metadata, schemas, validation rules, and generated reader-facing exhibit pages.

## Source Of Truth Boundary

This repo can publish public-facing material, but it is not the private editorial workspace and not the large artifact archive.

The canonical private editorial source remains the maintained Predictive History workspace. This public repository receives exported, reviewed, or deliberately public materials from that source.

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

Each exhibit should map to one chapter in Predictive History: Civilization or Predictive History: Apocalypse. A useful exhibit contains a small curated set of artifacts arranged into rooms:

- `entrance_artifact`
- `context_room`
- `primary_artifacts_and_texts`
- `comparison_artifacts`
- `pressure_systems`
- `caution_room`

Flat item inventories may be useful as imports or review exports, but they are not the museum source of truth.

## Human Curator Role

Human curators provide judgment that cannot be automated away: selection taste, cultural and historical balance, rights prudence, emotional calibration, representative caution, and final responsibility for why an artifact belongs in a chapter exhibit.
