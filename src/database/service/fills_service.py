from src.database.engine import TimescaleEngine
from src.database.model import FillsModel
from src.util import logger, DateTimeUtil
import traceback

class FillsService:

    @staticmethod
    def get_batch_by_created_at(batch, limit = 500, created_at = DateTimeUtil.get_24hrs_ago()):
        offset = (batch -1) * limit
        session = TimescaleEngine.get_session()
        user_bank_accounts = session.query(FillsModel).filter(FillsModel.created_at > created_at).order_by(FillsModel.created_at).limit(limit).offset(offset).all()
        return user_bank_accounts

    @staticmethod
    def get_by_order_ids_since(order_ids, since):
        logger.debug(f"getting fills for orders: {order_ids}")
        session = TimescaleEngine.get_session()
        fills = session.query(FillsModel).filter(FillsModel.created_at > since, FillsModel.order_id.in_(order_ids)).all()
        logger.debug(f"fetched fills for orders: {len(fills)}")
        return fills


