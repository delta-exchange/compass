from src.database.engine import IamEngine
from src.database.model import CorporateAccountModel

class CorporateAccountDetailsService:
    
    @staticmethod
    def get_by_user_ids(user_ids):
        session = IamEngine.get_session()
        try:
            corporate_accounts = session.query().filter(CorporateAccountModel.user_id.in_(user_ids)).all()
            return corporate_accounts
        finally:
            session.close()