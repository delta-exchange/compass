from src.util import DateTimeUtil
from src.database.engine import WalletEngine
from src.database.model import UserBankAccountModel, UserBankAccountStatusLogModel

class UserBankAccountService:
    
    @staticmethod
    def get_between(since, to, batch_size = 10000):
        session = WalletEngine.get_session()
        try:
            user_bank_accounts = session.query(UserBankAccountModel).filter(UserBankAccountModel.updated_at > since, UserBankAccountModel.updated_at <= to).order_by(UserBankAccountModel.updated_at).limit(batch_size).all()
            return user_bank_accounts
        finally:
            session.close()
    
    @staticmethod
    def get_by_user_ids(user_ids):
        session = WalletEngine.get_session()
        try:
            user_bank_accounts = session.query(UserBankAccountModel).filter(UserBankAccountModel.user_id.in_(user_ids), UserBankAccountModel.is_active == True).all()
            return user_bank_accounts
        finally:
            session.close()
    
    @staticmethod
    def get_by_ids(ids): 
        session = WalletEngine.get_session()
        try:
            user_bank_accounts = session.query(UserBankAccountModel).filter(UserBankAccountModel.id.in_(ids)).all()
            return user_bank_accounts
        finally:
            session.close()

    @staticmethod
    def get_user_bank_change_status_logs_by_status_and_between(status, since, to, batch_size = 10000):
        session = WalletEngine.get_session()
        try:
            user_bank_account_status_logs = session.query(UserBankAccountStatusLogModel).filter(UserBankAccountStatusLogModel.status == status, UserBankAccountStatusLogModel.created_at > since, UserBankAccountStatusLogModel.created_at <= to).order_by(UserBankAccountStatusLogModel.created_at.desc()).limit(batch_size).all()
            return user_bank_account_status_logs
        finally:
            session.close()

    @staticmethod
    def get_user_banks_by_user_ids_and_status(user_ids, status):
        session = WalletEngine.get_session()
        try:
            user_bank_accounts = session.query(UserBankAccountModel).filter(UserBankAccountModel.user_id.in_(user_ids), UserBankAccountModel.custodian_status == status).all()
            return user_bank_accounts
        finally:
            session.close()
