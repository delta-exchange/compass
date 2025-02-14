from src.database.service import WithdrawalService, UserDetailsService, UserBankAccountService, LoginHistoryService
from .report_service import ReportService
from src.util import logger, DateTimeUtil, AddressUtil
import traceback
from datetime import datetime, timezone, timedelta 

class WithdrawalTransactionService:

    @staticmethod
    def generate_transaction_details(from_time, to):
        try:
            report_name = f"TRN{DateTimeUtil.get_current_date()}03"
            logger.info(f'generating withdrawal transaction details into {report_name}')
            total_count = 0
            since = datetime.strptime(from_time, '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=timezone.utc)
            to = datetime.strptime(to, '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=timezone.utc)
            while True:
                withdrawals = WithdrawalService.get_between(since, to, batch_size=500)
                withdrawals_count = len(withdrawals)
                if withdrawals_count == 0: 
                    break
                else:
                    users_mapping = WithdrawalTransactionService.get_users_mapping(withdrawals)
                    
                    user_banks = UserBankAccountService.get_by_ids(list({withdrawal.user_bank_detail_id for withdrawal in withdrawals}))
                    withdrawal_banks_mapping = {user_bank.id: user_bank for user_bank in user_banks}
                
                    transactions_compass = WithdrawalTransactionService.convert_to_compass_format(withdrawals, users_mapping, withdrawal_banks_mapping)
                    ReportService.write_report(report_name, transactions_compass)

                    since = withdrawals[-1].updated_at
                    total_count += withdrawals_count
                
            logger.info(f'generated withdrawal transaction details for {total_count}')            
        except Exception as exception:
            logger.error(f'failed to generate withdrawal transaction details: {exception}')
            traceback.print_exc()
    
    @staticmethod
    def get_users_mapping(withdrawals):
        user_ids = list({withdrawal.user_id for withdrawal in withdrawals})
        users = UserDetailsService.get_by_user_ids(user_ids)
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
    def convert_to_compass_format(withdrawals, users_mapping, withdrawal_banks_mapping):
        transactions_compass = []
        for withdrawal in withdrawals:
            user = users_mapping.get(withdrawal.user_id)
            user_bank = withdrawal_banks_mapping.get(withdrawal.user_bank_detail_id) if user else None
            location = withdrawal.transaction_meta.get("location") if  withdrawal.transaction_meta else None
            city, state, country = AddressUtil.get_city_state_country_by_location(location)
            state_mapping = {1: "initiated", 2: "complete", 3: "cancelled", 4: "ready_to_process", 5: "ready_to_withdraw", 6: "ready_for_internal_processing"}

            transactions_compass.append({
                'TransactionBatchId': None,
                'TransactionId': withdrawal.id,
                'EXCHANGECODE': 'VA00041101',
                'PRODUCTCODE/ISIN Code': None,
                'MARKETTYPE': 'Cryptocurrency Derivatives Trading',
                'SEGMENTTYPE': 'Derivatives',
                'INSTRUCTIONTYPE': 'WITHDRAWAL',
                'TRANSACTIONTYPE': 'WITHDRAWAL',
                'TRANSACTIONDATETIME': withdrawal.updated_at,
                'FUTURE_OPTIONS_FLAG': False,
                'CALLORPUTTYPE': None,
                'STRIKEPRICE': None,
                'EXPIRYDATE': None,
                'TRANSACTIONINDICATOR': None,
                'CUSTOMERID': withdrawal.user_id,
                'ACCOUNTNO': user_bank.account_number if user_bank else None,
                'CUSTOMERNAME': f'{user.first_name} {user.last_name}' if user else None,
                'TRADESTATUS': state_mapping.get(withdrawal.state, 'unconfirmed'),
                'BRANCHCODE': user_bank.ifsc_code if user_bank else None,
                'TRADEPRICE': None,
                'TRADEQUANTITY': None,
                'NETPRICE': None,
                'ORDERNO': withdrawal.reference_id,
                'ORDERDATETIME': withdrawal.created_at,
                'SETTLEMENTDAYS': None,
                'PARTICIPANTCODE': None,
                'CUSTODIANCODE': withdrawal.custodian,
                'FUNDEDORBANK': None,
                'ISINCODE': None,
                'AUCTIONNO': None,
                'AUCTIONTYPE': None,
                'SETTLEMENTNO': None,
                'COUNTERBROKERID': None,
                'COUNTERCUSTOMERID': None,
                'COUNTERPARTYNAME': withdrawal.custodian,
                'COUNTERPARTYTYPE': 'VENDOR',
                'ACCTCURRENCYCODE': withdrawal.fiat_asset,
                'CURRENCYCODE':  withdrawal.fiat_asset,
                'CONVERSIONRATE': 1,
                'NARRATION': None,
                'USERID': withdrawal.user_id,
                'CHANNELTYPE': withdrawal.audit.get("matched_login_details", {}).get("source") if withdrawal.audit else None,
                'LASTTRADEDPRICE': None,
                'DELIVERYSTATUS': None,
                'BROKERAGEAMOUNT': 0.0,
                'ACCOUTACTIVATIONDATE': user.created_at if user else None,
                'PREVIOUSCLOSEPRICE': None,
                'AMOUNT': withdrawal.fiat_amount,
                'TRANSACTIONPROCESSED_IPADDRESS': withdrawal.transaction_meta.get("client_ip_address") if  withdrawal.transaction_meta else None,
                'TRANSACTIONPROCESSED_ADDRESS': withdrawal.transaction_meta.get("location") if  withdrawal.transaction_meta else None,
                'TRANSACTIONPROCESSED_CITY': city,
                'TRANSACTIONPROCESSED_PROVINCE_OR_STATE': state,
                'TRANSACTIONPROCESSED_PINCODE': None,
                'TRANSACTIONPROCESSED_COUNTRY': country,
                'TRANSACTIONPROCESSED_GEOLOCATION': None,
                'TRANSACTION_IDENTIFIER': 'FIAT_WITHDRAWAL'
            })
        
        return transactions_compass