"""Servicio de orquestacion para la ejecucion de scans."""

import logging
from uuid import UUID
from typing import Any

from sqlalchemy.orm import Session

from app.modules.assets.service import get_asset_by_id
from app.modules.scans.model import Scan
from app.modules.scans.repositories.scan_port_repository import create_scan_ports
from app.modules.scans.repositories.scan_repository import (
    create_scan,
    mark_scan_completed,
    mark_scan_failed,
    update_scan_command_xml_file,
)
from app.modules.scans.services.scan_execution_service import execute_scan
from app.modules.scans.services.vulnerability_service import process_vulnerabilities
from app.modules.scans.validators.scan_validator import (
    validate_before_vulnerability_processing,
    validate_run_scan,
    validate_scan_result,
)


logger = logging.getLogger(__name__)


def run_scan(
    db: Session,
    asset_id: UUID,
    profile: str = "quick",
) -> Scan | dict[str, Any]:
    """Ejecutar el flujo completo de escaneo tecnico y correlacion.

    Args:
        db: Sesion activa de SQLAlchemy.
        asset_id: Identificador del asset a escanear.
        profile: Perfil de escaneo a ejecutar.

    Returns:
        Instancia Scan en caso de fallo o resumen del proceso completado.
    """
    validate_run_scan(
        db=db,
        asset_id=asset_id,
        profile=profile,
    )

    asset = get_asset_by_id(db, asset_id)

    logger.info(">>> RUN_SCAN INICIADO")

    if asset is None:
        raise ValueError("Activo no encontrado")

    scan = create_scan(
        db=db,
        asset=asset,
        profile=profile,
    )

    result, hosts = execute_scan(
        target=asset.ip_address,
        profile=profile,
    )

    validate_scan_result(result)

    logger.info(">>> NMAP FINALIZADO")
    logger.debug(result)

    update_scan_command_xml_file(
        db=db,
        scan=scan,
        command=result["command"],
        xml_file=result["xml_file"],
    )

    if not result["success"]:
        mark_scan_failed(
            db=db,
            scan=scan,
        )

        return scan

    logger.info(f">>> HOSTS PARSEADOS: {len(hosts)}")

    created_ports, total_ports = create_scan_ports(
        db=db,
        scan=scan,
        hosts=hosts,
    )

    validate_before_vulnerability_processing(created_ports)

    total_vulnerabilities = process_vulnerabilities(
        db=db,
        created_ports=created_ports,
    )

    logger.info("REALIZANDO COMMIT...")

    db.commit()

    logger.info("COMMIT OK")

    mark_scan_completed(
        db=db,
        scan=scan,
    )

    return {
        "scan": scan,
        "ports": total_ports,
        "vulnerabilities": total_vulnerabilities,
    }