"""Punto de entrada de la aplicación FastAPI."""
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.controllers.route_controller import router

app = FastAPI(
    title="Comparador de algoritmos de búsqueda de rutas",
    description="BFS, DFS, Dijkstra y A* sobre un grafo dirigido ponderado.",
    version="1.0.0",
)
app.include_router(router)


@app.exception_handler(RequestValidationError)
async def validation_error_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
    """Devuelve errores 422 sin eco del valor recibido.

    El handler por defecto incluye el campo ``input`` en cada error; si el valor es
    NaN/Infinity, no es serializable a JSON y la respuesta terminaría en HTTP 500.
    """
    errores = [
        {"loc": list(e["loc"]), "msg": e["msg"], "type": e["type"]} for e in exc.errors()
    ]
    return JSONResponse(status_code=422, content={"detail": errores})
