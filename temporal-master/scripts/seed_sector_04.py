"""
seed_sector_04.py — Sector 04: Funciones (10 niveles, IDs 31–40).

Uso (desde la raíz del proyecto):
    python -m scripts.seed_sector_04

Comportamiento:
    1. Elimina solo los challenges con sector_id = 4.
    2. Inserta los 10 niveles del Sector 04 — curva easy → medium → hard.
    3. El Nivel 40 es Boss de Fase (is_phase_boss = True).

Temática técnica: def, parámetros, return, scope local, composición.
Narrativa: módulos de transmisión táctica del Nexo.
"""
import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.migrate_restructure_sectors import NEW_FUNCTIONS_CHALLENGES as SECTOR_04

# SECTOR_04 se importa del script de migración — es la fuente canónica.
# Para re-seedear: python -m scripts.seed_master --sector 4
