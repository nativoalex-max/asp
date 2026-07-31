from sqlalchemy.orm import Session

from app.modules.discovery.services.orchestration_service import run_discovery_service


def run_discovery(
    db: Session,
    client_id,
    target: str,
    profile: str = "quick",
):
    return run_discovery_service(
        db=db,
        client_id=client_id,
        target=target,
        profile=profile,
    )
