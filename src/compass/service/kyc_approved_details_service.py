from src.database.service import KycDocumentsService, UserDetailsService
from .report_service import ReportService
from src.util import logger, DateTimeUtil, AddressUtil, get_report_index


class KycApprovedDetailsService:

    @staticmethod
    def generate_approved_kyc_details(from_time, to_time):
        current_date = DateTimeUtil.get_current_date()
        logger.info(f'generating approved kyc details')
        total_count = 0
        while True:
            logger.info(f"From: {from_time}")
            report_name = f"KAD{current_date}" + get_report_index(total_count, 100000)
            approvals = KycDocumentsService.get_approved_kycs_between(from_time, to_time, 10000)
            approvals_count = len(approvals)
            if approvals_count == 0:
                break
            else:
                from_time = approvals[-1].updated_at
                user_ids = list({approval.user_id for approval in approvals})

                users = UserDetailsService.get_by_user_ids(user_ids)
                users_mapping = {user.id: user for user in users}

                user_kyc_details = KycDocumentsService.get_by_user_ids(user_ids)

                total_count += approvals_count

                kyc_approved_compass = KycApprovedDetailsService.convert_to_compass_format(
                    approvals, users_mapping, user_kyc_details
                )
                ReportService.write_report(report_name, kyc_approved_compass)

        logger.info(f'generated total {total_count} approved kyc details')

    @staticmethod
    def convert_to_compass_format(approvals, users_mapping, user_kyc_details):
        compass_list = []
        for approval in approvals:
            user = users_mapping.get(approval.user_id)
            kyc = user_kyc_details.get(approval.user_id, {})
            pincode, state, city = AddressUtil.extract_pincode_state_city(kyc.get("address"))

            if not state:
                state = user.region if user else None

            name = None
            if user and user.first_name and user.last_name:
                name = f"{user.first_name} {user.last_name}"
            elif user and user.first_name:
                name = user.first_name

            compass_list.append({
                "User ID": approval.user_id,
                "Name": name,
                "KYC Date": approval.updated_at,
                "City": city,
                "State": state,
                "Occupation": user.occupation if user else None,
                "Income Range": user.income if user else None,
            })
        return compass_list
