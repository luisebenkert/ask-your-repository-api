from apscheduler.schedulers.background import BackgroundScheduler

from .teams.placeholder_drives.drive import Drive


def add_background_jobs(app):
    sync_scheduler = BackgroundScheduler(deamon=False)

    for drive in Drive.all():
        drive.update(is_syncing=False)

    def sync_with_context():
        with app.app_context():
            print("syncing drives")
            Drive.sync_all()
            print("done")

    sync_scheduler.add_job(sync_with_context, "interval", seconds=5)
    if app.config["START_DRIVE_SYNC_WORKER"]:
        sync_scheduler.start()
    app.sync_scheduler = sync_scheduler
