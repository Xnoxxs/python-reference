
import requests

HASURA_URL = "https://your-hasura-instance/v1/metadata"
ADMIN_SECRET = "your-admin-secret"

def reload_metadata():
    payload = {
        "type": "reload_metadata",
        "args": {}
    }

    response = requests.post(
        HASURA_URL,
        json=payload,
        headers={
            "Content-Type": "application/json",
            "x-hasura-admin-secret": ADMIN_SECRET,
        }
    )

    response.raise_for_status()
    return response.json()
