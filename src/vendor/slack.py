import os
import requests
import json
from src.util import logger
import time

class SlackNotifier:
    @staticmethod
    def send_alert(message, retry_count=3):
        success = False
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
                success = True
            else:
                logger.error(f"Failed to send slack message. Status code: {response.status_code}, Response: {response.text}")
        except Exception as e:
            logger.error(f"An error occurred while sending slack alert: {e}")
        finally:
            if not success and retry_count > 0:
                time.sleep(2)
                logger.info(f"Retrying to send slack alert. Remaining retries: {retry_count - 1}")
                SlackNotifier.send_alert(message, retry_count - 1) if retry_count > 0 else None
