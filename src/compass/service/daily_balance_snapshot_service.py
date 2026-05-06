import os
import requests
from decimal import Decimal

from src.database.service import DailyBalanceIstService, ProductService
from .report_service import ReportService
from src.util import logger, DateTimeUtil, get_report_index

INR_TO_USD_RATE = Decimal("85")
USD_ASSET_SYMBOLS = ["USD", "REF_USD", "TFC_USD"]

class DailyBalanceSnapshotService:

    @staticmethod
    def generate_balance_snapshot(from_time, to_time):
        current_date = DateTimeUtil.get_current_date()
        logger.info("generating daily balance snapshot report")

        spot_price_map = DailyBalanceSnapshotService._build_spot_price_map()
        balances = list(DailyBalanceIstService.get_between(DateTimeUtil.add_days(from_time, -1), to_time))

        logger.info(f"fetched {len(balances)} balance records")

        rows = DailyBalanceSnapshotService._convert_to_report_format(balances, spot_price_map)

        report_name = f"BAL{current_date}" + get_report_index(len(rows), 100000)
        ReportService.write_report(report_name, rows)

        logger.info(f"generated {len(rows)} snapshot rows")

    @staticmethod
    def _build_spot_price_map():
        """Build asset_id -> spot_price (INR) map from spot live products and ticker API."""
        products = ProductService.get_spot_live_products()
        logger.info(f"fetched {len(products)} spot live products")

        api_base_url = os.getenv("DELTA_EXCHANGE_API_BASE_URL")
        asset_id_to_spot_price = {}

        for product in products:
            try:
                response = requests.get(
                    url=f"{api_base_url}/v2/tickers/{product.symbol}",
                    headers={"accept": "application/json"},
                )
                ticker = response.json().get("result", {})
                spot_price = ticker.get("spot_price")
                if spot_price is not None:
                    asset_id_to_spot_price[product.underlying_asset_id] = Decimal(str(spot_price))
                    logger.info(f"ticker {product.symbol}: spot_price={spot_price}")
            except Exception as e:
                logger.error(f"failed to fetch ticker for {product.symbol}: {e}")

        return asset_id_to_spot_price

    @staticmethod
    def _convert_to_report_format(balances, spot_price_map):
        rows = []
        for balance in balances:
            closing = balance.closing_balance or Decimal("0")

            if balance.asset_symbol in USD_ASSET_SYMBOLS:
                balance_usd = closing
            else:
                spot_price = spot_price_map.get(balance.asset_id)
                if spot_price is not None:
                    balance_usd = closing * spot_price / INR_TO_USD_RATE
                else:
                    balance_usd = None

            rows.append({
                "USER_ID": balance.user_id,
                "ASSET_TYPE": balance.asset_symbol,
                "BALANCE": closing,
                "BALANCE_USD": balance_usd,
            })
        return rows
