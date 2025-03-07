from src.database.service import KycDocumentsService
from .report_service import ReportService
from src.util import logger, DateTimeUtil, get_report_index

class KycRejectionDetailsService:

    @staticmethod
    def generate_rejected_kyc_details(from_time, to_time):
        logger.info(f'generating rejected kyc details')
        total_count = 0
        while True:
            logger.info(f"From: {from_time}")
            report_name = f"KRD18022025" + get_report_index(total_count, 100000)
            rejections = KycDocumentsService.get_rejected_kycs_between(from_time, to_time, 10000)
            rejections = KycRejectionDetailsService.get_latest_rejections(rejections)
            rejections_count = len(rejections)
            if rejections_count == 0: 
                break
            else:
                from_time = rejections[-1].updated_at
                user_ids = [rejection.user_id for rejection in rejections]
                rejection_stats = KycDocumentsService.get_rejection_stats_by_user_before(user_ids, from_time)
                rejection_stats_mapping = {}
                for stat in rejection_stats:
                    user_id, remark, count, first_date = stat
                    rejection_stats_mapping[f"{user_id}${remark}"] = {"count": count, "first_date": first_date}

                total_count += rejections_count
                
                kyc_rejections_compass = KycRejectionDetailsService.convert_to_compass_format(rejections, rejection_stats_mapping)
                ReportService.write_report(report_name, kyc_rejections_compass)
                
        logger.info(f'generated total {total_count} rejected kyc details')

    @staticmethod
    def get_latest_rejections(rejections):
        user_ids_mapping = {}
        for rejection in rejections:
            user_ids_mapping[f"{rejection.user_id}${rejection.remark}"] = rejection
        return list(user_ids_mapping.values())


    @staticmethod
    def convert_to_compass_format(kyc_rejections, rejection_stats_mapping):
        compass_list = []
        for rejection in kyc_rejections:
            rejection_stat = rejection_stats_mapping.get(f"{rejection.user_id}${rejection.remark}", {})
            compass_list.append({
                "Customer ID": rejection.user_id,
                "Vendor": rejection.vendor,
                "Remarks": rejection.remark,
                "Total Rejections": rejection_stat.get("count", 1),
                "Last Rejection Date": rejection.updated_at,
                "First Rejection Date": rejection_stat.get("first_date", rejection.updated_at)
            })
        return compass_list
    