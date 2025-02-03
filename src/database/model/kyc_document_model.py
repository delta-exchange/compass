from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class KycDocumentModel(Base):
    __tablename__ = 'kyc_documents'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    document_type = Column(Integer, nullable=False)
    document_value = Column(String(255), nullable=False)
    vector = Column(String(255), nullable=False)
    expiry_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow, nullable=False)
    document_number = Column(JSON, nullable=True)
    address = Column(JSON, nullable=True)