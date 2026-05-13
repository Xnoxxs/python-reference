


import requests
import json
from config.variables import MyVariables

def send_event(user_id: str, event_name: str, event_properties: dict = None):
    url = "https://api2.amplitude.com/2/httpapi"

    payload = {
        "api_key": MyVariables.amplitude_api_key,
        "events": [
            {
                "user_id": user_id,
                "event_type": event_name,
                "event_properties": event_properties or {}
            }
        ]
    }

    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=json.dumps(payload), headers=headers)


    if response.status_code == 200:
        print("Event sent successfully ✅")
    else:
        print(f"Error {response.status_code}: {response.text}")

send_event("user_123", "profile_refresh")

send_event(
    user_id = "user_789",
    event_name = "booking_made",
    event_properties = {
        "booking_id": 12345,
        "activity": "Jet Ski",
        "activity_id": 678,
        "price": 400,
        "currency": "EUR",
        "location": "Casablanca",
        "date": "2025-09-20T14:00:00Z",
        "payment_type": "card",
        "participants": 2
    }
)





