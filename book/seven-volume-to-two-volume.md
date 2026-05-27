# From The Old Seven Volumes To The Current Two

Predictive History was not originally organized for public readers as one two-volume artifact.

The older manuscript scaffold grouped the corpus into seven source families:

1. Volume I: Geo-Strategy
2. Volume II: Civilization
3. Volume III: Secret History
4. Volume IV: Game Theory
5. Volume V: Great Books
6. Volume VI: Essays
7. Volume VII: Interviews

The current public repository is organized differently. It is built for reading rather than source-production history:

- `ph-civ`: Volume I / Civilization
- `ph-apo`: Volume II / Apocalypse

That is the core membrane for this repository:

```text
old source-native scaffold -> current reader-native architecture
```

The old scaffold describes how the corpus was made. The current two-volume structure describes how the corpus should be read.

## The Organizing Shift

The seven-volume manuscript grouped material by source lane. The public repository groups material by civilizational role.

- **Civilization** is the law-discovery semester.
- **Apocalypse** is the law-application semester.

This means older series are rerouted by function rather than preserved as separate public volumes.

## Rerouting Table

| Old Manuscript Volume | Current Public Placement | Why It Moves There | Notes |
| --- | --- | --- | --- |
| Volume I: Geo-Strategy | Apocalypse | Pressure reading, conflict reading, and geopolitical application | Preserved physically through legacy provenance folders. |
| Volume II: Civilization | Civilization | Core law-discovery spine | This is the least transformed lane. |
| Volume III: Secret History | Mostly Apocalypse | Deep causal and application scaffolding for crisis, empire, evil, and collapse | Selected nodes such as `sh-11`, `sh-16`, `sh-17`, and `sh-18` also support Civilization. |
| Volume IV: Game Theory | Apocalypse | Explicit law-application and escalation lane | Later `gt-*` chapters are especially visible in `ph-apo`. |
| Volume V: Great Books | Civilization | Literary and imaginative law-discovery surface | Great Books is absorbed into Civilization by function. |
| Volume VI: Essays | Apocalypse | Written application texts tied to crisis, war, finance, and strategic realignment | Publicly routed through the `sub-*` essay lane. |
| Volume VII: Interviews | Not currently foregrounded as a public lane | Preserved as part of the older manuscript scaffold and provenance history | Interviews are not currently a major named pillar in the two-volume reader contract. |

## Important Mismatch: Essays And `book/volume-vii/`

Readers will notice that the current repository physically stores the public essay lane under `book/volume-vii/`.

That folder label is legacy migration residue and provenance metadata. It is not the authority on the older manuscript numbering.

The corrected manuscript-history statement is:

- old Volume VI = Essays
- old Volume VII = Interviews

So the physical path `book/volume-vii/` should be read as a legacy import location, not as proof that Essays were originally the seventh manuscript volume.

## How To Read The Repo

Use this simple rule:

```text
The old scaffold describes how the corpus was made.
The current two-volume structure describes how the corpus should be read.
```

If you want the law-discovery semester, read **Civilization**. If you want to see those laws applied under pressure, read **Apocalypse**.

The older `book/volume-*` folders still matter for provenance, but they are not the preferred growth contract for new public chapter work. New public Civilization-facing work should grow through `ph-civ/chapters/`. New public Apocalypse-facing work should grow through `ph-apo/chapters/`.
