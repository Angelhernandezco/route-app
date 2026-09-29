"""Construye el GeoJSON de salida a partir de la ruta y la geometría ya calculada."""
from app.algorithms.types import DistanceMatrix, Route
from app.models import Algorithm


def build_route_geojson(
    algorithm: Algorithm,
    route: Route,
    distance_matrix: DistanceMatrix,
    line_coordinates: list[list[float]],
    execution_time_ms: float,
) -> dict:
    """`line_coordinates` ya viene en formato GeoJSON: [[lng, lat], ...]."""
    total = sum(distance_matrix[a][b] for a, b in zip(route, route[1:]))  # type: ignore[misc]
    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {
                    "algorithm": algorithm.value,
                    "distance": round(total, 2),  # suma de la matriz OSRM (metros)
                    "route": route,               # índices originales, útil para depurar
                    "execution_time_ms": round(execution_time_ms, 4),  # solo el algoritmo, sin OSRM
                },
                "geometry": {"type": "LineString", "coordinates": line_coordinates},
            }
        ],
    }
