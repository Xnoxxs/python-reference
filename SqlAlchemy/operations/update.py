
from train.ORM.initialize import app, db
from train.ORM.models.booking import Booking
from train.ORM.models.user import User

from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy.dialects.postgresql import ARRAY, JSON

# Basic Update operation - All together
def update_user():
    db.session.query(Booking).filter(
        Booking.id == 1,
        Booking.user.has(authentication_id="ZklDmbWXmibm7TcUGpPPNPheakG2")
    ).update({
        Booking.people: 3,
    })

# Basic Update operation - Separated
def update1_user(authentication_id, new_name, new_device_token):
    user = db.session.query(User).filter_by(authentication_id=authentication_id).first()

    if not user:
        print("User not found")
        return

    user.name = new_name
    user.devices_tokens.append(new_device_token)
    # If the column type is mutable (like ARRAY or JSON in PostgreSQL),
    # SQLAlchemy might not detect internal list mutation.
    # flag_modified explicitly tells SQLAlchemy that the field changed.
    flag_modified(user, "devices_tokens")

    db.session.commit()
    print("User updated successfully")

# Passing in all new repositories in a single variable
def update2_user(authentication_id, data):
    user = db.session.query(User).filter_by(authentication_id=authentication_id).first()

    if not user:
        print("User not found")
        return

    # Get real db_setup column names
    columns = User.__table__.columns.keys()

    for key, value in data.items():

        # Only update actual DB columns
        if key in columns:

            # Set the new value on the instance
            # This marks the field as "updated" so SQLAlchemy knows it changed
            setattr(user, key, value)

            # Handle mutable PostgreSQL types (ARRAY, JSON)
            column = User.__table__.columns[key]

            # If the column type is mutable (like ARRAY or JSON in PostgreSQL),
            # SQLAlchemy may not automatically detect internal modifications.
            # flag_modified explicitly tells SQLAlchemy that the field changed.
            if isinstance(column.type, (ARRAY, JSON)):
                flag_modified(user, key)

    db.session.commit()
    print("User updated successfully")

# General Update Operation
def update_record(instance, data: dict):
    # Get the model class from the instance (e.g., User, Activity, Owner)
    model_class = type(instance)

    # Retrieve the names of actual db_setup columns defined in the table
    # This prevents updating relationships or non-column attributes
    columns = model_class.__table__.columns.keys()

    # Loop through each key-value pair provided in the update dictionary
    for key, value in data.items():

        # Only update the field if it exists as a real db_setup column
        if key in columns:

            # Set the new value on the instance
            # This marks the field as "updated" so SQLAlchemy knows it changed
            setattr(instance, key, value)

            # Get the column metadata from the model's table definition
            column = model_class.__table__.columns[key]

            # If the column type is mutable (like ARRAY or JSON in PostgreSQL),
            # SQLAlchemy may not automatically detect internal modifications.
            # flag_modified explicitly tells SQLAlchemy that the field changed.
            if isinstance(column.type, (ARRAY, JSON)):
                flag_modified(instance, key)

    # Commit the transaction to persist changes to the db_setup
    db.session.commit()
    print(f"{instance} updated successfully")

    # Return the updated instance (optional but useful for chaining or returning response repositories)
    return instance

if __name__ == "__main__":

    # You are using Flask-SQLAlchemy APIs that require an active application context to work.
    with app.app_context():
        id = "4UGBbsCCCzfHyARljLpbDUx4Hbc2"

        update1_user(
            authentication_id=id,
            new_name="New Hamza",
            new_device_token="hM9x2gk3fU"
        )


