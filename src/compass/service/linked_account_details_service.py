from src.database.service import UserBankAccountService
from .report_service import ReportService
from src.util import logger, DateTimeUtil, get_report_index

import traceback

class LinkedAccountDetailsService:

    @staticmethod
    def generate_linked_account_details(from_time, to):
        try:
            current_date = DateTimeUtil.get_current_date()
            logger.info(f'generating linked account details')
            total_count = 0
            while True:
                report_name = f"LAD{current_date}" + get_report_index(total_count, 100000)
                user_bank_accounts = UserBankAccountService.get_between(from_time, to, batch_size=10000)
                user_bank_accounts_count = len(user_bank_accounts)
                if user_bank_accounts_count == 0: 
                    break
                else:
                    from_time = user_bank_accounts[-1].updated_at
                    total_count += user_bank_accounts_count
                    
                    ReportService.write_report(report_name, LinkedAccountDetailsService.convert_to_compass_format(user_bank_accounts))
                
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