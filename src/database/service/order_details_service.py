from src.database.engine import LedgerEngine
from src.database.model import OrderDetailsModel
from sqlalchemy.sql import distinct
from sqlalchemy import func

class OrderDetailsService:

    @staticmethod
    def get_between(since, to, batch_size = 500):
        session = LedgerEngine.get_session()
        try:
            orders = session.query(OrderDetailsModel).filter(OrderDetailsModel.updated_at > since, OrderDetailsModel.updated_at <= to, OrderDetailsModel.avg_fill_price.is_(None)).order_by(OrderDetailsModel.updated_at).limit(batch_size).all()
            return orders
        finally:
            session.close()
    
    @staticmethod
    def get_user_ids_between(since, to):
        session = LedgerEngine.get_session()
        try:
            query = (
                session.query(OrderDetailsModel.user_id)
                .filter(OrderDetailsModel.updated_at > since, OrderDetailsModel.updated_at <= to)
                .distinct()
                .yield_per(1000) 
            )
            return [row[0] for row in query]
        finally:
            session.close()

    
    @staticmethod
    def get_first_and_last_by_user_ids(user_ids):
        session = LedgerEngine.get_session()
        try:
            orders = session.query(
                OrderDetailsModel.user_id,
                func.min(OrderDetailsModel.created_at).label("min_created_at"),
                func.max(OrderDetailsModel.created_at).label("max_created_at")
            ).filter(OrderDetailsModel.user_id.in_(user_ids)).group_by(OrderDetailsModel.user_id).all()
            return orders
        finally:
            session.close()