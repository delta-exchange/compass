import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class WalletEngine:
    _engine = create_engine(
        f"mysql+mysqlconnector://{os.getenv('WALLET_RDS_USERNAME')}:{os.getenv('WALLET_RDS_PASSWORD')}@{os.getenv('WALLET_RDS_HOSTNAME')}:{os.getenv('WALLET_RDS_PORT')}/{os.getenv('WALLET_RDS_DB_NAME')}",
        pool_size=100,
        max_overflow=5,
        pool_recycle=1800
    )

    _SessionLocal = sessionmaker(bind=_engine)

    @staticmethod
    def get_session():
        return WalletEngine._SessionLocal()