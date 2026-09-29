"""Servicio de BFS. No conoce OSRM: solo recibe la matriz."""
from app.algorithms.bfs import bfs
from app.algorithms.matrix import validate_matrix
from app.algorithms.types import DistanceMatrix, Route


def find_route(distance_matrix: DistanceMatrix) -> Route:
    """Ruta de BFS entre el primer (origen) y el último punto (destino), como índices."""
    n = validate_matrix(distance_matrix)
    return bfs(distance_matrix, source=0, target=n - 1)
