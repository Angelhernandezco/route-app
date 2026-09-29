"""A*: como Dijkstra, pero prioriza con f(n) = g(n) + h(n).

Heurística: h(n) = matrix[n][target], la distancia OSRM directa de n al destino.
Así seguimos usando solo la matriz de OSRM (sin Haversine). Es admisible cuando la
matriz cumple la desigualdad triangular, que las distancias por carretera cumplen
prácticamente siempre.
"""
import heapq
import math

from app.algorithms.path import build_path
from app.algorithms.types import DistanceMatrix, Route
from app.exceptions import NoRouteFoundError


def astar(matrix: DistanceMatrix, source: int, target: int) -> Route:
    n = len(matrix)

    def h(node: int) -> float:
        value = matrix[node][target]
        return 0.0 if value is None else value  # sin dato -> 0 (heurística neutra)

    g = [math.inf] * n
    g[source] = 0.0
    prev: dict[int, int | None] = {source: None}
    heap: list[tuple[float, int]] = [(h(source), source)]  # (f, nodo)

    while heap:
        f, u = heapq.heappop(heap)
        if u == target:
            return build_path(prev, source, target)
        if f > g[u] + h(u):
            continue  # entrada obsoleta
        for v in range(n):
            cost = matrix[u][v]
            if v == u or cost is None:
                continue
            new_g = g[u] + cost
            if new_g < g[v]:
                g[v] = new_g
                prev[v] = u
                heapq.heappush(heap, (new_g + h(v), v))

    raise NoRouteFoundError(f"No existe camino del punto {source} al punto {target} según la matriz de OSRM.")
