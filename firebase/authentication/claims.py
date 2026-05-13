

from firebase_admin import auth
import os

from flask import Flask
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials


app = Flask(__name__)
CORS(app)

# FIREBASE
# Path to the Firebase Admin SDK JSON key
firebase_service_key_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),  # -> /Users/skr/Documents/AnchitaFolder/Server
    "firebase_service_key_prod.json",
)
# Initialize Firebase Admin SDK
cred = credentials.Certificate(firebase_service_key_path)

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://anchita-5673c-default-rtdb.europe-west1.firebasedatabase.app',
    'storageBucket': 'anchita-5673c.appspot.com'  # 👈 Add your Firebase Storage bucket here
    # Replace with your actual Realtime Database URL
    # Open the Firebase Console.
    # Select your project.
    # Navigate to Realtime Database in the left-hand menu.
    # Look for the URL displayed at the top, which typically looks like:
    # https://your-database-name.firebaseio.com/
})

def set_pg_id_for_user(uid, pg_id):
    try:
        auth.set_custom_user_claims(uid, {"database_id": pg_id})
        user = auth.get_user(uid)
        print("Custom claims:", user.custom_claims)

    except Exception as e:
        print(f"Error: {e}")

from firebase_admin import auth

def delete_pg_id_for_user(uid: str):
    try:
        # Fetch the current user
        user = auth.get_user(uid)
        claims = user.custom_claims or {}

        # Delete only database_id if it exists
        if "database_id" in claims:
            del claims["database_id"]

        # Update the user's claims (without database_id)
        auth.set_custom_user_claims(uid, claims)

        print(f"Updated claims for {uid}: {claims}")
    except Exception as e:
        print(f"Error deleting database_id for {uid}: {e}")


#set_pg_id_for_user(uid="enje84C3tDdQaPGTRWqvlofg4RY2", pg_id=3)

#delete_pg_id_for_user(uid="enje84C3tDdQaPGTRWqvlofg4RY2")

uid = "SyZ15EzWWucsRkpkCQ2bSQmrv193"
user = auth.get_user(uid)

print(f"Custom claims: {user.custom_claims}")