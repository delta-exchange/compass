from sqlalchemy import (
    Column, BigInteger, Integer, String, Numeric, JSON, TIMESTAMP, ARRAY
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class FillsModel(Base):
    __tablename__ = 'fills'

    id = Column(BigInteger, primary_key=True)
    uuid = Column(String(255))
    user_id = Column(Integer)
    order_id = Column(String(255))
    client_order_id = Column(String(255))
    side = Column(Integer)
    counter_party_user_id = Column(Integer)
    product_id = Column(Integer)
    product_symbol = Column(String(255))
    settling_asset_id = Column(Integer)
    settling_asset_symbol = Column(String(255))
    fill_type = Column(Integer)
    size = Column(Numeric)
    contract_value = Column(Numeric)
    price = Column(Numeric)
    notional = Column(Numeric)
    notional_usd = Column(Numeric)
    fill_role = Column(Integer)
    commission = Column(Numeric)
    commission_rebate = Column(Numeric)
    tfc_used = Column(Numeric)
    tags = Column(ARRAY(String))
    meta_data = Column(JSON)  
    created_at = Column(TIMESTAMP)
    commission_deto = Column(Numeric)
    referrer_commission = Column(Numeric)
    net_effective_value = Column(Numeric)
    clearance_status = Column(Integer)
    clearance_info = Column(JSON) 
    pnl = Column(Numeric(36, 18))
    rmm_commission_status = Column(Integer)
    margin_mode = Column(Integer)
    contract_type = Column(Integer)
    persisted_at = Column(TIMESTAMP)