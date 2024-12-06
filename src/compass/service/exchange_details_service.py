from .report_service import ReportService
from src.util import logger

import traceback

class ExchangeDetailsService:

    @staticmethod
    def generate_exchange_details():
        logger.info(f'generating exchange details')
        exchange_details = [{
            'EXCHANGECODE': 'VA00041101',
            'MARKETTYPE': 'Cryptocurrency Derivatives Trading',
            'MARKETNAME': 'Cryptocurrency Derivatives Trading',
            'DESCRIPTION': 'Crypto derivatives trading, including futures, options, and indices'
        }]
        ReportService.write_report('ExchangeDetails', exchange_details)
        logger.info(f'generated exchange details')
