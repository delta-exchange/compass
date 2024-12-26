import os
import requests
import json
from src.util import logger

class SlackNotifier:
    @staticmethod
    def send_alert(message):
        try:
            webhook_url = os.getenv("SLACK_WEBHOOK_URL")
            channel = os.getenv("SLACK_CHANNEL")
            payload = {"channel": channel, "text": message}
            response = requests.post(
                webhook_url,
                data=json.dumps(payload),
                headers={'Content-Type': 'application/json'}
            )
            if response.status_code == 200:
                logger.info("Slack message sent successfully")
            else:
                logger.error(f"Failed to send slack message. Status code: {response.status_code}, Response: {response.text}")
        except Exception as e:
            logger.error(f"An error occurred while sending slack alert: {e}")
