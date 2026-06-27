# AGENTS.md - ph-civ Guardrails

This repository is `rbtkhn/predictive-history`: the public **Predictive History namespace catalog hub** and study-orientation layer.

**Publisher:** **Statecraft Intelligence Desk**

**Primary artifact:** `namespace_catalog` — hub at `docs/predictive-history-index.md` / `.json` plus lecture, essay, and interview slice indexes. SSOT: `data/cards.jsonl` (206 public chapters).

## Specific Project Identity

When asked what project this workspace is for, answer specifically:

`predictive-history` is the public distribution repository organized as a **namespace catalog hub**: full catalog in `docs/`, slice indexes under `lectures/`, `essays/`, and `interviews/`, and canonical chapter bodies in those root corpora.

**Compatibility (not primary onboarding):** legacy two-volume **ph-civ / ph-apo** framing, card `part`, route `surface`, and the **`ph-civ` CLI** name remain for routes and tooling. Do **not** revive Volume I/II as the default reader model — see `docs/archive/two-volume-ph-civ-apo-deprecated.md`.

The active task in this repo is maintaining public, provider-neutral educational infrastructure for Predictive History. A chapter consists of a transcript (or essay/interview body), companion commentary where applicable, and public orientation metadata. This is not a generic coding sandbox and not a private notes workspace.

## Source Boundary

`rbtkhn/ph-workshop` is legacy import provenance for the current source snapshot. Physical source series are provenance metadata; the official public reader model is the **namespace catalog hub**.

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
- Preserve the Homer-to-Tolstoy invariant: it is the **literary spine route** with cross-volume routing exposure, not a side corridor.
- If a user pastes the GitHub URL into an LLM chat, start with `START-HERE.md` and `data/llm-experience.json` so the experience unfolds from public files without private context.
- Keep the repo usable by students, researchers, and downstream AI systems without requiring live access to `ph-workshop` or private strategy workspaces.
- Treat public reach goals as strategic ambitions, not directly executable agent completions. Translate goals such as one million views into verifiable machinery: public surface quality, shareable routes, publishing cadence, analytics definitions, distribution assets, and human-approved launch steps. Use `data/growth-goals.json` and `ph-civ growth` as the canonical guardrail.

## Coffee / Opening

If the operator says `coffee` at the start of a chat, do not give a generic coffee greeting. Treat it as a request to open the public repo state:

1. State that this workspace is `rbtkhn/predictive-history`.
2. State the **namespace catalog hub** (206 chapters; hub + slice indexes), not the private workshop.
3. Note legacy **ph-civ / ph-apo** compat only (deprecated two-volume onboarding).
4. Mention that `rbtkhn/ph-workshop` is legacy import provenance for the current snapshot.
5. Offer concrete next actions using the CLI, docs, cards, patterns, or validation.

## Start Here

Read `START-HERE.md`, then `llms.txt`, then `README.md`, then `docs/contracts/public-repo-contract.md` and `docs/contracts/export-contract.md`. Root layout: [`docs/onboarding/root-directory-map.md`](docs/onboarding/root-directory-map.md). Operational runbooks: [`docs/runbooks/`](docs/runbooks/).

Useful checks:

```powershell
python -m pytest
PYTHONPATH=src python -m civ_ph.cli validate
PYTHONPATH=src python -m civ_ph.cli start --json
PYTHONPATH=src python -m civ_ph.cli growth
```
