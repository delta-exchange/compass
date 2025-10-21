import os
import time
import calendar
import json
from .trading_economics import TradingEconomicsCalendarAPI, TradingEconomicsEventWebPageScrapper
from .delta_exchange import DeltaExchangeCalendarAPI
from src.vendor import SlackNotifier
from src.util import logger

class CalendarEventsAggregator:

    @staticmethod
    def run_india(): 
        logger.info(f"running calendar events aggregator for India: {os.getenv('TRADING_ENGINE_MASTER_URL')}")
        CalendarEventsAggregator.execute()

    @staticmethod
    def run_global(): 
        TRADING_ENGINE_MASTER_URL = os.getenv("TRADING_ENGINE_MASTER_URL")
        os.environ['TRADING_ENGINE_MASTER_URL'] = os.getenv("TRADING_ENGINE_GLOBAL_MASTER_URL")
        logger.info(f"running calendar events aggregator for Global: {os.getenv('TRADING_ENGINE_MASTER_URL')}")
        CalendarEventsAggregator.execute(env="Global")
        os.environ['TRADING_ENGINE_MASTER_URL'] = TRADING_ENGINE_MASTER_URL

    @staticmethod
    def execute(env="India"):
        try:
            start_date, end_date = CalendarEventsAggregator.get_time_span()

            trading_economic_api_status, upcoming_trading_economics_events = TradingEconomicsCalendarAPI.get_calendar_events(start_date, end_date)

            if trading_economic_api_status != 200:
                SlackNotifier.send_alert(
                    os.getenv("SLACK_ECONOMIC_CALENDAR_WEBHOOK_URL"),
                    f"<!here> Trading Economics Calendar API Failed\n```status: {trading_economic_api_status}\nReason: {upcoming_trading_economics_events}```"
                )
                return
            
            upcoming_trading_economics_events = [
                event
                for event in upcoming_trading_economics_events
                if event["Ticker"] in [
                    "FDTR", # FOMC
                    "CPI YOY",
                    "USACIRM",
                    "USAPPIM", # PPI
                ]
            ]

            upcoming_trading_economics_events = CalendarEventsAggregator.add_event_descriptions(upcoming_trading_economics_events)

            events_to_register_on_delta_exchange = [{
                "title": CalendarEventsAggregator.get_delta_title(event["Event"], event["Ticker"]),
                "date": event["Date"][:10], # first 10: YYYY-MM-DD 
                "description": event["description"],
                "category": event["Category"],
                "tags": [event["Ticker"]],
                "created_by": "trading_economics_api",
                "source_id": event["CalendarId"],
                "source_url": CalendarEventsAggregator.get_trading_economics_event_url(event),
                "country": event["Country"],
                "timestamp": calendar.timegm(time.strptime(event["Date"], "%Y-%m-%dT%H:%M:%S"))
            } for event in upcoming_trading_economics_events]

            delta_exchange_api_status, upcoming_delta_exchange_registered_events = DeltaExchangeCalendarAPI.get_delta_calendar_events(start_date, end_date)

            if delta_exchange_api_status != 200:
                SlackNotifier.send_alert(
                    os.getenv("SLACK_ECONOMIC_CALENDAR_WEBHOOK_URL"),
                    f"<!here> Delta Exchange Calendar GET API Failed\n```status: {delta_exchange_api_status}\nReason: {upcoming_delta_exchange_registered_events}```"
                )
                return
            
            delta_event_identifiers = set([event["title"] + "-" + event["date"] for event in upcoming_delta_exchange_registered_events] + [event["source_url"] for event in upcoming_delta_exchange_registered_events if "source_url" in event])
            
            uniq_events_to_register_on_delta_exchange = []
            for event in events_to_register_on_delta_exchange:
                if event["title"] + "-" + event["date"] not in delta_event_identifiers and event["source_url"] not in delta_event_identifiers:
                    delta_event_identifiers.add(event["title"] + "-" + event["date"])
                    delta_event_identifiers.add(event["source_url"])
                    uniq_events_to_register_on_delta_exchange.append(event)
                else:
                    logger.info(f"Event already registered on delta exchange: {event}")

            CalendarEventsAggregator.register_events_on_delta_exchange(uniq_events_to_register_on_delta_exchange)
        except Exception as e:
            logger.error(f"Error in calendar events aggregator: {e}")
            SlackNotifier.send_alert(
                os.getenv("SLACK_ECONOMIC_CALENDAR_WEBHOOK_URL"),
                f"<!here> ({env})Error in calendar events aggregator\n```Reason: {e}```"
            )

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
                    f"<!here> Trading Economics Web Scrapper Failed\n```Reason: {description}```"
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
                    f"<!here> Delta Exchange Calendar POST API Failed\n```status: {delta_exchange_api_status}\nReason: {delta_exchange_api_response}```"
                )
            else:
                published_events.append({**event, "description": "..."})
        
        if published_events:
            SlackNotifier.send_alert(
                os.getenv("SLACK_ECONOMIC_CALENDAR_WEBHOOK_URL"),
                f"<!here> Total {len(published_events)} New Events Published\n```{json.dumps(published_events, indent=2)}```"
            )
        else:
            SlackNotifier.send_alert(
                os.getenv("SLACK_ECONOMIC_CALENDAR_WEBHOOK_URL"),
                f"<!here> No New Events Published"
            )

    @staticmethod
    def get_delta_title(title, ticker):
        if ticker == "FDTR":
            return "FOMC:Federal Open Market Committee Meeting"
        if ticker == "CPI YOY" or ticker == "USACIRM":
            return "US CPI:US Consumer Price Index"
        if ticker == "USAPPIM":
            return "US PPI:US Producer Price Index"

        return title
    
    @staticmethod
    def get_trading_economics_event_url(event):
        return f"{os.getenv('TRADING_ECONOMICS_WEB_URL')}{event['URL']}"