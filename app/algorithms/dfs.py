"""DFS iterativo: devuelve el primer camino que encuentra (no es el más corto)."""
from app.algorithms.path import build_path
from app.algorithms.types import DistanceMatrix, Route
from app.exceptions import NoRouteFoundError


def dfs(matrix: DistanceMatrix, source: int, target: int) -> Route:
    n = len(matrix)
    prev: dict[int, int | None] = {}
    stack: list[tuple[int, int | None]] = [(source, None)]  # (nodo, padre)

    while stack:
        u, parent = stack.pop()
        if u in prev:
            continue  # ya visitado
        prev[u] = parent
        if u == target:
            break
        # Se apilan en orden inverso para explorar primero el índice más bajo
        for v in range(n - 1, -1, -1):
            if v != u and matrix[u][v] is not None and v not in prev:
                stack.append((v, u))

    if target not in prev:
        raise NoRouteFoundError(f"No existe camino del punto {source} al punto {target} según la matriz de OSRM.")
    return build_path(prev, source, target)
