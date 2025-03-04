from src.database.service import UserBankAccountService
from .report_service import ReportService
from src.util import logger, DateTimeUtil, get_report_index

import traceback

class LinkedAccountDetailsService:

    @staticmethod
    def generate_linked_account_details(account_nos):
        try:
            report_name = f"LAD18022025XX"
            logger.info(f'generating linked account details')
            total_count, batch, batch_size = 0, 1, 1000
            while True:
                accounts_batch = account_nos[(batch-1)*batch_size:batch*batch_size]
                if not accounts_batch:
                    break
                user_bank_accounts = UserBankAccountService.get_by_account_nos(accounts_batch)
                ReportService.write_report(report_name, LinkedAccountDetailsService.convert_to_compass_format(user_bank_accounts))
                total_count += len(user_bank_accounts)
                batch += 1
                
            logger.info(f'generated total: {total_count} linked account details')
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