from src.database.engine import IamEngine
from src.database.model import KycDocumentModel
from src.util import Encrpytion

class KycDocumentsService:
    
    @staticmethod
    def get_by_user_ids(user_ids):
        session = IamEngine.get_session()
        kyc_list = session.query(KycDocumentModel).filter(KycDocumentModel.user_id.in_(user_ids)).order_by(KycDocumentModel.created_at).all()
        user_kyc_details = {}
        for kyc in kyc_list:
            user_kyc_details[kyc.user_id] = {} if kyc.user_id not in user_kyc_details else user_kyc_details[kyc.user_id]
            kyc_data = KycDocumentsService.__decrypt(kyc) 
            pan_number, aadhaar_number, address = kyc_data.get("pan_number"), kyc_data.get("aadhaar_number"), kyc_data.get("address")
            if pan_number:
                user_kyc_details[kyc.user_id]["pan_number"] = pan_number
            if aadhaar_number:
                user_kyc_details[kyc.user_id]["aadhaar_number"] = aadhaar_number
            if address:
                user_kyc_details[kyc.user_id]["address"] = address
        return user_kyc_details
    
    @staticmethod
    def __decrypt(kyc):
        if kyc.document_type == 0: # pan
            pan_vector, pan_cipher = kyc.vector, kyc.document_value
            pan = Encrpytion.decrypt_kyc_data(pan_vector, pan_cipher)
            return {"pan_number": pan}
        else: # aadhaar
            aadhaar_vector, aadhaar_cipher = kyc.vector, kyc.document_value
            aadhaar = Encrpytion.decrypt_kyc_data(aadhaar_vector, aadhaar_cipher)
            address = kyc.address
            if address:
                address_vector, address_cipher = kyc.address.get('vector'), kyc.address.get('value')
                address = Encrpytion.decrypt_kyc_data(address_vector, address_cipher)
            return {"aadhaar_number": aadhaar, "address": address}
        
        
