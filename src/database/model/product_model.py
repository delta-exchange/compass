from sqlalchemy import (
    Column, Integer, BigInteger, String, Boolean, DateTime, Date, Enum, JSON, ForeignKey, DECIMAL
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class ProductModel(Base):
    __tablename__ = 'products'
    
    id = Column(BigInteger, primary_key=True, nullable=False)
    symbol = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)
    underlying_asset_id = Column(BigInteger, nullable=True)
    settlement_time = Column(DateTime, nullable=True)
    product_type = Column(Integer, nullable=False)
    margin_percent = Column(DECIMAL(36, 18), nullable=False)
    impact_size = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    state = Column(Integer, nullable=False)
    settlement_price = Column(DECIMAL(36, 18), nullable=True)
    pricing_source = Column(String(255), nullable=True)
    tick_size = Column(DECIMAL(36, 18), nullable=False)
    basis_factor_max_limit = Column(DECIMAL(36, 18), nullable=False)
    trading_status = Column(Integer, nullable=False)
    commission_rate = Column(DECIMAL(36, 18), nullable=False, default="0.000000000000000000")
    position_size_limit = Column(Integer, nullable=False)
    default_leverage = Column(DECIMAL(36, 18), nullable=False)
    maker_commission_rate = Column(DECIMAL(36, 18), nullable=False, default="0.000000000000000000")
    quoting_asset_id = Column(BigInteger, nullable=False)
    settling_asset_id = Column(Integer, nullable=True)
    contract_type = Column(Integer, nullable=False, default=0)
    sort_priority = Column(Integer, nullable=True)
    maintenance_margin = Column(DECIMAL(36, 18), nullable=False)
    maintenance_margin_scaling_factor = Column(DECIMAL(36, 18), nullable=False)
    initial_margin_scaling_factor = Column(DECIMAL(36, 18), nullable=False)
    max_leverage_notional = Column(DECIMAL(36, 18), nullable=False)
    liquidation_penalty_factor = Column(DECIMAL(36, 18), nullable=False)
    leverage_slider_values = Column(String(255), nullable=True)
    contract_value = Column(DECIMAL(36, 18), nullable=False)
    spot_index_id = Column(BigInteger, nullable=True)
    is_quanto = Column(Boolean, nullable=True)
    strike_price = Column(DECIMAL(36, 18), nullable=True)