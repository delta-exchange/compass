
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
class CompassMasterGenerator:

    @staticmethod
    def start():
            # products = CompassMasterGenerator.get_list_from_file(os.path.join(os.getcwd(), 'missing', 'products.txt'))
            # logger.info(f"picked up {len(products)} missing products")
            # ProductDetailsService.generate_product_details(products)

            customers = CompassMasterGenerator.get_list_from_file(os.path.join(os.getcwd(), 'missing', 'customers.txt'))
            logger.info(f"picked up {len(customers)} missing customers")
            CustomerDetailsService.generate_customer_details_details(customers)

    @staticmethod
    def get_list_from_file(file):
        with open(file, "r") as f:
            return list({line.strip() for line in f})
          
