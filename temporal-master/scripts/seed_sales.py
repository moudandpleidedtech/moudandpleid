import json
from pathlib import Path

# Carga la data combinando los dos JSON de TPM
base_dir = Path(__file__).resolve().parent.parent / "app" / "data"

try:
    with open(base_dir / "codex_sales_mastery.json", "r", encoding="utf-8") as f:
        arch = json.load(f)
except Exception as e:
    arch = {}

SALES_MASTERY = []

def _tier(difficulty: str) -> int:
    return {"easy": 1, "medium": 2, "hard": 3, "expert": 3}.get(difficulty, 2)

# codex_sales_mastery.json: sectors → levels
for sector in arch.get("sectors", []):
    phase_name = sector.get("sector_name", "sales")
    for lvl in sector.get("levels", []):
        import json as _json
        concepts = lvl.get("concepts_taught", [])
        SALES_MASTERY.append({
            "codex_id":             "sales_mastery_v1",
            "level_order":          lvl.get("level_order"),
            "title":                lvl.get("title", ""),
            "description":          lvl.get("subtitle", lvl.get("lore_briefing", "Sin descripción")),
            "difficulty":           lvl.get("difficulty", "medium"),
            "difficulty_tier":      _tier(lvl.get("difficulty", "medium")),
            "base_xp_reward":       lvl.get("xp_reward", 100),
            "is_project":           lvl.get("is_boss_battle", False),
            "challenge_type":       lvl.get("challenge_type", "scenario"),
            "phase":                phase_name,
            "lore_briefing":        lvl.get("lore_briefing", ""),
            "pedagogical_objective": lvl.get("pedagogical_objective", ""),
            "theory_content":       lvl.get("example_strong_response", ""),
            "initial_code":         "",
            "expected_output":      "",
            "hints_json":           "[]",
            "test_inputs_json":     "[]",
            "concepts_taught_json": _json.dumps(concepts, ensure_ascii=False),
        })
