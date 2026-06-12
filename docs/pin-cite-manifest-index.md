# Pin-cite manifest index

**SSOT:** [`data/pin-cite/volume-i-anchors.yaml`](../data/pin-cite/volume-i-anchors.yaml)

| Tool | Role |
|------|------|
| `scripts/part_pin_cite_from_manifest.py --part NN` | Apply `###` rails + refresh L2 refs from manifest |
| `scripts/validate_pin_cite.py` | Every manifest slug has transcript `###`; phrases unique in lecture order |
| `scripts/part_vii_pin_cite_prep.py` … `part_x_pin_cite_prep.py` | Part-specific wrappers (delegate to manifest where wired) |

## Coverage (2026-06-12)

| Part | Chapters in manifest | Prep script |
|------|----------------------|-------------|
| I | `civ-01`–`06` | `part_i_pin_cite_prep.py` |
| II | `civ-07`–`13` | `sync_part_ii_to_manifest.py` (SSOT: `part_ii_tier_b_uplift` + `part_ii_iii_pin_cite_sweep`) |
| VII | `civ-35`–`41` | `part_vii_pin_cite_prep.py` |
| VIII | `civ-42`–`50` | `part_viii_pin_cite_prep.py` |
| IX | `civ-51`–`53` | `part_ix_pin_cite_prep.py` |
| X | `civ-54`–`60` | `part_x_pin_cite_prep.py` |

Parts III–VI remain on legacy prep scripts only (`part_ii_iii_pin_cite_sweep.py` … `part_vi_pin_cite_prep.py`); manifest extension for those parts is a follow-up.

**Discipline:** [`PIN-CITE-DISCIPLINE.md`](./PIN-CITE-DISCIPLINE.md)
