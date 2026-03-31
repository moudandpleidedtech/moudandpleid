import json
from pathlib import Path

# Carga la data combinando los dos JSON de TPM
base_dir = Path(__file__).resolve().parent.parent / "app" / "data"

try:
    with open(base_dir / "codex_tpm_architecture.json", "r", encoding="utf-8") as f:
        arch = json.load(f)
except Exception as e:
    arch = {"phases": []}

try:
    with open(base_dir / "codex_tpm_challenge00_levels.json", "r", encoding="utf-8") as f:
        levels_data = json.load(f)
except Exception as e:
    levels_data = {"levels": []}

TPM_MASTERY = []

# Extraer todos los niveles de levels_data
for lvl in levels_data.get("levels", []):
    TPM_MASTERY.append({
        "codex_id": "tpm_mastery_v1",
        "level_order": lvl.get("level_order"),
        "title": lvl.get("title", ""),
        "description": lvl.get("office_crisis", "Sin descripción"),
        "difficulty": lvl.get("difficulty", "medium"),
        "difficulty_tier": 2 if lvl.get("difficulty") == "medium" else (3 if lvl.get("difficulty") == "expert" else 1),
        "base_xp_reward": lvl.get("xp_reward", 100),
        "is_project": lvl.get("is_boss_battle", False),
        "challenge_type": lvl.get("challenge_type", "scenario"),
        "phase": lvl.get("phase", "desafio_00"),
        "lore_briefing": lvl.get("learning_trigger", ""),
        "pedagogical_objective": lvl.get("operator_task", ""),
        "initial_code": "",
        "expected_output": "",
        "hints_json": "[]",
        "test_inputs_json": "[]",
        "concepts_taught_json": "[]"
    })
