"""
seed_sector_22.py — Sector 22: Recursión (5 niveles, IDs 190–194).

Uso (desde la raíz del proyecto):
    python -m scripts.seed_sector_22

Comportamiento:
    1. Elimina solo los challenges con sector_id = 22.
    2. Inserta los 5 niveles del Sector 22 — medium → hard.
    3. El Nivel 194 es Boss de Fase (is_phase_boss = True).

Temática técnica: recursión, caso base, llamada recursiva, factorial,
                  fibonacci, recursión sobre listas.
Narrativa: El Laberinto del Nexo — el desafío final recursivo.
"""
import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.migrate_restructure_sectors import NEW_RECURSION_CHALLENGES as SECTOR_22

# SECTOR_22 se importa del script de migración — es la fuente canónica.
# Para re-seedear: python -m scripts.seed_master --sector 22
