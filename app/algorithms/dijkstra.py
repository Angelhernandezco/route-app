"""Implementación de Dijkstra (sin librerías de grafos) sobre una matriz de costos."""
import heapq
import math

from app.algorithms.types import DistanceMatrix, Route
from app.exceptions import NoRouteFoundError


def dijkstra(matrix: DistanceMatrix, source: int, target: int) -> Route:
    """Camino de menor costo de `source` a `target`.

    Grafo completo dirigido: cada índice es un nodo y matrix[i][j] el costo de la
    arista i -> j (None = sin arista). Devuelve la lista de índices del camino.
    """
    n = len(matrix)
    dist = [math.inf] * n
    prev: list[int | None] = [None] * n
    dist[source] = 0.0
    heap: list[tuple[float, int]] = [(0.0, source)]

    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue  # entrada obsoleta del heap
        if u == target:
            break  # ya no puede mejorar
        for v in range(n):
            cost = matrix[u][v]
            if v == u or cost is None:
                continue
            new_d = d + cost
            if new_d < dist[v]:
                dist[v] = new_d
                prev[v] = u
                heapq.heappush(heap, (new_d, v))

    if math.isinf(dist[target]):
        raise NoRouteFoundError(f"No existe camino del punto {source} al punto {target} según la matriz de OSRM.")

    path = [target]
    while path[-1] != source:
        path.append(prev[path[-1]])  # type: ignore[arg-type]
    path.reverse()
    return path
