# Pin-cite manifest index

**SSOT:** [`data/pin-cite/volume-i-anchors.yaml`](../data/pin-cite/volume-i-anchors.yaml)

| Tool | Role |
|------|------|
| `scripts/part_pin_cite_from_manifest.py --part NN` | Apply `###` rails + refresh L2 refs from manifest |
| `scripts/validate_pin_cite.py` | Every manifest slug has transcript `###`; phrases unique in lecture order |
| `scripts/part_vii_pin_cite_prep.py` … `part_x_pin_cite_prep.py` | Part-specific wrappers (delegate to manifest where wired) |

## Coverage (2026-06-10)

| Part | Chapters in manifest | Prep script |
|------|----------------------|-------------|
| I | `civ-01`–`06` | `part_i_pin_cite_prep.py` |
| VII | `civ-35`–`41` | `part_vii_pin_cite_prep.py` |
| VIII | `civ-42`–`50` | `part_viii_pin_cite_prep.py` |
| IX | `civ-51`–`53` | `part_ix_pin_cite_prep.py` |
| X | `civ-54`–`60` | `part_x_pin_cite_prep.py` |

Parts II–VI use legacy per-Part prep scripts (`part_ii_pin_cite_prep.py` … `part_vi_pin_cite_prep.py`).

**Discipline:** [`PIN-CITE-DISCIPLINE.md`](./PIN-CITE-DISCIPLINE.md)
