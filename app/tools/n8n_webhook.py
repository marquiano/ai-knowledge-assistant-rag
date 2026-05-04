import os
import requests
from dotenv import load_dotenv

load_dotenv()

N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL")


def send_n8n_alert(payload: dict) -> dict:
    if not N8N_WEBHOOK_URL:
        return {
            "sent": False,
            "reason": "N8N_WEBHOOK_URL not configured"
        }

    try:
        response = requests.post(
            N8N_WEBHOOK_URL,
            json=payload,
            timeout=10
        )

        return {
            "sent": response.ok,
            "status_code": response.status_code,
            "response": response.text[:500]
        }

    except Exception as error:
        return {
            "sent": False,
            "reason": str(error)
        }