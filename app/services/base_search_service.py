"""Clase base común de los services de búsqueda."""
from abc import ABC, abstractmethod

from app.utils.graph_utils import Graph, RouteResult


class SearchService(ABC):
    """Interfaz común: ``buscar(grafo, inicio, objetivo) -> RouteResult``.

    Aplica el patrón *template method*: ``buscar`` gestiona la validación y el caso
    trivial inicio == objetivo; cada subclase implementa solo ``_ejecutar``.
    """

    def validar_grafo(self, grafo: Graph) -> None:
        """Precondiciones propias del algoritmo. Por defecto no exige nada."""

    def buscar(
        self, grafo: Graph, inicio: str, objetivo: str, validar: bool = True
    ) -> RouteResult:
        """Busca una ruta de ``inicio`` a ``objetivo``.

        Args:
            grafo: grafo dirigido ponderado ``{origen: {destino: peso}}``.
            inicio: nodo inicial (debe existir).
            objetivo: nodo final (debe existir).
            validar: si es ``False`` se omite ``validar_grafo`` (el llamador ya lo
                hizo, p. ej. para no incluir la validación en la medición de tiempo).

        Raises:
            NoRouteError: si no existe ruta.
            NegativeWeightError: si el algoritmo no admite los pesos del grafo.
        """
        if validar:
            self.validar_grafo(grafo)
        if inicio == objetivo:
            return RouteResult(ruta=[inicio], costo_total=0.0)
        return self._ejecutar(grafo, inicio, objetivo)

    @abstractmethod
    def _ejecutar(self, grafo: Graph, inicio: str, objetivo: str) -> RouteResult:
        """Implementación del algoritmo (inicio != objetivo)."""
