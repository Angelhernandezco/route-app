import logging
import time

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.exceptions import AppError
from app.models import FeatureCollection, RouteRequest
from app.services import get_route_finder, osrm_service
from app.services.geojson_service import build_route_geojson

logger = logging.getLogger("route-app")

app = FastAPI(
    title="Route Algorithms Playground",
    description="Prueba algoritmos de ruteo sobre una matriz de distancias de OSRM y devuelve GeoJSON.",
    version="0.1.0",
)


@app.exception_handler(AppError)
async def app_error_handler(_: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


@app.exception_handler(Exception)
async def unexpected_error_handler(_: Request, exc: Exception) -> JSONResponse:
    logger.exception("Error interno inesperado", exc_info=exc)
    return JSONResponse(status_code=500, content={"detail": "Error interno inesperado."})


@app.post(
    "/route",
    response_model=FeatureCollection,
    summary="Calcula una ruta y la devuelve como GeoJSON",
    responses={
        422: {"description": "Entrada inválida o sin camino entre origen y destino"},
        502: {"description": "OSRM no respondió correctamente"},
    },
)
async def route(request: RouteRequest) -> dict:
    finder = get_route_finder(request.algorithm)                           # 1. elegir algoritmo
    matrix = await osrm_service.get_distance_matrix(request.coordinates)   # 2. matriz (Table)
    start = time.perf_counter()
    indices = finder(matrix)                                               # 3. ruta como índices
    execution_time_ms = (time.perf_counter() - start) * 1000               #    (solo el algoritmo)
    line = await osrm_service.get_route_geometry(request.coordinates, indices)  # 4. calles reales (Route)
    return build_route_geojson(request.algorithm, indices, matrix, line, execution_time_ms)   # 5. GeoJSON
