"""Breadth-First Search (búsqueda en anchura)."""
from collections import deque
from typing import Deque, Dict, Optional, Set

from app.utils.graph_utils import (
    Graph,
    RouteResult,
    calculate_path_cost,
    neighbors,
    reconstruct_path,
)
from app.exceptions import NoRouteError
from app.services.base_search_service import SearchService


class BfsService(SearchService):
    """BFS real: explora por niveles con una cola.

    Encuentra la ruta con **menor cantidad de aristas**, no necesariamente la de
    menor costo cuando los pesos son distintos.
    """

    def _ejecutar(self, grafo: Graph, inicio: str, objetivo: str) -> RouteResult:
        visitados: Set[str] = {inicio}
        padres: Dict[str, Optional[str]] = {inicio: None}
        cola: Deque[str] = deque([inicio])

        while cola:
            actual = cola.popleft()
            for vecino in neighbors(grafo, actual):
                if vecino in visitados:
                    continue
                visitados.add(vecino)
                padres[vecino] = actual
                if vecino == objetivo:
                    ruta = reconstruct_path(padres, inicio, objetivo)
                    return RouteResult(ruta, calculate_path_cost(grafo, ruta))
                cola.append(vecino)

        raise NoRouteError(inicio, objetivo)
