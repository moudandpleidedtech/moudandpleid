"""
Servicio de cálculo Elo (Prompt 20).

K-factor = 32.
Un jugador de Elo bajo que vence a uno de Elo alto recibe más puntos.
"""

K_FACTOR = 32


def expected_score(rating_a: int, rating_b: int) -> float:
    """Probabilidad esperada de victoria para el jugador A."""
    return 1.0 / (1.0 + 10.0 ** ((rating_b - rating_a) / 400.0))


def compute_elo_delta(winner_rating: int, loser_rating: int) -> int:
    """
    Devuelve los puntos que el ganador le roba al perdedor.
    Mínimo 1 punto siempre.
    """
    exp = expected_score(winner_rating, loser_rating)
    return max(1, round(K_FACTOR * (1.0 - exp)))
