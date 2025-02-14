from sqlalchemy import Column, Integer, String, BigInteger, DECIMAL, JSON, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class WithdrawalModel(Base):
    __tablename__ = 'withdrawals'

    id = Column(BigInteger, primary_key=True, nullable=False)
    user_id = Column(Integer, nullable=False)
    address = Column(String(255), nullable=False)
    memo = Column(Integer, nullable=True)
    amount = Column(DECIMAL(36, 18), nullable=False, default=0.000000000000000000)
    state = Column(Integer, nullable=False)
    transaction_meta = Column(JSON, nullable=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
    fee = Column(DECIMAL(36, 18), nullable=False, default=0.000000000000000000)
    asset_symbol = Column(String(255), nullable=True, default='BTC')
    audit = Column(JSON, nullable=True)
    network = Column(String(255), nullable=False)
    lock_version = Column(Integer, nullable=True, default=1)
    withdrawal_type = Column(Integer, nullable=False, default=0)
    custodian = Column(String(255), nullable=True)
    fiat_asset = Column(String(255), nullable=True)
    fiat_amount = Column(DECIMAL(36, 18), nullable=True)
    user_bank_detail_id = Column(Integer, nullable=True)
    is_internal_withdrawal_address = Column(Boolean, nullable=True, default=False)
    fiat_withdrawal_type = Column(Integer, nullable=True)
    is_referral_bonus_withdrawal = Column(Boolean, nullable=True, default=False)
    reference_id = Column(String(255), nullable=False)
    retry_count = Column(Integer, nullable=True, default=0)

