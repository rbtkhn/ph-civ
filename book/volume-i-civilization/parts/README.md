# Volume I — Reading Parts

Ten **Part doorways** overlay the [interwoven civilization spine](../interwoven-reader/README.md). Each Part is a contiguous spine slice (`civ-*` chapters plus woven companions) — not a reordering of the spine.

**Registry:** [`data/parts/volume-i-parts.json`](../../../data/parts/volume-i-parts.json)

**Scaffold:** `python scripts/scaffold_part_doorway.py` (from repo root)

**Validate:** `python scripts/validate_volume_i_parts.py`

## Parts I–X

| Part | Title | Chapters | Doorway |
|------|-------|----------|---------|
| I | The Dawn of Civilization | `civ-01`–`06` | [part-01-dawn-of-civilization.md](part-01-dawn-of-civilization.md) |
| II | The Hellenic World | `civ-07`–`13` | [part-02-hellenic-world.md](part-02-hellenic-world.md) |
| III | The Roman Imperium | `civ-14`–`17` | [part-03-roman-imperium.md](part-03-roman-imperium.md) |
| IV | The Ancient Foundations | `civ-18`–`23` | [part-04-ancient-foundations.md](part-04-ancient-foundations.md) |
| V | Christianity and Islam | `civ-24`–`28` | [part-05-christianity-and-islam.md](part-05-christianity-and-islam.md) |
| VI | The Medieval Imagination | `civ-29`–`34` | [part-06-medieval-imagination.md](part-06-medieval-imagination.md) |
| VII | The World After Rome | `civ-35`–`41` | [part-07-world-after-rome.md](part-07-world-after-rome.md) |
| VIII | The Birth of Modernity | `civ-42`–`50` | [part-08-birth-of-modernity.md](part-08-birth-of-modernity.md) |
| IX | The Age of Conscience | `civ-51`–`53` | [part-09-age-of-conscience.md](part-09-age-of-conscience.md) |
| X | The Rise of the Nation-State | `civ-54`–`60` | [part-10-rise-of-the-nation-state.md](part-10-rise-of-the-nation-state.md) |

### Index subtitles

| Part | Subtitle |
|------|----------|
| VI | Dante and Roman imagination through Holy Roman fiction |
| VII | Eurasian orders after Rome; Dante returns at close |

## Reading law

- Open the **interwoven spine** for canonical order; use Part doorways for law-discovery questions, companion weave, and corridor links.
- **Part** here ≠ lecture transcript "Part I / Part II" ≠ CIV-STATE Part 1/2/3.

## Part apparatus (hybrid commentary pilot)

When a Part has thick synthesis, use three sibling files:

| File | Role |
|------|------|
| `part-NN-{slug}.md` | Doorway — navigation, weave, corridors |
| `part-NN-{slug}-commentary.md` | Thick synthesis — prediction ledger, gb sections, counter-readings |
| `part-NN-{slug}-bibliography.md` | External sources — tagged `supports: civ-NN` / `gb-NN` |

**Hybrid pilot:** Part II (`part-02-hellenic-world-*`, `civ-07`–`civ-13`) and Part III (`part-03-roman-imperium-*`, `civ-14`–`civ-17`, `gb-08` stub). Chapter folders keep thin Layer 0–2 commentaries and link to Part apparatus.

Registry fields (optional per part): `commentary_path`, `bibliography_path` in [`volume-i-parts.json`](../../../data/parts/volume-i-parts.json).

## Part boundary tour

Machine-readable ten-stop tour: [`data/routes/part-boundary-tour.json`](../../../data/routes/part-boundary-tour.json) (complements [`ten_route_spine_seed`](../../../data/routes/seed.json)).
