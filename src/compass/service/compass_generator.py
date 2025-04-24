
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
from .kyc_rejection_details_service import KycRejectionDetailsService
from src.vendor import SlackNotifier, SCPTransfer
import traceback
import json
from datetime import datetime, timedelta

class CompassGenerator:

    @staticmethod
    def start(date=None):
        try:
            from_date, to_date = DateTimeUtil.get_last_date(), DateTimeUtil.get_today_date()
            if date:
                from_date = DateTimeUtil.get_date_from_string(date)
                logger.info(f'generating reports for date: {from_date}')
                to_date = datetime.strptime(from_date, "%Y-%m-%dT%H:%M:%S.%fZ") + timedelta(days=1)
                to_date = datetime.strftime(to_date, "%Y-%m-%dT%H:%M:%S.%fZ")

            reports_directory = os.path.join(os.getcwd(), 'reports', DateTimeUtil.get_current_date())
            logger.info(f'cleaning up reports for directory : {reports_directory}')
            if os.path.exists(reports_directory): shutil.rmtree(reports_directory)
            os.makedirs(reports_directory)

            # ExchangeDetailsService.generate_exchange_details()

            # ProductDetailsService.generate_product_details(from_date, to_date)
            # ExchangeTradesService.generate_trade_volume_details()

            # KycRejectionDetailsService.generate_rejected_kyc_details(from_date, to_date)

            # LinkedAccountDetailsService.generate_linked_account_details(from_date, to_date)
            # CustomerDetailsService.generate_customer_details_details(from_date, to_date)
            # CustomerLoginDetailsService.generate_customer_login_details(from_date, to_date)
            
            DepositTransactionService.generate_transaction_details(from_date, to_date)
            WithdrawalTransactionService.generate_transaction_details(from_date, to_date)
            FillTransactionDetailsService.generate_transaction_details(from_date, to_date)

            # CustomerLastTransactionDetailsService.generate_last_transaction_details(from_date, to_date)

            CompassGenerator.add_blank_reports_for_missing_data(reports_directory)
            SCPTransfer.push_files_to_remote_server_by_directory(reports_directory)
            SlackNotifier.send_alert('Compass cron\n```status: Success\n```')
        except:
            exception_message = traceback.format_exc()
            logger.error(f'An error occurred while generating reports: {exception_message}')
            SlackNotifier.send_alert(f'Compass cron\n```status: Failure\nReason: {exception_message}```')

    @staticmethod
    def add_blank_reports_for_missing_data(reports_directory):
        attributes_template_path = "src/compass/template/attributes.json"
        file_content = open(attributes_template_path, 'r') 
        attributes = json.load(file_content)
        for service in attributes:
            report_path = os.path.join(reports_directory, f'{service}{DateTimeUtil.get_current_date()}01.csv')
            if not os.path.exists(report_path):
                file = open(report_path, 'w')
                file.write(','.join(attributes[service]))
                file.close()
        eod_file_path = os.path.join(reports_directory, f"EOD{DateTimeUtil.get_current_date()}.csv")
        if not os.path.exists(eod_file_path):
            file = open(eod_file_path, 'w')
            file.close()
