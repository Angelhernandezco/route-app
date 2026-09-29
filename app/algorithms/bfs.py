"""BFS: camino con MENOS SALTOS (ignora los pesos de la matriz)."""
from collections import deque

from app.algorithms.path import build_path
from app.algorithms.types import DistanceMatrix, Route
from app.exceptions import NoRouteFoundError


def bfs(matrix: DistanceMatrix, source: int, target: int) -> Route:
    n = len(matrix)
    prev: dict[int, int | None] = {source: None}  # también sirve como "visitados"
    queue = deque([source])

    while queue:
        u = queue.popleft()
        if u == target:
            break
        for v in range(n):
            if v != u and matrix[u][v] is not None and v not in prev:
                prev[v] = u
                queue.append(v)

    if target not in prev:
        raise NoRouteFoundError(f"No existe camino del punto {source} al punto {target} según la matriz de OSRM.")
    return build_path(prev, source, target)
