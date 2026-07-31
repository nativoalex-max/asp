def update_total_hosts(db, job, hosts):
    job.total_hosts = len(hosts)
    db.commit()
    db.refresh(job)