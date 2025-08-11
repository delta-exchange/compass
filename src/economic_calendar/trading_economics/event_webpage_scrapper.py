import os
import requests
from bs4 import BeautifulSoup

class TradingEconomicsEventWebPageScrapper:
    @staticmethod
    def get_event_description(event_url):
        url = f"{os.getenv('TRADING_ECONOMICS_WEB_URL')}{event_url}"
        
        response = requests.get(url, headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
        })

        if response.status_code != 200:
            return False, response.text

        soup = BeautifulSoup(response.text, "html.parser")
        description_div = soup.find("div", id="historical-desc")

        if not description_div:
            return False, f"Event page description <div> not found. Page url: {url}"
        
        description_header = description_div.find("h2", id = "description")
        if not description_header:
            return False, f"Event page description <h2> not found. Page url: {url}"
        
        # remove child span inside <h2>
        description_header.find("span").decompose() 

        return True, description_header.get_text(strip=True)