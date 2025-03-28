from flask import Flask
from dotenv import load_dotenv, find_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from src.compass.service import CompassGenerator, CompassMasterGenerator
import os

load_dotenv(find_dotenv(), override=True)

scheduler = BackgroundScheduler()
scheduler.add_job(CompassGenerator.start, CronTrigger(hour="16", minute="30"), kwargs={"date": None})
# if os.getenv("MASTER_DUMP_CRON_ENABLED"):
#     scheduler.add_job(CompassMasterGenerator.start, CronTrigger(hour="5", minute="00"))
scheduler.start()

app = Flask(__name__)

if __name__ == "__main__":
    try:
        app.run(debug=True)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
