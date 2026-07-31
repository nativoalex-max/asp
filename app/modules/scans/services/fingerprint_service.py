"""Servicio para procesar fingerprints de puertos de un scan."""

from sqlalchemy.orm import Session

from app.modules.scans.port_model import ScanPort
from app.services.fingerprint.service import save_fingerprint


def process_fingerprints(
    db: Session,
    created_ports: list[ScanPort],
) -> None:
    for port in created_ports:
        save_fingerprint(
            db=db,
            scan_port=port,
        )