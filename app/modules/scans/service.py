from uuid import UUID

from sqlalchemy.orm import Session

from app.modules.scans.model import Scan
from app.modules.scans.services.orchestration_service import run_scan as run_scan_service


def get_scan(db: Session, scan_id: UUID):
    return db.query(Scan).filter(Scan.id == scan_id).first()


def list_scans(db: Session):
    return db.query(Scan).order_by(Scan.started_at.desc()).all()


def delete_scan(db: Session, scan: Scan):
    db.delete(scan)
    db.commit()


def run_scan(
    db: Session,
    asset_id: UUID,
    profile: str = "quick",
):
    return run_scan_service(
        db=db,
        asset_id=asset_id,
        profile=profile,
    )
