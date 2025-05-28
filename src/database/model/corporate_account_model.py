from sqlalchemy import Column, Integer, String, Date, JSON, Boolean, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class CorporateAccountModel(Base):
    __tablename__ = 'corporate_account'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    parent_corporate_id = Column(Integer, nullable=True)
    kyc_status = Column(String(255), default="pending" nullable=False)
    aml_check = Column(String(255), nullable=False)
    vendor = Column(String(255), nullable=False)
    meta_data = Column(JSON, nullable=True)
    kyc_expiry = Column(Date, nullable=True)
    country = Column(String(255), nullable=False)
    entity_name = Column(String(255), nullable=False)
    entity_registration_number = Column(String(255), nullable=False)
    document_number = Column(String(255), nullable=False)
    business_description = Column(String(255), nullable=True)
    kyc_required = Column(Boolean, nullable=True, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)