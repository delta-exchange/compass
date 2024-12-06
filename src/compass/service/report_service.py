import csv
import os

from src.util import logger, DateTimeUtil

class ReportService:

    @staticmethod
    def write_report(name, content):
        logger.info(f'writing report content into {name}.csv & content size: {len(content)}')
        report_path = os.path.join(os.getcwd(), 'reports', DateTimeUtil.get_current_date() , f'{name}.csv')
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        if len(content) == 0:
            return
        columns = list(content[0].keys())
        with open(report_path, "a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=columns)
            if file.tell() == 0:
                writer.writeheader()
            writer.writerows(content) 
