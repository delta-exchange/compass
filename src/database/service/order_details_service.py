from src.database.engine import LedgerEngine
from src.database.model import OrderDetailsModel
from sqlalchemy import func
from src.util import DateTimeUtil

class OrderDetailsService:

    @staticmethod
    def get_batch_since(batch, since, batch_size = 500):
        offset = (batch -1) * batch_size
        session = LedgerEngine.get_session()
        orders = session.query(OrderDetailsModel).filter(OrderDetailsModel.created_at > since).order_by(OrderDetailsModel.created_at).limit(batch_size).offset(offset).all()
        return orders
    
    @staticmethod
    def get_first_and_last_by_user_ids(user_ids):
        session = LedgerEngine.get_session()
        orders = session.query(
            OrderDetailsModel.user_id,
            func.min(OrderDetailsModel.created_at).label("min_created_at"),
            func.max(OrderDetailsModel.created_at).label("max_created_at")
        ).filter(OrderDetailsModel.user_id.in_(user_ids)).group_by(OrderDetailsModel.user_id).all()
        return orders
    
    @staticmethod
    def get_by_user_ids_and_created_at(user_ids, created_at):
        session = LedgerEngine.get_session()
        orders = session.query(OrderDetailsModel).filter(OrderDetailsModel.user_id.in_(user_ids), OrderDetailsModel.created_at > created_at).all()
        return orders