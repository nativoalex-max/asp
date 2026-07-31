from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Session

from app.modules.assets.service import get_asset_by_id
from app.modules.scans.model import Scan
from app.modules.scans.port_model import ScanPort
from app.modules.vulnerabilities.model import Vulnerability
from app.services.fingerprint.service import save_fingerprint
from app.parsers.nmap_parser import NmapParser
from app.scanners.nmap import NmapScanner
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

    scanner = NmapScanner()

    result = scanner.scan(
        target=asset.ip_address,
        profile=profile,
    )

    print(">>> NMAP FINALIZADO")
    print(result)

    scan.command = result["command"]
    scan.xml_file = result["xml_file"]

    db.commit()

    if not result["success"]:
        scan.status = "failed"
        scan.finished_at = datetime.utcnow()

        db.commit()
        db.refresh(scan)

        return scan

    hosts = NmapParser.parse(result["xml_file"])

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

    scan.status = "completed"
    scan.finished_at = datetime.utcnow()

    scan.duration = int(
        (scan.finished_at - scan.started_at).total_seconds()
    )

    db.commit()

    db.refresh(scan)

    return {
        "scan": scan,
        "ports": total_ports,
        "vulnerabilities": len(findings),
    }