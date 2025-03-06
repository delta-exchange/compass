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
        
        users = session.query(UserDetailsModel.id, UserDetailsModel.income, UserDetailsModel.parent_user_id).filter(UserDetailsModel.id.in_(user_ids)).all()
        
        parent_ids = {u.parent_user_id for u in users if u.income is None and u.parent_user_id is not None}
        
        parent_incomes = {}
        if parent_ids:
            parent_data = session.query(UserDetailsModel.id, UserDetailsModel.income).filter(UserDetailsModel.id.in_(parent_ids)).all()
            
            parent_incomes = {p.id: p.income for p in parent_data}

        return [dict(id=u.id, income=u.income if u.income is not None else parent_incomes.get(u.parent_user_id)) for u in users]

