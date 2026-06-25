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

## DOAC #16 — verbatim swap + section restore

[`interview-2026-05-07-diary-of-a-ceo`](interview-2026-05-07-diary-of-a-ceo/) uses an **operator verbatim paste** body with **Title Case section headings** (not lowercase slug headers). After replacing the transcript body under `## Part I: Full transcript`, re-apply sections and light ASR cleanup with:

```bash
python scripts/patch_doac_sections_asr.py
python -m civ_ph.cli index --force
python -m civ_ph.cli validate
```

**What the script does**

- Splits the verbatim body at **14 anchor phrases** (see `SECTION_ANCHORS` in the script; section map pinned from commit `c01fe76`).
- Inserts `### Title Case — …` headings from `SECTION_TITLES`.
- Applies light ASR fixes (e.g. `Professor Dieng` → `Professor Jiang`, duplicate-word cleanup).
- Rewrites frontmatter: `transcript_source: operator_paste`, `transcript_curation: curated_sectioned`, `transcript_fidelity: exact_body_match`.

**Staging (optional):** operator paste can land in `data/interviews/_land_doac/body.txt` before manual or scripted merge into the packet transcript. Keep staging **UTF-8** only — files under `data/` are scanned by `ph-civ validate`; UTF-16 artifacts will fail the public-boundary read pass.
