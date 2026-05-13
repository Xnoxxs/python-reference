
from flask import jsonify, request
from flask import Flask
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials
import requests
import os
from google.auth.transport.requests import Request
from google.oauth2 import service_account

app = Flask(__name__)
CORS(app)

# FIREBASE
# Path to the Firebase Admin SDK JSON key
firebase_service_key_path = os.path.join(os.path.dirname(__file__), "firebase_service_key_prod.json")

FIREBASE_PROJECT_NUMBER = "183878051036"  # Hardcode the project number

APP_CHECK_URL = (
    f"https://firebaseappcheck.googleapis.com/v1beta/projects/"
    f"{FIREBASE_PROJECT_NUMBER}:verifyAppCheckToken"
)

# Function to get OAuth2 access token
def get_access_token():
    """Get OAuth2 access token for Firebase App Check API"""
    try:
        credentials = service_account.Credentials.from_service_account_file(
            firebase_service_key_path,
            scopes=['https://www.googleapis.com/auth/firebase']
        )
        credentials.refresh(Request())
        return credentials.token
    except Exception as e:
        print(f"Error getting access token: {e}")
        return None

# GET is used to request repositories
# So here when I call /home, it will return "Welcome to the API" to my app
@app.route('/home', methods=['GET'])
def home():
    ok, result = verify_app_check()
    if not ok:
        return jsonify({"error": "Unauthorized", "details": result}), 401
    return jsonify("Welcome to the API!")

# POST is used to perform actions and if you want , return a result
# For example, when I call /images I am adding 2 + 2 and returning the result to my app
@app.route('/images', methods=['POST'])
def add():
    result = 2 + 2
    response = {
        "message": "The result of 2 + 2 is",
        "result": result
    }
    return jsonify(response), 200


def verify_app_check():
    token = request.headers.get("X-Firebase-AppCheck")
    if not token:
        return False, "❌ Missing App Check token in request headers"

    payload = {"appCheckToken": token}

    # Get OAuth2 access token
    access_token = get_access_token()
    if not access_token:
        return False, "❌ Failed to get OAuth2 access token"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    try:
        resp = requests.post(
            APP_CHECK_URL,
            json=payload,
            headers=headers,
            timeout=5
        )

        print("🔹 App Check verification request:")
        print(f"  URL: {resp.request.url}")
        print(f"  Headers: {resp.request.headers}")
        print(f"  Body Sent: {resp.request.body}")
        print(f"🔹 App Check response:")
        print(f"  Status: {resp.status_code}")
        print(f"  Body: {resp.text}")

        if resp.status_code == 200:
            decoded = resp.json()
            return True, decoded
        else:
            return False, {
                "status_code": resp.status_code,
                "error": resp.text,
                "url": resp.request.url
            }

    except Exception as e:
        return False, f"❌ Exception while verifying App Check: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)







