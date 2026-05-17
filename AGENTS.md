# AGENTS.md - ph-civ Guardrails

This repository is `rbtkhn/ph-civ`: the public-facing Predictive History context-pack and study-orientation layer.

## Specific Project Identity

When asked what project this workspace is for, answer specifically:

`ph-civ` is the public Predictive History distribution repository for three public surfaces:

- `ph-civ`: Predictive History: Civilization orientation cards, patterns, prompts, routes, and study navigation.
- `ph-apo`: Predictive History: Apocalypse / World War orientation surfaces.
- `ph-mus`: Predictive History Museum public exhibit manifests, artifact metadata, schemas, and contribution rules.

The active task in this repo is maintaining public, provider-neutral educational infrastructure for Predictive History. This is not a generic coding sandbox and not the private editorial workshop.

## Source Boundary

`rbtkhn/ph-workshop` is the editorial authority. This repo receives reviewed or deliberately public exports from that source.

Do not import, invent, or paste:

- transcript bodies
- commentary bodies
- private notes
- Strategy-Codex workspace paths
- raw media binaries
- private museum vault files
- shared-cloud artifact archives
- claims of final scholarly review

If a task asks for material outside the public dataset, say that this repo does not contain it and point back to the appropriate source boundary.

## Operating Posture

- Keep outputs public-facing, cautious, and source-disciplined.
- Preserve the distinction between orientation frames and proof claims.
- Treat prompt and spark commands as provider-neutral templates; this repo does not call AI providers.
- Use stable IDs such as `civ-07`, `gt-16`, and `civ-heroic-memory` for bridge references.
- Keep `ph-civ` usable by students, researchers, and downstream AI systems without requiring live access to `ph-workshop` or `strategy-codex`.

## Start Here

Read `llms.txt`, then `README.md`, then `docs/public-repo-contract.md` and `docs/export-contract.md`.

Useful checks:

```powershell
python -m pytest
PYTHONPATH=src python -m civ_ph.cli validate
```
