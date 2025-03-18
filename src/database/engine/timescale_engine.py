import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.util import logger
from urllib.parse import quote

class TimescaleEngine:
    _engine = create_engine(
        f"postgresql://{os.getenv('TIMESCALE_USERNAME')}:{quote(os.getenv('TIMESCALE_PASSWORD'), safe='')}@{os.getenv('TIMESCALE_HOST')}:{os.getenv('TIMESCALE_PORT')}/{os.getenv('TIMESCALE_DB_NAME')}",
        pool_size=100,
        max_overflow=5,
        pool_recycle=1800
    )

    _SessionLocal = sessionmaker(bind=_engine)

    @staticmethod
    def get_session():
        return TimescaleEngine._SessionLocal()
