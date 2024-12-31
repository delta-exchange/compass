from src.util import DateTimeUtil
from src.database.engine import IamEngine
from src.database.model import UserDetailsModel

class UserDetailsService:
    
    @staticmethod
    def get_batch_by_created_at(batch, limit = 500, created_at = DateTimeUtil.get_24hrs_ago()):
        offset = (batch -1) * limit
        session = IamEngine.get_session()
        users = session.query(UserDetailsModel).filter(UserDetailsModel.created_at > created_at).order_by(UserDetailsModel.created_at).limit(limit).offset(offset).all()
        return users
    
    @staticmethod
    def get_by_user_ids(user_ids):
        session = IamEngine.get_session()
        users = session.query(UserDetailsModel).filter(UserDetailsModel.id.in_(user_ids)).all()
        return users