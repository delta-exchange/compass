from src.database.service import OrderDetailsService, LoginHistoryService, UserDetailsService
from .report_service import ReportService
from src.util import logger, DateTimeUtil

import traceback

class CustomerLastTransactionDetailsService:

    @staticmethod
    def generate_last_transaction_details():
        try:
            users = LoginHistoryService.get_users_by_created_at()
            user_ids =  list(map(lambda user: user[0], users))
            batch, batch_size, last_transactions_count = 1, 100, 0
            while True:
                logger.info(f'generating customer last transaction details for batch {batch}')
                user_ids_batch = user_ids[(batch - 1) * batch_size : batch * batch_size]
                if len(user_ids_batch) == 0:
                    break

                transactions = OrderDetailsService.get_first_and_last_by_user_ids(user_ids_batch)
                transactions = list(map(lambda transaction: {'user_id': transaction[0], 'first_transaction': transaction[1], 'last_transaction': transaction[2]}, transactions))
                transactions = list(filter(lambda transaction: transaction.get('last_transaction') > DateTimeUtil.get_date_from_string(DateTimeUtil.get_24hrs_ago()), transactions))

                users = UserDetailsService.get_by_user_ids(user_ids_batch)
                
                transactions_compass = CustomerLastTransactionDetailsService.__convert_to_compass_format(transactions, users)
                ReportService.write_report('CustomerLastTransactionDetails', transactions_compass)

                last_transactions_count += len(transactions_compass)
                batch += 1
            logger.info(f'generated customer last transaction details for {last_transactions_count}')
                
            
        except Exception as exception:
            logger.error(f'failed to generate customer last transaction details: {exception}')
            traceback.print_exc()

    @staticmethod
    def __convert_to_compass_format(transactions, users):
        transactions_compass = []
        for transaction in transactions:
            user_id = transaction.get('user_id')
            for user in users:
                if user.id == user_id:
                    user_exchange_status, reason = CustomerLastTransactionDetailsService.__get_user_exchange_status(user)
                    transactions_compass.append({
                        'CUSTOMERID': user_id,
                        'EXCHANGECODE': 'VA00041101',
                        'FIRSTTRADEDATE': transaction.get('first_transaction'),
                        'LASTTRADEDATE': transaction.get('last_transaction'),
                        'CUSTOMEREXCSTAT': user_exchange_status,
                        'CUSTOMEREXCSTATREASON': reason
                    })
                    break
        return transactions_compass
    
    @staticmethod
    def __get_user_exchange_status(user):
        if user.is_deleted:
            return 'NotActive', 'Account Closed'
        if not user.is_kyc_done:
            return 'Active', 'KYC Pending'
        if user.is_kyc_refresh_required:
            return 'Active', 'ReKYC Pending'
        return 'Active', 'Active'