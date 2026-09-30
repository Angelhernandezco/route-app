"""Algoritmo A*."""
import heapq
import math
from typing import Callable, Dict, List, Optional, Set, Tuple

from app.utils.graph_utils import (
    Graph,
    RouteResult,
    neighbors,
    reconstruct_path,
    validate_non_negative_weights,
)
from app.exceptions import NoRouteError
from app.services.base_search_service import SearchService

Heuristic = Callable[[str, str], float]


class AStarService(SearchService):
    """A* con prioridad ``f(n) = g(n) + h(n)``.

    La heurística por defecto es ``h(n) = 0`` (admisible y consistente), por lo que
    el resultado es óptimo, igual que Dijkstra. Para usar una heurística real se puede
    pasar una función ``(nodo_actual, nodo_final) -> float`` al constructor o
    sobrescribir :meth:`heuristic` en una subclase (p. ej. con coordenadas).
    """

    def __init__(self, heuristica: Optional[Heuristic] = None) -> None:
        self._heuristica = heuristica

    def heuristic(self, nodo_actual: str, nodo_final: str) -> float:
        """Estimación del costo restante h(n). Por defecto 0."""
        if self._heuristica is not None:
            return self._heuristica(nodo_actual, nodo_final)
        return 0

    def validar_grafo(self, grafo: Graph) -> None:
        validate_non_negative_weights(grafo)

    def _ejecutar(self, grafo: Graph, inicio: str, objetivo: str) -> RouteResult:
        g_costos: Dict[str, float] = {inicio: 0.0}  # g(n)
        padres: Dict[str, Optional[str]] = {inicio: None}
        # Entradas: (f, g, nodo)
        cola: List[Tuple[float, float, str]] = [
            (self.heuristic(inicio, objetivo), 0.0, inicio)
        ]
        cerrados: Set[str] = set()

        while cola:
            _, g_actual, actual = heapq.heappop(cola)
            if actual in cerrados:
                continue
            if actual == objetivo:
                return RouteResult(reconstruct_path(padres, inicio, objetivo), g_actual)
            cerrados.add(actual)

            for vecino, peso in neighbors(grafo, actual).items():
                if vecino in cerrados:
                    continue
                g_nuevo = g_actual + peso
                if g_nuevo < g_costos.get(vecino, math.inf):
                    g_costos[vecino] = g_nuevo
                    padres[vecino] = actual
                    f = g_nuevo + self.heuristic(vecino, objetivo)
                    heapq.heappush(cola, (f, g_nuevo, vecino))

        raise NoRouteError(inicio, objetivo)
