from src.database.engine import IamEngine
from src.database.model import KycDocumentModel
from .iam_service import IAMService

class KycDocumentsService:
    
    @staticmethod
    def get_by_user_ids(user_ids):
        session = IamEngine.get_session()
        kyc_list = session.query(KycDocumentModel).filter(KycDocumentModel.user_id.in_(user_ids)).order_by(KycDocumentModel.created_at).all()

        encrypted_data = [{"value": kyc.document_value, "vector": kyc.vector} for kyc in kyc_list if kyc.document_value and kyc.vector]
        encrypted_data = encrypted_data + [{"value": kyc.address.get('value'), "vector": kyc.address.get('vector')} for kyc in kyc_list if kyc.document_type == 1 and kyc.address and kyc.address.get('value') and kyc.address.get('vector')]
        if encrypted_data:
            decrypted_data = IAMService.get_decrypted_data(encrypted_data)

            decrypted_data_mapping = {data['value']: data['decrypted_value'] for data in decrypted_data}

            user_kyc_details = {kyc.user_id: {} for kyc in kyc_list}
            for kyc in kyc_list:
                if kyc.vector and kyc.document_value:
                    if kyc.document_type == 0:
                        user_kyc_details[kyc.user_id]["pan_number"] = decrypted_data_mapping.get(kyc.document_value)
                    else:
                        user_kyc_details[kyc.user_id]["aadhaar_number"] = decrypted_data_mapping.get(kyc.document_value)
                        if kyc.address and kyc.address.get('value') and kyc.address.get('vector'):
                            user_kyc_details[kyc.user_id]["address"] = decrypted_data_mapping.get(kyc.address.get('value'))
            return user_kyc_details
        return {}