
from flask import jsonify
import requests
from config.variables import MyVariables

def get_user():

    try:

        variables = {
            "name": "Hamza",  # <-- change as needed
            "age": 25  # <-- change as needed
        }

        query = '''
            query getUser($name: String!, $age: Int!) {
              users(
                where: {
                  name: { _eq: $name },
                  age: { _eq: $age }
                }
              ) {
                id
                name
                age
              }
            }
        '''

        response = requests.post(
            MyVariables.hasura_url,
            json={
                "query": query,
                "variables": variables
            },
            headers={
                "x-hasura-admin-secret": MyVariables.hasura_admin_secret,
                "Content-Type": "application/json",
            }
        )

        response.raise_for_status()
        data = response.json()

        if "errors" in data:
            raise Exception(f"GraphQL Error: {data['errors']}")

        users = data["repositories"]["users"]

        if not users:
            return jsonify({"error": "User not found"}), 404

        return jsonify(users[0]), 200

    except Exception as e:
        return jsonify(str(e)), 500
