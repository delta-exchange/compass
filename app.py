from flask import Flask
from dotenv import load_dotenv, find_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from src.compass.service import CompassGenerator, CompassMasterGenerator, ReportsCleaner
import os

load_dotenv(find_dotenv(), override=True)

scheduler = BackgroundScheduler()
scheduler.add_job(CompassGenerator.start, CronTrigger(hour="0", minute="0"), kwargs={"date": None})
scheduler.add_job(ReportsCleaner.clean_older_reports, CronTrigger(hour="1", minute="0"))
scheduler.start()

app = Flask(__name__)

if __name__ == "__main__":
    try:
        app.run(debug=True)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
