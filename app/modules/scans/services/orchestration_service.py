from uuid import UUID

from sqlalchemy.orm import Session

from app.modules.assets.service import get_asset_by_id
from app.modules.scans.port_model import ScanPort
from app.modules.scans.repositories.scan_repository import (
    create_scan,
    mark_scan_completed,
    mark_scan_failed,
    update_scan_command_xml_file,
)
from app.modules.scans.services.scan_execution_service import execute_scan
from app.modules.vulnerabilities.model import Vulnerability
from app.services.fingerprint.service import save_fingerprint
from app.services.correlation.engine import CorrelationEngine


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

    print("=" * 60)

    for port in created_ports:
        save_fingerprint(
            db=db,
            scan_port=port,
        )

    db.flush()

    for p in created_ports[:3]:
        print(
            "PORT:",
            p.port,
            "ID:",
            p.id,
            "CPE:",
            p.cpe,
        )

    print("=" * 60)

    findings = CorrelationEngine.correlate(created_ports)

    print(f"CREATED PORTS: {len(created_ports)}")
    print(f"FINDINGS: {len(findings)}")

    if findings:
        print("PRIMER SCAN_PORT_ID:", findings[0]["scan_port"].id)
        print("PRIMER CVE:", findings[0]["cve"])

    for finding in findings:

        db.add(
            Vulnerability(
                scan_port_id=finding["scan_port"].id,
                cve=finding["cve"],
                severity=finding["severity"],
                cvss=finding["cvss"],
                description=finding["description"],
                reference=finding["reference"],
                source="NVD",
            )
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
        "vulnerabilities": len(findings),
    }