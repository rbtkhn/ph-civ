# Pin-cite discipline — Volume I hybrid apparatus

**Scope:** WORK-layer coherence for `ph-civ` Part commentary + chapter Layer-2 claim tables + lecture transcripts. Not external legal citation or public `ph-civ` ship copy.

**Goal:** A general reader can move **Part overview → chapter claims → transcript passage** without scrolling a megagraph or trusting a blanket `:32`.

---

## Two layers (both required for “Met”)

| Layer | Artifact | What it does |
|-------|----------|----------------|
| **1. Transcript rails** | `### kebab-slug` headings in `*-transcript.md` | Breaks lecture wall into named movements; slugs are human-readable handles |
| **2. L2 pin-cites** | `civ-NN-transcript.md#slug` in chapter + Part claim tables | Ties each claim row to one movement, not a line number |

**Invariant:** Verbatim body text is not rewritten during pin-cite prep — only structural `###` inserts (and optional inline ` ### slug` normalization to own lines).

---

## Slug rules

- **Format:** `kebab-case`, ASCII, stable across Part and chapter tables (`#gilgamesh-pyramid-dialectic`, not `#section-4`).
- **Semantics:** Name the *argument neighborhood* (mechanism, close-read, handoff), not ASR noise.
- **Count:** Typically **6–10** sections per civ chapter; **8** when aligned to the standard L2 claim table.
- **Order:** Sections follow **lecture order**; script splits on first unique phrase match per slug (see `scripts/part_*_pin_cite_prep.py`).
- **Duplicates:** Reuse the same `#anchor` on multiple claim rows when one movement supports several claims (Part IV/V pattern).

---

## Sync rules (Part ↔ chapter)

1. **Part commentary** claim tables are SSOT for Part-facing refs once Phase 1+ claim authoring exists.
2. **Chapter commentary** Layer-2 rows must use the **same `#anchor` vocabulary** as the Part section for that chapter (no chapter-only line numbers left behind after a sweep).
3. **Great Books:** GB Part sections already use `#anchor` on `gb-NN-transcript.md`; civ chapters at the weave host follow the same discipline.
4. After refresh, set `analysis_depth: layer2_drafted` on chapter commentaries when rows were `:32` or bare line refs.

---

## Tiered debt (when full sectioning is optional)

| Tier | Ref shape | Reader experience | Action |
|------|-----------|-------------------|--------|
| **A — Met** | `#anchor` | Jump to movement by name | Done (Parts IV–V; Part VI `civ-29`–`34` 2026-06-09; Part VII `civ-35`–`37` + wedge `civ-40`–`41` 2026-06-09; Part III `civ-14`–`17`; Part II `civ-07`–`13` incl. Tier-B uplift) |
| **B — Interim** | `:32-35` line ranges | Better than blanket `:32`; still line-literacy | None in Part II civ spine after uplift |
| **C — Debt** | `:32` blanket or orphan line | “Somewhere in this file” | Section + anchor refresh (priority sweep) |

---

## Prep workflow (idempotent)

1. Draft or verify **8 claim rows** (chapter or Part table).
2. Choose **unique split phrases** per slug from the transcript (grep-first; no guessing).
3. Run the part-scoped script (`part_iv_pin_cite_prep.py`, `part_v_pin_cite_prep.py`, `part_ii_iii_pin_cite_sweep.py`).
4. Run `python scripts/validate_volume_i_parts.py`.
5. Update the Part `PART-NN-HYBRID-READINESS.md` pin-cite row when the part clears.

**Do not:** substitute summary for verbatim in transcripts; invent anchors without a phrase match; mix Part slug names with different chapter slugs for the same movement.

---

## Scripts (repo)

| Script | Parts / chapters |
|--------|------------------|
| `scripts/part_iv_pin_cite_prep.py` | `civ-19`–`23` |
| `scripts/part_v_pin_cite_prep.py` | `civ-24`–`28` |
| `scripts/part_ii_iii_pin_cite_sweep.py` | `civ-11`, `civ-13`–`17` (low-debt sweep) |
| `scripts/part_ii_tier_b_uplift.py` | `civ-07`–`10`, `civ-12` (Tier-B → Tier A) |
| `scripts/part_vi_pin_cite_prep.py` | `civ-29`–`34` |
| `scripts/part_vii_pin_cite_civ41.py` | `civ-41` (Part VII wedge close) |
| `scripts/part_vii_pin_cite_civ40.py` | `civ-40` (Part VII wedge bridge) |
| `scripts/part_vii_pin_cite_civ35.py` | `civ-35` (Part VII Viking open) |
| `scripts/part_vii_pin_cite_civ36.py` | `civ-36` (Viking pair — Norse memory) |
| `scripts/part_vii_pin_cite_civ37.py` | `civ-37` (Islamic Golden Age) |

---

## Ceiling (honest limits)

- ASR transcripts → anchors mark **argument neighborhoods**, not word-perfect quotes.
- External-verify and public copy still need their own passes; pin-cite is **internal reader-orientation**, not merge authority.

**Readiness pointers:** [Part IV](../book/volume-i-civilization/parts/PART-04-HYBRID-READINESS.md) · [Part V](../book/volume-i-civilization/parts/PART-05-HYBRID-READINESS.md) · [Part VI](../book/volume-i-civilization/parts/PART-06-HYBRID-READINESS.md) · [Part VII](../book/volume-i-civilization/parts/PART-07-HYBRID-READINESS.md) · [Part III](../book/volume-i-civilization/parts/PART-03-HYBRID-READINESS.md)
