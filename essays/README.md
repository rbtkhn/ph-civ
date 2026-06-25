# Essays

**Canonical public home** for Predictive History **Substack and long-form essay** chapters.

Repo path: **`essays/`** at the repository root (sibling to [`ph-civ/`](ph-civ/README.md), [`ph-apo/`](ph-apo/README.md), [`book/`](book/), [`sources/`](sources/)).

## ID scheme

- **Canonical `source_id`:** `essay-01` … `essay-37` (zero-padded two digits).
- **Packet path:** `essays/essay-NN/essay-NN-transcript.md`, `essay-NN-commentary.md`, `README.md`.
- **Workshop map:** frozen `es-01` … `es-32` in strategy-codex `codex/predictive-history/metadata/sources.yaml` promote to `essay-01` … `essay-32`; `essay-33` … `essay-37` are earlier public intakes.
- **Legacy:** `sub-*` essay IDs and `book/volume-vii/sub-*` stubs are **deprecated** — redirects only.

## Recategorization (operator policy)

Essays are **medium-first** on **`essays/<source_id>/`** with catalog surface **`ph-civ`** / part **`civilization`**.

Reader rollup under [`book/volume-ii-apocalypse/sub/`](book/volume-ii-apocalypse/sub/) may remain as **cross-links**; **`essays/essay-NN/`** is the canonical namespace.

## Corpus scope

- **Public today:** 37 `essay-*` chapter packets on repo-root `essays/`.

## Packet shape

Each essay chapter:

- `essay-NN-transcript.md` — verbatim essay body
- `essay-NN-commentary.md` — open commentary canvas
- `README.md` — public study doorway (`## Source Video` + Substack URL)

Registry: [`data/cards.jsonl`](../data/cards.jsonl) · catalog: [`docs/predictive-history-index.md`](../docs/predictive-history-index.md).

## Catalog fields

| Field | Value |
|-------|--------|
| `source_id` | `essay-NN` |
| `series` | `essays` |
| `part` | `civilization` |
| `surface` | `ph-civ` |
| `source_paths.*` | under `essays/essay-NN/` |

Intake script: [`scripts/intake_essays_phase2.py`](../scripts/intake_essays_phase2.py)
