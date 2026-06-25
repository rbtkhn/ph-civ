# Start Here For LLM Chats

**Publisher:** **Statecraft Intelligence Desk**

If someone pastes `https://github.com/rbtkhn/predictive-history` into a ChatGPT chat or any other LLM, start here.

`ph-civ` is the public two-volume Predictive History artifact. It is not a private workshop and not a media vault. The repo is designed so a reader and an LLM can unfold the experience together from public files only.

## What This Is

- `ph-civ`: Volume I / Predictive History: Civilization. It discovers the laws of history.
- `ph-apo`: Volume II / Predictive History: Apocalypse. It applies the laws of history.

One chapter consists of a lecture transcript, a companion commentary, and public orientation/navigation metadata.

## Root Chapter Corpora

Medium-first namespaces at the repository root (siblings to `book/`):

- [`essays/`](essays/README.md) — Substack and long-form essays (`essay-01` … `essay-43`)
- [`lectures/`](lectures/README.md) — reserved lecture namespace; most lecture chapters still live under `book/` until recanonicalized
- [`interviews/`](interviews/README.md) — 15 public interview provenance packets (`interview-YYYY-MM-DD-{host-slug}`); cataloged under **Provenance** in the chapter index

## First Chat Flow

1. Identify the repo as the two-volume public ph-civ artifact.
2. Load `data/llm-experience.json` for the unfolding map.
3. Use `llms-full.txt` when the chat needs a full one-shot context packet after the compact map.
4. Use `data/routes/seed.json` for the first 10-route spine seed.
5. Use `data/routes/first-tour.json` and `docs/first-tour.md` when the reader chooses to continue the first tour.
6. Begin with the Homer-to-Tolstoy spine, then branch into Volume II application routes.
7. Use `docs/two-volumes-one-reader-map.md` when the reader needs the clean public explanation for why the older seven-lane scaffold is now read as two volumes.
8. Treat `data/bilingual-loop.json` and `docs/bilingual-civilizational-bridge.md` as a trilingual identity/growth layer and localization roadmap, not a replacement for `first_tour`.
9. If the pasted URL is a direct chapter folder, switch to `study` mode for that folder: open its `README.md`, transcript, commentary canvas, and public card.
10. When quoting or interpreting, return to the relevant transcript and commentary under `book/`.
11. Use `data/predictive-history-index.json` when the reader needs the full chapter catalog (205 public chapters: lectures, Substack essays, and provenance interviews) or must resolve a `source_id` to paths and source URLs.
12. Use `docs/source-lattice.md` when the main difficulty is traversal discipline: doorway versus transcript versus commentary versus bridge.

## First Response Contract

If you are an LLM reading this repository from a pasted GitHub URL: Do not stop at a generic repository summary or ask only "what would you like to do next?" Start the experience.

Your first response should:

1. Say that you are using `START-HERE.md`, `llms.txt`, and `llms-full.txt`.
2. Name the default mode as `first_tour`.
3. State the two-volume frame: Volume I discovers the laws of history; Volume II applies them; chapter folders are the study surface.
4. Open the 10-route seed by naming the first move: Homer-to-Tolstoy begins with `civ-07`.
5. Offer the reader a compact choice: continue the first tour, study one route, open a chapter folder, or switch modes.

Template:

```text
I am starting from START-HERE.md, llms.txt, and llms-full.txt. Default mode: first_tour.

ph-civ is the two-volume public Predictive History artifact: Volume I discovers the laws of history, Volume II applies them, and chapter folders and study edition are the reader surfaces.

I will begin with the 10-route spine seed. The opening path is Homer-to-Tolstoy, starting at civ-07, with the guardrail that this is the Volume I literary spine, not a side corridor.

Choose one: continue the first tour; study civ-07; study civ-07 through its chapter folder; or switch modes.
```

## Reader Modes

- `first_tour`: orient the reader to the two volumes and the 10-route seed.
- `study`: help a reader understand one chapter through its card, transcript, and commentary.
- `catalog`: browse or resolve chapters across both volumes via `data/predictive-history-index.json`.
- `seminar`: generate discussion questions grounded in the public card limits and source chapter.
- `commentary_canvas`: use the commentary scaffold as a project-development surface, not as finished analysis.
- `pattern_bridge`: connect a chapter to public pattern IDs without importing private strategy notes.
- `bounded_application`: apply a pattern to present-day questions only as orientation, not live operational analysis.

## Guardrails

- Homer to Tolstoy is the Volume I literary spine, not a side corridor.
- `sh-16` is a routed Tolstoy endpoint via an Anna Karenina coda, not a dedicated Tolstoy lecture.
- two-volume public artifact.
- Application routes are public orientation only, not quotation-grade live operational analysis.
- Commentaries are open project canvases and should not be treated as final scholarly review.
- Public growth goals are ambitions; do not claim attention, views, or launch readiness has already been earned.
- Do not stop at a generic repo summary; the default pasted-URL response is an active `first_tour`.
- A chapter-folder URL is a study doorway, not a replacement for `first_tour`; follow the folder README and keep review status visible.
- The trilingual bridge ambition is not propaganda, not anti-Western, not civilizational flattery, and not a translation dump.
- `ph-civ-ru` is roadmap metadata only, not a Russian edition, not live war analysis, and not a translation dump.
- `ph-civ-zh` and `ph-civ-ru` are downstream mirrors of canonical `ph-civ`, not sibling sources of truth.

## Useful Starting Files

- `essays/README.md`
- `lectures/README.md`
- `interviews/README.md`
- `llms.txt`
- `llms-full.txt`
- `README.md`
- `AGENTS.md`
- `docs/public-repo-contract.md`
- `docs/export-contract.md`
- `data/llm-experience.json`
- `data/routes/seed.json`
- `data/routes/first-tour.json`
- `data/routes/choreography.json`
- `data/cards.jsonl`
- `data/predictive-history-index.json`
- `docs/predictive-history-index.md`
- `data/patterns.json`
- `docs/first-tour.md`
- `docs/two-volumes-one-reader-map.md`
- `docs/source-lattice.md`
- `data/bilingual-loop.json`
- `docs/bilingual-civilizational-bridge.md`
- `docs/chapter-folder-links.md`
- `docs/predictive-history-index.md` (chapter catalog + source URLs; legacy `docs/source-video-index.md` redirects here)
