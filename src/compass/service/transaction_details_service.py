from src.database.service import OrderDetailsService, LoginHistoryService, UserDetailsService, UserBankAccountService, FillsService, ProductService
from .report_service import ReportService
from src.util import logger, DateTimeUtil

import traceback

class TransactionDetailsService:

    @staticmethod
    def generate_transaction_details():
        try:
            users = LoginHistoryService.get_users_by_created_at()
            user_ids =  list(map(lambda user: user[0], users))
            batch, batch_size, transactions_count = 1, 100, 0
            while True:
                logger.info(f'generating transaction details for batch {batch}')
                user_ids_batch = user_ids[(batch - 1) * batch_size : batch * batch_size]
                if len(user_ids_batch) == 0:
                    break

                user_banks = UserBankAccountService.get_by_user_ids(user_ids_batch)

                transactions = OrderDetailsService.get_by_user_ids_and_created_at(user_ids_batch)
            
                order_ids = [ str(transaction.id) for transaction in transactions ]
                order_fills = FillsService.get_by_order_ids(order_ids)

                counter_party_users = [ order_fill.counter_party_user_id for order_fill in order_fills ]
                all_users = user_ids_batch + counter_party_users
                users = UserDetailsService.get_by_user_ids(all_users)

                product_symbols = [transaction.product_symbol for transaction in transactions]
                products = ProductService.get_by_product_symbols(product_symbols)
                
                transactions_compass = TransactionDetailsService.__convert_to_compass_format(transactions, users, user_banks, order_fills, products)
                ReportService.write_report('Transaction', transactions_compass)

                transactions_count += len(transactions_compass)
                batch += 1
            logger.info(f'generated transaction details for {transactions_count}')            
        except Exception as exception:
            logger.error(f'failed to generate transaction details: {exception}')
            traceback.print_exc()

    @staticmethod
    def __convert_to_compass_format(transactions, users, user_banks, order_fills, products):
        users = dict(map(lambda user: (user.id, user), users))
        user_banks = dict(map(lambda user_bank: (user_bank.user_id, user_bank), user_banks))
        order_fills = dict(map(lambda order_fill: (order_fill.order_id, order_fill), order_fills))

        transactions_compass = []
        for transaction in transactions:
            order_id = transaction.id
            user_id = transaction.user_id
            product_symbol = transaction.product_symbol
            product = products.get(product_symbol) if product_symbol in products else {}
            user = users.get(user_id) 
            user_bank = user_banks.get(user_id) 
            order_fill = order_fills.get(order_id)
            counter_party_user_id = order_fill.counter_party_user_id if order_fill else None
            counter_party_user = users.get(counter_party_user_id) if counter_party_user_id else None

            transactions_compass.append({
                'TransactionBatchId': None,
                'TransactionId': transaction.id,
                'EXCHANGECODE': 'VA00041101',
                'PRODUCTCODE/ISIN Code': product_symbol,
                'MARKETTYPE': 'Cryptocurrency Derivatives Trading',
                'SEGMENTTYPE': 'Derivatives',
                'INSTRUCTIONTYPE': None,
                'TRANSACTIONTYPE': transaction.order_type,
                'TRANSACTIONDATETIME': transaction.created_at,
                'FUTURE_OPTIONS_FLAG': True,
                'CALLORPUTTYPE': product.contract_type,
                'STRIKEPRICE': product.strike_price,
                'EXPIRYDATE': None,
                'TRANSACTIONINDICATOR': None,
                'CUSTOMERID': user_id,
                'ACCOUNTNO': user_bank.account_number if user_bank else None,
                'CUSTOMERNAME': f'{user.first_name} {user.last_name}' if user else None,
                'TRADESTATUS': transaction.state,
                'BRANCHCODE': user_bank.ifsc_code if user_bank else None,
                'TRADEPRICE': transaction.avg_fill_price,
                'TRADEQUANTITY': transaction.size,
                'NETPRICE': transaction.avg_fill_price,
                'ORDERNO': transaction.id,
                'ORDERDATETIME': transaction.created_at,
                'SETTLEMENTDAYS': None,
                'PARTICIPANTCODE': None,
                'CUSTODIANCODE': None,
                'FUNDEDORBANK': None,
                'ISINCODE': None,
                'AUCTIONNO': None,
                'AUCTIONTYPE': None,
                'SETTLEMENTNO': None,
                'COUNTERBROKERID': None,
                'COUNTERCUSTOMERID': order_fill.counter_party_user_id if order_fill else None,
                'COUNTERPARTYNAME': f'{counter_party_user.first_name} {counter_party_user.last_name}' if counter_party_user else None,
                'COUNTERPARTYTYPE': None,
                'ACCTCURRENCYCODE': None,
                'CURRENCYCODE': None,
                'CONVERSIONRATE': 85,
                'NARRATION': None,
                'USERID': user_id,
                'CHANNELTYPE': transaction.meta_data.get('source'),
                'LASTTRADEDPRICE': transaction.avg_fill_price,
                'DELIVERYSTATUS': None,
                'BROKERAGEAMOUNT': None,
                'ACCOUTACTIVATIONDATE': None,
                'PREVIOUSCLOSEPRICE': None,
                'AMOUNT': None,
                'TRANSACTIONPROCESSED_IPADDRESS': transaction.meta_data.get('ip'),
                'TRANSACTIONPROCESSED_ADDRESS': None,
                'TRANSACTIONPROCESSED_CITY': None,
                'TRANSACTIONPROCESSED_PROVINCE_OR_STATE': None,
                'TRANSACTIONPROCESSED_PINCODE': None,
                'TRANSACTIONPROCESSED_COUNTRY': None,
                'TRANSACTIONPROCESSED_GEOLOCATION': None
            })
        
        return transactions_compass