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

# Extraer todos los niveles de levels_data
# codex_sales_mastery.json tiene "phases" y dentro "modules" o "boss_challenges"
for phase in arch.get("phases", []):
    for module in phase.get("modules", []):
        for lvl in module.get("sample_levels", []):
            SALES_MASTERY.append({
                "codex_id": "sales_mastery_v1",
                "level_order": lvl.get("level"),
                "title": lvl.get("title", ""),
                "description": lvl.get("business_context", "Sin descripción"),
                "difficulty": lvl.get("difficulty", "medium"),
                "difficulty_tier": 2 if lvl.get("difficulty") == "medium" else (3 if lvl.get("difficulty") == "expert" else 1),
                "base_xp_reward": lvl.get("xp_reward", 100),
                "is_project": False,
                "challenge_type": lvl.get("format", "scenario"),
                "phase": phase.get("phase_codename", "desafio_sales"),
                "lore_briefing": lvl.get("scenario", ""),
                "pedagogical_objective": lvl.get("operator_task", ""),
                "initial_code": "",
                "expected_output": "",
                "hints_json": "[]",
                "test_inputs_json": "[]",
                "concepts_taught_json": "[]"
            })
    boss = phase.get("phase_boss")
    if boss:
        SALES_MASTERY.append({
            "codex_id": "sales_mastery_v1",
            "level_order": boss.get("level"),
            "title": boss.get("boss_codename", ""),
            "description": boss.get("scenario", "Boss Battle"),
            "difficulty": "expert",
            "difficulty_tier": 3,
            "base_xp_reward": boss.get("phase_reward", {}).get("xp_reward", 800),
            "is_project": True,
            "challenge_type": "boss_battle",
            "phase": phase.get("phase_codename", "desafio_sales"),
            "lore_briefing": boss.get("scenario", ""),
            "pedagogical_objective": boss.get("win_condition", ""),
            "initial_code": "",
            "expected_output": "",
            "hints_json": "[]",
            "test_inputs_json": "[]",
            "concepts_taught_json": "[]"
        })
