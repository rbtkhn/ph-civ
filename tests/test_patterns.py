import json

from civ_ph.cli import main, validate_patterns
from civ_ph.data import load_cards, load_patterns, patterns_for_source


def test_patterns_command_lists_eight_seed_patterns(capsys):
    assert main(["patterns"]) == 0
    out = capsys.readouterr().out
    assert "civ-elite-overproduction" in out
    assert "civ-chokepoint-pressure" in out
    assert len(load_patterns()) == 8


def test_pattern_json_returns_chokepoint_sources(capsys):
    assert main(["pattern", "civ-chokepoint-pressure", "--format", "json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["pattern_id"] == "civ-chokepoint-pressure"
    assert payload["source_ids"] == ["geo-14", "gt-16"]


def test_bridge_source_returns_linked_patterns(capsys):
    assert main(["bridge", "gt-16", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["source_id"] == "gt-16"
    assert [p["pattern_id"] for p in payload["patterns"]] == ["civ-chokepoint-pressure"]
    assert [p["pattern_id"] for p in patterns_for_source("gt-16")] == [
        "civ-chokepoint-pressure"
    ]


def test_validate_patterns_rejects_duplicate_and_unknown_source():
    cards = load_cards()
    base = dict(load_patterns()[0])
    duplicate = dict(base)
    unknown = dict(base)
    unknown["pattern_id"] = "civ-test-unknown"
    unknown["source_ids"] = ["nope-99"]

    errors = validate_patterns([base, duplicate, unknown], cards)

    assert "duplicate pattern_id: civ-elite-overproduction" in errors
    assert "civ-test-unknown unknown source_id: nope-99" in errors
