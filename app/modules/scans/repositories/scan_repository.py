"""Repositorio para operaciones de persistencia de la entidad Scan."""

from datetime import datetime

from sqlalchemy.orm import Session

from app.modules.assets.model import Asset
from app.modules.scans.model import Scan


def create_scan(db: Session, asset: Asset, profile: str) -> Scan:
    """Crear y persistir un scan en estado running.

    Args:
        db: Sesion activa de SQLAlchemy.
        asset: Asset objetivo del escaneo.
        profile: Perfil de escaneo.

    Returns:
        Instancia del scan creada y refrescada.
    """
    scan = Scan(
        asset_id=asset.id,
        scanner="nmap",
        target=asset.ip_address,
        profile=profile,
        status="running",
        started_at=datetime.utcnow(),
    )

    db.add(scan)
    db.commit()
    db.refresh(scan)

    return scan


def update_scan_command_xml_file(
    db: Session,
    scan: Scan,
    command: str,
    xml_file: str,
) -> None:
    """Persistir metadatos tecnicos del resultado del scanner.

    Args:
        db: Sesion activa de SQLAlchemy.
        scan: Scan persistido a actualizar.
        command: Comando ejecutado por el scanner.
        xml_file: Ruta del archivo XML generado.
    """
    scan.command = command
    scan.xml_file = xml_file

    db.commit()


def mark_scan_failed(db: Session, scan: Scan) -> None:
    """Marcar un scan como failed y persistir el estado.

    Args:
        db: Sesion activa de SQLAlchemy.
        scan: Scan persistido a actualizar.
    """
    scan.status = "failed"
    scan.finished_at = datetime.utcnow()

    db.commit()
    db.refresh(scan)


def mark_scan_completed(db: Session, scan: Scan) -> None:
    """Marcar un scan como completed y persistir su duracion.

    Args:
        db: Sesion activa de SQLAlchemy.
        scan: Scan persistido a actualizar.
    """
    scan.status = "completed"
    scan.finished_at = datetime.utcnow()

    scan.duration = int(
        (scan.finished_at - scan.started_at).total_seconds()
    )

    db.commit()

    db.refresh(scan)