from .report_service import ReportService
from src.util import logger, DateTimeUtil
import os
import requests

import traceback

class ExchangeTradesService:

    @staticmethod
    def generate_trade_volume_details():
        report_name = f"ETD{DateTimeUtil.get_current_date()}01"
        logger.info(f'generating exchange trade volume details')
        tickers = ExchangeTradesService.__get_tickers()
        tickers_compass = ExchangeTradesService.__convert_to_compass_format(tickers)
        ReportService.write_report(report_name, tickers_compass)
        logger.info(f'generated exchange trade volume details')

    @staticmethod
    def __get_tickers():
        api_base_url = os.getenv('DELTA_EXCHANGE_API_BASE_URL')
        tickers_response = requests.get(url = f'{api_base_url}/v2/tickers', headers={'accept': 'application/json'})
        tickers = tickers_response.json().get('result')
        return tickers
    
    @staticmethod
    def __convert_to_compass_format(tickers):
        return [{
            'EXCHANGECODE': 'VA00041101',
            'SCRIPTCODE': ticker.get('product_id'),
            'ORG_SCRIPTCODE': ticker.get('product_id'),
            'SCRIPTNAME': ticker.get('symbol'),
            'SCRIPTRATE': ticker.get('mark_price'),
            'COMSCRIPTCODE': None,
            'SCRIPCATID': ticker.get('contract_type'),
            'SC_GROUP': ticker.get('contract_type'),
            'SC_TYPE': ticker.get('contract_type'),
            'OPENINGPRICE': ticker.get('open'),
            'TODAYSHIGH': ticker.get('high'),
            'TODAYSLOW': ticker.get('low'),
            'DAILYSETTLPRICE': ticker.get('close'),
            'PREVIOUSCLOSE': None,
            'TOTALTRADES': None,
            'DAILYVOLUME': ticker.get('volume'),
            'DAILYVALUE': ticker.get('turnover'),
            'STRIKEPRICE': ticker.get('strike_price')
        } for ticker in tickers]