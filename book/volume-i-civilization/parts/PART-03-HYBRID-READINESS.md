---
part_id: part-03-roman-imperium
plan_status: phase1_complete
scaffold_version: ph_civ_part_commentary_v1
template_from: part-02-hellenic-world (hybrid pilot)
inventory_date: 2026-06-09
---

# Part III Hybrid Apparatus — Readiness Inventory

Planning doc for extending the **Part II hybrid model** (thin chapter + thick Part commentary/bibliography) to **Part III — The Roman Imperium** (`civ-14`–`civ-17` + `gb-08`).

**Law-discovery question (registry):** How does imperial machinery acquire a literary soul?

**Spine note:** `spine_slice_warning: true` — Rome block appears before Part IV ancient-worlds floor in interwoven order.

---

## Maturity gate (when to implement)

| Gate | Threshold | Current (2026-06-09) |
|------|-----------|----------------------|
| Chapter Layer 0–2 | All four chapters have transcript-anchored claims + line/section refs | **Met** — seed depth, Layers 0–2 populated |
| Chapter slimming | Willing to move Layers 3–6 to Part apparatus | **Not started** — chapters still full scaffold |
| GB weave | `gb-08` @ `civ-17` interwoven; `gb-07` anti-Homer lecture matures Part link | **Partial** — gb-08 seed; gb-07 Part II section drafted |
| Cross-Part bridge | Part II Homer grammar ↔ Part III Virgil inversion documented | **Partial** — gb-07 pointer in Part II; civ-17 ↔ civ-07 link in chapter Layer 5 |
| Validator | `volume_i_parts.py` Part III checks (mirror Part II) | **Not wired** |
| ASR | civ-14–17 in normalization scope if needed | **Out of scope** until operator extends pilot |

**Recommendation:** **Phase 1 ready** (author Part III commentary draft + bibliography from existing chapter Layers 0–2). **Phase 2** (slim chapters + stub gb-08) after Part III law-discovery answer is reviewed once.

---

## Chapter inventory (`volume-ii/` packets)

| Chapter | Core thesis (Layer 0) | L2 claims | L3 predictions | analysis_depth | Part section weight |
|---------|----------------------|-----------|----------------|----------------|---------------------|
| `civ-14` | Rome rises via manpower, citizenship, cohesion — Hannibal/Cannae crisis | 8 | 2 pending | seed | **Thick** — republican machinery + Punic arc |
| `civ-15` | Caesar as mythmaker; narrative + action; assassination as identity threat | 8 | 2+ pending | seed | **Thick** — late republic narrative weapon |
| `civ-16` | Caesar's will → Octavian settlement; Augustan republican theater | 8 | 2+ pending | seed | **Thick** — empire birth mechanics |
| `civ-17` | Homer vs Virgil; literature as Roman soul / state epic | 8 | 2 pending | seed | **Thick** — literary soul capstone; pairs `gb-08` |

**Legacy wrappers:** `civilization-spine/civ-14`–`civ-17` READMEs still point at `volume-ii/` packets only — no Part apparatus links yet (expected pre-implementation).

---

## Great Books weave

| GB | Anchor | Role | Commentary state | Part III placement |
|----|--------|------|------------------|-------------------|
| `gb-08` | `civ-17` | interwoven | seed scaffold | **`### gb-08`** canonical section in Part commentary (like gb-03 in Part II) |
| `gb-07` | `civ-07` (Part II) | interwoven | Part II section drafted | **Cross-part pointer** only — anti-Homer frame; do not duplicate full Aeneid close-read in Part II |

**Stub target:** `gb-08-commentary.md` → route to `part-03-roman-imperium-commentary.md#gb-08` (mirror gb-03 stub pattern).

---

## Part III artifacts

| Artifact | Status (2026-06-09) |
|----------|---------------------|
| `part-03-roman-imperium-commentary.md` | **Created** — Phase 1 draft |
| `part-03-roman-imperium-bibliography.md` | **Created** — Phase 1 seeded |
| `volume-i-parts.json` commentary/bib paths | **Wired** |
| `part-03-roman-imperium.md` Apparatus block | **Wired** |
| Slim `civ-14`–`civ-17` commentaries | Phase 2 |
| README + transcript frontmatter Part links | Phase 2 |
| `gb-08-commentary.md` stub route | Phase 2 |
| Validator Part III checks | Phase 3 |

---

## Roman grammar spine (draft for Part commentary)

Working mechanism chain to validate against lectures:

1. **Citizenship-manpower** — open body, cohesion triad (`civ-14`)
2. **External crisis** — Hannibal, Cannae, Punic endgame (`civ-14`)
3. **Mythmaker** — Caesar narrates conquest into legitimacy (`civ-15`)
4. **Will-heir settlement** — Octavian converts assassination into empire (`civ-16`)
5. **Literary soul** — Aeneid / Homer-Virgil war for Roman identity (`civ-17`, `gb-08`)

**Cross-links:** Part II conquest-carrier (`civ-11`–`civ-13`) → Roman absorption; Homer corridor (`homer-to-dante`, `homer-to-tolstoy`).

---

## Implementation phases

### Phase 1 — Author only (~1 session)

- Draft Part III commentary + bibliography from existing Layer 0–2
- Fold civ-14–17 Layer 3 predictions into Part ledger
- Wire registry + doorway apparatus links
- Do **not** slim chapters yet

### Phase 2 — Reader reshape (~1 session)

- Slim civ-14–17 commentaries
- Stub `gb-08-commentary.md`
- Update civilization-spine READMEs (6-step lattice + Part links)
- Transcript YAML frontmatter only

### Phase 3 — Validator + docs (~half session)

- Extend `volume_i_parts.py` Part III checks (mirror `part-02-hellenic-world` block)
- Update `docs/commentary-canvas.md` / `docs/source-lattice.md` with Part III example
- Optional: section anchors on `gb-08-transcript.md`

---

## Risks / counter-readings to front-load

| Topic | Note |
|-------|------|
| Character typology (Greek/Carthaginian/Roman) | Lecture shorthand — bibliography must carry scholarship |
| Caesar myth-maker | Distinct from standard prosopography — label as lecture frame |
| Augustus-as-Virgil-author (gb-07) | Strong lecture claim; counter-read in Part bibliography |
| Homer vs Virgil binary (`civ-17`) | Medium counter-evidence already in Layer 4 — preserve in Part section |
| `spine_slice_warning` | Part commentary must explain interwoven order vs historical chronology |

---

## Out of scope (Part III pilot)

- Part I or Parts IV–X apparatus
- Moving `gb-07` canonical body from Part II to Part III (keep pointer)
- Museum room retargeting
- civ-14–17 transcript body / ASR edits

---

## Next operator pick

After Part II deepen commit: run **Phase 1** author pass, or push Part II deepen first.
