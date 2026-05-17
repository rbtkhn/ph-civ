from civ_ph.cli import main
from civ_ph.data import load_cards, load_spine


def test_loads_all_seeded_cards():
    cards = load_cards()
    assert len(cards) == 140
    assert {"civilization", "world-war"} <= {card["part"] for card in cards}


def test_show_known_card_json(capsys):
    assert main(["show", "civ-41", "--format", "json"]) == 0
    assert "\"source_id\": \"civ-41\"" in capsys.readouterr().out


def test_invalid_source_id_returns_nonzero(capsys):
    assert main(["show", "nope-99"]) == 2
    assert "Unknown source_id" in capsys.readouterr().err


def test_prompt_creative_contains_boundaries(capsys):
    assert main(["prompt", "gb-01", "--mode", "creative"]) == 0
    out = capsys.readouterr().out
    assert "Limits:" in out
    assert "gb-01" in out


def test_validate_passes(capsys):
    assert main(["validate"]) == 0
    assert "card_count: 140" in capsys.readouterr().out


def test_exported_source_repo_uses_workshop():
    cards = load_cards()
    assert {card["source_snapshot"]["repo"] for card in cards} == {"rbtkhn/ph-workshop"}


def test_literary_spine_ends_with_tolstoy():
    spine = load_spine()
    assert spine["sequence"][-1]["author"] == "Tolstoy"
    assert spine["sequence"][-1]["source_ids"] == ["sh-16"]


def test_compat_alias_still_works(capsys):
    from civ_ph.cli import compat_main
    assert compat_main(["validate"]) == 0
    assert capsys.readouterr().err == ""


def test_public_surfaces_are_named(capsys):
    assert main(["surface", "ph-civ"]) == 0
    assert "Predictive History: Civilization" in capsys.readouterr().out


def test_surface_scoped_commands(capsys):
    from civ_ph.cli import apo_main, mus_main
    assert main(["list"]) == 0
    assert "civ-07" in capsys.readouterr().out
    assert apo_main(["list"]) == 0
    out = capsys.readouterr().out
    assert "gt-16" in out
    assert "civ-07" not in out
    assert apo_main(["status"]) == 0
    assert "ph-apo" in capsys.readouterr().out
    assert mus_main(["list"]) == 0
    assert "gt-16" in capsys.readouterr().out


def test_public_routes(capsys):
    from civ_ph.cli import apo_main, mus_main
    assert main(["route", "civ-07", "--json"]) == 0
    out = capsys.readouterr().out
    assert "\"museum\"" in out
    assert "corpus/media-packs/civ-07.md" in out
    assert apo_main(["route", "gt-16", "--json"]) == 0
    assert "corpus/media-packs/gt-16.md" in capsys.readouterr().out
    assert mus_main(["route", "civ-07", "--json"]) == 0
    assert "corpus/media-packs/civ-07.md" in capsys.readouterr().out
