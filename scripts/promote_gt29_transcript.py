"""Promote gt-29 full transcript from sources capture into lectures/."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "sources/predictive-history/game-theory/gt-29.md"
LEC = ROOT / "lectures/game-theory/gt-29/gt-29-transcript.md"

FRONTMATTER = """---
source_id: "gt-29"
title: "Game Theory #29: Final Examination"
source_series: "Game Theory"
publication_date: "2026-06-04"
source_url: "https://www.youtube.com/watch?v=RE2UribEFIo"
video_id: "RE2UribEFIo"
transcript_status: "public_transcript"
transcript_fidelity: "exact_body_match"
transcript_source: "user_pasted_public_transcript"
representation_not_endorsement: true
review_status: "provisional"
source_captured_at: "2026-06-04"
fidelity_review_note: "Lecture transcript promoted from sources capture 2026-06-26; bodies aligned pending external ASR verification."
part: "world-war"
part_role: "world-war"
date_inference_note: "Publication date inferred from lecture references to 'next Sunday, June 7' and 'tomorrow will be my last class'."
---

# Game Theory #29: Final Examination

## Part I: Full transcript

"""

SELF_LINK = re.compile(
    r"^Canonical public source capture:\n"
    r"\[sources/predictive-history/game-theory/gt-29\.md\]\([^\)]+\)\n\n",
    re.MULTILINE,
)


def extract_transcript_body(text: str) -> str:
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        text = text[end + 5 :]
    marker = "## Part I: Full transcript"
    idx = text.find(marker)
    body = text[idx + len(marker) :].lstrip("\n")
    return SELF_LINK.sub("", body, count=1)


def main() -> None:
    body = extract_transcript_body(SRC.read_text(encoding="utf-8"))
    payload = FRONTMATTER + body
    LEC.write_text(payload, encoding="utf-8")
    SRC.write_text(payload, encoding="utf-8")
    print(f"wrote {LEC.relative_to(ROOT)} ({len(payload)} chars)")
    print(f"synced {SRC.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
