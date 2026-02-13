from sqlalchemy import (
    Column, Integer, String, DateTime
)
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class UserBankAccountStatusLogModel(Base):
    __tablename__ = 'user_bank_detail_status_logs'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, nullable=False)
    user_bank_detail_id = Column(Integer, nullable=False)
    remark = Column(String(255), nullable=True)
    status = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=True)