"""Tipos compartidos por los algoritmos.

matrix[i][j] = costo (metros) de ir del punto i al punto j, donde el índice
i es la posición del punto en la lista de coordenadas original.
None = OSRM no encontró camino entre esos dos puntos (no hay arista).
"""
DistanceMatrix = list[list[float | None]]
Route = list[int]  # índices de los puntos originales, p. ej. [0, 3, 5, 2, 4]
