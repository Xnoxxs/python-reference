
from train.ORM.initialize import app, db
from train.ORM.models.user import User

# Basic Insert operation
def insert1_user(authentication_id, name, email, devices_tokens):

    new_user = User(
        authentication_id=authentication_id,
        name=name,
        email=email,
        devices_tokens=devices_tokens
    )

    db.session.add(new_user)   # Add instance to session
    db.session.commit()        # Persist to db_setup

    print("User inserted successfully")
    return new_user

# Passing in all new repositories in a single variable
def insert2_user(data: dict):

    # Get real db_setup column names
    columns = User.__table__.columns.keys()

    # Keep only valid columns (don't include all attributes)
    final_data = {
        key: value for key, value in data.items()
        if key in columns
    }

    new_user = User(**final_data)

    db.session.add(new_user)
    db.session.commit()

    print("User inserted successfully")
    return new_user

# General Insert Operation
def insert_record(model_class, data: dict):

    # Get real db_setup columns
    columns = model_class.__table__.columns.keys()

    # Filter only valid columns
    final_data = {
        key: value for key, value in data.items()
        if key in columns
    }

    new_instance = model_class(**final_data)

    db.session.add(new_instance)
    db.session.commit()

    print(f"{new_instance} inserted successfully")

    return new_instance

if __name__ == "__main__":

    # You are using Flask-SQLAlchemy APIs that require an active application context to work.
    with app.app_context():
        id = "4UGBbsCCCzfHyARljLpbDUx4Hbc2"

        insert1_user(
            authentication_id="auth_999",
            name="Hamza",
            email="hamza@email.com",
            devices_tokens=["token1"]
        )

        insert2_user({
            "authentication_id": "auth_1000",
            "name": "New User",
            "email": "new@email.com",
            "devices_tokens": ["tokenA"],
            "push_notifications_permission": True
        })

        insert_record(User, {
            "authentication_id": "auth_2000",
            "name": "Generic Insert",
            "email": "generic@email.com",
            "devices_tokens": ["tokenX"]
        })
