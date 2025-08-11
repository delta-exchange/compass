import os
import requests

class DeltaExchangeCalendarAPI:
    @staticmethod
    def get_delta_calendar_events(start_date, end_date, page = 1):
        url = f"{os.getenv('TRADING_ENGINE_MASTER_URL')}/v2/support/events?start_date={start_date}&end_date={end_date}&page={page}&page_size=100"
        
        response = requests.get(url)

        if response.status_code != 200:
            return response.status_code, response.text
        
        result = response.json()["result"]
        
        if result["events"]:
            next_events_status, next_events = DeltaExchangeCalendarAPI.get_delta_calendar_events(start_date, end_date, result["meta"]["page"] + 1)

            if next_events_status != 200:
                return next_events_status, next_events

            return response.status_code, (result["events"] + next_events)

        return response.status_code, result["events"]
    
    @staticmethod
    def register_event(event):
        url = f"{os.getenv('TRADING_ENGINE_MASTER_URL')}/v2/support/events"

        response = requests.post(url, json = event)

        if response.status_code != 201:
            return response.status_code, response.text

        return response.status_code, response.json()