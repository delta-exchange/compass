from src.util import DateTimeUtil
from src.database.engine import IamEngine
from src.database.model import UserDetailsModel
from sqlalchemy import or_
class UserDetailsService:
    
    @staticmethod
    def get_batch_by_since(batch, since, batch_size = 500):
        offset = (batch -1) * batch_size
        session = IamEngine.get_session()
        users = session.query(UserDetailsModel).filter(UserDetailsModel.created_at > since).order_by(UserDetailsModel.created_at).limit(batch_size).offset(offset).all()
        return users
    
    @staticmethod
    def get_by_user_ids(user_ids):
        session = IamEngine.get_session()
        users = session.query(UserDetailsModel).filter(UserDetailsModel.id.in_(user_ids)).all()
        return users