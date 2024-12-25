from src.database.service import OrderDetailsService, LoginHistoryService, UserDetailsService, UserBankAccountService, FillsService
from .report_service import ReportService
from src.util import logger, DateTimeUtil

import os
import traceback
import requests

class ProductDetailsService:

    @staticmethod
    def generate_product_details():
        products = ProductDetailsService.__get_products()   
        products_compass = ProductDetailsService.__convert_to_compass_format(products)
        ReportService.write_report('PrdouctCode Details', products_compass)
        products_count = len(products_compass)
        logger.info(f'generated product details for {products_count}')  

    @staticmethod
    def __get_products():
        api_base_url = os.getenv('DELTA_EXCHANGE_API_BASE_URL')
        products_response = requests.get(url = f'{api_base_url}/v2/products', headers={'accept': 'application/json'})
        products = products_response.json().get('result')
        return products          
        

    @staticmethod
    def __convert_to_compass_format(products):
        return list(map(lambda product: {
            "SCRIPCODE": product.get("id"),
            "SCRIPNAME": product.get("symbol"),
            "ISSUEDCAPITAL": None,
        }, products))
    