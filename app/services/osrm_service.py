"""Único módulo que conoce OSRM.

- Table Service  -> matriz de distancias (la usan los algoritmos).
- Route Service  -> SOLO la geometría de calles para dibujar la ruta que el algoritmo ya eligió.
"""
from typing import Any

import httpx

from app import config
from app.algorithms.types import DistanceMatrix, Route
from app.exceptions import OSRMError
from app.models import Coordinate


def _coords_path(coordinates: list[Coordinate]) -> str:
    # OSRM espera "lng,lat" separados por ";"
    return ";".join(f"{c.lng},{c.lat}" for c in coordinates)


async def _get_json(path: str, params: dict[str, str]) -> dict[str, Any]:
    """GET a OSRM con manejo común de errores de red, HTTP y JSON."""
    url = f"{config.OSRM_BASE_URL}{path}"
    try:
        async with httpx.AsyncClient(timeout=config.OSRM_TIMEOUT_SECONDS) as client:
            response = await client.get(url, params=params)
    except httpx.TimeoutException as exc:
        raise OSRMError("Timeout al conectar con OSRM.") from exc
    except httpx.RequestError as exc:
        raise OSRMError(f"No se pudo conectar con OSRM: {exc.__class__.__name__}") from exc

    try:
        data = response.json()
    except ValueError as exc:
        raise OSRMError(f"OSRM devolvió una respuesta que no es JSON (HTTP {response.status_code}).") from exc

    if response.status_code != 200 or not isinstance(data, dict) or data.get("code") != "Ok":
        detail = (data.get("message") or data.get("code")) if isinstance(data, dict) else None
        raise OSRMError(f"OSRM respondió con error (HTTP {response.status_code}): {detail or 'sin detalle'}")
    return data


# ---------------- Table Service ----------------
def _parse_distances(data: dict, expected_size: int) -> DistanceMatrix:
    distances = data.get("distances")
    if distances is None:
        raise OSRMError("La respuesta de OSRM no contiene la matriz 'distances'.")
    if not isinstance(distances, list) or len(distances) != expected_size:
        raise OSRMError("La matriz 'distances' de OSRM no tiene el tamaño esperado.")

    matrix: DistanceMatrix = []
    for i, row in enumerate(distances):
        if not isinstance(row, list) or len(row) != expected_size:
            raise OSRMError(f"La fila {i} de 'distances' no tiene el tamaño esperado.")
        parsed: list[float | None] = []
        for j, value in enumerate(row):
            if value is None:
                # null = OSRM no encontró ruta entre i y j. Se conserva como "sin arista".
                parsed.append(None)
            elif isinstance(value, (int, float)) and not isinstance(value, bool):
                parsed.append(float(value))
            else:
                raise OSRMError(f"Valor inválido en distances[{i}][{j}]: {value!r}")
        matrix.append(parsed)
    return matrix


async def get_distance_matrix(coordinates: list[Coordinate]) -> DistanceMatrix:
    """Table Service: matriz de distancias (metros) entre todos los puntos."""
    path = f"/table/v1/{config.OSRM_PROFILE}/{_coords_path(coordinates)}"
    data = await _get_json(path, {"annotations": "distance"})
    return _parse_distances(data, expected_size=len(coordinates))


# ---------------- Route Service (solo geometría) ----------------
async def get_route_geometry(coordinates: list[Coordinate], route: Route) -> list[list[float]]:
    """Geometría real de calles [[lng, lat], ...] pasando por los puntos de `route`, en ese orden.

    El orden lo decide el algoritmo; OSRM solo dibuja el trazado entre puntos consecutivos.
    """
    waypoints = [coordinates[i] for i in route]
    path = f"/route/v1/{config.OSRM_PROFILE}/{_coords_path(waypoints)}"
    data = await _get_json(path, {"overview": "full", "geometries": "geojson", "steps": "false"})

    try:
        geometry = data["routes"][0]["geometry"]
        line = geometry["coordinates"]
    except (KeyError, IndexError, TypeError) as exc:
        raise OSRMError("La respuesta de OSRM Route no contiene 'routes[0].geometry.coordinates'.") from exc

    if not isinstance(line, list) or len(line) < 2 or not all(isinstance(p, list) and len(p) >= 2 for p in line):
        raise OSRMError("La geometría devuelta por OSRM Route es inválida.")
    return [[float(p[0]), float(p[1])] for p in line]
