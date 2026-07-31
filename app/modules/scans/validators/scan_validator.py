"""Validador para verificar reglas de negocio relacionadas con Scans."""

from uuid import UUID
from typing import Any

from sqlalchemy.orm import Session

from app.modules.scans.model import Scan
from app.modules.scans.port_model import ScanPort


def validate_run_scan(
    db: Session,
    asset_id: UUID,
    profile: str = "quick",
) -> None:
    """Punto de extension para validaciones previas al escaneo.

    Args:
        db: Sesion activa de SQLAlchemy.
        asset_id: Identificador del asset a escanear.
        profile: Perfil de escaneo a ejecutar.
    """


def validate_scan_result(result: dict[str, Any]) -> None:
    """Punto de extension para validar el resultado del scanner.

    Args:
        result: Resultado crudo devuelto por el scanner.
    """


def validate_before_delete(scan: Scan) -> None:
    """Punto de extension para validaciones previas a eliminar un scan.

    Args:
        scan: Instancia persistida del scan a eliminar.
    """


def validate_before_vulnerability_processing(
    created_ports: list[ScanPort],
) -> None:
    """Punto de extension antes de correlacionar vulnerabilidades.

    Args:
        created_ports: Lista de puertos creados para correlacion.
    """
