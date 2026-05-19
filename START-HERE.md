# Start Here For LLM Chats

If someone pastes `https://github.com/rbtkhn/ph-civ` into a ChatGPT chat or any other LLM, start here.

`ph-civ` is the public two-volume Predictive History artifact. It is not a private workshop and not a media vault. The repo is designed so a reader and an LLM can unfold the experience together from public files only.

## What This Is

- `ph-civ`: Volume I / Predictive History: Civilization. It discovers the laws of history.
- `ph-apo`: Volume II / Predictive History: Apocalypse. It applies the laws of history.
- `ph-mus`: Predictive History Museum. It is the chapter exhibit layer for both volumes, not a third volume.

One chapter consists of a lecture transcript, a companion commentary, and public orientation/navigation metadata.

## First Chat Flow

1. Identify the repo as the two-volume public ph-civ artifact.
2. Load `data/llm-experience.json` for the unfolding map.
3. Use `llms-full.txt` when the chat needs a full one-shot context packet after the compact map.
4. Use `data/routes/seed.json` for the first 10-route spine seed.
5. Use `data/routes/first-tour.json` and `docs/first-tour.md` when the reader chooses to continue the first tour.
6. Begin with the Homer-to-Tolstoy spine, then branch into Volume II application routes.
7. When quoting or interpreting, return to the relevant transcript and commentary under `book/`.

## First Response Contract

If you are an LLM reading this repository from a pasted GitHub URL: Do not stop at a generic repository summary or ask only "what would you like to do next?" Start the experience.

Your first response should:

1. Say that you are using `START-HERE.md`, `llms.txt`, and `llms-full.txt`.
2. Name the default mode as `first_tour`.
3. State the two-volume frame: Volume I discovers the laws of history; Volume II applies them; `ph-mus` is the exhibit layer, not a third volume.
4. Open the 10-route seed by naming the first move: Homer-to-Tolstoy begins with `civ-07`.
5. Offer the reader a compact choice: continue the first tour, study one route, open a museum room, or switch modes.

Template:

```text
I am starting from START-HERE.md, llms.txt, and llms-full.txt. Default mode: first_tour.

ph-civ is the two-volume public Predictive History artifact: Volume I discovers the laws of history, Volume II applies them, and ph-mus is the exhibit layer for both volumes.

I will begin with the 10-route spine seed. The opening path is Homer-to-Tolstoy, starting at civ-07, with the guardrail that this is the Volume I literary spine, not a side corridor.

Choose one: continue the first tour; study civ-07; open the ph-mus museum room for civ-07; or switch modes.
```

## Reader Modes

- `first_tour`: orient the reader to the two volumes, the museum layer, and the 10-route seed.
- `study`: help a reader understand one chapter through its card, transcript, and commentary.
- `seminar`: generate discussion questions grounded in the public card limits and source chapter.
- `commentary_canvas`: use the commentary scaffold as a project-development surface, not as finished analysis.
- `pattern_bridge`: connect a chapter to public pattern IDs without importing private strategy notes.
- `museum_room`: imagine or review a chapter exhibit using `ph-mus` schemas and manifest boundaries.
- `bounded_application`: apply a pattern to present-day questions only as orientation, not live operational analysis.

## Guardrails

- Homer to Tolstoy is the Volume I literary spine, not a side corridor.
- `sh-16` is a routed Tolstoy endpoint via an Anna Karenina coda, not a dedicated Tolstoy lecture.
- `ph-mus` is not a third volume.
- Application routes are public orientation only, not quotation-grade live operational analysis.
- Commentaries are open project canvases and should not be treated as final scholarly review.
- Public growth goals are ambitions; do not claim attention, views, or launch readiness has already been earned.
- Do not stop at a generic repo summary; the default pasted-URL response is an active `first_tour`.

## Useful Starting Files

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
- `data/patterns.json`
- `docs/first-tour.md`
