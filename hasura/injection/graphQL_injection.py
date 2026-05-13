
# Let say I get these from the body of the http request
name = "Hamza"
email = "hamza@example.com"

mutation1 = f"""
    mutation InsertUser {{
      insert_users_one(
        object: {{
            name: {name},
            email: {email}
        }}
      ) 
      {{
        id
        name
        email
      }}
    }}
"""

# Hacker modifies "name" and puts this query instead
name = '"Hamza"}}) {{id}}, delete_users(where: {{}}) {{affected_rows}} , second:insert_users_one(object: {{name:"Evil",'
# Result: All users are deleted
mutation = f'''
    mutation InsertUser {{
      insert_train_one(
          object: {{
            name: "Hamza"
      }}) {{
        id
      }},
      delete_train(where: {{}}) {{
        affected_rows
      }},
      second: insert_train_one(
          object: {{
            name:"Evil",
            email: "{email}"   
          }}
          ) {{
            id
            name
            email
          }}
        }}
'''