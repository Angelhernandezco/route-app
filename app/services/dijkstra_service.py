"""Algoritmo de Dijkstra."""
import heapq
import math
from typing import Dict, List, Optional, Set, Tuple

from app.utils.graph_utils import (
    Graph,
    RouteResult,
    neighbors,
    reconstruct_path,
    validate_non_negative_weights,
)
from app.exceptions import NoRouteError
from app.services.base_search_service import SearchService


class DijkstraService(SearchService):
    """Ruta de menor costo con min-heap. Requiere pesos no negativos."""

    def validar_grafo(self, grafo: Graph) -> None:
        validate_non_negative_weights(grafo)

    def _ejecutar(self, grafo: Graph, inicio: str, objetivo: str) -> RouteResult:
        distancias: Dict[str, float] = {inicio: 0.0}
        padres: Dict[str, Optional[str]] = {inicio: None}
        cola: List[Tuple[float, str]] = [(0.0, inicio)]
        cerrados: Set[str] = set()

        while cola:
            distancia, actual = heapq.heappop(cola)
            if actual in cerrados:  # entrada obsoleta del heap
                continue
            if actual == objetivo:  # extraído con su distancia mínima definitiva
                return RouteResult(reconstruct_path(padres, inicio, objetivo), distancia)
            cerrados.add(actual)

            for vecino, peso in neighbors(grafo, actual).items():
                if vecino in cerrados:
                    continue
                candidata = distancia + peso  # relajación de la arista
                if candidata < distancias.get(vecino, math.inf):
                    distancias[vecino] = candidata
                    padres[vecino] = actual
                    heapq.heappush(cola, (candidata, vecino))

        raise NoRouteError(inicio, objetivo)
