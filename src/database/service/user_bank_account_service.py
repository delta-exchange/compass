from src.util import DateTimeUtil
from src.database.engine import WalletEngine
from src.database.model import UserBankAccountModel

class UserBankAccountService:
    
    @staticmethod
    def get_batch_by_created_at(batch, limit = 500, created_at = DateTimeUtil.get_24hrs_ago()):
        offset = (batch -1) * limit
        session = WalletEngine.get_session()
        user_bank_accounts = session.query(UserBankAccountModel).filter(UserBankAccountModel.created_at > created_at, UserBankAccountModel.is_active == True).order_by(UserBankAccountModel.created_at).limit(limit).offset(offset).all()
        return user_bank_accounts
    
    @staticmethod
    def get_by_user_ids(user_ids):
        session = WalletEngine.get_session()
        user_bank_accounts = session.query(UserBankAccountModel).filter(UserBankAccountModel.user_id.in_(user_ids), UserBankAccountModel.is_active == True).all()
        return user_bank_accounts
        
