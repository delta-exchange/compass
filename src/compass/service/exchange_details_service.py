from .report_service import ReportService
from src.util import logger, DateTimeUtil

import traceback

class ExchangeDetailsService:

    @staticmethod
    def generate_exchange_details():
        report_name = f"EXD{DateTimeUtil.get_current_date()}01"
        logger.info(f'generating exchange details')
        exchange_details = [{
            'EXCHANGECODE': 'VA00041101',
            'MARKETTYPE': 'Cryptocurrency Derivatives Trading',
            'MARKETNAME': 'Cryptocurrency Derivatives Trading',
            'DESCRIPTION': 'Crypto derivatives trading, including futures, options, and indices'
        }]
        ReportService.write_report(report_name, exchange_details)
        logger.info(f'generated exchange details')
