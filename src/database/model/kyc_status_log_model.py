from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.orm import declarative_base
import datetime

Base = declarative_base()

class KycStatusLogModel(Base):
    __tablename__ = 'kyc_status_logs'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    remark = Column(String, nullable=True)
    status = Column(String, nullable=False)
    kyc_verification_type = Column(String, nullable=True)
    vendor = Column(String, nullable=True)
    country = Column(String, nullable=True)
    vendor_status = Column(String, nullable=True)
    meta_data = Column(JSON, nullable=False, default={})
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow, nullable=False)
