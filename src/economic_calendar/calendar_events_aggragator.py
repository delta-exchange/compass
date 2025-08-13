import os
import time
import calendar
import json
from .trading_economics import TradingEconomicsCalendarAPI, TradingEconomicsEventWebPageScrapper
from .delta_exchange import DeltaExchangeCalendarAPI
from src.vendor import SlackNotifier

MAX_COUNT_TRADING_ECONOMIC_EVENTS_OF_PUSH_NOTIFICATION = 1

class CalendarEventsAggregator:
    @staticmethod
    def execute():
        start_date, end_date = CalendarEventsAggregator.get_time_span()

        trading_economic_api_status, upcoming_trading_economics_events = TradingEconomicsCalendarAPI.get_calendar_events(start_date, end_date)

        if trading_economic_api_status != 200:
            SlackNotifier.send_alert(
                os.getenv("SLACK_ECONOMIC_CALENDAR_WEBHOOK_URL"),
                f"Trading Economics Calendar API Failed\n```status: {trading_economic_api_status}\nReason: {upcoming_trading_economics_events}```"
            )
            return
        
        delta_exchange_api_status, upcoming_delta_exchange_registered_events = DeltaExchangeCalendarAPI.get_delta_calendar_events(start_date, end_date)

        if delta_exchange_api_status != 200:
            SlackNotifier.send_alert(
                os.getenv("SLACK_ECONOMIC_CALENDAR_WEBHOOK_URL"),
                f"Delta Exchange Calendar GET API Failed\n```status: {delta_exchange_api_status}\nReason: {upcoming_delta_exchange_registered_events}```"
            )
            return

        upcoming_delta_exchange_registered_event_ids = {
            str(event["meta_data"]["source_id"])
            for event in upcoming_delta_exchange_registered_events
            if event["meta_data"] and event["meta_data"].get("source_id")
        }

        upcoming_trading_economics_events_to_register = [
            event 
            for event in upcoming_trading_economics_events 
            if event["CalendarId"] not in upcoming_delta_exchange_registered_event_ids
        ]

        upcoming_trading_economics_events_to_register = CalendarEventsAggregator.add_event_descriptions(upcoming_trading_economics_events_to_register) 

        events_to_register_on_delta_exchange = [{
            "title": event["Event"],
            "date": event["Date"][:10], # first 10: YYYY-MM-DD 
            "description": event["description"],
            "category": event["Category"],
            "tags": [event["Ticker"]],
            "created_by": "trading_economics_api",
            "source_id": event["CalendarId"],
            "source_url": f"{os.getenv('TRADING_ECONOMICS_WEB_URL')}{event['URL']}",
            "country": event["Country"],
            "timestamp": calendar.timegm(time.strptime(event["Date"], "%Y-%m-%dT%H:%M:%S"))
        } for event in upcoming_trading_economics_events_to_register]

        upcoming_trading_economics_events_of_push_notification = [
            event
            for event in events_to_register_on_delta_exchange
            if event["tags"][0] in [
                "FDTR", # FOMC
                "CPI YOY",
                "USACIRM",
                "USAPPIM", # PPI
            ]
        ]

        events_to_register_on_delta_exchange = upcoming_trading_economics_events_of_push_notification[:MAX_COUNT_TRADING_ECONOMIC_EVENTS_OF_PUSH_NOTIFICATION]

        CalendarEventsAggregator.register_events_on_delta_exchange(events_to_register_on_delta_exchange)


    @staticmethod
    def get_time_span():
        now = time.time()
        start_date = time.strftime("%Y-%m-%d", time.localtime(now))

        after_time_seconds = 30 * 24 * 60 * 60
        end_date = time.strftime("%Y-%m-%d", time.localtime(now + after_time_seconds))

        return start_date, end_date
    
    @staticmethod
    def add_event_descriptions(events):
        updated_events = []
        for event in events:
            is_scraped, description = TradingEconomicsEventWebPageScrapper.get_event_description(event["URL"])

            if not is_scraped:
                event["description"] = event["Event"]
                SlackNotifier.send_alert(
                    os.getenv("SLACK_ECONOMIC_CALENDAR_WEBHOOK_URL"),
                    f"Trading Economics Web Scrapper Failed\n```Reason: {description}```"
                )
            else:
                event["description"] = description

            updated_events.append(event)

        return updated_events
        
    @staticmethod
    def register_events_on_delta_exchange(events):
        published_events = []
        for event in events:
            delta_exchange_api_status, delta_exchange_api_response = DeltaExchangeCalendarAPI.register_event(event)

            if delta_exchange_api_status != 201:
                SlackNotifier.send_alert(
                    os.getenv("SLACK_ECONOMIC_CALENDAR_WEBHOOK_URL"),
                    f"Delta Exchange Calendar POST API Failed\n```status: {delta_exchange_api_status}\nReason: {delta_exchange_api_response}```"
                )
            else:
                published_events.append({**event, "description": "..."})
        
        if published_events:
            SlackNotifier.send_alert(
                os.getenv("SLACK_ECONOMIC_CALENDAR_WEBHOOK_URL"),
                f"Total {len(published_events)} New Events Published\n```{json.dumps(published_events, indent=2)}```"
            )
