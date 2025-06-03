from sqlalchemy import Column, Integer, String, Date, JSON, Boolean, DateTime, DECIMAL
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class CorporateUBOModel(Base):
    __tablename__ = 'corporate_ubos'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), nullable=False)
    name = Column(String(255), default="")
    address = Column(String(255), default="")
    first_name = Column(String(255), default="")
    last_name = Column(String(255), default="")
    employement_status = Column(String(255), nullable=True)
    corporate_account_id = Column(Integer, nullable=False)
    share_holding_percentage = Column(DECIMAL(36, 18), nullable=True)
    meta_data = Column(JSON, nullable=True)
    dob = Column(Date, nullable=True)
    email_verification_status = Column(String(255))
    proof_of_identity_status = Column(String(255), default="pending", nullable=False)
    proof_of_address_status = Column(String(255), default="pending", nullable=False)
    country = Column(String(255), nullable=True)
    is_kyc_done = Column(Boolean, default=False)
    is_kyc_refresh_required = Column(Boolean, default=False)
    kyc_expiry_date = Column(DateTime, nullable=True)
    kyc_required = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
