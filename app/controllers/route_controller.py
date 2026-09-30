"""Controller HTTP: único endpoint de negocio ``POST /api/ruta``."""
from fastapi import APIRouter, Depends, HTTPException

from app.exceptions import GraphSearchError, NoRouteError
from app.models.route_models import RouteRequest, RouteResponse
from app.services.route_service import RouteService

router = APIRouter(prefix="/api", tags=["Rutas"])


def get_route_service() -> RouteService:
    """Dependencia que provee el ``RouteService`` (sobrescribible en pruebas)."""
    return RouteService()


@router.post(
    "/ruta",
    response_model=RouteResponse,
    summary="Calcula una ruta con BFS, DFS, A* o Dijkstra",
    responses={
        404: {"description": "No existe ruta entre estadoInicial y estadoFinal."},
        422: {"description": "Request inválido (nodo inexistente, peso negativo, grafo vacío, ...)."},
    },
)
def calcular_ruta(
    request: RouteRequest,
    route_service: RouteService = Depends(get_route_service),
) -> RouteResponse:
    """Ejecuta el algoritmo indicado y devuelve ruta, costo total y tiempo (ms)."""
    try:
        resultado, tiempo_ms = route_service.ejecutar(
            request.tipoRuta, request.grafo, request.estadoInicial, request.estadoFinal
        )
    except NoRouteError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    except GraphSearchError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error

    return RouteResponse(
        algoritmo=request.tipoRuta,
        ruta=resultado.ruta,
        costoTotal=resultado.costo_total,
        tiempoEjecucionMs=round(tiempo_ms, 6),
    )
