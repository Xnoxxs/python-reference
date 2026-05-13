

# Basic query - get users
query1 = '''
    query getUsers {
      users {
          id
          name
      }
    }
'''

query2 = '''
    query getUser {
      users_by_pk(id: 1) {
        id
        email
        name
        created_at
      }
    }

'''

# Query users by filtering: id != 1 / country == "Spain" / age > 25 / name == "Jack" or "Mark"
# Order by newest created: DESC order large → Small / New → old / A → Z
# get a max of 20

query3 = '''
    query getUser {
      users(
        where: {
          id: { _neq: 1 }
          country: { _eq: "Spain" }
          age: { _gt: 25 }
          name: { _in: ["Jack", "Mark"] }
        }
        order_by: { created: desc }
        limit: 20
      ) 
      {
        id
        name
      }
    }
'''

# Query a table and get it relation
query4 = '''
    query getBookings {
      bookings {
        id
        date
        price
        review {
            id
            score
        }
      }
    }
'''

# Query a table and filter by value in its relation
query5  = '''
    query getBookings {
      bookings (
        where : {
            review: {
               score: { _lt: 4 }
            }
        }
      ) {
        id
        date
        price
        review {
            id
            score
        }
      }
    }
'''

# Get the count of a relation (like how many bookings each user has)
query6 = '''
query {
  users {
    id
    name
    booking_aggregate {
      aggregate {
        count
      }
    }
  }
}
'''

