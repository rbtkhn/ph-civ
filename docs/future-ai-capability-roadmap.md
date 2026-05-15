# Future AI Capability Roadmap

`civ-ph` should be treated not merely as a static export, but as a future-facing civilizational context layer that becomes more useful as AI interfaces mature.

## Likely Capability Unlocks

1. **Native context-pack import**
   AI systems may increasingly support structured project memory, MCP resources, knowledge packs, or app connectors. `civ-ph` should remain easy to ingest as JSONL, Markdown, schema-valid cards, and eventually an MCP server.

2. **Promptless study flows**
   Users should not need to know the right question in advance. Commands like `civ-ph start`, `civ-ph spark`, `civ-ph path`, and `civ-ph today` should generate first questions, guided sessions, and next steps automatically.

3. **Agentic reading companions**
   AI agents will be able to walk a user through a path over multiple sessions: resume Homer to Tolstoy, quiz a lecture, compare a chapter to another, or continue a study thread from prior context. This requires stable IDs, paths, review status, and typed relations.

4. **Multimodal context**
   Media packs can become a major asset as AI systems accept images, maps, objects, timelines, and screenshots as first-class context. The media-pack schema should stay link-first, rights-safe, and machine-readable.

5. **Voice and tutor personalization**
   The same card should eventually render as seminar tutor, skeptical counter-reader, exam prep, creative prompt, or introductory guide. This argues for structured payloads and modular prompt templates.

6. **Citation and provenance enforcement**
   AI systems will likely improve at source-bounded answers. `civ-ph` should preserve clear boundaries between orientation cards, transcripts, commentary, and quote-grade claims.

7. **Graph navigation**
   Cross-volume corridors may become a core feature: not only searching for a card, but following routes such as Homer to Dante to Dostoevsky, Rome's afterlives, or pressure corridors in World War. Typed edges should remain stable and parseable.

8. **Local/offline AI**
   As local models improve, `civ-ph` should work well as a small portable package that can be installed once and used by local agents without dependence on any single AI provider.

9. **Community contribution workflows**
   Human curators can contribute media inventories, prompt improvements, path refinements, and guardrail notes. Schemas and validators should make contribution review straightforward.

10. **Adaptive learning metrics**
    Later versions may track which cards confuse users, which paths are most used, where sparks fail, and what questions people ask. These metrics can improve the context layer without altering source materials.

## Design Principle

Structured context now, richer interfaces later.

Future work should bias toward stable IDs, plain JSON/JSONL, schema validation, Markdown readability, MCP readiness, promptless commands, media-pack compatibility, no source-text leakage, strong provenance boundaries, and first-good-question generation as a core user experience.
