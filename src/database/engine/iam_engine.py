import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class IamEngine:
    __engine = None
    __session = None

    @staticmethod
    def __ensure_loaded():
        if IamEngine.__engine is None:
            username = os.getenv('IAM_RDS_USERNAME')
            password = os.getenv('IAM_RDS_PASSWORD')
            host = os.getenv('IAM_RDS_HOSTNAME')
            port = os.getenv('IAM_RDS_PORT')
            database = os.getenv('IAM_RDS_DB_NAME')
            IamEngine.__engine = create_engine(f'mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database}')
            Session = sessionmaker(bind=IamEngine.__engine)
            IamEngine.__session = Session()

    @staticmethod
    def get_session():
        IamEngine.__ensure_loaded()
        return IamEngine.__session