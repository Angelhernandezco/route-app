# Comparador de algoritmos de búsqueda de rutas

API en **FastAPI** con **un solo endpoint de negocio** (`POST /api/ruta`) para probar
**BFS, DFS, Dijkstra y A\*** sobre un **grafo dirigido y ponderado**. Devuelve la ruta
encontrada, su costo total y el tiempo de ejecución del algoritmo. Los algoritmos están
implementados a mano (solo `deque`, `heapq`, `set` y `dict`) con fines educativos.

## Estructura

```text
app/
├── main.py                       # App FastAPI y manejo de errores 422
├── exceptions.py                 # Excepciones de dominio
├── controllers/route_controller.py   # POST /api/ruta
├── models/route_models.py        # RouteRequest / RouteResponse (Pydantic)
├── services/
│   ├── base_search_service.py    # Interfaz común de los algoritmos
│   ├── bfs_service.py  dfs_service.py  dijkstra_service.py  a_star_service.py
│   └── route_service.py          # Selecciona el algoritmo y mide el tiempo
└── algorithms/graph_utils.py     # RouteResult, reconstrucción de ruta, costo, validaciones
ejemplos/                         # JSON de prueba (10, 30 y 50 nodos)
```

Flujo: `HTTP → RouteController → RouteService → (Bfs|Dfs|Dijkstra|AStar)Service → RouteResult → RouteResponse`.

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Ejecución y Swagger

```bash
uvicorn app.main:app --reload
```

Swagger UI: **http://127.0.0.1:8000/docs** (el endpoint ya trae un ejemplo precargado:
*POST /api/ruta → Try it out → Execute*).

## Uso del endpoint

`POST /api/ruta`

```json
{
  "tipoRuta": "Dijkstra",
  "grafo": {
    "A": {"B": 4, "C": 2},
    "B": {"A": 4, "D": 5, "E": 3},
    "C": {"A": 2, "F": 6, "G": 7},
    "D": {"B": 5},
    "E": {"B": 3, "F": 1},
    "F": {"C": 6, "E": 1},
    "G": {"C": 7}
  },
  "estadoInicial": "A",
  "estadoFinal": "C"
}
```

Respuesta (el tiempo varía en cada ejecución):

```json
{ "algoritmo": "Dijkstra", "ruta": ["A", "C"], "costoTotal": 2.0, "tiempoEjecucionMs": 0.0123 }
```

`tipoRuta` admite `"BFS"`, `"DFS"`, `"A*"` y `"Dijkstra"`.

### Decisiones de diseño

* **Grafo dirigido**: `"A": {"B": 4}` NO crea `B -> A`. La inversa solo existe si se declara.
  Un nodo que solo aparece como destino (sin clave propia) existe y no tiene salidas.
* **Sin ruta → `404`** con el mensaje `No existe una ruta entre estadoInicial ('X') y estadoFinal ('Y').`
* **Validaciones → `422`**: nodo inicial/final inexistente, grafo vacío, pesos `null`, strings,
  booleanos, `NaN`, `Infinity`, `tipoRuta` desconocido, y pesos negativos con Dijkstra/A\*
  (BFS y DFS sí los aceptan, pues no usan los pesos para decidir).
* **Inicio = final** → `{"ruta": ["A"], "costoTotal": 0}`.
* **Tiempo**: `time.perf_counter()` alrededor de la llamada al algoritmo únicamente
  (la validación de request, de nodos y de pesos negativos se hace antes del cronómetro;
  la serialización, después).
* `costoTotal` es el costo **de la ruta que encontró ese algoritmo**, no el mínimo global.

## Ejemplos sobre el grafo anterior

| Caso | BFS | DFS | Dijkstra | A\* (h=0) |
|------|-----|-----|----------|-----------|
| `A -> C` | `[A,C]` costo 2 | `[A,B,E,F,C]` costo **14** | `[A,C]` costo 2 | `[A,C]` costo 2 |
| `A -> G` | `[A,C,G]` costo 9 | `[A,B,E,F,C,G]` costo **21** | `[A,C,G]` costo 9 | `[A,C,G]` costo 9 |
| `A -> F` | `[A,C,F]` costo 8 | `[A,B,E,F]` costo 8 | `[A,C,F]` costo 8 | `[A,C,F]` costo 8 |
| `A -> A` | `[A]` costo 0 | `[A]` costo 0 | `[A]` costo 0 | `[A]` costo 0 |

(En `A -> F` hay empate de costo 8 entre `A,C,F` y `A,B,E,F`; ambos son óptimos.)
Para probar el error 404, agrega un nodo aislado, p. ej. `"H": {}` y pide `A -> H`.

## Grafos de prueba (`ejemplos/`)

Tres requests listos para pegar en Swagger (`POST /api/ruta`), todos dirigidos, con pesos
enteros entre 1 y 20 y con ruta garantizada entre el primer y el último nodo:

| Archivo | Nodos | Aristas | Inicio → Final |
|---------|-------|---------|----------------|
| `ejemplos/grafo_10_nodos.json` | 10 (`A`–`J`) | 30 | `A → J` |
| `ejemplos/grafo_30_nodos.json` | 30 (`N01`–`N30`) | 111 | `N01 → N30` |
| `ejemplos/grafo_50_nodos.json` | 50 (`N01`–`N50`) | 175 | `N01 → N50` |

Vienen con `"tipoRuta": "Dijkstra"`; cambia ese campo para comparar algoritmos. Costos obtenidos:

| Archivo | BFS | DFS | Dijkstra / A\* |
|---------|-----|-----|----------------|
| 10 nodos | 26 (2 aristas) | 122 (9 aristas) | 26 |
| 30 nodos | 46 (3 aristas) | 334 (29 aristas) | **33** (4 aristas) |
| 50 nodos | 26 (2 aristas) | 629 (49 aristas) | 26 |

El de 30 nodos muestra que BFS (menos aristas) no coincide con el menor costo, y en los tres
DFS devuelve rutas muy largas y caras.

Desde la terminal:

```bash
curl -X POST http://127.0.0.1:8000/api/ruta -H "Content-Type: application/json" \
     -d @ejemplos/grafo_30_nodos.json
```

## Los algoritmos

**BFS (anchura).** Usa una cola FIFO y explora por niveles: primero los vecinos a 1 arista,
luego a 2, etc. Guarda visitados y predecesores, y se detiene al descubrir el objetivo.
Devuelve la ruta con **menos aristas**.

**DFS (profundidad).** Usa una pila explícita: avanza por un camino hasta el fondo y
retrocede al quedarse sin salida. Devuelve la **primera** ruta que encuentra (los vecinos se
exploran en el orden declarado en el JSON). No es una búsqueda exhaustiva de rutas.

**Dijkstra.** Usa un min-heap ordenado por distancia acumulada. Extrae siempre el nodo con
menor distancia conocida, relaja sus aristas (`dist[u] + w < dist[v]`) y se detiene cuando el
objetivo es **extraído** del heap, momento en que su distancia ya es definitiva.

**A\*.** Como Dijkstra, pero el heap se ordena por `f(n) = g(n) + h(n)`:

* `g(n)`: costo acumulado desde el origen hasta `n`.
* `h(n)`: estimación del costo restante de `n` al objetivo.
* `f(n)`: prioridad del nodo.

### Buscar por aristas vs. por costo

BFS mide la distancia en **número de aristas** (todas valen lo mismo). Dijkstra/A\* miden la
distancia en **suma de pesos**. Con pesos iguales coinciden; con pesos distintos no.
Ejemplo: `A -> D` directo cuesta 10 (1 arista), pero `A -> B -> C -> D` cuesta 3 (3 aristas).
BFS elige la primera; Dijkstra, la segunda.

### Por qué BFS y DFS no garantizan costo mínimo

BFS minimiza aristas, no pesos, así que una ruta corta en aristas puede ser cara. DFS ni
siquiera minimiza aristas: devuelve la primera ruta hallada, que depende del orden de
exploración (en `A -> G` devuelve costo 21 frente al óptimo 9).

### Por qué Dijkstra necesita pesos no negativos

Dijkstra asume que, al extraer un nodo con distancia mínima, ninguna ruta posterior puede
mejorarla, porque agregar aristas nunca reduce el costo. Con una arista negativa eso falla:
un camino más largo podría terminar siendo más barato, y un nodo ya cerrado tendría que
reabrirse. Por eso el servicio rechaza pesos negativos (A\* con `h=0` hereda la restricción).

### Por qué A\* usa `f(n) = g(n) + h(n)`

`g` refleja lo ya recorrido (como Dijkstra) y `h` orienta la búsqueda hacia el objetivo, de
modo que se expanden primero los nodos que parecen llevar a la meta con menor costo total.
Si `h` es **admisible** (nunca sobreestima) y consistente, A\* encuentra la ruta óptima
expandiendo normalmente menos nodos que Dijkstra.

### Por qué la versión inicial usa `h(n) = 0`

El request solo trae nodos y costos de aristas: no hay coordenadas ni información para
estimar distancias, y inventar una heurística a partir de los nombres de los nodos sería
incorrecto. `h(n)=0` es trivialmente admisible y consistente, así que `f(n)=g(n)` y A\*
conserva la optimalidad de Dijkstra. La arquitectura queda lista para una heurística real:

```python
AStarService(heuristica=lambda actual, final: distancia_euclidiana(actual, final))
# o bien subclasificar AStarService y sobrescribir heuristic(nodo_actual, nodo_final)
```

## Complejidad (V = nodos, E = aristas)

| Algoritmo | Tiempo | Espacio | Óptimo en costo |
|-----------|--------|---------|-----------------|
| BFS | O(V + E) | O(V) | No (sí en nº de aristas) |
| DFS | O(V + E) | O(V + E) (la pila puede acumular hasta E entradas) | No |
| Dijkstra (heap) | O((V + E) log V) | O(V + E) por entradas duplicadas en el heap | Sí (pesos ≥ 0) |
| A\* | Peor caso O((V + E) log V); depende de la heurística | O(V + E) | Sí, con heurística admisible |
