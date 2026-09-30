"""Utilidades compartidas por todos los algoritmos de búsqueda."""
from dataclasses import dataclass
from typing import Dict, List, Optional, Set

from app.exceptions import NegativeWeightError

Graph = Dict[str, Dict[str, float]]


@dataclass(frozen=True)
class RouteResult:
    """Resultado interno común de cualquier algoritmo de búsqueda."""

    ruta: List[str]
    costo_total: float


def neighbors(grafo: Graph, nodo: str) -> Dict[str, float]:
    """Vecinos salientes de ``nodo`` (grafo dirigido). Un nodo sin clave no tiene salidas."""
    return grafo.get(nodo, {})


def all_nodes(grafo: Graph) -> Set[str]:
    """Todos los nodos: claves del grafo y nodos que solo aparecen como destino."""
    nodos: Set[str] = set(grafo)
    for destinos in grafo.values():
        nodos.update(destinos)
    return nodos


def reconstruct_path(
    padres: Dict[str, Optional[str]], inicio: str, objetivo: str
) -> List[str]:
    """Reconstruye la ruta ``inicio -> objetivo`` siguiendo los predecesores."""
    ruta: List[str] = []
    actual: Optional[str] = objetivo
    while actual is not None:
        ruta.append(actual)
        actual = padres[actual]
    ruta.reverse()
    if ruta[0] != inicio:  # protección: nunca debería ocurrir
        raise ValueError("Los predecesores no conducen al nodo inicial.")
    return ruta


def calculate_path_cost(grafo: Graph, ruta: List[str]) -> float:
    """Suma los pesos de las aristas recorridas (no la cantidad de nodos)."""
    return float(
        sum(grafo[origen][destino] for origen, destino in zip(ruta, ruta[1:]))
    )


def validate_non_negative_weights(grafo: Graph) -> None:
    """Lanza ``NegativeWeightError`` si alguna arista tiene peso negativo."""
    for origen, destinos in grafo.items():
        for destino, peso in destinos.items():
            if peso < 0:
                raise NegativeWeightError(
                    f"Peso negativo en la arista {origen} -> {destino} ({peso}). "
                    "Este algoritmo requiere pesos no negativos."
                )
