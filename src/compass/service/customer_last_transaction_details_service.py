from src.database.service import OrderDetailsService, LoginHistoryService, UserDetailsService
from .report_service import ReportService
from src.util import logger, DateTimeUtil

import traceback

class CustomerLastTransactionDetailsService:

    @staticmethod
    def generate_last_transaction_details(from_time, to):
        try:
            report_name = f"CTD{DateTimeUtil.get_current_date()}01"
            logger.info(f'generating customer last transaction details into {report_name}')
        
            user_ids = OrderDetailsService.get_user_ids_between(from_time, to)
            batch, batch_size, last_transactions_count = 1, 500, 0

            while True:
                user_ids_batch = user_ids[(batch - 1) * batch_size : batch * batch_size]
                user_ids_count = len(user_ids_batch)
                if user_ids_count == 0: 
                    break
                else:
                    last_transactions_count += user_ids_count
                    batch += 1

                    orders = OrderDetailsService.get_first_and_last_by_user_ids(user_ids_batch)
                    orders = [{'user_id': transaction[0], 'first_transaction': transaction[1], 'last_transaction': transaction[2]} for transaction in orders]

                    users = UserDetailsService.get_by_user_ids(user_ids_batch)
                    users_mapping = CustomerLastTransactionDetailsService.get_users_mapping(users)
                    
                    transactions_compass = CustomerLastTransactionDetailsService.convert_to_compass_format(orders, users_mapping)
                    ReportService.write_report(report_name, transactions_compass)

                    
            logger.info(f'generated customer last transaction details for {last_transactions_count}')
                
            
        except Exception as exception:
            logger.error(f'failed to generate customer last transaction details: {exception}')
            traceback.print_exc()
    
    @staticmethod
    def get_users_mapping(users):
        users_mapping = {user.id: user for user in users}

        subaccount_users_parent_id_mapping = {user.id: user.parent_user_id for user in users if user.parent_user_id}
        parent_user_ids = list(subaccount_users_parent_id_mapping.values())
        parent_users = UserDetailsService.get_by_user_ids(parent_user_ids)
        parent_users_mapping = {user.id: user for user in parent_users}
        
        for user_id, parent_user_id in subaccount_users_parent_id_mapping.items():
            parent = parent_users_mapping.get(parent_user_id)
            if parent:
                users_mapping[user_id] = parent
        return users_mapping

    @staticmethod
    def convert_to_compass_format(transactions, users_mapping):
        transactions_compass = []
        for transaction in transactions:
            user_id = transaction.get('user_id')
            user = users_mapping.get(user_id)
            user_exchange_status, reason = CustomerLastTransactionDetailsService.get_user_exchange_status(user)

            transactions_compass.append({
                'CUSTOMERID': user_id,
                'EXCHANGECODE': 'VA00041101',
                'FIRSTTRADEDATE': transaction.get('first_transaction'),
                'LASTTRADEDATE': transaction.get('last_transaction'),
                'CUSTOMEREXCSTAT': user_exchange_status,
                'CUSTOMEREXCSTATREASON': reason
            })
                    
        return transactions_compass
    
    @staticmethod
    def get_user_exchange_status(user):
        if user.is_deleted:
            return 'NotActive', 'Account Closed'
        if not user.is_kyc_done:
            return 'Active', 'KYC Pending'
        if user.is_kyc_refresh_required:
            return 'Active', 'ReKYC Pending'
        return 'Active', 'Active'