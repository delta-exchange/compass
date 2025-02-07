from src.database.service import LoginHistoryService
from .report_service import ReportService
from src.util import logger, DateTimeUtil

import traceback

class CustomerLoginDetailsService:

    @staticmethod
    def generate_customer_login_details(from_time):
        report_name = f"CLD{DateTimeUtil.get_current_date()}01"
        try:
            batch, login_histories_count = 1, 0
            while True:
                logger.info(f'generating customer login details for batch {batch}')

                login_histories = LoginHistoryService.get_batch_since(batch, from_time)
                if len(login_histories) == 0: break

                ReportService.write_report(report_name, CustomerLoginDetailsService.convert_to_compass_format(login_histories))
                batch += 1
                login_histories_count += len(login_histories)
            logger.info(f'generated customer login details for {login_histories_count} login histories')
        except Exception as exception:
            logger.error(f'failed to generate customer login details: {exception}')
            traceback.print_exc()

    @staticmethod
    def convert_to_compass_format(login_histories):
        login_histories_compass = []
        for login in login_histories:
            city, state, country = CustomerLoginDetailsService.get_city_state_country(login.location)
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
    
    @staticmethod
    def get_city_state_country(location):
        if location is None:
            return None, None, None
        location = location.split(',')
        city, state, country = location[0].strip(), location[1].strip(), location[2].strip()
        return city, state, country