from src.database.service import OrderDetailsService, FillsService, UserDetailsService, UserBankAccountService, ProductService
from .report_service import ReportService
from src.util import logger, DateTimeUtil

import traceback

class OrderTransactionDetailsService:

    @staticmethod
    def generate_transaction_details(from_time, to):
        try:
            report_name = f"TRN{DateTimeUtil.get_current_date()}02"
            logger.info(f'generating order details into {report_name}')
            total_count = 0
            while True:
                orders = OrderDetailsService.get_between(from_time, to, batch_size=500)
                order_count = len(orders)
                if len(orders) == 0: 
                    break
                else:
                    from_time = orders[-1].updated_at
                    total_count += order_count

                    users_mapping = OrderTransactionDetailsService.get_users_mapping(orders)
                    
                    user_banks = UserBankAccountService.get_by_user_ids(list({user.id for user in users_mapping.values()}))
                    user_banks_mapping = {user_bank.user_id: user_bank for user_bank in user_banks}
                
                    products = ProductService.get_by_product_symbols(list({order.product_symbol for order in orders}))
                    products_mapping = {product.symbol: product for product in products}

                    transactions_compass = OrderTransactionDetailsService.convert_to_compass_format(orders, users_mapping, user_banks_mapping, products_mapping)
                    ReportService.write_report(report_name, transactions_compass)
                
            logger.info(f'generated total {total_count} order details')            
        except Exception as exception:
            logger.error(f'failed to generate order details: {exception}')
            traceback.print_exc()
    
    @staticmethod
    def get_users_mapping(orders):
        user_ids = list({order.user_id for order in orders})
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
    def convert_to_compass_format(orders, users_mapping, user_banks_mapping, products_mapping):
        transactions_compass = []
        for order in orders:
            product = products_mapping.get(order.product_symbol)
            user = users_mapping.get(order.user_id)
            user_bank = user_banks_mapping.get(user.id) if user else None

            transactions_compass.append({
                'TransactionBatchId': None,
                'TransactionId': order.id,
                'EXCHANGECODE': 'VA00041101',
                'PRODUCTCODE/ISIN Code': order.product_id,
                'MARKETTYPE': 'Cryptocurrency Derivatives Trading',
                'SEGMENTTYPE': 'Derivatives',
                'INSTRUCTIONTYPE': 'ORDER',
                'TRANSACTIONTYPE': order.order_type,
                'TRANSACTIONDATETIME': order.created_at,
                'FUTURE_OPTIONS_FLAG': True,
                'CALLORPUTTYPE': product.contract_type if product else None,
                'STRIKEPRICE': product.strike_price if product else None,
                'EXPIRYDATE': product.settlement_time if product else None,
                'TRANSACTIONINDICATOR': None,
                'CUSTOMERID': order.user_id,
                'ACCOUNTNO': user_bank.account_number if user_bank else None,
                'CUSTOMERNAME': f'{user.first_name} {user.last_name}' if user else None,
                'TRADESTATUS': 1,
                'BRANCHCODE': user_bank.ifsc_code if user_bank else None,
                'TRADEPRICE': None,
                'TRADEQUANTITY': order.size,
                'NETPRICE': None,
                'ORDERNO': order.id,
                'ORDERDATETIME': order.created_at,
                'SETTLEMENTDAYS': None,
                'PARTICIPANTCODE': None,
                'CUSTODIANCODE': None,
                'FUNDEDORBANK': None,
                'ISINCODE': None,
                'AUCTIONNO': None,
                'AUCTIONTYPE': None,
                'SETTLEMENTNO': None,
                'COUNTERBROKERID': None,
                'COUNTERCUSTOMERID': None,
                'COUNTERPARTYNAME': None,
                'COUNTERPARTYTYPE': 'Individual',
                'ACCTCURRENCYCODE': None,
                'CURRENCYCODE': None,
                'CONVERSIONRATE': 85,
                'NARRATION': None,
                'USERID': order.user_id,
                'CHANNELTYPE': order.meta_data.get('source'),
                'LASTTRADEDPRICE': None,
                'DELIVERYSTATUS': None,
                'BROKERAGEAMOUNT': None,
                'ACCOUTACTIVATIONDATE': user.created_at if user else None,
                'PREVIOUSCLOSEPRICE': None,
                'AMOUNT': None,
                'TRANSACTIONPROCESSED_IPADDRESS': order.meta_data.get('ip'),
                'TRANSACTIONPROCESSED_ADDRESS': None,
                'TRANSACTIONPROCESSED_CITY': None,
                'TRANSACTIONPROCESSED_PROVINCE_OR_STATE': None,
                'TRANSACTIONPROCESSED_PINCODE': None,
                'TRANSACTIONPROCESSED_COUNTRY': None,
                'TRANSACTIONPROCESSED_GEOLOCATION': None,
                'TRANSACTION_IDENTIFIER': 'ORDER',
                "PNL": None
            })
        
        return transactions_compass