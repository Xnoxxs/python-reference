

# Multiple mutations in one query
batch1 = """
    mutation BatchOperation {
      insert_activities_one(
        objects: { name: "Jet Ski", price: 120 }
      ) {
        affected_rows
      }
    
      delete_activity_media(where: { id: { _eq: 42 } }) {
        affected_rows
      }
    }
"""

# If in the batch, if you have two of the same mutation types, you need to differentiate them
# Ex - Here I am calling "insert_activities_one" twice,
#       therefore, I had to put second: for the second one to differentiate them
# else it will cause an error, this is how graphQL works
"""
    mutation BatchOperation {
      insert_activities_one(
          objects: { name: "Boat Ride", price: 300 }
      ) {
        affected_rows
      }
      
      delete_activity_media(where: { id: { _eq: 42 } }) {
        affected_rows
      }
      
      second:insert_activities_one(
        objects: { name: "Jet Ski", price: 120 }
      ) {
        affected_rows
      }
    }
"""

# You can reference the output of one mutation in another

"""
mutation {
      newBooking: insert_bookings_one(
         object: {user_id: "user_123",activity_id: "activity_456",date: "2025-11-04T10:00:00Z"}
     ) {
       id
     }
     newTransaction: insert_transactions_one(
         object: {
            booking_id: newBooking.id,
            payment_id: "pi_3QdExampleStripeId123"}
     ) {
       id
     }
    }

}


"""