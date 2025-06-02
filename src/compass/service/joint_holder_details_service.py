from src.database.service import UserDetailsService, KycDocumentsService, CorporateAccountDetailsService, UserBankAccountService
from .report_service import ReportService
from src.util import logger, DateTimeUtil, get_report_index
from src.database.engine import IamEngine
from src.database.model import CorporateUBOModel, KycStatusLogModel, CorporateAccountModel, CorporateKycStatusLogModel

import traceback

class JointHolderDetailsService:

    @staticmethod
    def generate_joint_holder_details(from_time, to):
        try:
            current_date = DateTimeUtil.get_current_date()
            logger.info(f'generating joint holder details')
            total_count = 0
            while True:
                logger.info(f"From: {from_time}")
                logger.info(f"To: {to}")
                report_name = f"JHD{current_date}" + get_report_index(total_count, 100000)
                
                # Get corporate UBOs
                session = IamEngine.get_session()
                try:
                    ubos = session.query(CorporateUBOModel).filter(
                        CorporateUBOModel.updated_at > from_time,
                        CorporateUBOModel.updated_at <= to
                    ).order_by(CorporateUBOModel.updated_at).limit(2000).all()
                    logger.info(f"Found {len(ubos)} UBOs")
                finally:
                    session.close()

                if not ubos:
                    break

                from_time = ubos[-1].updated_at
                total_count += len(ubos)

                # Get corporate accounts for UBOs
                corporate_account_ids = [ubo.corporate_account_id for ubo in ubos]
                session = IamEngine.get_session()
                try:
                    corporate_accounts = session.query(CorporateAccountModel).filter(
                        CorporateAccountModel.id.in_(corporate_account_ids)
                    ).all()
                    corporate_accounts_mapping = {ca.id: ca for ca in corporate_accounts}
                finally:
                    session.close()

                # Get user IDs from corporate accounts
                user_ids = [ca.user_id for ca in corporate_accounts]
                users = UserDetailsService.get_by_user_ids(user_ids)
                users_mapping = {user.id: user for user in users}

                # Get KYC details
                user_kyc_details_mapping = KycDocumentsService.get_by_user_ids(user_ids)

                # Get bank account details
                user_bank_accounts = UserBankAccountService.get_by_user_ids(user_ids)
                bank_accounts_mapping = {account.user_id: account for account in user_bank_accounts}

                # Get corporate KYC status logs for effective dates
                session = IamEngine.get_session()
                try:
                    ubo_ids = [ubo.id for ubo in ubos]
                    corporate_kyc_status_logs = session.query(CorporateKycStatusLogModel).filter(
                        CorporateKycStatusLogModel.ubo_id.in_(ubo_ids),
                        CorporateKycStatusLogModel.status == 'approved'
                    ).all()
                    corporate_kyc_status_mapping = {log.ubo_id: log for log in corporate_kyc_status_logs}
                    logger.info(f"Found {len(corporate_kyc_status_mapping)} approved corporate KYC status logs")
                finally:
                    session.close()

                joint_holders = JointHolderDetailsService.convert_to_compass_format(
                    ubos,
                    corporate_accounts_mapping,
                    users_mapping,
                    user_kyc_details_mapping,
                    bank_accounts_mapping,
                    corporate_kyc_status_mapping
                )
                logger.info(f"Converted {len(joint_holders)} records to compass format")

                ReportService.write_report(
                    report_name,
                    joint_holders
                )

            logger.info(f'generated joint holder details for {total_count} records')
        except Exception as exception:
            logger.error(f'failed to generate joint holder details: {exception}')
            traceback.print_exc()

    @staticmethod
    def get_joint_holder_type(entity_name):
        if not entity_name:
            return "To be filled manually"
            
        entity_name = entity_name.lower()
        if any(x in entity_name for x in ['pvt', 'private', 'ltd', 'limited']):
            return "Director"
        elif 'huf' in entity_name:
            return "Karta"
        elif 'llp' in entity_name:
            return "Partner"
        else:
            return "To be filled manually"

    @staticmethod
    def convert_to_compass_format(ubos, corporate_accounts_mapping, users_mapping, user_kyc_details_mapping, bank_accounts_mapping, corporate_kyc_status_mapping):
        joint_holders = []
        for ubo in ubos:
            corporate_account = corporate_accounts_mapping.get(ubo.corporate_account_id)
            if not corporate_account:
                logger.debug(f"corporate account with id: {ubo.corporate_account_id} not found")
                continue

            user = users_mapping.get(corporate_account.user_id) if corporate_account.user_id else None
            if not user:
                logger.debug(f"user with id: {corporate_account.user_id} not found")
                # Continue processing even if user is not found
                user_id = None
            else:
                user_id = user.id

            kyc = user_kyc_details_mapping.get(user_id, {}) if user_id else {}
            bank_account = bank_accounts_mapping.get(user_id) if user_id else None
            kyc_status = corporate_kyc_status_mapping.get(ubo.id)

            joint_holder_type = JointHolderDetailsService.get_joint_holder_type(corporate_account.entity_name)

            joint_holder_data = {
                'AccountNo': bank_account.account_number if bank_account else None,
                'CustomerId': user_id,
                'JointHolderType': joint_holder_type,
                'JointHolderName': f"{ubo.first_name} {ubo.last_name}".strip() if (ubo.first_name or ubo.last_name) else ubo.name,
                'RelationCode': joint_holder_type,
                'EffectiveDate': kyc_status.created_at if kyc_status else None,
                'Ineffective Date': None,
                'DIN / DPIN': None,
                'DATA_SOURCE': None,
                'UPDATE_TIMESTAMP': ubo.updated_at,
                'EXTRACTION_DATE': None
            }
            joint_holders.append(joint_holder_data)

        return joint_holders
        