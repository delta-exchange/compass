from src.database.service import UserBankAccountService
from .report_service import ReportService
from src.util import logger, DateTimeUtil

import traceback

class LinkedAccountDetailsService:

    @staticmethod
    def generate_linked_account_details(from_time):
        report_name = f"LAD{DateTimeUtil.get_current_date()}01"
        try:
            batch, user_bank_accounts_count = 1, 0
            while True:
                logger.info(f'generating linked account details for batch {batch}')

                user_bank_accounts = UserBankAccountService.get_batch_since(batch, from_time)
                if len(user_bank_accounts) == 0: break

                ReportService.write_report(report_name, LinkedAccountDetailsService.convert_to_compass_format(user_bank_accounts))
                batch += 1
                user_bank_accounts_count += len(user_bank_accounts)
        
            logger.info(f'generated linked account details for {user_bank_accounts_count} user bank accounts')
        except Exception as exception:
            logger.error(f'failed to generate linked account details: {exception}')
            traceback.print_exc()

    @staticmethod
    def convert_to_compass_format(user_bank_accounts):
        return [{
            'CustomerId': user_bank_account.user_id,
            'LinkedAccountNo': user_bank_account.account_number,
            'LinkedBankCode': user_bank_account.ifsc_code,
            'LinkedBankName': user_bank_account.bank_name,
            'LinkedBankBranchCode': user_bank_account.ifsc_code,
            'LinkedBankIFSCCode': user_bank_account.ifsc_code,
            'LinkedBranchMICRNo': None,
            'LinkedAccountOpenedDate': None,
            'LinkedProductCode': None,
            'LinkedProductType': None,
            'LinkedAccountCurrency': 'INR',
            'LinkedAccountStatus': user_bank_account.custodian_status,
            'AccountLinkedDateTime': user_bank_account.created_at
        } for user_bank_account in user_bank_accounts]