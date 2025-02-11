import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.util import logger


class TimescaleEngine:
    @staticmethod
    def get_session():
        username = os.getenv('TIMESCALE_USERNAME')
        password = os.getenv('TIMESCALE_PASSWORD')
        host = os.getenv('TIMESCALE_HOST')
        port = os.getenv('TIMESCALE_PORT')
        database = os.getenv('TIMESCALE_DB_NAME')
        engine = create_engine(f'postgresql://{username}:{password}@{host}:{port}/{database}')
        Session = sessionmaker(bind=engine)
        return Session()