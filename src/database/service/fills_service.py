from src.database.engine import TimescaleEngine
from src.database.model import FillsModel

class FillsService:

    @staticmethod
    def get_between(since, to, batch_size=500):
        session = TimescaleEngine.get_session()
        fills = session.query(FillsModel).filter(FillsModel.created_at > since, FillsModel.created_at <= to).limit(batch_size).all()
        return fills