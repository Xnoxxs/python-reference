
# rollback_demo.py — run: python rollback_demo.py
from sqlalchemy.orm import sessionmaker

from config.initialize import app, db
from app.models.user import User

TEST_AUTH_ID = "TEST_UID_123"
DO_ROLLBACK = True  # False → commit and user stays in DB

def main():
    with app.app_context():
        # Create a connection to database (like a sort of tunnel)
        connection = db.engine.connect()
        # Database says: "Okay, I will temporarily track all changes on this connection using transaction."
        transaction = connection.begin()

        # Create a session tied to this connection
        # This is what allows you to execute operations onto the database
        Session = sessionmaker(bind=connection)
        session = Session()

        try:

            session.add(
                User(
                    authentication_id=TEST_AUTH_ID,
                    name="Hamza",
                    email="hamza@test.com",
                    password="123456",
                    photo="https://example.com/photo.png",
                    devices_tokens=[],
                )
            )
            # At this point the user: session.add(User(...)),  exists ONLY in Python memory.
            # flush() sends the SQL statement to the database immediately
            # But DOES NOT permanently save the sql statement
            session.flush()
            print("After flush (same transaction):", session.query(User).filter_by(authentication_id=TEST_AUTH_ID).first())

            # After flush:
            # Database row exists temporarily
            # BUT:
            # Transaction not finalized yet
            # Meaning:
            # rollback can still erase it
            # commit can still save it

        finally:
            session.close()
            # Checks whether this transaction is still open/alive.
            if transaction.is_active:
                if DO_ROLLBACK:
                    transaction.rollback()
                    print("Rolled back — changes undone")
                else:
                    transaction.commit()
                    print("Committed — changes saved")
            connection.close()

    # CHECK: Retrieve user to see if he is in database or not
    with app.app_context():
        after = (
            db.session.query(User)
            .filter(User.authentication_id == TEST_AUTH_ID)
            .first()
        )
        print("Is user in database:", after)

if __name__ == "__main__":
    main()