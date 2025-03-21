from src.util import DateTimeUtil
from src.database.engine import IamEngine
from src.database.model import UserDetailsModel

class UserDetailsService:
    
    @staticmethod
    def get_between(since, to, batch_size = 500):
        session = IamEngine.get_session()
        try:
            users = session.query(UserDetailsModel).filter(UserDetailsModel.updated_at > since, UserDetailsModel.updated_at <= to).order_by(UserDetailsModel.updated_at).limit(batch_size).all()
            return users
        finally:
            session.close()
    
    @staticmethod
    def get_by_user_ids(user_ids):
        session = IamEngine.get_session()
        try:
            users = session.query(UserDetailsModel).filter(UserDetailsModel.id.in_(user_ids)).all()
            return users
        finally:
            session.close()