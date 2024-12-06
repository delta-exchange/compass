from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, JSON, create_engine
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class UserBankAccountModel(Base):
    __tablename__ = 'user_bank_details'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, nullable=False)
    account_name = Column(String(255), nullable=True)
    account_number = Column(String(255), nullable=False)
    ifsc_code = Column(String(255), nullable=False)
    bank_name = Column(String(255), nullable=True)
    customized_bank_name = Column(String(255), nullable=True)
    custodian = Column(String(255), nullable=False)
    custodian_status = Column(String(255), default="initiated", nullable=True)
    custodian_reference_id = Column(String(255), nullable=True)
    number_of_transactions = Column(Integer, default=0, nullable=False)
    is_active = Column(Boolean, default=True, nullable=True)
    va_number = Column(String(255), nullable=True)
    va_unique_number = Column(String(255), nullable=True)
    va_ifsc_code = Column(String(255), nullable=True)
    va_hash_id = Column(String(255), nullable=True)
    is_van_mapped = Column(Boolean, default=False, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=True)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=True)    
    meta_data = Column(JSON, nullable=True)