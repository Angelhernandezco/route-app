"""Modelos Pydantic de entrada (request) y salida (GeoJSON)."""
from enum import Enum
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class Algorithm(str, Enum):
    BFS = "BFS"
    DFS = "DFS"
    A_STAR = "A*"
    DIJKSTRA = "Dijkstra"


class Coordinate(BaseModel):
    lat: float = Field(..., ge=-90, le=90, description="Latitud en grados (-90 a 90)", examples=[25.7905])
    lng: float = Field(..., ge=-180, le=180, description="Longitud en grados (-180 a 180)", examples=[-108.9858])


class RouteRequest(BaseModel):
    algorithm: Algorithm = Field(..., description="Algoritmo de búsqueda a utilizar")
    coordinates: list[Coordinate] = Field(
        ...,
        min_length=2,
        max_length=100,  # límite del servidor demo de OSRM
        description=(
            "Puntos en orden. El primero es el origen y el último es el destino; "
            "el índice de cada punto en esta lista es su índice en la matriz de distancias."
        ),
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "algorithm": "Dijkstra",
                "coordinates": [
                    {"lat": 25.7905, "lng": -108.9858},
                    {"lat": 25.7891, "lng": -108.9870},
                    {"lat": 25.7875, "lng": -108.9840},
                ],
            }
        }
    )


# ---- Salida: GeoJSON ----
class LineStringGeometry(BaseModel):
    type: Literal["LineString"] = "LineString"
    coordinates: list[list[float]] = Field(..., description="Lista de [longitud, latitud]")


class Feature(BaseModel):
    type: Literal["Feature"] = "Feature"
    properties: dict[str, Any]
    geometry: LineStringGeometry


class FeatureCollection(BaseModel):
    type: Literal["FeatureCollection"] = "FeatureCollection"
    features: list[Feature]
