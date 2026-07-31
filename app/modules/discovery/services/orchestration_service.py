from sqlalchemy.orm import Session

from app.modules.discovery.services.asset_service import get_or_create_asset
from app.modules.discovery.services.discovery_scan_service import execute_discovery_scan
from app.modules.discovery.job_service import (
    create_job,
    finish_job,
    fail_job,
    update_progress,
)
from app.modules.scans.service import run_scan


def run_discovery_service(
    db: Session,
    client_id,
    target: str,
    profile: str = "quick",
):
    job = create_job(
        db=db,
        target=target,
        profile=profile,
    )

    try:

        hosts = execute_discovery_scan(
            target=target,
            profile=profile,
        )

        print("=" * 60)
        print(f"DISCOVERY: Hosts encontrados: {len(hosts)}")
        print("=" * 60)

        job.total_hosts = len(hosts)
        db.commit()
        db.refresh(job)

        created = 0
        existing = 0
        scans = []

        total_hosts = len(hosts)

        for index, host in enumerate(hosts, start=1):

            ip = host["ip"]

            print(f"Procesando host {index}/{total_hosts}: {ip}")

            update_progress(
                db=db,
                job=job,
                processed=index,
                total=total_hosts,
                current_host=ip,
            )

            asset, created, existing = get_or_create_asset(
                db=db,
                client_id=client_id,
                host=host,
                ip=ip,
                created=created,
                existing=existing,
            )

            scan = run_scan(
                db=db,
                asset_id=asset.id,
                profile=profile,
            )

            scans.append(scan)

        finish_job(
            db=db,
            job=job,
        )

        return {
            "job_id": str(job.id),
            "hosts": total_hosts,
            "created_assets": created,
            "existing_assets": existing,
            "scans": scans,
        }

    except Exception as ex:

        print(f"ERROR DISCOVERY: {ex}")

        fail_job(
            db=db,
            job=job,
        )

        raise
