



from flask import jsonify
import requests
from config.variables import MyVariables

def update():

    try:

        # Updating a user in table "users"

        mutation1 = '''
            mutation {
              update_users_by_pk(
                pk_columns: { id: 12 },
                _set: { email: "new.email@example.com" }
              ) {
                id
                name
                email
              }
            }
        '''

        # With variables
        variables = {
            "user_id": 2,
            "user_data": {
                "email": "hamza@example.com",
                "name": "Hamza"
            }
        }

        mutation2 = '''
            mutation (
                $user_id: Int!, 
                $user_data: users_set_input!
            ) {
              update_users_by_pk(pk_columns: {id: $user_id}, _set: $user_data) {
                id
                name
                email
              }
            }
        '''

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