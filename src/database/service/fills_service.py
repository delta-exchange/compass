from src.database.engine import TimescaleEngine
from src.database.model import FillsModel

class FillsService:

    @staticmethod
    def get_between(since, to, batch_size=500):
        session = TimescaleEngine.get_session()
        try:
            fills = session.query(FillsModel).filter(FillsModel.created_at > since, FillsModel.created_at <= to).order_by(FillsModel.created_at).limit(batch_size).all()
            return fills
        finally:
            session.close()