from src.database.service import UserDetailsService, KycDocumentsService, LoginHistoryService
from .report_service import ReportService
from src.util import logger, DateTimeUtil, AddressUtil, get_report_index

import traceback

class CustomerDetailsService:

    @staticmethod
    def generate_customer_details_details(customer_ids):
        try:
            logger.info(f'generating customer details')
            batch_no, batch_size, total_count = 1, 10000, 0
            report_name = f"CPD{18022025}XX"
            while True:
                batch = customer_ids[(batch_no-1)*batch_size:batch_no*batch_size]
                if not batch:
                    break
                users = UserDetailsService.get_by_user_ids(batch)
                logger.info(f"Asked {len(batch)} users; Got {len(users)} users from db")
                ReportService.write_report(report_name, CustomerDetailsService.convert_to_compass_format(users))
                total_count += len(batch)
                batch_no += 1
                
            logger.info(f'generated customer details for {total_count} users')
        except Exception as exception:
            logger.error(f'failed to generate customer details: {exception}')
            traceback.print_exc()

    @staticmethod
    def convert_to_compass_format(users):
        return [{'Customer ID': user['id'],'CUSTOMER_FAMILYCODE/CUSTOMER_GROUPCODE': user['parent_user_id'] if user['parent_user_id'] else user['id']}  for user in users]