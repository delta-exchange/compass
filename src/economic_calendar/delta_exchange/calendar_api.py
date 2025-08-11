import os
import requests

class DeltaExchangeCalendarAPI:
    @staticmethod
    def get_delta_calendar_events(after = None):
        url = f"{os.getenv('TRADING_ENGINE_SLAVE_URL')}/v2/events/summary?page_size=100"

        if after:
            url += f"&after={after}"
        
        response = requests.get(url)

        if response.status_code != 200:
            return response.status_code, response.text
        
        result = response.json()["result"]

        if not result["meta"]["after"]:
            return response.status_code, response.json()["result"]["events"]
        
        next_events_status, next_events = DeltaExchangeCalendarAPI.get_delta_calendar_events(result["meta"]["after"])

        if next_events_status != 200:
            return next_events_status, next_events

        return response.status_code, (result["events"] + next_events)
    
    @staticmethod
    def register_event(event):
        url = f"{os.getenv('TRADING_ENGINE_MASTER_URL')}/v2/support/events"

        response = requests.post(url, json = event)

        if response.status_code != 200:
            return response.status_code, response.text

        return response.status_code, response.json()