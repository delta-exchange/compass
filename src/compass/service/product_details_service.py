from src.database.service import ProductService
from .report_service import ReportService
from src.util import logger, DateTimeUtil, get_report_index

class ProductDetailsService:

    @staticmethod
    def generate_product_details(product_ids):
        report_name = f"PRD18022025XX"
        batch_no, batch_size, total_count = 1, 1000, 0
        logger.info(f'generating product details')
        while True:
            batch = product_ids[(batch_no-1)*batch_size:batch_no*batch_size]
            if not batch:
                break
            products = ProductService.get_by_product_ids(batch)
            products_compass = ProductDetailsService.convert_to_compass_format(products)
            ReportService.write_report(report_name, products_compass)
            total_count += len(products)
            batch_no += 1
    
        logger.info(f'generated total {total_count} product details')

    @staticmethod
    def convert_to_compass_format(products):
        return list(map(lambda product: {
            "SCRIPCODE": product.id,
            "SCRIPNAME": product.symbol,
            "ISSUEDCAPITAL": None,
        }, products))
    