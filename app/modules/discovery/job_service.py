from datetime import datetime

from sqlalchemy.orm import Session

from app.modules.discovery.model import DiscoveryJob


def create_job(
    db: Session,
    target: str,
    profile: str,
) -> DiscoveryJob:

    job = DiscoveryJob(
        target=target,
        profile=profile,
        status="running",
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    return job


def update_progress(
    db: Session,
    job: DiscoveryJob,
    processed: int,
    total: int,
    current_host: str,
):

    job.processed_hosts = processed
    job.total_hosts = total
    job.current_host = current_host

    db.commit()


def finish_job(
    db: Session,
    job: DiscoveryJob,
):

    job.status = "completed"
    job.finished_at = datetime.utcnow()

    if job.started_at:
        job.duration = int(
            (job.finished_at - job.started_at).total_seconds()
        )

    db.commit()


def fail_job(
    db: Session,
    job: DiscoveryJob,
):

    job.status = "failed"
    job.finished_at = datetime.utcnow()

    if job.started_at:
        job.duration = int(
            (job.finished_at - job.started_at).total_seconds()
        )

    db.commit()
