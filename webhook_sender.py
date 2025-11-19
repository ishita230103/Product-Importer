# backend/app/services/webhook_sender.py

import requests

def send_test_webhook(url: str, event: str):
    """
    Sends a simple webhook test payload.
    """

    payload = {
        "event": event,
        "message": "Test webhook from Product Importer",
        "status": "ok"
    }

    try:
        res = requests.post(url, json=payload, timeout=5)
        return {
            "status_code": res.status_code,
            "response": res.text[:500]  # limit size for safety
        }
    except Exception as e:
        return {"error": str(e)}
