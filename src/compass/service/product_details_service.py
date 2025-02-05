from src.database.service import ProductService
from .report_service import ReportService
from src.util import logger, DateTimeUtil

class ProductDetailsService:

    @staticmethod
    def generate_product_details():
        report_name = f"PRD{DateTimeUtil.get_current_date()}01"
        batch, total_products = 1, 0
        while(True):
            logger.info(f'fetching products batch {batch}')
            products_batch = ProductService.get_batch_by_created_at(batch)
            if len(products_batch) == 0:
                break
            products_compass = ProductDetailsService.__convert_to_compass_format(products_batch)
            ReportService.write_report(report_name, products_compass)
            total_products += len(products_batch)
            batch += 1   

        logger.info(f'generated total {total_products} product details')

    @staticmethod
    def __convert_to_compass_format(products):
        return list(map(lambda product: {
            "SCRIPCODE": product.id,
            "SCRIPNAME": product.symbol,
            "ISSUEDCAPITAL": None,
        }, products))
    