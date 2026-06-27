# Essay dated-ID migration (2026-06-26)

## Summary

All 43 public essay packets migrated from sequential **`essay-NN`** to **`essay-YYYY-MM-DD-{substack-slug}`**, matching the interview namespace pattern.

## Hard cut

- **Canonical `source_id`:** dated pattern only.
- **Legacy `essay-NN`:** crosswalk in [`data/essays/manifest.json`](../data/essays/manifest.json) only — no CLI aliases, no redirect stubs.
- **Old GitHub folder URLs** such as `https://github.com/rbtkhn/predictive-history/tree/main/essays/essay-07` **404** after this change.
- **Substack URLs** (`predictivehistory.substack.com/p/{slug}`) are unchanged.

## Operator commands

```bash
python scripts/rename_essays_to_dated_ids.py   # one-time; already applied
PYTHONPATH=src python -m civ_ph.cli index --force
PYTHONPATH=src python -m civ_ph.cli validate
```

## New intakes

[`scripts/intake_essays_phase2.py`](../scripts/intake_essays_phase2.py) emits dated IDs from `publication_date` + `substack_slug`. Check manifest for same-day collisions before landing.
