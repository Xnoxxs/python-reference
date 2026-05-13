




from flask import jsonify
import requests
from config.variables import MyVariables

def insert():

    try:

        # Inserting a user to table "users"

        mutation1 = '''
            mutation {
              insert_users_one(object: { name: "Hamza", email: "hamza@example.com" }) {
                id
                name
                email
              }
            }
        '''
        # With variables
        mutation2 = '''
            mutation ($user: users_insert_input!) {
              insert_users_one(object: $user) {
                id
                name
                email
              }
            }

        '''

        # Define variables
        variables = {
            "name": "Hamza",
            "email": "hamza@example.com"
        }

        # You can replace this part with the execute() function to maintain centralized code
        response = requests.post(
            MyVariables.hasura_url,
            json={
                "query": mutation2,
                "variables": variables
            },
            headers={
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