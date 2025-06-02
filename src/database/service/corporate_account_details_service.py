from src.database.engine import IamEngine
from src.database.model import CorporateAccountModel

class CorporateAccountDetailsService:
    
    @staticmethod
    def get_by_user_ids(user_ids):
        session = IamEngine.get_session()
        try:
            corporate_accounts = session.query(CorporateAccountModel).filter(CorporateAccountModel.user_id.in_(user_ids)).all()
            return {account.user_id: account for account in corporate_accounts}
        finally:
            session.close()