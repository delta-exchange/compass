from sqlalchemy import Column, Integer, String, Float, JSON, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class DepositModel(Base):
    __tablename__ = 'fiat_deposits'

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(String(20), nullable=True)
    user_id = Column(Integer, nullable=False)
    fiat_currency = Column(String(255), nullable=False)
    fiat_amount = Column(Float, nullable=True)
    fiat_fee = Column(Float, nullable=True)
    fiat_amount_in_usd = Column(Float, nullable=True)
    user_bank_details_id = Column(Integer, nullable=True)
    custodian_bank_detail_id = Column(Integer, nullable=True)
    payment_method = Column(String(50), nullable=True)
    asset_symbol = Column(String(255), nullable=False)
    asset_network = Column(String(255), nullable=True)
    wallet_address = Column(String(255), nullable=True)
    asset_amount = Column(Float, nullable=True)
    blockchain_asset_amount = Column(Float, nullable=True)
    status = Column(String(255), nullable=False)
    custodian = Column(String(255), nullable=False)
    custodian_tx_id = Column(String(255), nullable=True)
    custodian_reference_id = Column(String(255), nullable=True)
    tx_hash = Column(String(1024), nullable=True)
    meta_data = Column(JSON, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=True)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=True)