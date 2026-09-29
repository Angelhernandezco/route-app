# Route Algorithms Playground

API mínima con FastAPI para probar algoritmos de ruteo. Un solo endpoint (`POST /route`):
consulta el **OSRM Table Service** para obtener la matriz de distancias, ejecuta el algoritmo
elegido sobre esa matriz y devuelve un **GeoJSON** listo para pegar en [geojson.io](https://geojson.io).

Por ahora solo **Dijkstra** está implementado. BFS, DFS y A\* están preparados (devuelven `501`).

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Configuración

```bash
cp .env.example .env
```

Variables (todas opcionales; si no existen se usan los valores de `.env.example`):

| Variable | Descripción |
|---|---|
| `OSRM_BASE_URL` | URL base de OSRM (por defecto el servidor demo público) |
| `OSRM_PROFILE` | `driving`, `walking`, `cycling` |
| `OSRM_TIMEOUT_SECONDS` | Timeout de las peticiones a OSRM |

## Ejecutar

```bash
uvicorn app.main:app --reload --env-file .env
```

(`--env-file .env` carga tus variables; sin él se usan los valores por defecto.)

Abre **http://localhost:8000/docs**.

## Probar

1. En Swagger UI abre `POST /route` → **Try it out**.
2. Pega el body:

```json
{
  "algorithm": "Dijkstra",
  "coordinates": [
    {"lat": 25.7905, "lng": -108.9858},
    {"lat": 25.7891, "lng": -108.9870},
    {"lat": 25.7875, "lng": -108.9840}
  ]
}
```

3. Pulsa **Execute**, copia el *Response body* completo.
4. Ve a https://geojson.io y pégalo en el panel JSON de la derecha (reemplaza el contenido).

Con curl:

```bash
curl -X POST http://localhost:8000/route -H "Content-Type: application/json" \
  -d '{"algorithm":"Dijkstra","coordinates":[{"lat":25.7905,"lng":-108.9858},{"lat":25.7891,"lng":-108.9870},{"lat":25.7875,"lng":-108.9840}]}'
```

## Convenciones

- `coordinates[0]` = origen, `coordinates[-1]` = destino. No es un TSP: no se obliga a visitar todos los puntos.
- El índice de cada punto en la lista es su índice en la matriz (`matrix[i][j]` = metros de `i` a `j`).
- La ruta es una lista de índices (`[0, 3, 5, 2, 4]`); el GeoJSON se construye después con `[lng, lat]`.
- `properties.distance` (metros) se suma con la matriz de OSRM; `properties.route` guarda los índices.

## Errores

| Código | Causa |
|---|---|
| 400 | Matriz inválida (no cuadrada, costos negativos) |
| 422 | JSON inválido, menos de 2 coordenadas, o sin camino entre origen y destino |
| 501 | Algoritmo aún no implementado (BFS, DFS, A\*) |
| 502 | OSRM no responde, timeout, error HTTP, o respuesta sin `distances` |
| 500 | Error interno inesperado |

Un `null` en la matriz de OSRM significa "sin ruta entre esos dos puntos" y se trata como arista inexistente.

## Estructura

```
app/
├── main.py                  # endpoint y manejo de errores
├── config.py                # variables de entorno
├── exceptions.py            # errores de dominio → códigos HTTP
├── models/route.py          # modelos Pydantic (request y GeoJSON)
├── services/
│   ├── __init__.py          # registro Algoritmo → find_route
│   ├── osrm_service.py      # único módulo que habla con OSRM
│   ├── dijkstra_service.py  # find_route(matrix) -> [índices]
│   ├── bfs_service.py       # TODO
│   ├── dfs_service.py       # TODO
│   ├── astar_service.py     # TODO
│   └── geojson_service.py   # coordenadas + ruta -> FeatureCollection
└── algorithms/
    ├── dijkstra.py          # implementación propia (heapq)
    ├── matrix.py            # validación común de la matriz
    └── types.py
```
