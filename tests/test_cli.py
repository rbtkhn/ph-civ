import json
from pathlib import Path

from civ_ph.cli import main
from civ_ph.data import (
    load_cards,
    load_choreography,
    load_course_architecture,
    load_growth_goals,
    load_llm_experience,
    load_museum_index,
    load_route_seed,
    load_spine,
)

ROOT = Path(__file__).resolve().parents[1]


def test_loads_all_seeded_cards():
    cards = load_cards()
    assert len(cards) == 140
    assert {"civilization", "world-war"} <= {card["part"] for card in cards}


def test_all_cards_have_local_transcript_and_commentary():
    cards = load_cards()
    transcript_paths = []
    commentary_paths = []
    for card in cards:
        transcript_path = ROOT / card["source_paths"]["source_chapter_path"]
        commentary_path = ROOT / card["source_paths"]["commentary_path"]
        assert transcript_path.exists(), card["source_id"]
        assert commentary_path.exists(), card["source_id"]
        transcript_paths.append(transcript_path)
        commentary_paths.append(commentary_path)

    assert len(set(transcript_paths)) == 140
    assert len(set(commentary_paths)) == 140


def test_all_commentaries_have_open_project_canvas():
    required = [
        "canvas_status: open",
        "analysis_depth: seed",
        "scaffold_version: ph_civ_commentary_canvas_v1",
        "## Project Canvas",
        "### Project Leverage",
        "### Laws / Patterns Exposed",
        "### Volume Role",
        "### Museum Hooks",
        "### Strategy / Present-Day Application",
        "### Counter-Readings",
        "### Open Questions",
        "### Build Notes / Future Enhancements",
    ]
    for card in load_cards():
        commentary_path = ROOT / card["source_paths"]["commentary_path"]
        text = commentary_path.read_text(encoding="utf-8")
        for marker in required:
            assert marker in text, f"{card['source_id']} missing {marker}"


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
    assert spine["spine_id"] == "homer-to-tolstoy"
    assert spine["structural_role"] == "volume_i_literary_spine"
    assert spine["routing_role"] == "cross_volume_exposure"
    assert spine["launch_readiness"] == "defined_not_launch_ready"
    assert "first public reader" in spine["first_reader_gap"]
    assert spine["sequence"][-1]["author"] == "Tolstoy"
    assert spine["sequence"][-1]["source_ids"] == ["sh-16"]


def test_literary_spine_path_surfaces_launch_readiness(capsys):
    assert main(["path", "homer-to-tolstoy"]) == 0
    out = capsys.readouterr().out
    assert "launch_readiness: defined_not_launch_ready" in out
    assert "first_reader_gap:" in out
    assert "guardrail:" in out


def test_two_volume_architecture_is_primary():
    architecture = load_course_architecture()
    assert architecture["primary_artifact"] == "two_volume_ph_civ"
    assert architecture["volumes"]["volume_i"]["surface"] == "ph-civ"
    assert architecture["volumes"]["volume_i"]["role"] == "law_discovery"
    assert architecture["volumes"]["volume_ii"]["surface"] == "ph-apo"
    assert architecture["volumes"]["volume_ii"]["role"] == "law_application"
    assert architecture["museum"]["surface"] == "ph-mus"
    assert architecture["museum"]["role"] == "chapter_exhibit_layer"
    assert "ph-mus" not in {volume["surface"] for volume in architecture["volumes"].values()}
    assert architecture["bridge_support_nodes"] == ["sh-11", "sh-16", "sh-17", "sh-18"]


def test_public_surfaces_are_named(capsys):
    assert main(["surface", "ph-civ"]) == 0
    assert "Predictive History: Civilization" in capsys.readouterr().out


def test_status_leads_with_two_volume_artifact(capsys):
    assert main(["status"]) == 0
    out = capsys.readouterr().out
    assert "two-volume public Predictive History artifact" in out
    assert "Volume I / ph-civ / Civilization" in out
    assert "Volume II / ph-apo / Apocalypse" in out


def test_llm_native_bootloader_contract(capsys):
    start_here = ROOT / "START-HERE.md"
    assert start_here.exists()
    start_text = start_here.read_text(encoding="utf-8")
    assert "pastes `https://github.com/rbtkhn/ph-civ` into a ChatGPT chat or any other LLM" in start_text
    assert "First Response Contract" in start_text
    assert "Do not stop at a generic repository summary" in start_text
    assert "Default mode: first_tour" in start_text
    assert "Homer to Tolstoy is the Volume I literary spine" in start_text
    assert "Anna Karenina coda" in start_text
    assert "ph-mus` is not a third volume" in start_text

    experience = load_llm_experience()
    assert experience["start_here"] == "START-HERE.md"
    assert experience["full_context"]["path"] == "llms-full.txt"
    assert experience["full_context"]["purpose"] == "one_shot_llm_context_packet"
    assert experience["first_response_contract"]["default_mode"] == "first_tour"
    assert "generic repository summary" in experience["first_response_contract"]["anti_pattern"]
    assert experience["first_response_contract"]["required_opening_files"] == [
        "START-HERE.md",
        "llms.txt",
        "llms-full.txt",
    ]
    assert experience["first_response_contract"]["opening_route"] == "civ-07"
    assert experience["first_response_contract"]["opening_path"] == "homer-to-tolstoy"
    assert any("Choose one:" in line for line in experience["first_response_contract"]["template"])
    assert experience["public_surfaces"]["volume_i"]["surface"] == "ph-civ"
    assert experience["public_surfaces"]["volume_ii"]["surface"] == "ph-apo"
    assert experience["public_surfaces"]["museum"]["surface"] == "ph-mus"
    assert experience["public_surfaces"]["museum"]["not_a_volume"] is True
    assert experience["first_seed"]["route_ids"] == load_route_seed()["route_ids"]
    guardrails = "\n".join(experience["guardrails"])
    assert "Homer to Tolstoy" in guardrails
    assert "Anna Karenina coda" in guardrails
    assert "ph-mus is not a third volume" in guardrails

    assert main(["start", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["experience_id"] == "ph_civ_llm_native_bootloader"
    assert payload["full_context"]["path"] == "llms-full.txt"
    assert payload["first_response_contract"]["default_mode"] == "first_tour"
    assert payload["first_seed"]["route_ids"] == load_route_seed()["route_ids"]


def test_llms_full_context_packet_exists():
    packet = ROOT / "llms-full.txt"
    assert packet.exists()
    text = packet.read_text(encoding="utf-8")
    assert "full one-shot LLM context packet" in text
    assert "https://github.com/rbtkhn/ph-civ" in text
    assert "First Response Contract" in text
    assert "Do not stop at a generic repository summary" in text
    assert "Default mode: `first_tour`" in text
    assert "starting at civ-07" in text
    assert "Homer to Tolstoy is the Volume I literary spine" in text
    assert "Anna Karenina coda" in text
    assert "`ph-mus` is not a third volume" in text
    assert "Do not claim live geopolitical certainty" in text


def test_volumes_command_returns_architecture(capsys):
    assert main(["volumes", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["primary_artifact"] == "two_volume_ph_civ"
    assert payload["volumes"]["volume_i"]["surface"] == "ph-civ"
    assert payload["volumes"]["volume_i"]["role"] == "law_discovery"
    assert payload["volumes"]["volume_ii"]["surface"] == "ph-apo"
    assert payload["volumes"]["volume_ii"]["role"] == "law_application"
    assert payload["museum"]["surface"] == "ph-mus"
    assert payload["museum"]["role"] == "chapter_exhibit_layer"
    assert payload["unique_card_count"] == 140


def test_volume_command_lists_conceptual_membership(capsys):
    assert main(["volume", "volume-i", "--json"]) == 0
    volume_i = json.loads(capsys.readouterr().out)
    volume_i_ids = {card["source_id"] for card in volume_i["cards"]}
    assert {"civ-01", "gb-01", "sh-11", "sh-16", "sh-17", "sh-18"} <= volume_i_ids
    assert volume_i["role"] == "law_discovery"

    assert main(["volume", "volume-ii", "--json"]) == 0
    volume_ii = json.loads(capsys.readouterr().out)
    volume_ii_ids = {card["source_id"] for card in volume_ii["cards"]}
    assert {"geo-01", "gt-01", "sh-01", "sh-28"} <= volume_ii_ids
    assert volume_ii["role"] == "law_application"


def test_growth_goals_translate_outcomes_to_agent_machinery():
    growth_goals = load_growth_goals()
    assert growth_goals["goal_system"] == "ph_civ_public_growth"
    assert growth_goals["agent_goal_policy"]["must_translate_outcome_to_machinery"] is True
    campaign = growth_goals["campaigns"][0]
    assert campaign["campaign_id"] == "one_million_views_2026"
    assert campaign["status"] == "strategic_ambition"
    assert campaign["target_count"] == 1000000
    assert campaign["target_date"] == "2026-12-31"
    assert "source-disciplined educational trust" in campaign["unresolved_tension"]
    assert campaign["success_requires_external_audience_behavior"] is True
    assert campaign["human_approval_required_for_publication"] is True
    assert "achieved" not in campaign["status"]
    assert campaign["first_live_wedge"]["wedge_id"] == "launch_volume_i_spine"
    assert campaign["first_live_wedge"]["launch_readiness"] == "defined_not_launch_ready"
    assert "deserves audience growth" in campaign["first_live_wedge"]["readiness_question"]
    assert "Homer-to-Tolstoy route" in campaign["first_live_wedge"]["scope"]
    assert "without claiming views have already been earned" in campaign["first_live_wedge"]["done_when"]
    assert "analytics plan defines what counts as a view across GitHub, web, video, social, and document surfaces" in campaign["measurable_agent_outputs"]
    assert "distribution calendar converts the target into weekly and monthly milestones" in campaign["measurable_agent_outputs"]


def test_growth_command_returns_agent_goal_policy(capsys):
    assert main(["growth", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["agent_goal_policy"]["must_translate_outcome_to_machinery"] is True
    assert payload["campaigns"][0]["campaign_id"] == "one_million_views_2026"
    assert payload["campaigns"][0]["first_live_wedge"]["wedge_id"] == "launch_volume_i_spine"
    assert payload["campaigns"][0]["first_live_wedge"]["launch_readiness"] == "defined_not_launch_ready"


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
    payload = json.loads(capsys.readouterr().out)
    assert payload["route_type"] == "spine"
    assert "literature alone drives history" in payload["caveat"]
    assert payload["museum"]["exhibit_path"] == "corpus/media-packs/civ-07.md"
    assert main(["route", "civ-17", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["route_type"] == "spine"
    assert "Virgil and Rome" in payload["what_changes_here"]
    assert apo_main(["route", "gt-16", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["route_type"] == "application"
    assert payload["museum"]["exhibit_path"] == "corpus/media-packs/gt-16.md"
    assert main(["route", "sh-16", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["surface"] == "ph-apo"
    assert payload["route_type"] == "coda"
    assert "Anna Karenina coda" in payload["caveat"]
    assert "not a dedicated Tolstoy lecture" in payload["caveat"]
    assert apo_main(["route", "sh-16", "--json"]) == 0
    assert json.loads(capsys.readouterr().out)["route_type"] == "coda"
    assert mus_main(["route", "civ-07", "--json"]) == 0
    assert json.loads(capsys.readouterr().out)["museum"]["exhibit_path"] == "corpus/media-packs/civ-07.md"


def test_ten_route_spine_seed_guardrails():
    routes = load_choreography()
    route_ids = [route["source_id"] for route in routes]
    assert route_ids == [
        "civ-07",
        "civ-17",
        "civ-29",
        "civ-51",
        "gb-02",
        "gb-09",
        "geo-14",
        "gt-16",
        "sh-16",
        "sh-28",
    ]
    assert load_route_seed()["seed_id"] == "ten_route_spine_seed"
    assert load_route_seed()["route_ids"] == route_ids
    assert set(route_ids) == {exhibit["source_id"] for exhibit in load_museum_index()}
    route_types = {route["source_id"]: route["route_type"] for route in routes}
    assert route_types["civ-17"] == "spine"
    assert route_types["gb-02"] == "paired_close_reading"
    assert route_types["gb-09"] == "paired_close_reading"
    assert route_types["geo-14"] == "application"
    assert route_types["gt-16"] == "application"
    assert route_types["sh-28"] == "application"
    assert route_types["sh-16"] == "coda"
    sh16 = next(route for route in routes if route["source_id"] == "sh-16")
    assert sh16["surface"] == "ph-apo"
    assert "Anna Karenina coda" in sh16["caveat"]
    assert "not a dedicated Tolstoy lecture" in sh16["caveat"]
