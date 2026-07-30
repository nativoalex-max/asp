from apscheduler.schedulers.background import BackgroundScheduler

from app.services.nvd.updater import NVDUpdater


scheduler = BackgroundScheduler()

updater = NVDUpdater()


def start_scheduler():

    scheduler.add_job(
        updater.incremental_sync,
        trigger="cron",
        hour=2,
        minute=0,
        id="nvd_update",
        replace_existing=True,
    )

    scheduler.start()

    print("NVD Scheduler iniciado")
