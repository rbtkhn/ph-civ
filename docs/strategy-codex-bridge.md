# Strategy-Codex Bridge

`ph-civ` is the public civilizational reference layer. `strategy-codex` is the live workshop where current-event analysis, raw inputs, operator judgment, and work-in-progress synthesis happen.

The bridge between them is intentionally small: strategy-codex may cite public `pattern_id` values and public `source_id` cards from this repository. It should not import private notes, transcripts, commentary bodies, or workshop paths into `ph-civ`.

## How To Use Patterns

- Cite a stable `pattern_id` when a strategy page needs a reusable civilizational frame.
- Pair the `pattern_id` with the relevant public `source_id` when possible.
- Treat pattern records as orientation aids, not proof of a live claim.
- Use current primary evidence for live events, forecasts, military claims, and attribution.

Example:

```text
pattern:civ-chokepoint-pressure
sources: geo-14, gt-16
use: public frame for Hormuz / shipping / energy pressure
```

## Boundary

Do not use `ph-civ` as a strategy inbox, raw-input store, or private editorial workspace. If a strategy-codex page needs a civilizational frame, cite the pattern and continue the live analysis in strategy-codex.
