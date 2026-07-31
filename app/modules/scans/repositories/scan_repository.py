from datetime import datetime

from app.modules.scans.model import Scan


def create_scan(db, asset, profile):
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


def update_scan_command_xml_file(db, scan, command, xml_file):
    scan.command = command
    scan.xml_file = xml_file

    db.commit()


def mark_scan_failed(db, scan):
    scan.status = "failed"
    scan.finished_at = datetime.utcnow()

    db.commit()
    db.refresh(scan)


def mark_scan_completed(db, scan):
    scan.status = "completed"
    scan.finished_at = datetime.utcnow()

    scan.duration = int(
        (scan.finished_at - scan.started_at).total_seconds()
    )

    db.commit()

    db.refresh(scan)