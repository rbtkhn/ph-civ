# Predictive History Public Repository

For AI agents and new chats: start with `START-HERE.md`, then `AGENTS.md` and `llms.txt`. If a user pastes `https://github.com/rbtkhn/ph-civ` into an LLM chat, use `START-HERE.md`, `data/llm-experience.json`, and `llms-full.txt` as the unfolding map and one-shot context packet. Do not stop at a generic repository summary or "what would you like to do next?" response; begin the `first_tour` through the 10-route spine seed unless the reader chooses another mode. This repo is the public Predictive History distribution layer, not the private editorial workshop.

This repository is the public-facing home for the two-volume ph-civ artifact. It contains three related Predictive History surfaces:

- `ph-civ`: **Volume I / Predictive History: Civilization** - discovers the laws of history.
- `ph-apo`: **Volume II / Predictive History: Apocalypse** - applies the laws of history.
- `ph-mus`: **Predictive History Museum** - chapter exhibit layer for both volumes.

The repo name `ph-civ` names the public repository and the Volume I surface. The repo as a whole is the two-volume public artifact: `ph-civ`, `ph-apo`, and `ph-mus` together.

It also contains the chapter body for each source item. In this repo, one chapter consists of the lecture transcript, companion commentary, and public orientation/navigation metadata. The package lets students and AI systems explore historical placement, reading posture, pressure points, limits, return paths, and guided prompts alongside the chapter text.

This package is independent educational infrastructure. It is not official course material, not endorsement, and not a substitute for the source lectures, transcripts, commentary, or external verification.

## Repository Role

This repo is the public distribution layer. It should contain public cards, public navigation, schemas, prompts, contribution instructions, generated manifests, and small text metadata.

It should not become the large-media vault. Museum artifacts must be stored in a local museum vault and mirrored in a shared document cloud workspace. Git tracks manifests, exhibit metadata, derived thumbnails when appropriate, and validation rules, not the full artifact archive.

## What Is Included

- 140 public cards from Predictive History snapshot `56a4a08`.
- 140 lecture transcripts under `book/`.
- 140 chapter commentaries under `book/`, each seeded as an open commentary canvas.
- Two conceptual volumes: Volume I / Civilization / `ph-civ`, and Volume II / Apocalypse / `ph-apo`.
- Series coverage: Civilization, Great Books, Geo-Strategy, Game Theory, and Secret History.
- The Homer-to-Tolstoy literary spine as the Volume I literary spine with cross-volume routing exposure.
- Provider-neutral prompt templates.
- Eight public civilizational pattern IDs for downstream strategy-facing reference.
- Public museum exhibit and artifact schemas.
- Curator instructions for chapter-level exhibit assembly across both volumes.

## What Is Excluded

- Private notes or private workspace paths.
- External-source bibliography claims beyond the orientation cards.
- LLM provider integrations, API calls, or hidden model dependencies.
- Large image, audio, video, document, or scan archives.
- URL-only artifact submissions treated as complete museum work.

## Install For Local Development

```bash
python -m pip install -e .
```

## CLI

```bash
ph-civ list
ph-civ list --part civilization
ph-civ list --series game-theory --json
ph-civ show civ-41 --format json
ph-civ search Dante
ph-civ prompt gb-01 --mode creative
ph-civ spark gt-16 --count 5
ph-civ spine
ph-civ path homer-to-tolstoy
ph-civ validate
ph-civ status
ph-civ start
ph-civ start --json
ph-civ growth
ph-civ volumes
ph-civ volume volume-i --json
ph-civ route civ-07 --json
ph-civ patterns
ph-civ pattern civ-chokepoint-pressure --format json
ph-civ bridge gt-16 --json
ph-civ bridge civ-07 --format markdown
ph-apo list
ph-apo status
ph-apo route gt-16 --json
ph-mus list
ph-mus status
ph-mus route civ-07 --json
```

All prompt and spark commands are template-only. They do not call an AI provider. Pattern commands expose public civilizational frames for downstream strategy analysis; they do not import live strategy workspace material. Use **`ph-civ`** as the public CLI (`python -m civ_ph.cli …` invokes the same code when running from source).

## Commentary Canvas

The chapter commentaries are the project canvas. They are seeded for all chapters, but they are not treated as complete analysis. Each commentary has a shared `Project Canvas` scaffold for later chapter-by-chapter development: project leverage, laws and patterns, volume role, museum hooks, strategy application, counter-readings, open questions, and build notes.

See `docs/commentary-canvas.md`.

## Public Growth

Large reach targets, such as one million public views by the end of 2026, are strategic ambitions rather than directly executable agent tasks. Treat them as campaign pressure: convert the ambition into one live publishing wedge, then ship only human-approved assets with clear metrics.

The first live wedge is the Volume I literary spine: make the Homer-to-Tolstoy route shareable, connect it to the two-volume ph-civ narrative, pair it with one publishable chapter/commentary/museum path sample, and define what counts as a view before public distribution.

This wedge is defined, not automatically launch-ready. The unresolved tension is whether the route has enough source-disciplined educational trust to deserve audience growth, not only whether the CLI can render it.

The canonical growth guardrail lives in `data/growth-goals.json` and is exposed with:

```bash
ph-civ growth --json
```

## Literary Spine

```text
Homer -> Virgil -> Dante -> Shakespeare -> Dostoevsky -> Tolstoy
```

Homer to Tolstoy is the Volume I literary spine, not a side corridor. It uses cross-volume routing exposure where needed. Tolstoy is routed through `sh-16`, where *Anna Karenina* appears as a source-backed coda rather than a dedicated Tolstoy lecture.

## Predictive History Museum

The museum is organized around chapter exhibits, not flat item rows. Each chapter in Predictive History: Civilization and Predictive History: Apocalypse should eventually have one corresponding `ph-mus` exhibit with stored artifacts, rights notes, room placement, and a clear visitor path.

The current public route export lives in `data/routes/choreography.json`, with the public museum manifest index in `data/museum/index.json`.

See `docs/public-repo-contract.md`, `docs/media-inventory-guide.md`, `schemas/museum-exhibit.schema.json`, and `schemas/museum-artifact.schema.json`.

## License

License is pending. See `LICENSE-PENDING.md`.
