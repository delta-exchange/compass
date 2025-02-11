from sqlalchemy import (
    Column, Integer, BigInteger, String, Numeric, JSON, TIMESTAMP, ARRAY, create_engine
)
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import JSONB

Base = declarative_base()

class FillsModel(Base):
    __tablename__ = 'fills'

    id = Column(BigInteger, primary_key=True, nullable=False)
    uuid = Column(String, nullable=False)
    user_id = Column(Integer, nullable=False)
    order_id = Column(String, nullable=False)
    client_order_id = Column(String, nullable=True)
    side = Column(Integer, nullable=False)
    counter_party_user_id = Column(Integer, nullable=True)
    product_id = Column(Integer, nullable=True)
    product_symbol = Column(String, nullable=True)
    settling_asset_id = Column(Integer, nullable=True)
    settling_asset_symbol = Column(String, nullable=True)
    fill_type = Column(Integer, nullable=False)
    size = Column(Numeric, nullable=False)
    contract_value = Column(Numeric, nullable=False)
    price = Column(Numeric, nullable=False)
    notional = Column(Numeric, nullable=True)
    notional_usd = Column(Numeric, nullable=True)
    fill_role = Column(Integer, nullable=False)
    commission = Column(Numeric, nullable=True)
    commission_rebate = Column(Numeric, nullable=True)
    tfc_used = Column(Numeric, nullable=True)
    tags = Column(ARRAY(String), nullable=True)
    meta_data = Column(JSON, nullable=True)
    created_at = Column(TIMESTAMP, nullable=False)
    commission_deto = Column(Numeric, nullable=True)
    referrer_commission = Column(Numeric, nullable=True)
    net_effective_value = Column(Numeric, nullable=True)
    clearance_status = Column(Integer, nullable=False)
    clearance_info = Column(JSONB, nullable=True)
    pnl = Column(Numeric, nullable=True)
    rmm_commission_status = Column(Integer, nullable=True)
    margin_mode = Column(Integer, nullable=True)
    contract_type = Column(Integer, nullable=True)
    persisted_at = Column(TIMESTAMP, nullable=True)