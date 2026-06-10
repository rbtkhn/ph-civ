# Commentary Canvas

Commentaries are working surfaces for enhancing and leveraging ph-civ. A seeded commentary is not finished analysis. It is a protected surface for later synthesis.

## Hybrid model (Volume I Parts pilot)

**Chapter commentary (thin receipt)** — one per chapter folder:

- Layer 0–2: metadata, neutral summary, transcript pin-cites
- `## Part apparatus` pointer to the parent Part commentary and bibliography
- Minimal `Project Canvas (chapter-local)` — open questions only

**Part commentary (thick synthesis)** — one per Volume I Part (pilot: Part II only):

- Cross-chapter prediction ledger, Hellenic grammar, corridor placement
- Great Books sections (`### gb-NN`) when woven into the Part
- External counter-readings; links to Part bibliography

**Part bibliography** — sibling markdown (`part-NN-{slug}-bibliography.md`):

- External primary/secondary sources only; every entry tagged `supports: civ-NN` and/or `gb-NN`
- Chapter commentaries link here; do not duplicate bib blocks per chapter

Naming law: see `book/volume-i-civilization/parts/README.md`.

## Chapter commentary (thin)

Every chapter commentary should preserve:

- the lecture transcript as the source body, without rewriting it
- Layer 0–2 source-backed notes with line references
- open canvas metadata in frontmatter
- a Part apparatus pointer when the chapter belongs to a Part with apparatus files

Required frontmatter (chapter):

- `commentary_status`
- `canvas_status: open`
- `analysis_depth: seed` (or `layer2_drafted` when Layer 2 is populated)
- `scaffold_version: ph_civ_commentary_canvas_v1`

Optional when Part apparatus exists:

- `part_id`, `part_commentary_path`, `part_bibliography_path` on transcript or commentary

Cross-chapter predictions, external counter-readings, and bibliography belong in **Part** files, not duplicated in chapter commentaries.

## Part commentary (thick)

Required frontmatter (Part):

- `part_id`, `part_number`, `volume: I`
- `commentary_status`, `canvas_status: open`
- `scaffold_version: ph_civ_part_commentary_v1`
- `doorway_path`, `bibliography_path`

Part Project Canvas sections mirror the chapter canvas at Part grain (leverage, patterns, museum hooks, strategy, open questions).

The scaffold is intentionally permissive. It should invite development without implying that commentary is complete.
