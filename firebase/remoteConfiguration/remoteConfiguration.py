

import json
import requests
from google.auth.transport.requests import Request
from google.oauth2 import service_account

from initialize_firebase import firebase_service_key_path, project_id

# Firebase Remote Config API URL
REMOTE_CONFIG_URL = f"https://firebaseremoteconfig.googleapis.com/v1/projects/{project_id}/remoteConfig"


# Function to get access token for Firebase Remote Config
def get_access_token():
    SCOPES = ["https://www.googleapis.com/auth/firebase.remoteconfig"]

    try:
        creds = service_account.Credentials.from_service_account_file(
            firebase_service_key_path, scopes=SCOPES
        )
        creds.refresh(Request())  # Refresh token

        return creds.token

    except Exception as e:
        print(f"Error retrieving access token: {e}")
        return None


# Function to fetch Firebase Remote Config
def get_remote_config():
    try:
        token = get_access_token()
        if not token:
            print("Failed to retrieve access token.")
            return None

        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
        }

        response = requests.get(REMOTE_CONFIG_URL, headers=headers)

        if response.status_code == 200:
            config_data = json.loads(response.text)
            return config_data
        else:
            print(f"Error fetching Remote Config: {response.text}")
            return None

    except Exception as e:
        print(f"Exception occurred: {e}")
        return None


# Function to extract a specific parameter value from Firebase Remote Config
def get_remote_config_value(key):

    try:
        if key in get_remote_config().get("parameters", {}):
            return get_remote_config()["parameters"][key]["defaultValue"]["value"]
        else:
            print(f"'{key}' not found in Remote Config.")
            return None
    except Exception as e:
        print(f"Error retrieving '{key}': {e}")
        return None


