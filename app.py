from flask import Flask
from dotenv import load_dotenv, find_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from src.compass.service import CompassGenerator, CompassMasterGenerator
import os
from datetime import datetime

load_dotenv(find_dotenv(), override=True)

scheduler = BackgroundScheduler()
target_date = datetime(2025, 2, 28, 8, 47)
scheduler.add_job(CompassMasterGenerator.start, CronTrigger(year=target_date.year, month=target_date.month, day=target_date.day, hour=target_date.hour, minute=target_date.minute, second=target_date.second))
scheduler.start()

app = Flask(__name__)

if __name__ == "__main__":
    try:
        app.run(debug=True)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
