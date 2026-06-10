---
part_id: part-06-medieval-imagination
plan_status: phase0_inventory
scaffold_version: ph_civ_part_commentary_v1
template_from: part-05-christianity-and-islam (hybrid pilot)
inventory_date: 2026-06-09
---

# Part VI Hybrid Apparatus — Readiness Inventory

Planning doc for extending the **Part II–V hybrid model** (thin chapter + thick Part commentary/bibliography) to **Part VI — The Medieval Imagination** (`civ-29`–`civ-34` + `gb-09`/`gb-10` weave @ `civ-29`–`30`).

**Law-discovery question (registry):** How does epic inheritance become pilgrimage, comedy, and a new architecture of the self?

**Spine note:** `spine_slice_warning: false` — contiguous block (`civ-29`→`civ-34`). **Structural seam:** Dante **opens** here (`civ-29`–`30`); the [Homer-to-Dante](../../../data/corridors/homer-to-dante.md) corridor **returns** at `civ-41` (Part VII) — this Part is a **bookend open**, not Dante's close.

**Cross-Part ingress:** [Part V `civ-28`](./part-05-christianity-and-islam-commentary.md#civ-28) Augustinian/Islamic field → Dante rebuttal (`civ-29`); prediction row **Pending** until Part VI apparatus exists.

---

## Maturity gate (when to implement)

| Gate | Threshold | Current (2026-06-09) |
|------|-----------|----------------------|
| Chapter Layer 0–2 | All six chapters have transcript-anchored claims + line/section refs | **Partial** — L2 tables exist (6–8 claims each); **all** use blanket `transcript.md:32` (Tier C pin-cite debt) |
| Chapter slimming | Willing to move Layers 3–6 to Part apparatus | **Not met** — full Layer 0–6 in each `volume-ii/civ-29`–`34` commentary |
| GB weave | Registry `great_books_weave` + Part `### gb-NN` sections | **Partial** — `gb-09`/`gb-10` packets exist in `volume-v/`; **no** Part VI commentary file; **no** stub routing from Part doorway |
| Cross-Part bridge | Part V `civ-28` → Dante/Augustine rebuttal; Homer corridor open | **Partial** — Part V forward row **Pending**; doorway + corridor links wired |
| Validator | `volume_i_parts.py` Part VI README checks | **Not met** — no Part VI apparatus paths in registry |
| Theology / literary guardrails | Bibliography + counter-readings for Dante/Augustine/Rome claims | **Not met** — no `part-06-*-bibliography.md` |

**Recommendation:** Phase 0 inventory **done**. Before Phase 1: run pin-cite prep on `civ-29`–`34` (mirror Parts II–V `#anchor` discipline); decide whether `civ-31` (oceanic currents) gets **thick** Part section or stays bridge to Part VII prediction grammar.

---

## Chapter inventory (`volume-ii/` packets)

| Chapter | Core thesis (Layer 0) | L2 claims | L3 | analysis_depth | Part section weight (draft) |
|---------|----------------------|-----------|-----|----------------|-----------------------------|
| `civ-29` | Dante rebuts Augustine — love, imagination, agency, poetic cosmology | 8 | yes | seed | **Thick** — Commedia opener; Augustine clash; corridor **open** |
| `civ-30` | Dante displaces Virgil/Homer — love, freedom, error, ascent | 8 | yes | seed | **Thick** — unreliable-guide arc; pairs `gb-09`/`gb-10` |
| `civ-31` | Second-semester reset — oceanic-currents model + live geopolitics | 6 | yes | seed | **Medium** — model bridge; date-sensitive L3 needs guardrails |
| `civ-32` | Rome as war republic/empire — citizenship, Caracalla, America analogy | 6 | yes | seed | **Medium** — Rome recap inside medieval Part |
| `civ-33` | Byzantium as eastern Roman survival — walls, Nicaea, bureaucracy | 6 | yes | seed | **Medium** — east/west legitimacy split |
| `civ-34` | Holy Roman Empire as useful fiction — Charlemagne, Augustine blueprint | 6 | yes | seed | **Thick** — closes Part law question (fiction + local order) |

**Legacy wrappers:** `civilization-spine/civ-29`–`civ-34` and `volume-ii/civ-29`–`34` READMEs use **4-step** lattice — **no Part apparatus links** (expected pre-implementation).

**Pin-cite debt:** **High** — all six chapters: L2 refs → `*-transcript.md:32` only; transcripts need `###` section rails per [`docs/PIN-CITE-DISCIPLINE.md`](../../../docs/PIN-CITE-DISCIPLINE.md). No Part VI sweep script yet.

**Commentary shape:** Full Layers 0–6 (not slimmed). `completeness_state: in-review` on sampled packets.

---

## Great Books weave

| GB | Anchor(s) | Role | Packet | Part VI placement (draft) |
|----|-----------|------|--------|---------------------------|
| `gb-09` | `civ-29`, `civ-30` | interwoven | `book/volume-v/gb-09/` — seed commentary, transcript pending rights | **`### gb-09`** — Dante capstone (duplicate registry rows = same lecture, two spine anchors) |
| `gb-10` | `civ-30` | interwoven | `book/volume-v/gb-10/` — seed commentary | **`### gb-10`** — pair with `civ-30` Homer displacement |

**Law:** Civilization lectures own spine narrative; GB sections **pointer + close-read**, not full transcript mirror in Part file.

**Registry:** `secret_history_companions: []` · corridors: `homer-to-dante`, `homer-to-tolstoy`

---

## Corridor touchpoints

| Corridor | Part VI role | Notes |
|----------|--------------|-------|
| [homer-to-dante](../../../data/corridors/homer-to-dante.md) | **Opens** @ `civ-29` | Epic → pilgrimage; completes @ `civ-41` (Part VII) |
| [homer-to-tolstoy](../../../data/corridors/homer-to-tolstoy.md) | Touch @ Dante/Rome imagination | Long arc; Part VI supplies Dante + Roman afterlife beats |

---

## Part VI artifacts

| Artifact | Status (2026-06-09) |
|----------|---------------------|
| `part-06-medieval-imagination-commentary.md` | **Not started** |
| `part-06-medieval-imagination-bibliography.md` | **Not started** |
| `volume-i-parts.json` `commentary_path` / `bibliography_path` | **Not wired** |
| `part-06-medieval-imagination.md` Apparatus block | **Planned** — readiness pointer only |
| `PART-06-HYBRID-READINESS.md` | **Done** — this inventory |
| Pin-cite `civ-29`–`34` | **Not started** |
| Slim `civ-29`–`34` commentaries | **Not started** |
| README 6-step lattice + Part links | **Not started** |
| Validator Part VI README checks | **Not started** |
| GB stub routing (`gb-09`/`gb-10` from Part doorway) | **Not started** |

---

## Cross-Part ingress (from Part V `civ-28`)

| Prediction | Strength | Status (2026-06-09) | Part VI test |
|------------|----------|---------------------|--------------|
| Dante/medieval arc follows Islamic + Augustinian field | C | **Pending** | `civ-29` Augustine rebuttal |
| Sacred legitimacy → poetic/imagination architecture | C | **Pending** | `civ-29`–`30` + `gb-09` |
| Eastward dissent / imperial whitewashing carries to Rome–Byzantium split | E | **Partial** (Part V) | `civ-33`–`34` |

---

## Medieval imagination grammar spine (draft)

1. **Epic → pilgrimage** — Commedia structure; apocalyptic overturn; human agency (`civ-29`)
2. **Homer/Virgil displacement** — unreliable guide; love without possession; poetic surgery (`civ-30`, `gb-09`/`gb-10`)
3. **Oceanic currents** — second-semester model; borderlands; prediction grammar (`civ-31`)
4. **Roman inheritance** — republic/empire citizenship; America analogy (`civ-32`)
5. **Byzantine survival** — east Roman continuity; Nicaea; stagnation (`civ-33`)
6. **Holy Roman fiction** — Charlemagne legitimacy; Augustine blueprint; useful fiction close (`civ-34`)

**Cross-links:** Part V [`civ-28`](./part-05-christianity-and-islam-commentary.md#civ-28); forward [Part VII](./part-07-world-after-rome.md) (`civ-35` world orders; `civ-41` Dante close).

---

## Implementation phases

### Phase 0 — Inventory — **Done** (2026-06-09)

### Phase 1 — Author only (~1–2 sessions) — **Not started**

- Create `part-06-medieval-imagination-commentary.md` + `-bibliography.md`
- Wire `volume-i-parts.json` paths + doorway Apparatus block
- Seed prediction ledger + `gb-09`/`gb-10` pointer sections

### Phase 2 — Reader reshape (~1–2 sessions) — **Not started**

- Pin-cite prep script for `civ-29`–`34` (section rails + `#anchor` L2 refs)
- Slim chapters to Layer 0–2 + Part pointer
- Update `volume-ii/` READMEs (6-step lattice)

### Phase 3 — Validator + docs (~half session) — **Not started**

- Extend `volume_i_parts.py` Part VI checks (mirror Part V)
- Update `parts/README.md`, `docs/commentary-canvas.md`, `docs/source-lattice.md`

---

## Risks / counter-readings to front-load

| Topic | Note |
|-------|------|
| Dante vs Augustine (`civ-29`) | Patristic vs Commedia theology — keep source-layer discipline |
| Renaissance/Reformation/Science seeds (`civ-29`) | Lecture chain ≠ historical causation |
| Paul-as-spy / Virgil unreliable narrator (`civ-30`) | Literary reading vs biographical claim |
| Live geopolitics in `civ-31` | Date-stamp L3; separate model from news |
| America–Rome analogy (`civ-32`) | Structural analogy ≠ prediction proof |
| Byzantine refutation frame (`civ-33`) | Scholarly consensus vs lecture dissent |
| Holy Roman “fiction” (`civ-34`) | Voltaire quip vs institutional history |
| Duplicate `gb-09` anchors | Registry lists two rows — one Part `### gb-09` section |
| Homer-to-Dante bookend | Do not treat `civ-34` as corridor **close** — `civ-41` owns close |

---

## Out of scope (Part VI pilot)

- Parts VII–X apparatus · `civ-41` Dante close (Part VII) · SH companions · transcript re-ingest

---

## Next operator pick

**Pin-cite prep** `civ-29`–`34`, **Phase 1** author Part VI commentary, **push** local commits, or **external-verify** Part V bibliography.
