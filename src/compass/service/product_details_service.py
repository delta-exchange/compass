from src.database.service import ProductService
from .report_service import ReportService
from src.util import logger, DateTimeUtil, get_report_index

class ProductDetailsService:

    @staticmethod
    def generate_product_details(from_time, to_time):
        current_date = DateTimeUtil.get_current_date()
        logger.info(f'generating product details')
        total_count = 0
        while True:
            report_name = f"PRD{current_date}" + get_report_index(total_count, 100000)
            products = ProductService.get_between(from_time, to_time, batch_size=10000)
            products_count = len(products)
            if products_count == 0: 
                break
            else:
                from_time = products[-1].updated_at
                total_count += len(products)
                
                products_compass = ProductDetailsService.convert_to_compass_format(products)
                ReportService.write_report(report_name, products_compass)
                
        logger.info(f'generated total {total_count} product details')

    @staticmethod
    def convert_to_compass_format(products):
        return list(map(lambda product: {
            "SCRIPCODE": product.id,
            "SCRIPNAME": product.symbol,
            "ISSUEDCAPITAL": None,
        }, products))
    