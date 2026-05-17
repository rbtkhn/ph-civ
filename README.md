# Predictive History Public Repository

This repository is the public-facing home for three related Predictive History surfaces:

- **Predictive History: Civilization**
- **Predictive History: Apocalypse**
- **Predictive History Museum**

It also contains `civ-ph`, a lightweight, provider-neutral study tool for public Predictive History orientation cards. The package lets students and AI systems explore historical placement, reading posture, pressure points, limits, return paths, and guided prompts without importing transcripts or commentary bodies.

This package is independent educational infrastructure. It is not official course material, not endorsement, and not a substitute for the source lectures, transcripts, commentary, or external verification.

## Repository Role

This repo is the public distribution layer. It should contain public cards, public navigation, schemas, prompts, contribution instructions, generated manifests, and small text metadata.

It should not become the large-media vault. Museum artifacts must be stored in a local museum vault and mirrored in a shared document cloud workspace. Git tracks manifests, exhibit metadata, derived thumbnails when appropriate, and validation rules, not the full artifact archive.

## What Is Included

- 140 public civ-ph cards from Predictive History snapshot `56a4a08`.
- Two course parts: Civilization and World War.
- Series coverage: Civilization, Great Books, Geo-Strategy, Game Theory, and Secret History.
- The Homer-to-Tolstoy literary spine.
- Provider-neutral prompt templates.
- Public museum exhibit and artifact schemas.
- Curator instructions for chapter-level exhibit assembly.

## What Is Excluded

- Full transcripts.
- Commentary bodies.
- Private notes or Strategy-Codex paths.
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
civ-ph list
civ-ph list --part civilization
civ-ph list --series game-theory --json
civ-ph show civ-41 --format json
civ-ph search Dante
civ-ph prompt gb-01 --mode creative
civ-ph spark gt-16 --count 5
civ-ph spine
civ-ph path homer-to-tolstoy
civ-ph validate
```

All prompt and spark commands are template-only. They do not call an AI provider. The old `ph-civ` command is kept only as a temporary deprecated alias for `civ-ph`.

## Literary Spine

```text
Homer -> Virgil -> Dante -> Shakespeare -> Dostoevsky -> Tolstoy
```

Tolstoy is routed through `sh-16`, where *Anna Karenina* appears as a source-backed coda rather than a dedicated Tolstoy lecture.

## Predictive History Museum

The museum is organized around chapter exhibits, not flat item rows. Each chapter in Predictive History: Civilization and Predictive History: Apocalypse should eventually have one exhibit with stored artifacts, rights notes, room placement, and a clear visitor path.

See `docs/public-repo-contract.md`, `docs/media-inventory-guide.md`, `schemas/museum-exhibit.schema.json`, and `schemas/museum-artifact.schema.json`.

## License

License is pending. See `LICENSE-PENDING.md`.
