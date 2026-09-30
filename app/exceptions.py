"""Excepciones de dominio de la aplicación."""


class GraphSearchError(Exception):
    """Error base para cualquier problema de búsqueda sobre el grafo (HTTP 422 por defecto)."""


class InvalidGraphError(GraphSearchError):
    """El grafo recibido no es válido (por ejemplo, está vacío)."""


class NodeNotFoundError(GraphSearchError):
    """Un nodo solicitado no existe en el grafo."""


class NegativeWeightError(GraphSearchError):
    """El grafo contiene pesos negativos y el algoritmo no los admite."""


class NoRouteError(GraphSearchError):
    """No existe ruta entre los nodos solicitados (HTTP 404)."""

    def __init__(self, inicio: str, objetivo: str) -> None:
        super().__init__(
            f"No existe una ruta entre estadoInicial ('{inicio}') "
            f"y estadoFinal ('{objetivo}')."
        )
