from src.util import DateTimeUtil
from src.database.engine import IamEngine
from src.database.model import LoginHistoryModel
from sqlalchemy.sql import distinct
from sqlalchemy import func, or_

class LoginHistoryService:
    
    @staticmethod
    def get_since(since, to, batch_size = 10000):
        session = IamEngine.get_session()
        login_histories = session.query(LoginHistoryModel).filter(LoginHistoryModel.created_at > since, LoginHistoryModel.created_at <= to).order_by(LoginHistoryModel.created_at).limit(batch_size).all()
        return login_histories
    
    @staticmethod
    def get_unique_locations():
        session = IamEngine.get_session()
        locations = session.query(distinct(LoginHistoryModel.location)).all()
        return [location[0] for location in locations]
    
    @staticmethod
    def get_by_user_id_and_since(user_ids, since):
        session = IamEngine.get_session()
        logins_since = session.query(LoginHistoryModel).filter(LoginHistoryModel.created_at >= since, LoginHistoryModel.user_id.in_(user_ids)).order_by(LoginHistoryModel.created_at).all()
        return logins_since
