from flask import jsonify
import requests
from config.variables import MyVariables


def insert_booking_and_transaction():
    try:
        # ✅ Define the GraphQL mutation with variables
        mutation = '''
            mutation InsertBookingAndTransaction(
                $booking_data: bookings_insert_input!, 
                $transaction_data: transactions_insert_input!
            ) {

              newBooking: insert_bookings_one(object: $booking_data) {
                id
              }

              newTransaction: insert_transactions_one(object: $transaction_data) {
                id
              }
            }
        '''

        # ✅ Example variable repositories (hardcoded for now)
        variables = {
            "booking_data": {
                "user_id": "user_123",
                "activity_id": "activity_456",
                "date": "2025-11-04T10:00:00Z"
            },
            "transaction_data": {
                "booking_id": 789,  # You can dynamically link if doing from code
                "amount": 120.00,
                "stripe_id": "pi_3QdExampleStripeId123"
            }
        }

        # ✅ Send the request to Hasura
        response = requests.post(
            MyVariables.hasura_url,
            json={
                "query": mutation,
                "variables": variables
            },
            headers={
                "x-hasura-admin-secret": MyVariables.hasura_admin_secret,
                "Content-Type": "application/json",
            }
        )

        # ✅ Raise if the request failed
        response.raise_for_status()
        data = response.json()

        # ✅ Handle GraphQL-level errors
        if "errors" in data:
            raise Exception(f"GraphQL Error: {data['errors']}")

        # ✅ Print and return successful repositories
        print("✅ Mutation succeeded:", data["repositories"])
        return jsonify(data["repositories"]), 200

    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({"error": str(e)}), 500
