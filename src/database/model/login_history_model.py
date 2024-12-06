from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, BigInteger
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class LoginHistoryModel(Base):
    __tablename__ = 'login_histories'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, nullable=False)
    ip = Column(String(255), nullable=True)
    user_agent = Column(String(255), nullable=True)
    location = Column(String(255), nullable=True)
    created_at = Column(DateTime, nullable=False)
    status = Column(String(255), nullable=True)
    reason = Column(String(255), nullable=True)
    source = Column(Integer, nullable=False, default=0)
    device_id = Column(String(255), nullable=True)
    is_sub_account_login = Column(Boolean, nullable=True, default=False)
    login_type = Column(Integer, nullable=True)  