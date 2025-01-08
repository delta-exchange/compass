import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class IamEngine:
    @staticmethod
    def get_session():
        username = os.getenv('IAM_RDS_USERNAME')
        password = os.getenv('IAM_RDS_PASSWORD')
        host = os.getenv('IAM_RDS_HOSTNAME')
        port = os.getenv('IAM_RDS_PORT')
        database = os.getenv('IAM_RDS_DB_NAME')
        engine = create_engine(f'mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database}')
        Session = sessionmaker(bind=engine)
        return Session()