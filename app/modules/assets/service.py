from uuid import UUID

from sqlalchemy.orm import Session, selectinload

from app.modules.assets.model import Asset
from app.modules.assets.schema import AssetCreate, AssetUpdate
from app.modules.scans.model import Scan
from app.modules.scans.port_model import ScanPort


def get_assets(db: Session):
    return db.query(Asset).order_by(Asset.name).all()


def get_asset_by_id(db: Session, asset_id: UUID):
    return db.query(Asset).filter(Asset.id == asset_id).first()


def get_asset_by_ip(db: Session, ip_address: str):
    return db.query(Asset).filter(Asset.ip_address == ip_address).first()


def create_asset(db: Session, asset: AssetCreate):
    db_asset = Asset(
        client_id=asset.client_id,
        name=asset.name,
        hostname=asset.hostname,
        ip_address=asset.ip_address,
        dns_name=asset.dns_name,
        mac_address=asset.mac_address,
        operating_system=asset.operating_system,
        os_version=asset.os_version,
        manufacturer=asset.manufacturer,
        model=asset.model,
        asset_type=asset.asset_type,
        environment=asset.environment,
        criticality=asset.criticality,
        owner=asset.owner,
        location=asset.location,
        description=asset.description,
        is_active=asset.is_active,
    )

    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)

    return db_asset


def update_asset(db: Session, db_asset: Asset, asset: AssetUpdate):
    data = asset.model_dump(exclude_unset=True)

    for key, value in data.items():
        setattr(db_asset, key, value)

    db.commit()
    db.refresh(db_asset)

    return db_asset


def delete_asset(db: Session, db_asset: Asset):
    db.delete(db_asset)
    db.commit()


def get_asset_drawer(db: Session, asset_id: UUID):
    asset = (
        db.query(Asset)
        .options(
            selectinload(Asset.scans)
            .selectinload(Scan.ports)
            .selectinload(ScanPort.vulnerabilities)
        )
        .filter(Asset.id == asset_id)
        .first()
    )

    if not asset:
        return None

    scans = list(asset.scans or [])

    # Determinar último scan de forma segura (evitar errores si started_at es None)
    last_scan = None
    last_ts = None

    for s in scans:
        ts = None
        if getattr(s, "started_at", None):
            ts = s.started_at
        elif getattr(s, "finished_at", None):
            ts = s.finished_at

        if ts and (last_ts is None or ts > last_ts):
            last_ts = ts
            last_scan = s

    ports: list[dict] = []
    vulnerabilities: list[dict] = []

    seen_port_ids = set()
    seen_vulns = set()
    seen_open_port_ids = set()

    critical = 0
    high = 0
    medium = 0
    low = 0

    if last_scan:
        for port in last_scan.ports:
            port_id = str(port.id)

            if port_id in seen_port_ids:
                continue

            seen_port_ids.add(port_id)

            try:
                if (port.state or "").lower() == "open":
                    seen_open_port_ids.add(port_id)
            except Exception:
                pass

            ports.append(
                {
                    "id": port_id,
                    "port": port.port,
                    "protocol": port.protocol,
                    "state": port.state,
                    "service": port.service,
                    "product": port.product,
                    "version": port.version,
                    "cpe": port.cpe,
                }
            )

            for vuln in port.vulnerabilities:
                key = (vuln.cve or "").strip()

                if not key:
                    key = str(getattr(vuln, "id", ""))

                if key in seen_vulns:
                    continue

                seen_vulns.add(key)

                vulnerabilities.append(
                    {
                        "id": str(getattr(vuln, "id", None)) if getattr(vuln, "id", None) is not None else None,
                        "cve": vuln.cve,
                        "severity": vuln.severity,
                        "cvss": float(vuln.cvss) if getattr(vuln, "cvss", None) else None,
                        "description": vuln.description,
                        "reference": vuln.reference,
                        "source": vuln.source,
                    }
                )

                severity = (vuln.severity or "").lower()

                if severity == "critical":
                    critical += 1
                elif severity == "high":
                    high += 1
                elif severity == "medium":
                    medium += 1
                elif severity == "low":
                    low += 1

    # manejar client_id None
    client_id = str(asset.client_id) if getattr(asset, "client_id", None) else None

    return {
        "asset": {
            "id": str(asset.id),
            "client_id": client_id,
            "name": asset.name,
            "hostname": asset.hostname,
            "ip_address": asset.ip_address,
            "dns_name": asset.dns_name,
            "mac_address": asset.mac_address,
            "operating_system": asset.operating_system,
            "os_version": asset.os_version,
            "manufacturer": asset.manufacturer,
            "model": asset.model,
            "asset_type": asset.asset_type,
            "environment": asset.environment,
            "criticality": asset.criticality,
            "owner": asset.owner,
            "location": asset.location,
            "description": asset.description,
            "is_active": asset.is_active,
        },
        "stats": {
            "total_scans": len(scans),
            "open_ports": len(seen_open_port_ids),
            "vulnerabilities": len(vulnerabilities),
            "critical": critical,
            "high": high,
            "medium": medium,
            "low": low,
        },
        "last_scan": {
            "id": str(last_scan.id) if last_scan else None,
            "status": last_scan.status if last_scan else None,
            "started_at": last_scan.started_at.isoformat() if last_scan and getattr(last_scan, "started_at", None) else None,
            "finished_at": last_scan.finished_at.isoformat() if last_scan and getattr(last_scan, "finished_at", None) else None,
            "duration": last_scan.duration if last_scan else None,
            "target": last_scan.target if last_scan else None,
        },
        "ports": ports,
        "vulnerabilities": vulnerabilities,
    }