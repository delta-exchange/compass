from src.util import DateTimeUtil
from src.database.engine import WalletEngine
from src.database.model import UserBankAccountModel

class UserBankAccountService:
    
    @staticmethod
    def get_batch_since(batch, since, batch_size = 500):
        offset = (batch -1) * batch_size
        session = WalletEngine.get_session()
        user_bank_accounts = session.query(UserBankAccountModel).filter(UserBankAccountModel.created_at > since).order_by(UserBankAccountModel.created_at).limit(batch_size).offset(offset).all()
        return user_bank_accounts
    
    @staticmethod
    def get_by_user_ids(user_ids):
        session = WalletEngine.get_session()
        user_bank_accounts = session.query(UserBankAccountModel).filter(UserBankAccountModel.user_id.in_(user_ids), UserBankAccountModel.is_active == True).all()
        return user_bank_accounts
        
