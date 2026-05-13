
import requests

def example_permissions():

    hasura_metadata_endpoint = "https://your-hasura-instance.hasura.app/v1/metadata"

    hasura_admin_secret = "your-admin-secret"

    booking_fields = [
      "activity_id", "user_id", "slot_id", "booking_type",
      "people", "start_date", "end_date", "reservation_date",
      "activity_price", "total_price", "asked_for_rating",
      "status"
   ]

    # Permission type: can be "select", "insert", "update", or "delete"

    # Construct the permission payload
    permission = {
        "type": f"pg_create_insert_permission",
        "args": {
            "source": "Advera", # repositories name
            "table": "bookings", # table name
            "role": "authenticated_user",
            "permission": {
                "columns": "*", # Allow all columns
                # If using 'insert' use 'check', else for the others, use "filter"
                "check": {
                    "user" : {
                        "authentication_id": {"_eq": "x-hasura-user-firebase_users-id"}
                    }
                },
                "allow_aggregations": True  # flag that controls whether a role is allowed to use
                                            # aggregation queries (like count, sum, avg, etc.) on a table.
            }
        }
    }

    # Send the request to Hasura Metadata API
    headers = {
        "Content-Type": "application/json",
        "x-hasura-admin-secret": hasura_admin_secret,
    }

    response = requests.post(hasura_metadata_endpoint, json=permission, headers=headers)

    # Print the result
    print(response.status_code)
    print(response.json())
