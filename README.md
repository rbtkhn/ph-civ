# civ-ph

civ-ph is a lightweight, provider-neutral study tool for Predictive History orientation cards. It packages public civ-ph cards from `rbtkhn/predictive-history` so students and AI systems can explore historical placement, reading posture, pressure points, limits, return paths, and guided prompts without importing transcripts or commentary bodies.

This package is independent educational infrastructure. It is not official course material, not endorsement, and not a substitute for the source lectures, transcripts, commentary, or external verification.

## What Is Included

- 140 public civ-ph cards from Predictive History snapshot `56a4a08`.
- Two course parts: Civilization and World War.
- Series coverage: Civilization, Great Books, Geo-Strategy, Game Theory, and Secret History.
- The Homer-to-Tolstoy literary spine.
- Provider-neutral prompt templates.
- Media-inventory schema and curator instructions.

## What Is Excluded

- Full transcripts.
- Commentary bodies.
- Private notes or Strategy-Codex paths.
- External-source bibliography claims beyond the orientation cards.
- LLM provider integrations, API calls, or hidden model dependencies.

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

## Media Inventory

Human curators collect candidate public references for the whole civ-ph corpus. See `docs/media-curator-bounty.md`, `docs/media-inventory-guide.md`, and `schemas/media-inventory-item.schema.json`.

## License

License is pending. See `LICENSE-PENDING.md`.
