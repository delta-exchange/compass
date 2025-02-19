from src.database.service import FillsService, UserDetailsService, UserBankAccountService, ProductService, LoginHistoryService
from .report_service import ReportService
from src.util import logger, DateTimeUtil, AddressUtil
from datetime import datetime, timezone, timedelta

import traceback

class FillTransactionDetailsService:

    @staticmethod
    def generate_transaction_details(from_time, to):
        try:
            report_name = f"TRN{18022025}05"
            logger.info(f'generating transaction details into {report_name}')
            total_count = 0
            since = datetime.strptime(from_time, '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=timezone.utc)
            to = datetime.strptime(to, '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=timezone.utc)
            while True:
                logger.info(f"From: {since}")
                order_fills = FillsService.get_between(since, to, batch_size=500)
                order_fills_count = len(order_fills)
                if order_fills_count == 0: 
                    break
                else:
                    users_mapping = FillTransactionDetailsService.get_users_mapping(order_fills)
                    
                    user_banks = UserBankAccountService.get_by_user_ids(list({user.id for user in users_mapping.values()}))
                    user_banks_mapping = {user_bank.user_id: user_bank for user_bank in user_banks}
                
                    products = ProductService.get_by_product_symbols(list({fill.product_symbol for fill in order_fills}))
                    products_mapping = {product.symbol: product for product in products}

                    logins = LoginHistoryService.get_by_user_id_and_since([user_id for user_id in users_mapping], since - timedelta(days=15))
                    logins_mapping = {}
                    for login in logins:
                        if not logins_mapping.get(login.user_id):
                            logins_mapping[login.user_id] = [login]
                        else:
                            logins_mapping[login.user_id].append(login)

                    transactions_compass = FillTransactionDetailsService.convert_to_compass_format(order_fills, users_mapping, user_banks_mapping, products_mapping, logins_mapping)
                    ReportService.write_report(report_name, transactions_compass)

                    since = order_fills[-1].created_at
                    total_count += order_fills_count
                
            logger.info(f'generated totoal {total_count} transaction details')            
        except Exception as exception:
            logger.error(f'failed to generate transaction details: {exception}')
            traceback.print_exc()
    
    @staticmethod
    def get_users_mapping(order_fills):
        user_ids = list({fill.user_id for fill in order_fills} | {fill.counter_party_user_id for fill in order_fills})
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
    def convert_to_compass_format(orders_fills, users_mapping, user_banks_mapping, products_mapping, logins_mapping):
        transactions_compass = []
        for fill in orders_fills:
            product = products_mapping.get(fill.product_symbol)
            user = users_mapping.get(fill.user_id)
            user_bank = user_banks_mapping.get(user.id) if user else None
            counter_party_user_id = fill.counter_party_user_id
            counter_party_user = users_mapping.get(counter_party_user_id) if counter_party_user_id else None
            user_logins = logins_mapping.get(user.id, []) if user else []
            login = next((login for login in user_logins[::-1] if login.created_at <= fill.created_at), None)
            city, state, country = AddressUtil.get_city_state_country_by_login(login)

            transactions_compass.append({
                'TransactionBatchId': None,
                'TransactionId': fill.id,
                'EXCHANGECODE': 'VA00041101',
                'PRODUCTCODE/ISIN Code': fill.product_id,
                'MARKETTYPE': 'Cryptocurrency Derivatives Trading',
                'SEGMENTTYPE': 'Derivatives',
                'INSTRUCTIONTYPE': 'FILL',
                'TRANSACTIONTYPE': fill.fill_type,
                'TRANSACTIONDATETIME': fill.created_at,
                'FUTURE_OPTIONS_FLAG': True,
                'CALLORPUTTYPE': product.contract_type if product else None,
                'STRIKEPRICE': product.strike_price if product else None,
                'EXPIRYDATE': product.settlement_time if product else None,
                'TRANSACTIONINDICATOR': None,
                'CUSTOMERID': fill.user_id,
                'ACCOUNTNO': user_bank.account_number if user_bank else None,
                'CUSTOMERNAME': f'{user.first_name} {user.last_name}' if user else None,
                'TRADESTATUS': "filled",
                'BRANCHCODE': user_bank.ifsc_code if user_bank else None,
                'TRADEPRICE': fill.price,
                'TRADEQUANTITY': fill.size,
                'NETPRICE': fill.price,
                'ORDERNO': fill.id,
                'ORDERDATETIME': fill.created_at,
                'SETTLEMENTDAYS': None,
                'PARTICIPANTCODE': None,
                'CUSTODIANCODE': None,
                'FUNDEDORBANK': None,
                'ISINCODE': None,
                'AUCTIONNO': None,
                'AUCTIONTYPE': None,
                'SETTLEMENTNO': None,
                'COUNTERBROKERID': None,
                'COUNTERCUSTOMERID': counter_party_user_id,
                'COUNTERPARTYNAME': f'{counter_party_user.first_name} {counter_party_user.last_name}' if counter_party_user else None,
                'COUNTERPARTYTYPE': 'Individual' if counter_party_user_id != -4 else 'LiquidationEngine',
                'ACCTCURRENCYCODE': fill.settling_asset_symbol,
                'CURRENCYCODE': fill.settling_asset_symbol,
                'CONVERSIONRATE': 85,
                'NARRATION': None,
                'USERID': fill.user_id,
                'CHANNELTYPE': fill.meta_data.get("source"),
                'LASTTRADEDPRICE': fill.price,
                'DELIVERYSTATUS': None,
                'BROKERAGEAMOUNT': fill.commission,
                'ACCOUTACTIVATIONDATE': user.created_at if user else None,
                'PREVIOUSCLOSEPRICE': None,
                'AMOUNT': fill.notional,
                'TRANSACTIONPROCESSED_IPADDRESS': login.ip if login else None,
                'TRANSACTIONPROCESSED_ADDRESS': login.location if login else None,
                'TRANSACTIONPROCESSED_CITY': city,
                'TRANSACTIONPROCESSED_PROVINCE_OR_STATE': state,
                'TRANSACTIONPROCESSED_PINCODE': None,
                'TRANSACTIONPROCESSED_COUNTRY': country,
                'TRANSACTIONPROCESSED_GEOLOCATION': None,
                'TRANSACTION_IDENTIFIER': 'ORDER_FILL'
            })
        
        return transactions_compass