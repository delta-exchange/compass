from src.database.service import OrderDetailsService, FillsService, UserDetailsService, UserBankAccountService, ProductService
from .report_service import ReportService
from src.util import logger, DateTimeUtil

import traceback

class TransactionDetailsService:

    @staticmethod
    def generate_transaction_details(from_time):
        report_name = f"TRN{DateTimeUtil.get_current_date()}01"
        try:
            batch, transactions_count = 1, 0
            while True:
                logger.info(f'generating transaction details for batch {batch}')

                orders = OrderDetailsService.get_batch_since(batch, from_time)
                if len(orders) == 0: break

                orders_fills_mapping = TransactionDetailsService.get_order_fills_mapping(orders, from_time)

                users_mapping = TransactionDetailsService.get_users_mapping(orders, orders_fills_mapping)
                
                user_banks = UserBankAccountService.get_by_user_ids(list({user.id for user in users_mapping.values()}))
                user_banks_mapping = {user_bank.user_id: user_bank for user_bank in user_banks}
            
                products = ProductService.get_by_product_symbols(list({order.product_symbol for order in orders}))
                products_mapping = {product.symbol: product for product in products}

                transactions_compass = TransactionDetailsService.convert_to_compass_format(orders, orders_fills_mapping, users_mapping, user_banks_mapping, products_mapping)
                ReportService.write_report(report_name, transactions_compass)

                transactions_count += len(transactions_compass)
                batch += 1
    
            logger.info(f'generated transaction details for {transactions_count}')            
        except Exception as exception:
            logger.error(f'failed to generate transaction details: {exception}')
            traceback.print_exc()

    @staticmethod
    def get_order_fills_mapping(orders, from_time):
        orders_fills_mapping = {}
        filled_orders = [order for order in orders if order.size != order.unfilled_size]
        if len(filled_orders) > 0:
            order_ids = [str(order.id) for order in filled_orders]
            fills = FillsService.get_by_order_ids_since(order_ids, from_time)
            for fill in fills:
                orders_fills_mapping[int(fill.order_id)] = fill
        return orders_fills_mapping
    
    @staticmethod
    def get_users_mapping(orders, orders_fills_mapping):
        user_ids = list({order.user_id for order in orders} | {fill.counter_party_user_id for fill in orders_fills_mapping.values()})
        users = UserDetailsService.get_by_user_ids(user_ids)
        users_mapping = {user.id: user for user in users}

        subaccount_users_parent_id_mapping = {user.user_id: user.parent_user_id for user in users if user.parent_user_id}
        parent_user_ids = list(subaccount_users_parent_id_mapping.values())
        parent_users = UserDetailsService.get_by_user_ids(parent_user_ids)
        parent_users_mapping = {user.id: user for user in parent_users}
        
        for user_id, parent_user_id in subaccount_users_parent_id_mapping.items():
            parent = parent_users_mapping.get(parent_user_id)
            if parent:
                users_mapping[user_id] = parent
        return users_mapping
    
    @staticmethod
    def convert_to_compass_format(orders, orders_fills_mapping, users_mapping, user_banks_mapping, products_mapping):
        transactions_compass = []
        for order in orders:
            product = products_mapping.get(order.product_symbol)
            user = users_mapping.get(order.user_id)
            user_bank = user_banks_mapping.get(user.id) if user else None
            order_fill = orders_fills_mapping.get(order.id)
            counter_party_user_id = order_fill.counter_party_user_id if order_fill else None
            counter_party_user = users_mapping.get(counter_party_user_id) if counter_party_user_id else None

            if order_fill:
                logger.debug(f"Order ID: {order.id} Counter Party: {counter_party_user_id}")

            transactions_compass.append({
                'TransactionBatchId': None,
                'TransactionId': order.id,
                'EXCHANGECODE': 'VA00041101',
                'PRODUCTCODE/ISIN Code': order.product_symbol,
                'MARKETTYPE': 'Cryptocurrency Derivatives Trading',
                'SEGMENTTYPE': 'Derivatives',
                'INSTRUCTIONTYPE': order.order_type,
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
                'TRADESTATUS': order.state,
                'BRANCHCODE': user_bank.ifsc_code if user_bank else None,
                'TRADEPRICE': order.avg_fill_price,
                'TRADEQUANTITY': order.size - order.unfilled_size,
                'NETPRICE': order.avg_fill_price,
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
                'COUNTERCUSTOMERID': counter_party_user_id,
                'COUNTERPARTYNAME': f'{counter_party_user.first_name} {counter_party_user.last_name}' if counter_party_user else None,
                'COUNTERPARTYTYPE': order_fill.fill_type if order_fill else None,
                'ACCTCURRENCYCODE': order_fill.settling_asset_symbol if order_fill else None,
                'CURRENCYCODE': order_fill.settling_asset_symbol if order_fill else None,
                'CONVERSIONRATE': 85,
                'NARRATION': order_fill.fill_type if order_fill else None,
                'USERID': order.user_id,
                'CHANNELTYPE': order.meta_data.get('source'),
                'LASTTRADEDPRICE': order.avg_fill_price,
                'DELIVERYSTATUS': None,
                'BROKERAGEAMOUNT': order_fill.commission if order_fill else None,
                'ACCOUTACTIVATIONDATE': user.created_at if user else None,
                'PREVIOUSCLOSEPRICE': None,
                'AMOUNT': order_fill.notional if order_fill else None,
                'TRANSACTIONPROCESSED_IPADDRESS': order.meta_data.get('ip'),
                'TRANSACTIONPROCESSED_ADDRESS': None,
                'TRANSACTIONPROCESSED_CITY': None,
                'TRANSACTIONPROCESSED_PROVINCE_OR_STATE': None,
                'TRANSACTIONPROCESSED_PINCODE': None,
                'TRANSACTIONPROCESSED_COUNTRY': None,
                'TRANSACTIONPROCESSED_GEOLOCATION': None
            })
        
        return transactions_compass