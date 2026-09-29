"""Validaciones comunes de la matriz, reutilizables por todos los algoritmos."""
from app.algorithms.types import DistanceMatrix
from app.exceptions import InvalidInputError


def validate_matrix(matrix: DistanceMatrix) -> int:
    """Verifica que la matriz sea cuadrada, con al menos 2 nodos y sin costos negativos.

    Devuelve el número de nodos.
    """
    n = len(matrix)
    if n < 2:
        raise InvalidInputError("Se necesitan al menos 2 puntos (origen y destino).")
    for i, row in enumerate(matrix):
        if len(row) != n:
            raise InvalidInputError(f"La matriz no es cuadrada: la fila {i} tiene {len(row)} columnas y se esperaban {n}.")
        for j, value in enumerate(row):
            if value is not None and value < 0:
                raise InvalidInputError(f"Costo negativo en matrix[{i}][{j}]: Dijkstra no lo admite.")
    return n
