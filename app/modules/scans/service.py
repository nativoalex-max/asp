"""Servicio facade del modulo Scans."""

from uuid import UUID
from typing import Any

from sqlalchemy.orm import Session

from app.modules.scans.model import Scan
from app.modules.scans.services.orchestration_service import run_scan as run_scan_service
from app.modules.scans.validators.scan_validator import (
    validate_before_delete,
)


def get_scan(db: Session, scan_id: UUID) -> Scan | None:
    """Obtener un scan por su identificador.

    Args:
        db: Sesion activa de SQLAlchemy.
        scan_id: Identificador unico del scan.

    Returns:
        Instancia del scan si existe, en caso contrario None.
    """
    return db.query(Scan).filter(Scan.id == scan_id).first()


def list_scans(db: Session) -> list[Scan]:
    """Listar scans ordenados por fecha de inicio descendente.

    Args:
        db: Sesion activa de SQLAlchemy.

    Returns:
        Lista de scans ordenados por started_at descendente.
    """
    return db.query(Scan).order_by(Scan.started_at.desc()).all()


def delete_scan(db: Session, scan: Scan) -> None:
    """Eliminar un scan persistido.

    Args:
        db: Sesion activa de SQLAlchemy.
        scan: Instancia del scan a eliminar.
    """
    validate_before_delete(scan)

    db.delete(scan)
    db.commit()


def run_scan(
    db: Session,
    asset_id: UUID,
    profile: str = "quick",
) -> Any:
    """Delegar la ejecucion del escaneo al servicio de orquestacion.

    Args:
        db: Sesion activa de SQLAlchemy.
        asset_id: Identificador del asset a escanear.
        profile: Perfil de escaneo a ejecutar.

    Returns:
        Resultado devuelto por el servicio de orquestacion.
    """
    return run_scan_service(
        db=db,
        asset_id=asset_id,
        profile=profile,
    )
