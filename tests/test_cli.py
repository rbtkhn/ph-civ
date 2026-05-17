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


def test_reserved_surface_commands(capsys):
    from civ_ph.cli import apo_main, mus_main
    assert apo_main(["status"]) == 0
    assert "ph-apo" in capsys.readouterr().out
    assert mus_main(["status"]) == 0
    assert "ph-mus" in capsys.readouterr().out
