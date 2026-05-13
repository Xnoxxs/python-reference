

from flask import jsonify
import requests
from config.variables import MyVariables

def get_user():

    user_auth_id = "XXXXXXXX" # get the firebase_users id of the user from the request
    try:
        query = '''
            query getUser {
              users {
                  id
                  name
              }
            }
        '''

        # You can replace this part with the execute() function to maintain centralized code
        response = requests.post(
            MyVariables.hasura_url,
            json={"query": query},
            headers={
                "x-hasura-role": "authenticated_user",  # ✅ assigned by server
                "x-hasura-user-firebase_users-id": user_auth_id,  # ✅ Firebase uid

                "x-hasura-admin-secret": MyVariables.hasura_admin_secret,
                "Content-Type": "application/json",
            }
        )

        # Raise error if request failed
        response.raise_for_status()

        data = response.json()
        if "errors" in data:
            raise Exception(f"GraphQL Error: {data['errors']}")

        print(f"repositories: {data}")
        return jsonify(data["repositories"]["users"][0]), 200
    except Exception as e:
        return jsonify(str(e)), 500