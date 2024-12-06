import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class LedgerEngine:
    __engine = None
    __session = None

    @staticmethod
    def __ensure_loaded():
        if LedgerEngine.__engine is None:
            username = os.getenv('LS_RDS_USERNAME')
            password = os.getenv('LS_RDS_PASSWORD')
            host = os.getenv('LS_RDS_HOSTNAME')
            port = os.getenv('LS_RDS_PORT')
            database = os.getenv('LS_RDS_DB_NAME')
            LedgerEngine.__engine = create_engine(f'mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database}')
            Session = sessionmaker(bind=LedgerEngine.__engine)
            LedgerEngine.__session = Session()

    @staticmethod
    def get_session():
        LedgerEngine.__ensure_loaded()
        return LedgerEngine.__session