"""Utilidades comunes para reconstruir caminos."""
from app.algorithms.types import Route


def build_path(prev: dict[int, int | None], source: int, target: int) -> Route:
    """Reconstruye el camino source -> target a partir del diccionario de predecesores."""
    path = [target]
    while path[-1] != source:
        path.append(prev[path[-1]])  # type: ignore[arg-type]
    path.reverse()
    return path
