from src.database.engine import WalletEngine
from src.database.model import DepositModel

class DepositService:

    @staticmethod
    def get_between(since, to, batch_size = 10000):
        session = WalletEngine.get_session()
        try:
            deposits = session.query(DepositModel).filter(DepositModel.updated_at > since, DepositModel.updated_at <= to).order_by(DepositModel.updated_at).limit(batch_size).all()
            return deposits
        finally:
            session.close()