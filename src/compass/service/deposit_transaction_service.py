from src.database.service import DepositService, UserDetailsService, UserBankAccountService, LoginHistoryService
from .report_service import ReportService
from src.util import logger, DateTimeUtil, AddressUtil
import traceback
from datetime import datetime, timezone, timedelta

class DepositTransactionService:

    @staticmethod
    def generate_transaction_details(from_time, to):
        try:
            report_name = f"TRN{DateTimeUtil.get_current_date()}02"
            logger.info(f'generating deposit transaction details into {report_name}')
            total_count = 0
            since = datetime.strptime(from_time, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)
            to = datetime.strptime(to, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)
            while True:
                deposits = DepositService.get_between(since, to, batch_size=500)
                deposits_count = len(deposits)
                if deposits_count == 0: 
                    break
                else:
                    since = deposits[-1].updated_at
                    total_count += deposits_count 

                    users_mapping = DepositTransactionService.get_users_mapping(deposits)

                    user_banks = UserBankAccountService.get_by_ids(list({deposit.user_bank_details_id for deposit in deposits}))
                    deposit_banks_mapping = {user_bank.id: user_bank for user_bank in user_banks}

                    logins = LoginHistoryService.get_by_user_id_and_since([user_id for user_id in users_mapping], since - timedelta(days=15))
                    logins_mapping = {}
                    for login in logins:
                        if not logins_mapping.get(login.user_id):
                            logins_mapping[login.user_id] = [login]
                        else:
                            logins_mapping[login.user_id].append(login)

                    transactions_compass = DepositTransactionService.convert_to_compass_format(deposits, users_mapping, deposit_banks_mapping, logins_mapping)
                    ReportService.write_report(report_name, transactions_compass)
                
            logger.info(f'generated total {total_count} deposit transaction details')            
        except Exception as exception:
            logger.error(f'failed to generate deposit transaction details: {exception}')
            traceback.print_exc()
    
    @staticmethod
    def get_users_mapping(deposits):
        user_ids = list({deposit.user_id for deposit in deposits})
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
    def convert_to_compass_format(deposits, users_mapping, deposit_banks_mapping, logins_mapping):
        transactions_compass = []
        for deposit in deposits:
            user = users_mapping.get(deposit.user_id)
            user_bank = deposit_banks_mapping.get(deposit.user_bank_details_id) if user else None
            user_logins = logins_mapping.get(user.id, []) if user else []
            login = next((login for login in user_logins[::-1] if login.created_at <= deposit.updated_at), None)
            city, state, country = AddressUtil.get_city_state_country_by_login(login)

            transactions_compass.append({
                'TransactionBatchId': None,
                'TransactionId': deposit.id,
                'EXCHANGECODE': 'VA00041101',
                'PRODUCTCODE/ISIN Code': None,
                'MARKETTYPE': 'Cryptocurrency Derivatives Trading',
                'SEGMENTTYPE': 'Derivatives',
                'INSTRUCTIONTYPE': 'DEPOSIT',
                'TRANSACTIONTYPE': 'DEPOSIT',
                'TRANSACTIONDATETIME': deposit.created_at,
                'FUTURE_OPTIONS_FLAG': False,
                'CALLORPUTTYPE': None,
                'STRIKEPRICE': None,
                'EXPIRYDATE': None,
                'TRANSACTIONINDICATOR': None,
                'CUSTOMERID': deposit.user_id,
                'ACCOUNTNO': user_bank.account_number if user_bank else None,
                'CUSTOMERNAME': f'{user.first_name} {user.last_name}' if user else None,
                'TRADESTATUS': deposit.status,
                'BRANCHCODE': user_bank.ifsc_code if user_bank else None,
                'TRADEPRICE': None,
                'TRADEQUANTITY': None,
                'NETPRICE': None,
                'ORDERNO': deposit.order_id,
                'ORDERDATETIME': deposit.created_at,
                'SETTLEMENTDAYS': None,
                'PARTICIPANTCODE': None,
                'CUSTODIANCODE': deposit.custodian,
                'FUNDEDORBANK': None,
                'ISINCODE': None,
                'AUCTIONNO': None,
                'AUCTIONTYPE': None,
                'SETTLEMENTNO': None,
                'COUNTERBROKERID': None,
                'COUNTERCUSTOMERID': None,
                'COUNTERPARTYNAME': deposit.custodian,
                'COUNTERPARTYTYPE': 'VENDOR',
                'ACCTCURRENCYCODE': deposit.fiat_currency,
                'CURRENCYCODE':  deposit.fiat_currency,
                'CONVERSIONRATE': 1,
                'NARRATION': None,
                'USERID': deposit.user_id,
                'CHANNELTYPE': None,
                'LASTTRADEDPRICE': None,
                'DELIVERYSTATUS': None,
                'BROKERAGEAMOUNT': deposit.fiat_fee,
                'ACCOUTACTIVATIONDATE': user.created_at if user else None,
                'PREVIOUSCLOSEPRICE': None,
                'AMOUNT': deposit.fiat_amount,
                'TRANSACTIONPROCESSED_IPADDRESS': login.ip if login else None,
                'TRANSACTIONPROCESSED_ADDRESS': login.location if login else None,
                'TRANSACTIONPROCESSED_CITY': city,
                'TRANSACTIONPROCESSED_PROVINCE_OR_STATE': state,
                'TRANSACTIONPROCESSED_PINCODE': None,
                'TRANSACTIONPROCESSED_COUNTRY': country,
                'TRANSACTIONPROCESSED_GEOLOCATION': None,
                'TRANSACTION_IDENTIFIER': 'FIAT_DEPOSIT'
            })
        
        return transactions_compass