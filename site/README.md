# Study edition site (Phase 0)

Generated static reader skin for ph-civ. SSOT remains markdown under `book/`.

## Build

```bash
python scripts/build_study_edition.py --chapter civ-07
python scripts/validate_study_edition.py --chapter civ-07
```

## Preview locally

Open `site/dist/study/civ-07/index.html` in a browser (assets load via relative paths).

## Layout

- `site/_data/chapters/` — JSON bundles (build output)
- `site/dist/study/<source_id>/` — HTML study pages
- `site/assets/` — shared CSS/JS

Spec: [`docs/study-edition.md`](../docs/study-edition.md)
