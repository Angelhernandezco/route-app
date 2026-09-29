"""Servicio de DFS. No conoce OSRM: solo recibe la matriz."""
from app.algorithms.dfs import dfs
from app.algorithms.matrix import validate_matrix
from app.algorithms.types import DistanceMatrix, Route


def find_route(distance_matrix: DistanceMatrix) -> Route:
    """Ruta de DFS entre el primer (origen) y el último punto (destino), como índices."""
    n = validate_matrix(distance_matrix)
    return dfs(distance_matrix, source=0, target=n - 1)
