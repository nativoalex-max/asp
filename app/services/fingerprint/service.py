from sqlalchemy.orm import Session

from app.models.fingerprint import Fingerprint
from app.modules.scans.port_model import ScanPort


def save_fingerprint(
    db: Session,
    scan_port: ScanPort,
):
    """
    Guarda un fingerprint asociado a un ScanPort.
    """

    confidence = 100 if scan_port.cpe else 70

    fingerprint = Fingerprint(
        scan_port_id=scan_port.id,
        source="nmap",
        vendor=None,
        product=scan_port.product,
        version=scan_port.version,
        cpe=scan_port.cpe,
        confidence=confidence,
    )

    db.add(fingerprint)

    return fingerprint
