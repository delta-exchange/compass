from src.util import DateTimeUtil
from src.database.engine import IamEngine
from src.database.model import UserDetailsModel

class UserDetailsService:
    
    @staticmethod
    def get_between(since, to, batch_size = 500):
        session = IamEngine.get_session()
        users = session.query(UserDetailsModel).filter(UserDetailsModel.updated_at > since, UserDetailsModel.updated_at <= to).order_by(UserDetailsModel.updated_at).limit(batch_size).all()
        return users
    

    @staticmethod
    def get_by_user_ids(user_ids):
        session = IamEngine.get_session()
        users = session.query(UserDetailsModel.id, UserDetailsModel.parent_user_id).filter(
            UserDetailsModel.id.in_(user_ids)
        ).all()
        return [dict(id=u.id, parent_user_id=u.parent_user_id) for u in users]
