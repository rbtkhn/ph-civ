"""Lecture transcript section rails — baseline ratchet tests."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))


def _audit_counts() -> dict[str, int]:
    proc = subprocess.run(
        [sys.executable, str(SCRIPTS / "lecture_section_pass.py"), "audit"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    counts: dict[str, int] = {}
    for line in proc.stdout.splitlines():
        if line.startswith("status:"):
            # status: {'slug': 69, 'flat': 80, ...}
            counts = eval(line.split(":", 1)[1].strip())
    return counts


def test_lecture_rails_strict_title_case():
    counts = _audit_counts()
    assert counts.get("title_case") == 149
    assert sum(counts.values()) == 149


def test_lecture_audit_strict_exit_zero():
    proc = subprocess.run(
        [
            sys.executable,
            str(SCRIPTS / "lecture_section_pass.py"),
            "audit",
            "--strict",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr


def test_slug_to_title_preserves_github_anchor():
    from lecture_rails_lib import github_heading_anchor, slug_to_title

    slug = "stalin-greatest-man-thesis"
    title = slug_to_title(slug)
    assert title == "Stalin Greatest Man Thesis"
    assert github_heading_anchor(title) == slug


def test_pin_cite_verifier_runs():
    proc = subprocess.run(
        [sys.executable, str(SCRIPTS / "verify_transcript_pin_cites.py"), "--source-id", "civ-59"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr
