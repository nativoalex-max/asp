"""Repositorio para persistencia de puertos asociados a un Scan."""

from typing import Any

from sqlalchemy.orm import Session

from app.modules.scans.model import Scan
from app.modules.scans.port_model import ScanPort


def create_scan_ports(
    db: Session,
    scan: Scan,
    hosts: list[dict[str, Any]],
) -> tuple[list[ScanPort], int]:
    """Crear y persistir puertos descubiertos para un scan.

    Args:
        db: Sesion activa de SQLAlchemy.
        scan: Scan al que se asocian los puertos.
        hosts: Hosts parseados desde el resultado del scanner.

    Returns:
        Tupla con la lista de puertos creados y el total de puertos.
    """
    total_ports = 0
    created_ports = []

    for host in hosts:

        for port in host["ports"]:

            db_port = ScanPort(
                scan_id=scan.id,
                port=port["port"],
                protocol=port["protocol"],
                state=port["state"],
                service=port.get("service"),
                product=port.get("product"),
                version=port.get("version"),
                extra_info=port.get("extra_info"),
                cpe=port.get("cpe"),
            )

            db.add(db_port)
            created_ports.append(db_port)

            total_ports += 1

    db.flush()

    return created_ports, total_ports