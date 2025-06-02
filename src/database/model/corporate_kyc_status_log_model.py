from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class CorporateKycStatusLogModel(Base):
    __tablename__ = 'corporate_kyc_status_logs'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    corporate_account_id = Column(Integer, nullable=True, default=None)
    remark = Column(String(255), nullable=True)
    status = Column(String(255), nullable=False)  # Maps to KycStatus enum
    corporate_verification_type = Column(String(255), nullable=False)  # Maps to CorporateVerificationType enum
    ubo_id = Column(Integer, nullable=True, default=None)
    vendor = Column(String(255), nullable=True)
    country = Column(String(255), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)