# Essays

**Canonical public home** for Predictive History **Substack and long-form essay** chapters.

Repo path: **`essays/`** at the repository root (sibling to [`lectures/`](../lectures/README.md), [`interviews/`](../interviews/README.md), [`ph-civ/`](../ph-civ/README.md), [`ph-apo/`](../ph-apo/README.md), [`book/`](../book/), [`sources/`](../sources/)).

## Public ID scheme

**Pattern:** `essay-YYYY-MM-DD-{substack-slug}`

Examples: `essay-2025-08-06-vision-mission-goals`, `essay-2025-09-27-the-empire-goes-to-war`.

| Field | Detail |
| --- | --- |
| **Date** | Substack `publication_date` (pinned in [`data/essays/manifest.json`](../data/essays/manifest.json)) |
| **Slug** | `substack_slug` from packet frontmatter (URL path segment) |
| **Folder** | `essays/{source_id}/` with essay body, commentary canvas, and README |
| **Catalog** | ph-civ essays surface in [`docs/predictive-history-index.md`](../docs/predictive-history-index.md) |

**Public today:** 43 essay chapter packets (`essay-2025-08-06-vision-mission-goals` … `essay-2026-06-19-peace-in-our-time`).

### Workshop crosswalk (`es-*`)

Frozen workshop `es-01` … `es-32` in strategy-codex `codex/predictive-history/metadata/sources.yaml` map to dated public IDs. Full legacy ↔ dated crosswalk: [`data/essays/manifest.json`](../data/essays/manifest.json) (`legacy_source_id`, optional `workshop_source_id`, `source_id`).

| Legacy | Workshop | Example dated `source_id` |
| --- | --- | --- |
| `essay-01` | `es-01` | `essay-2025-08-06-vision-mission-goals` |
| `essay-32` | `es-32` | `essay-2025-10-15-secret-history-10-the-war-of-heaven` (see manifest for exact slug) |
| `essay-33` … `essay-43` | — | public intakes after workshop promotion |

**Deprecated:** sequential `essay-NN` folder URLs (`…/essays/essay-07/…`) **404 after 2026-06-26 hard cut**. Substack canonical URLs are unchanged. See [`docs/essay-dated-id-migration.md`](../docs/essay-dated-id-migration.md).

**Same-day collision rule:** if two essays share a `publication_date`, append `-2` or a title fragment to the slug before assigning `source_id` (none in corpus today).

## Recategorization (operator policy)

Essays are **medium-first** on **`essays/<source_id>/`** with catalog surface **`ph-civ`** / part **`civilization`**.

Reader rollup under [`book/volume-ii-apocalypse/sub/`](../book/volume-ii-apocalypse/sub/) may remain as **cross-links**; **`essays/essay-YYYY-MM-DD-*`** is the canonical namespace.

## Packet shape

Each essay chapter:

- `{source_id}.md` — verbatim essay body
- `{source_id}-commentary.md` — open commentary canvas
- `README.md` — public study doorway (`## Source` + Substack URL)

Registry: [`data/cards.jsonl`](../data/cards.jsonl) · catalog: [`docs/predictive-history-index.md`](../docs/predictive-history-index.md).

## Catalog fields

| Field | Value |
|-------|--------|
| `source_id` | `essay-YYYY-MM-DD-{substack-slug}` |
| `series` | `essays` |
| `part` | `civilization` |
| `surface` | `ph-civ` |
| `source_paths.*` | under `essays/{source_id}/` |

Intake script: [`scripts/intake_essays_phase2.py`](../scripts/intake_essays_phase2.py)
