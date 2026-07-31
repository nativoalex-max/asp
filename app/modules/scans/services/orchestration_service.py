from uuid import UUID

from sqlalchemy.orm import Session

from app.modules.assets.service import get_asset_by_id
from app.modules.scans.repositories.scan_port_repository import create_scan_ports
from app.modules.scans.repositories.scan_repository import (
    create_scan,
    mark_scan_completed,
    mark_scan_failed,
    update_scan_command_xml_file,
)
from app.modules.scans.services.scan_execution_service import execute_scan
from app.modules.scans.services.vulnerability_service import process_vulnerabilities


def run_scan(
    db: Session,
    asset_id: UUID,
    profile: str = "quick",
):
    asset = get_asset_by_id(db, asset_id)

    print(">>> RUN_SCAN INICIADO")

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

    print(">>> NMAP FINALIZADO")
    print(result)

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

    print(f">>> HOSTS PARSEADOS: {len(hosts)}")

    created_ports, total_ports = create_scan_ports(
        db=db,
        scan=scan,
        hosts=hosts,
    )

    total_vulnerabilities = process_vulnerabilities(
        db=db,
        created_ports=created_ports,
    )

    print("REALIZANDO COMMIT...")

    db.commit()

    print("COMMIT OK")

    mark_scan_completed(
        db=db,
        scan=scan,
    )

    return {
        "scan": scan,
        "ports": total_ports,
        "vulnerabilities": total_vulnerabilities,
    }