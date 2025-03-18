import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote

class LedgerEngine:
    _engine = create_engine(
        f"mysql+mysqlconnector://{os.getenv('LS_RDS_USERNAME')}:{quote(os.getenv('LS_RDS_PASSWORD'), safe='')}@{os.getenv('LS_RDS_HOSTNAME')}:{os.getenv('LS_RDS_PORT')}/{os.getenv('LS_RDS_DB_NAME')}",
        pool_size=100,
        max_overflow=5,
        pool_recycle=1800
    )

    _SessionLocal = sessionmaker(bind=_engine)

    @staticmethod
    def get_session():
        return LedgerEngine._SessionLocal()