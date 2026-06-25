# Interviews

Public provenance packets for Predictive History interview-form source material.

Repo path: **`interviews/`** at the repository root (sibling to [`essays/`](../essays/README.md), [`lectures/`](../lectures/README.md), [`book/`](../book/), [`ph-civ/`](../ph-civ/README.md)).

## Public ID scheme

**Pattern:** `interview-YYYY-MM-DD-{host-slug}`

Examples: `interview-2025-11-24-glenn-diesen`, `interview-2026-05-07-diary-of-a-ceo`.

| Field | Detail |
| --- | --- |
| **Date** | YouTube upload date (pinned in [`data/interviews/manifest.json`](../data/interviews/manifest.json)) |
| **Host slug** | Lowercase hyphenated host or show name |
| **Folder** | `interviews/{source_id}/` with transcript, commentary canvas, and README |
| **Catalog** | Provenance surface in [`docs/predictive-history-index.md`](../docs/predictive-history-index.md) |

**Public today:** 16 interview chapter packets (`interview-2025-10-30-cyrus-janssen` … `interview-2026-05-07-diary-of-a-ceo`).

## Workshop crosswalk (`vi-*` and external)

| Workshop | Public `source_id` | Upload date |
| --- | --- | --- |
| `vi-01` | `interview-2025-10-30-cyrus-janssen` | 2025-10-30 |
| `vi-02` | `interview-2025-11-24-glenn-diesen` | 2025-11-24 |
| `vi-03` | `interview-2026-01-05-glenn-diesen` | 2026-01-05 |
| `vi-04` | `interview-2026-01-18-danny-haiphong` | 2026-01-18 |
| `vi-05` | `interview-2026-01-22-dimitri-lascaris` | 2026-01-22 |
| `vi-06` | `interview-2026-01-26-glenn-diesen` | 2026-01-26 |
| `vi-07` | `interview-2026-03-02-breaking-points` | 2026-03-02 |
| `vi-08` | `interview-2026-03-07-nima` | 2026-03-07 |
| `vi-09` | `interview-2026-03-09-sneako` | 2026-03-09 |
| `vi-10` | `interview-2026-03-16-endgame` | 2026-03-16 |
| `vi-11` | `interview-2026-03-20-tucker-carlson` | 2026-03-20 |
| `vi-12` | `interview-2026-04-01-jay-shapiro` | 2026-04-01 |
| `vi-13` | `interview-2026-04-07-patrick-bet-david` | 2026-04-07 |
| `vi-14` | `interview-2026-04-13-glenn-diesen` | 2026-04-13 |
| `vi-15` | `interview-2026-04-13-sneako-dugin` | 2026-04-13 |

### External (not in workshop `vi-*`)

| Registry | Public `source_id` | Upload date | Source |
| --- | --- | --- | --- |
| `ext-doac-01` | `interview-2026-05-07-diary-of-a-ceo` | 2026-05-07 | [Diary of a CEO / Steven Bartlett](https://www.youtube.com/watch?v=BTJGr78-zyw) |

Cards use `part: provenance`, `series: interviews`, `derived_corpus: provenance`, `placement_weight: light`. They appear in the **Provenance** section of the chapter catalog; they are not foreground Volume I/II spine routes.

Related: [`book/provenance/`](../book/provenance/README.md) · catalog [`docs/predictive-history-index.md`](../docs/predictive-history-index.md) · intake manifest [`data/interviews/manifest.json`](../data/interviews/manifest.json).
