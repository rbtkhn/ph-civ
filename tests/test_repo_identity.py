from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_agent_identity_contract_exists():
    text = read_text("AGENTS.md")

    assert "rbtkhn/ph-civ" in text
    assert "public Predictive History" in text
    assert "not the private editorial workshop" in text
    assert "rbtkhn/ph-workshop" in text
    assert "generic coffee greeting" in text


def test_llms_load_contract_names_boundaries():
    text = read_text("llms.txt")

    assert "public consumption layer" in text
    assert "transcript bodies" in text
    assert "commentary bodies" in text
    assert "Strategy-Codex paths" in text


def test_readme_points_new_chats_to_identity_contract():
    text = read_text("README.md")

    assert "AGENTS.md" in text
    assert "llms.txt" in text
