import os
import shutil
from src.util import DateTimeUtil, logger
from datetime import datetime, timedelta

class ReportsCleaner:

    @staticmethod
    def clean_older_reports():
        cutoff_date = datetime.today() - timedelta(days=33)

        reports_directory = os.path.join(os.getcwd(), 'reports')
        directory_list = os.listdir(reports_directory)
        for directory in directory_list:
            directory_path = os.path.join(reports_directory, directory)
            directory_date = datetime.strptime(directory, '%d%m%Y')
            if os.path.exists(directory_path) and directory_date < cutoff_date: 
                shutil.rmtree(directory_path)
                logger.info(f'reports cleaned for date: {directory}')

    
    @staticmethod
    def clean_reports_by_date(date=None):
        if not date:
            date = DateTimeUtil.get_current_date()
        reports_directory = os.path.join(os.getcwd(), 'reports', date)
        if os.path.exists(reports_directory): 
            shutil.rmtree(reports_directory)
            logger.info(f'reports cleaned for date: {date}')
        else:
            logger.error(f'reports not found for date: {date}')