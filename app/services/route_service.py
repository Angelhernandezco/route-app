"""Selección y ejecución del algoritmo de búsqueda."""
import time
from typing import Dict, Optional, Tuple

from app.utils.graph_utils import Graph, RouteResult, all_nodes
from app.exceptions import InvalidGraphError, NodeNotFoundError
from app.services.a_star_service import AStarService
from app.services.base_search_service import SearchService
from app.services.bfs_service import BfsService
from app.services.dfs_service import DfsService
from app.services.dijkstra_service import DijkstraService


class RouteService:
    """Elige el service adecuado según ``tipoRuta`` y lo ejecuta midiendo su tiempo."""

    def __init__(self, servicios: Optional[Dict[str, SearchService]] = None) -> None:
        self._servicios: Dict[str, SearchService] = servicios or {
            "BFS": BfsService(),
            "DFS": DfsService(),
            "Dijkstra": DijkstraService(),
            "A*": AStarService(),
        }

    def obtener_servicio(self, tipo_ruta: str) -> SearchService:
        """Devuelve el service asociado a ``tipo_ruta``."""
        try:
            return self._servicios[tipo_ruta]
        except KeyError:
            raise InvalidGraphError(f"Algoritmo no soportado: '{tipo_ruta}'.") from None

    @staticmethod
    def validar_nodos(grafo: Graph, inicio: str, objetivo: str) -> None:
        """Verifica que el grafo no esté vacío y que ambos estados existan."""
        if not grafo:
            raise InvalidGraphError("El grafo no puede estar vacío.")
        nodos = all_nodes(grafo)
        if inicio not in nodos:
            raise NodeNotFoundError(f"estadoInicial '{inicio}' no existe en el grafo.")
        if objetivo not in nodos:
            raise NodeNotFoundError(f"estadoFinal '{objetivo}' no existe en el grafo.")

    def ejecutar(
        self, tipo_ruta: str, grafo: Graph, inicio: str, objetivo: str
    ) -> Tuple[RouteResult, float]:
        """Valida, ejecuta el algoritmo y devuelve ``(resultado, tiempo_ms)``.

        El tiempo mide **únicamente** la llamada a ``buscar``; las validaciones se
        hacen antes del cronómetro.
        """
        servicio = self.obtener_servicio(tipo_ruta)
        self.validar_nodos(grafo, inicio, objetivo)
        servicio.validar_grafo(grafo)

        inicio_t = time.perf_counter()
        resultado = servicio.buscar(grafo, inicio, objetivo, validar=False)
        fin_t = time.perf_counter()

        return resultado, (fin_t - inicio_t) * 1000
