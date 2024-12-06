from src.database.engine import TimescaleEngine
from src.database.model import FillsModel
from src.util import logger
import traceback

class FillsService:

    @staticmethod
    def get_by_order_ids(order_ids):
        try: 
            # session = TimescaleEngine.get_session()
            # fills = session.query(FillsModel).filter(FillsModel.order_id.in_(order_ids)).all()
            # return fills
            return []
        except Exception as exception:
            logger.error(f'error occurred while fetching fills: {exception}')
            traceback.print_exc()
            return []

