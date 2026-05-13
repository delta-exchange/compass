from src.database.engine import TimescaleEngine
from src.database.model import DailyBalanceIstModel

class DailyBalanceIstService:

    @staticmethod
    def get_between(since, to):
        session = TimescaleEngine.get_session()
        try:
            query = (
                session.query(DailyBalanceIstModel)
                .filter(
                    DailyBalanceIstModel.date > since,
                    DailyBalanceIstModel.date <= to
                )
                .yield_per(10000)
                .execution_options(stream_results=True)
            )
            for record in query:
                yield record
        finally:
            session.close()
