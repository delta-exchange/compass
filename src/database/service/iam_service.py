import os
import requests


class IAMService:
    @staticmethod
    def get_decrypted_data(encrypted_data):
        BASE_URL = os.getenv("DELTA_EXCHANGE_IAM_API_BASE_URL")
        request_payload = {
            "documents": encrypted_data
        }
        response = requests.post(f"{BASE_URL}/v2/support/decrypt_data", json=request_payload)
        response.raise_for_status() 
        return response.json().get("result")