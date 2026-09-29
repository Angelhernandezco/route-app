"""Registro de algoritmos (Strategy simple).

Cada servicio expone `find_route(distance_matrix) -> list[int]`.
Para activar un nuevo algoritmo basta implementar su `find_route`;
el endpoint no necesita cambios.
"""
from collections.abc import Callable

from app.algorithms.types import DistanceMatrix, Route
from app.models import Algorithm
from app.services import astar_service, bfs_service, dfs_service, dijkstra_service

RouteFinder = Callable[[DistanceMatrix], Route]

ROUTE_FINDERS: dict[Algorithm, RouteFinder] = {
    Algorithm.DIJKSTRA: dijkstra_service.find_route,
    Algorithm.BFS: bfs_service.find_route,
    Algorithm.DFS: dfs_service.find_route,
    Algorithm.A_STAR: astar_service.find_route,
}


def get_route_finder(algorithm: Algorithm) -> RouteFinder:
    return ROUTE_FINDERS[algorithm]
