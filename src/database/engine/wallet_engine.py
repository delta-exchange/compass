import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class WalletEngine:
    __engine = None
    __session = None

    @staticmethod
    def __ensure_loaded():
        if WalletEngine.__engine is None:
            username = os.getenv('WALLET_RDS_USERNAME')
            password = os.getenv('WALLET_RDS_PASSWORD')
            host = os.getenv('WALLET_RDS_HOSTNAME')
            port = os.getenv('WALLET_RDS_PORT')
            database = os.getenv('WALLET_RDS_DB_NAME')
            WalletEngine.__engine = create_engine(f'mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database}')
            Session = sessionmaker(bind=WalletEngine.__engine)
            WalletEngine.__session = Session()

    @staticmethod
    def get_session():
        WalletEngine.__ensure_loaded()
        return WalletEngine.__session