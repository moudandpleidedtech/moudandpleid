"""
rank_service.py — Sistema de Rangos de Operador DAKI EdTech

Rangos progresivos basados en el level_order del último desafío completado:

  L1–L10:   Trainee              (Novato)
  L11–L30:  Grid Crawler          (Rastreador de Red)
  L31–L60:  Cypherpunk Specialist  (Especialista en Cifrado)
  L61–L99:  Neural Architect       (Arquitecto Neural)
  L100:     Netzach Operative      (Operativo Netzach) — Rango máximo

Sistema de Points:
  Cada desafío completado otorga level_order puntos (distintos del XP).
  Un operador con L50 completado acumula 50 pts de ese challenge.
  Los points son la métrica de progreso curricular para leaderboards.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class RankDef:
    codename: str    # identificador almacenado en DB y mostrado en certificado
    title_es: str    # descripción narrativa en español


# Tabla canónica — (level_order_min, level_order_max, RankDef)
_RANK_TABLE: list[tuple[int, int, RankDef]] = [
    (0,   10,  RankDef("Trainee",               "Novato")),
    (11,  30,  RankDef("Grid Crawler",           "Rastreador de Red")),
    (31,  60,  RankDef("Cypherpunk Specialist",  "Especialista en Cifrado")),
    (61,  99,  RankDef("Neural Architect",       "Arquitecto Neural")),
    (100, 100, RankDef("Netzach Operative",      "Operativo Netzach")),
]

DEFAULT_RANK = "Trainee"

# Índice de orden para comparar rangos
_RANK_ORDER: dict[str, int] = {
    r.codename: i for i, (_, _, r) in enumerate(_RANK_TABLE)
}


def compute_rank(level_order: int | None) -> str:
    """
    Devuelve el codename del rango que corresponde al level_order completado.

    None (tutorial sin sector, L0) → "Trainee".
    Valores > 100 → "Netzach Operative".
    """
    if level_order is None:
        return DEFAULT_RANK
    for lo, hi, rank in _RANK_TABLE:
        if lo <= level_order <= hi:
            return rank.codename
    return _RANK_TABLE[-1][2].codename


def rank_promotes(old_rank: str, new_rank: str) -> bool:
    """
    True si new_rank es un rango superior (mayor índice) que old_rank.
    Garantiza que el rango nunca baje.
    """
    return _RANK_ORDER.get(new_rank, 0) > _RANK_ORDER.get(old_rank, 0)


def get_rank_title(codename: str) -> str:
    """Devuelve la descripción narrativa española del codename, o el propio codename."""
    for _, _, r in _RANK_TABLE:
        if r.codename == codename:
            return r.title_es
    return codename
