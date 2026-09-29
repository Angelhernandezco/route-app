"""Configuración leída de variables de entorno (con valores por defecto)."""
import os

OSRM_BASE_URL: str = os.getenv("OSRM_BASE_URL", "https://router.project-osrm.org").rstrip("/")
OSRM_PROFILE: str = os.getenv("OSRM_PROFILE", "driving")
OSRM_TIMEOUT_SECONDS: float = float(os.getenv("OSRM_TIMEOUT_SECONDS", "10"))
