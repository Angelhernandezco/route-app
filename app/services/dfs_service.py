"""Depth-First Search (búsqueda en profundidad)."""
from typing import Dict, List, Optional, Set, Tuple

from app.utils.graph_utils import (
    Graph,
    RouteResult,
    calculate_path_cost,
    neighbors,
    reconstruct_path,
)
from app.exceptions import NoRouteError
from app.services.base_search_service import SearchService


class DfsService(SearchService):
    """DFS real con pila explícita.

    Devuelve la primera ruta que encuentra al profundizar; **no garantiza** menor
    costo ni menor cantidad de aristas. Los vecinos se exploran en el orden en que
    aparecen declarados en el grafo.
    """

    def _ejecutar(self, grafo: Graph, inicio: str, objetivo: str) -> RouteResult:
        visitados: Set[str] = set()
        padres: Dict[str, Optional[str]] = {}
        pila: List[Tuple[str, Optional[str]]] = [(inicio, None)]

        while pila:
            actual, padre = pila.pop()
            if actual in visitados:
                continue
            visitados.add(actual)
            padres[actual] = padre

            if actual == objetivo:
                ruta = reconstruct_path(padres, inicio, objetivo)
                return RouteResult(ruta, calculate_path_cost(grafo, ruta))

            # Se apilan en orden inverso para explorar primero el primer vecino.
            for vecino in reversed(list(neighbors(grafo, actual))):
                if vecino not in visitados:
                    pila.append((vecino, actual))

        raise NoRouteError(inicio, objetivo)
