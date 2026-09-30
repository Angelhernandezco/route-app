"""Modelos Pydantic de request y response."""
import math
from typing import Dict, List, Literal

from pydantic import BaseModel, ConfigDict, StrictFloat, field_validator


class RouteRequest(BaseModel):
    """Solicitud de búsqueda de ruta sobre un grafo dirigido ponderado."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "tipoRuta": "Dijkstra",
                "grafo": {
                    "A": {"B": 4, "C": 2},
                    "B": {"A": 4, "D": 5, "E": 3},
                    "C": {"A": 2, "F": 6, "G": 7},
                    "D": {"B": 5},
                    "E": {"B": 3, "F": 1},
                    "F": {"C": 6, "E": 1},
                    "G": {"C": 7},
                },
                "estadoInicial": "A",
                "estadoFinal": "C",
            }
        }
    )

    tipoRuta: Literal["BFS", "DFS", "A*", "Dijkstra"]
    # StrictFloat: acepta enteros/decimales JSON, rechaza strings, null y booleanos.
    grafo: Dict[str, Dict[str, StrictFloat]]
    estadoInicial: str
    estadoFinal: str

    @field_validator("grafo")
    @classmethod
    def validar_grafo(
        cls, grafo: Dict[str, Dict[str, float]]
    ) -> Dict[str, Dict[str, float]]:
        """El grafo no puede ser vacío y los pesos deben ser finitos (sin NaN/Infinity)."""
        if not grafo:
            raise ValueError("El grafo no puede estar vacío.")
        for origen, destinos in grafo.items():
            for destino, peso in destinos.items():
                if not math.isfinite(peso):
                    raise ValueError(
                        f"Peso inválido en {origen} -> {destino}: debe ser un número finito."
                    )
        return grafo


class RouteResponse(BaseModel):
    """Resultado de la búsqueda."""

    algoritmo: str
    ruta: List[str]
    costoTotal: float
    tiempoEjecucionMs: float
