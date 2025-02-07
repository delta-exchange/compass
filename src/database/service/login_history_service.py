from src.util import DateTimeUtil
from src.database.engine import IamEngine
from src.database.model import LoginHistoryModel

class LoginHistoryService:
    
    @staticmethod
    def get_batch_since(batch, since, batch_size = 500):
        offset = (batch -1) * batch_size
        session = IamEngine.get_session()
        login_histories = session.query(LoginHistoryModel).filter(LoginHistoryModel.created_at > since).order_by(LoginHistoryModel.created_at).limit(batch_size).offset(offset).all()
        return login_histories
    
    @staticmethod
    def get_users_by_created_at(created_at = DateTimeUtil.get_24hrs_ago()):
        session = IamEngine.get_session()
        users = session.query(LoginHistoryModel.user_id).filter(LoginHistoryModel.created_at > created_at).distinct().all()
        return users
        
