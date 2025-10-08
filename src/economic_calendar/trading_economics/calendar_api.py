import os
import requests

class TradingEconomicsCalendarAPI:
    @staticmethod
    def get_calendar_events(start_date, end_date, country = "united states", event_impact = 3):
        url = f"{os.getenv('TRADING_ECONOMICS_API_URL')}/calendar/country/{country}/{start_date}/{end_date}?c={os.getenv('TRADING_ECONOMICS_API_KEY')}&f=json&importance={event_impact}"

        response = requests.get(url)

        if response.status_code != 200:
            return response.status_code, response.text
        
        return response.status_code, response.json()
