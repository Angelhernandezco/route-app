"""Servicio de Dijkstra. No conoce OSRM: solo recibe la matriz."""
from app.algorithms.dijkstra import dijkstra
from app.algorithms.matrix import validate_matrix
from app.algorithms.types import DistanceMatrix, Route


def find_route(distance_matrix: DistanceMatrix) -> Route:
    """Camino de menor costo entre el primer y el último punto.

    origen = índice 0, destino = índice n-1. Devuelve índices de la lista
    original de coordenadas, p. ej. [0, 3, 5, 2, 4].
    """
    n = validate_matrix(distance_matrix)
    return dijkstra(distance_matrix, source=0, target=n - 1)
