from src.database.engine import WalletEngine
from src.database.model import WithdrawalModel
class WithdrawalService:

    @staticmethod
    def get_between(since, to, batch_size = 10000):
        session = WalletEngine.get_session()
        deposits = session.query(WithdrawalModel).filter(WithdrawalModel.updated_at > since, WithdrawalModel.updated_at <= to).order_by(WithdrawalModel.updated_at).limit(batch_size).all()
        return deposits