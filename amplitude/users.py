
import requests
import json
from config.variables import MyVariables

# When you set the user properties,
#The Amplitude UI doesn’t always refresh immediately.
# You usually need to trigger another event from that user,
# so the user profile updates.

def set_user_properties(user_id: str, user_properties: dict):
    url = "https://api2.amplitude.com/2/httpapi"

    payload = {
        "api_key": MyVariables.amplitude_api_key,
        "events": [
            {
                "user_id": user_id,
                "event_type": "$identify",
                "user_properties": user_properties
            }
        ]
    }

    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=json.dumps(payload), headers=headers)

    if response.status_code == 200:
        print("User properties set successfully ✅")
    else:
        print(f"Error {response.status_code}: {response.text}")

"""
# Example usage
send_event(
    user_id="user_123",
    event_name="reviews",
    event_properties={
        "booking_id": 456,
        "activity": "Jet Ski",
        "amount": 120,
        "currency": "EUR"
    }
)
"""


def remove_user_property(user_id: str, property_name: str):
    url = "https://api2.amplitude.com/2/httpapi"

    payload = {
        "api_key": MyVariables.amplitude_api_key,
        "events": [
            {
                "user_id": user_id,
                "event_type": "$identify",
                "user_properties": {
                    "$unset": [property_name]  # ✅ remove this custom property
                }
            }
        ]
    }

    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=json.dumps(payload), headers=headers)

    if response.status_code == 200:
        print(f"✅ User property '{property_name}' unset successfully")
    else:
        print(f"❌ Error {response.status_code}: {response.text}")


# Example usage
remove_user_property("user_123", "gender")

