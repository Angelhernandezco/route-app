"""Servicio de A*. No conoce OSRM: solo recibe la matriz."""
from app.algorithms.astar import astar
from app.algorithms.matrix import validate_matrix
from app.algorithms.types import DistanceMatrix, Route


def find_route(distance_matrix: DistanceMatrix) -> Route:
    """Ruta de A* entre el primer (origen) y el último punto (destino), como índices."""
    n = validate_matrix(distance_matrix)
    return astar(distance_matrix, source=0, target=n - 1)
