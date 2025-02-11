from src.database.service import LoginHistoryService
from .report_service import ReportService
from src.util import logger, DateTimeUtil

import traceback

class CustomerLoginDetailsService:

    @staticmethod
    def generate_customer_login_details(from_time, to):
        try:
            report_name = f"CLD{DateTimeUtil.get_current_date()}01"
            logger.info(f'generating customer login details into {report_name}')
            total_count = 0
            while True:
                login_histories = LoginHistoryService.get_since(from_time, to, batch_size=10000)
                login_histories_count = len(login_histories)
                if login_histories_count == 0: 
                    break
                else:
                    from_time = login_histories[-1].created_at
                    total_count += login_histories_count

                    ReportService.write_report(report_name, CustomerLoginDetailsService.convert_to_compass_format(login_histories))
                
            logger.info(f'generated total {total_count} customer login details')
        except Exception as exception:
            logger.error(f'failed to generate customer login details: {exception}')
            traceback.print_exc()

    @staticmethod
    def convert_to_compass_format(login_histories):
        login_histories_compass = []
        for login in login_histories:
            city, state, country = login.location.split(', ') if login.location else (None,)*3 
            login_histories_compass.append({
                'Customer ID': login.user_id,
                'CUSTOMERLOGIN_DATETIME': login.created_at,
                'CUSTOMERLOGIN_IPADDRESS': login.ip,
                'CUSTOMERLOGIN_ADDRESS': login.location,
                'CUSTOMERLOGIN_CITY': city,
                'CUSTOMERLOGIN_PROVINCE_OR_STATE': state,
                'CUSTOMERLOGIN_PINCODE': None,
                'CUSTOMERLOGIN_COUNTRY': country,
                'CUSTOMERLOGIN_GEOLOCATION': login.location
            })
        return login_histories_compass