from sqlalchemy import (
    Column, Integer, String, Numeric, TIMESTAMP
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class DailyBalanceIstModel(Base):
    __tablename__ = 'user_daily_balance_ist'

    date = Column(TIMESTAMP, primary_key=True, nullable=False)
    user_id = Column(Integer, primary_key=True, nullable=False)
    asset_id = Column(Integer, primary_key=True, nullable=False)
    asset_symbol = Column(String, nullable=True)
    opening_balance = Column(Numeric, nullable=True)
    closing_balance = Column(Numeric, nullable=True)
