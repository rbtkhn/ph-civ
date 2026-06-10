---
part_id: part-05-christianity-and-islam
plan_status: phase0_inventory
scaffold_version: ph_civ_part_commentary_v1
template_from: part-04-ancient-foundations (hybrid pilot)
inventory_date: 2026-06-09
---

# Part V Hybrid Apparatus — Readiness Inventory

Planning doc for extending the **Part II/III/IV hybrid model** (thin chapter + thick Part commentary/bibliography) to **Part V — Christianity and Islam** (`civ-24`–`civ-28` + `sh-18` deepening @ `civ-28`).

**Law-discovery question (registry):** How does sacred legitimacy migrate across revelations and empires?

**Spine note:** `spine_slice_warning: false` — contiguous interwoven block (`civ-24`→`civ-28`); not an out-of-order floor slice like Part IV.

**Cross-Part ingress:** [Part IV `civ-23`](./part-04-ancient-foundations-commentary.md#civ-23) Zoroastrian/Jewish merge → Christianity unit; prediction ledger rows **Pending** until Part V apparatus exists.

---

## Maturity gate (when to implement)

| Gate | Threshold | Current (2026-06-09) |
|------|-----------|----------------------|
| Chapter Layer 0–2 | All five chapters have transcript-anchored claims + line/section refs | **Partial** — 8 L2 claims each; **`analysis_depth: seed`**; all L2 refs **`civ-*-transcript.md:32`** (single megagraph; **no `###` transcript sections**) |
| Chapter slimming | Willing to move Layers 3–6 to Part apparatus | **Not met** — `civ-24`–`28` retain **full Layer 0–6** (+ `civ-25` Tolstoy Lens block) |
| GB weave | Registry `great_books_weave` | **N/A** — empty array; no `gb-NN` Part sections required |
| SH companion | `sh-18` @ `civ-28` deepening documented | **Partial** — doorway + registry wired; staged wrapper in `secret-history-support/`; **`volume-vi/sh-18/`** seed commentary; no Part `### sh-18` section yet |
| Cross-Part bridge | Part IV `civ-23` handoff + Yahwist/covenant/messianic carry | **Partial** — Part IV forward links exist; **`civ-24` Layer 5 cites `civ-23`**; Part IV ledger rows for Part V still **Pending** |
| Validator | `volume_i_parts.py` Part V README checks (mirror Part IV) | **Not started** |
| Interfaith / theology guardrails | Bibliography + counter-readings for Jesus/Paul/Islam claims | **Required before Phase 1 author** — not yet seeded at Part grain |

**Recommendation:** Phase 0 inventory only. **Do not** open Phase 1 author until megagraph pin-cite split (or section anchors) + interfaith bibliography seed + Part IV ingress row confirmation. Highest sensitivity Part in Volume I hybrid pilot so far.

---

## Chapter inventory (`volume-ii/` packets)

| Chapter | Core thesis (Layer 0) | L2 claims | L3 predictions | analysis_depth | Part section weight |
|---------|----------------------|-----------|----------------|----------------|---------------------|
| `civ-24` | Historical vs biblical vs Gnostic Jesus; martyrdom; original-sin/Yahwist clash; Paul preview | 8 | 2 pending | seed | **Thick** — source-layer opener; bridges `civ-22`/`civ-23` |
| `civ-25` | Paul as hinge from Jesus movement to Christianity; faith/circumcision; Paul-as-spy thesis | 8 | 2 pending | seed | **Thick** — Roman-carrier / Gentile opening; highest political-theology risk |
| `civ-26` | Constantine + Nicaea godhead → monotheism as reality-order; money/science/nation-state preview | 8 | 2 pending | seed | **Thick** — imperial-theological hinge; broad modernity chain |
| `civ-27` | Augustine takes Church out of history; City of God; obedience doctrine; eastward to Arabia | 8 | 2 pending | seed | **Thick** — post-Rome-sack legitimacy; Dark Ages frame |
| `civ-28` | Muhammad / early Islam as revolutionary Abrahamic synthesis; expansion analogies; imperial whitewashing | 8 | 2 pending | seed | **Thick** — Islam close; pairs `sh-18`; forward Part VI Dante |

**Legacy wrappers:** `civilization-spine/civ-24`–`civ-28` and `volume-ii/civ-24`–`28` READMEs use **4-step** lattice — **no Part apparatus links** (expected pre-implementation).

**Pin-cite debt:** **All five** chapters — Layer 2 refs overwhelmingly `civ-*-transcript.md:32`; transcripts have **no `###` section anchors**.

---

## Companion weave (not Great Books)

| Companion | Anchor | Role | Packet state | Part V placement |
|-----------|--------|------|--------------|------------------|
| `sh-18` | `civ-28` | deepening | seed in `volume-vi/sh-18/`; staged wrapper in `secret-history-support/` | **`### sh-18`** pointer section in Part commentary (parallel to Part IV `sh-17`) |

**Law:** Civilization lecture (`civ-28`) owns the spine; `sh-18` cross-links — do not duplicate full SH body in Part file.

**Registry:** `great_books_weave: []` · `corridor_touchpoints: []`

---

## Part V artifacts

| Artifact | Status (2026-06-09) |
|----------|---------------------|
| `part-05-christianity-and-islam-commentary.md` | **Not created** |
| `part-05-christianity-and-islam-bibliography.md` | **Not created** |
| `volume-i-parts.json` `commentary_path` / `bibliography_path` | **Not wired** |
| `part-05-christianity-and-islam.md` Apparatus block | **Not wired** |
| `PART-05-HYBRID-READINESS.md` | **Done** — this inventory |
| Slim `civ-24`–`civ-28` commentaries | **Not started** |
| README 6-step lattice + Part links | **Not started** |
| Transcript YAML `part_id` + Part paths | **Not started** |
| Validator Part V README checks | **Not started** |

---

## Cross-Part ingress (from Part IV `civ-23`)

| Prediction | Strength | Status (2026-06-09) | Part V test |
|------------|----------|---------------------|-------------|
| Persian/Cyrus/Zoroastrian merge precedes Christianity unit | E | **Confirmed** (Part IV) | `civ-24` follows `civ-23` in spine |
| Christianity inherits Persian/Jewish strands **distinctly** | C | **Pending** | Do not collapse influence lines in Part V synthesis |
| Word/covenant/argument-with-God themes carry to Part V | C | **Pending** | `civ-24` original sin vs Yahwist |
| Zoroastrian–Christian single pipeline | — | **Guardrailed** (Part IV) | influence ≠ causation |

---

## Christianity–Islam grammar spine (draft)

1. **Source-layer Jesus** — historical vs biblical vs Gnostic; martyrdom; original-sin/Yahwist tension (`civ-24`)
2. **Pauline transformation** — Gentile/faith opening; Roman protection; Paul-as-spy frame (`civ-25`)
3. **Imperial monotheism** — Constantine; Nicaea; monotheism as closed reality-order (`civ-26`)
4. **Church above history** — Augustine; City of God; eastward dissent (`civ-27`)
5. **Islamic revolutionary universalism** — Muhammad source field; jihad/land/debt frame (`civ-28`, pairs `sh-18`)

**Cross-links:** Part IV [`civ-23`](./part-04-ancient-foundations-commentary.md#civ-23); forward [Part VI](./part-06-medieval-imagination.md) (`civ-29`).

---

## Implementation phases

### Phase 0 — Inventory — **Done** (2026-06-09)

### Phase 1 — Author only (~1–2 sessions) — **Not started**

### Phase 2 — Reader reshape (~1–2 sessions) — **Not started**

### Phase 3 — Validator + docs (~half session) — **Not started**

---

## Risks / counter-readings to front-load

| Topic | Note |
|-------|------|
| Historical vs biblical vs Gnostic Jesus (`civ-24`) | Source-layer discipline |
| Original sin vs Yahwist (`civ-24`) | Tie to `civ-22`; patristic bibliography |
| Paul-as-spy thesis (`civ-25`) | Highest political risk; keep bounded |
| Constantine / Nicaea (`civ-26`) | Separate imperial history from lecture philosophy |
| Augustine polemic (`civ-27`) | Lucretia/obedience passages — text vs institution |
| Muhammad source scarcity (`civ-28`) | Analogies ≠ proof |
| Jihad / revolution framing (`civ-28`) | Islamic-studies review before `complete` |
| Zoroastrian merger carry (`civ-23`→`28`) | Part IV guardrail: influence ≠ single pipeline |
| `sh-18` duplication | Pointer only |

---

## Out of scope (Part V pilot)

- Parts VI–X apparatus · GB stub routing · SH body merge · transcript re-ingest

---

## Next operator pick

**Phase 1 author**, **external-verify** Part V Layer 2 claims first, or **confirm Part IV ingress rows** before Part V prediction ledger.
