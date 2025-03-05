
import os
import shutil
from src.util import DateTimeUtil, logger
from .linked_account_details_service import LinkedAccountDetailsService
from .customer_login_details_service import CustomerLoginDetailsService
from .exchange_details_service import ExchangeDetailsService
from .customer_details_service import CustomerDetailsService
from.exchange_trades_service import ExchangeTradesService
from .customer_last_transaction_details_service import CustomerLastTransactionDetailsService
from .fill_transaction_service import FillTransactionDetailsService
from .deposit_transaction_service import DepositTransactionService
from .withdrawal_transaction_service import WithdrawalTransactionService
from .product_details_service import ProductDetailsService
from .order_transaction_service import OrderTransactionDetailsService
from src.vendor import SlackNotifier, SCPTransfer
import traceback
import json
import os
import csv
class CompassMasterGenerator:

    @staticmethod
    def start():
            # products = CompassMasterGenerator.get_list_from_file(os.path.join(os.getcwd(), 'missing', 'products.txt'))
            # logger.info(f"picked up {len(products)} missing products")
            # ProductDetailsService.generate_product_details(products)

            # customers = CompassMasterGenerator.get_list_from_file(os.path.join(os.getcwd(), 'missing', 'customers.txt'))
            # logger.info(f"picked up {len(customers)} missing customers")
            # CustomerDetailsService.generate_customer_details_details(customers)

            # linked_accounts = CompassMasterGenerator.get_list_from_file(os.path.join(os.getcwd(), 'missing', 'linkedaccounts.txt'))
            # logger.info(f"picked up {len(linked_accounts)} missing linked accounts")
            # LinkedAccountDetailsService.generate_linked_account_details(linked_accounts)
            
            customer_report_directory = os.path.join(os.getcwd(), 'reports', '18022025')
            files = CompassMasterGenerator.get_all_files(customer_report_directory)
            for file in files:
                logger.info(f"picked up {file} for parent account id generation")
                user_ids = CompassMasterGenerator.get_user_ids_from_file(os.path.join(os.getcwd(), 'reports', '18022025', file))
                CustomerDetailsService.generate_customer_details_details(user_ids)
    
    @staticmethod
    def get_all_files(directory):
        files = [f for f in os.listdir(directory) if f.startswith('CST') and os.path.isfile(os.path.join(directory, f))]
        return files


    @staticmethod
    def get_user_ids_from_file(file):
        user_ids = set()
        with open(file, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter='|')
            next(reader)  
            for row in reader:
                if row:  
                    user_ids.add(row[0])
        return list(user_ids)