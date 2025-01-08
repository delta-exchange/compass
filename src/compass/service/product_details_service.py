from src.database.service import ProductService
from .report_service import ReportService
from src.util import logger

class ProductDetailsService:

    @staticmethod
    def generate_product_details():
        products = []
        batch = 1
        while(True):
            logger.info(f'fetching products batch {batch}')
            products_batch = ProductService.get_batch_by_created_at(batch)
            if len(products_batch) == 0:
                break
            products += products_batch
            batch += 1   
        products_compass = ProductDetailsService.__convert_to_compass_format(products)
        ReportService.write_report('ProductCode Details', products_compass)
        products_count = len(products_compass)
        logger.info(f'generated product details for {products_count}')

    @staticmethod
    def __convert_to_compass_format(products):
        return list(map(lambda product: {
            "SCRIPCODE": product.id,
            "SCRIPNAME": product.symbol,
            "ISSUEDCAPITAL": None,
        }, products))
    