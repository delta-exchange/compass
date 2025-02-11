from sqlalchemy import Column, Integer, String, Float, Enum, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class WithdrawalModel(Base):
    __tablename__ = "fiat_withdrawals"

    id = Column(Integer, primary_key=True, autoincrement=True)
    withdrawal_reference_id = Column(String(255), nullable=False)
    # utr = Column(String(50), nullable=True)
    user_id = Column(Integer, nullable=False)
    user_bank_detail_id = Column(Integer, nullable=True)
    fiat_currency = Column(String(255), nullable=False)
    fiat_amount = Column(Float, nullable=False)
    custodian_fiat_amount = Column(Float, nullable=True)
    custodian_reference_id = Column(String(255), nullable=True)
    withdrawal_type = Column(Enum("fiat", "prepaid_fiat"), nullable=False, default="fiat")
    asset_symbol = Column(String(255), nullable=True)
    asset_network = Column(String(255), nullable=True)
    wallet_address = Column(String(255), nullable=True)
    asset_amount = Column(Float, nullable=False)
    custodian = Column(String(255), nullable=True)
    custodian_status = Column(String(255), nullable=True)
    payment_method = Column(String(50), nullable=True)
    delta_tx_id = Column(String(255), nullable=True)
    tx_id = Column(String(255), nullable=True)
    created_at = Column(DateTime, nullable=True, server_default=func.current_timestamp())
    updated_at = Column(DateTime, nullable=True, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
