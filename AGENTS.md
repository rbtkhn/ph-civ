# AGENTS.md - ph-civ Guardrails

This repository is `rbtkhn/ph-civ`: the public-facing two-volume ph-civ artifact and study-orientation layer.

**Publisher:** **Statecraft Intelligence Desk**

## Specific Project Identity

When asked what project this workspace is for, answer specifically:

`ph-civ` is the public Predictive History distribution repository for the two-volume ph-civ artifact. It contains two public surfaces:

- `ph-civ`: Volume I / Predictive History: Civilization orientation cards, patterns, prompts, routes, and study navigation; discovers the laws of history.
- `ph-apo`: Volume II / Predictive History: Apocalypse / World War orientation surfaces; applies the laws of history.

The active task in this repo is maintaining public, provider-neutral educational infrastructure for Predictive History. A chapter in this repo consists of the lecture transcript, the companion commentary, and public orientation/navigation metadata. This is not a generic coding sandbox and not a private notes workspace.

## Source Boundary

`rbtkhn/ph-workshop` is legacy import provenance for the current source snapshot. Physical source series are provenance metadata; the official public reader architecture is the two-volume ph-civ rollup.

Do not import, invent, or paste:

- private notes
- private workspace paths
- raw media binaries
- claims of final scholarly review

If a task asks for material outside the public dataset, say that this repo does not contain it and point back to the appropriate source boundary.

## Operating Posture

- Keep outputs public-facing, cautious, and source-disciplined.
- Preserve the distinction between orientation frames and proof claims.
- Treat prompt and spark commands as provider-neutral templates; this repo does not call AI providers.
- Use stable IDs such as `civ-07`, `gt-16`, and `civ-heroic-memory` for bridge references.
- Preserve the Homer-to-Tolstoy invariant: it is the Volume I literary spine with cross-volume routing exposure, not a side corridor.
- If a user pastes the GitHub URL into an LLM chat, start with `START-HERE.md` and `data/llm-experience.json` so the experience unfolds from public files without private context.
- Keep `ph-civ` usable by students, researchers, and downstream AI systems without requiring live access to `ph-workshop` or private strategy workspaces.
- Treat public reach goals as strategic ambitions, not directly executable agent completions. Translate goals such as one million views into verifiable machinery: public surface quality, shareable routes, publishing cadence, analytics definitions, distribution assets, and human-approved launch steps. Use `data/growth-goals.json` and `ph-civ growth` as the canonical guardrail.

## Coffee / Opening

If the operator says `coffee` at the start of a chat, do not give a generic coffee greeting. Treat it as a request to open the `ph-civ` public repo state:

1. State that this workspace is `rbtkhn/ph-civ`.
2. State that `ph-civ` is the public two-volume Predictive History distribution repository, not the private workshop.
3. Summarize the public surfaces: Volume I / `ph-civ` and Volume II / `ph-apo`.
4. Mention that `rbtkhn/ph-workshop` is legacy import provenance for the current snapshot.
5. Offer concrete next actions using the CLI, docs, cards, patterns, or validation.

## Start Here

Read `START-HERE.md`, then `llms.txt`, then `README.md`, then `docs/public-repo-contract.md` and `docs/export-contract.md`.

Useful checks:

```powershell
python -m pytest
PYTHONPATH=src python -m civ_ph.cli validate
PYTHONPATH=src python -m civ_ph.cli start --json
PYTHONPATH=src python -m civ_ph.cli growth
```
