import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class TimescaleEngine:
    __engine = None
    __session = None

    @staticmethod
    def __ensure_loaded():
        if TimescaleEngine.__engine is None:
            username = os.getenv('TIMESCALE_USERNAME')
            password = os.getenv('TIMESCALE_PASSWORD')
            host = os.getenv('TIMESCALE_HOSTNAME')
            port = os.getenv('TIMESCALE_PORT')
            database = os.getenv('TIMESCALE_DB_NAME')
            TimescaleEngine.__engine = create_engine(f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}')
            Session = sessionmaker(bind=TimescaleEngine.__engine)
            TimescaleEngine.__session = Session()

    @staticmethod
    def get_session():
        TimescaleEngine.__ensure_loaded()
        return TimescaleEngine.__session