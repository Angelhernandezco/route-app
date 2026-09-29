"""Excepciones de dominio. main.py las traduce a códigos HTTP."""


class AppError(Exception):
    """Base de los errores controlados de la aplicación."""

    status_code = 500

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class InvalidInputError(AppError):
    """Datos de entrada o matriz inválidos."""

    status_code = 400


class OSRMError(AppError):
    """OSRM no respondió correctamente."""

    status_code = 502


class NoRouteFoundError(AppError):
    """No existe camino entre origen y destino con la matriz dada."""

    status_code = 422


class AlgorithmNotImplementedError(AppError):
    """El algoritmo existe en la arquitectura pero aún no está implementado."""

    status_code = 501
