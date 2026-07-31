from sqlalchemy.orm import Session
from uuid import UUID


def validate_run_scan(
    db: Session,
    asset_id: UUID,
    profile: str = "quick",
) -> None:
    """Punto de extensión para validaciones previas al escaneo."""


def validate_scan_result(result: dict) -> None:
    """Punto de extensión para validar el resultado del scanner."""


def validate_before_delete(scan) -> None:
    """Punto de extensión para validaciones previas a eliminar un scan."""


def validate_before_vulnerability_processing(
    created_ports,
) -> None:
    """Punto de extensión antes de correlacionar vulnerabilidades."""
