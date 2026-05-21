
import pytest
from sqlalchemy.orm import sessionmaker

from config.initialize import app, db


@pytest.fixture
def db_transaction():
    with app.app_context():
        # Create a connection to database (like a sort of tunnel)
        connection = db.engine.connect()
        # Database says: "Okay, I will temporarily track all changes on this connection."
        transaction = connection.begin()

        # Create a session tied to this connection
        # This is what allows you to execute operations onto the database

        Session = sessionmaker(bind=connection)
        session = Session()

        # It is the pause point where pytest runs your test, then comes when it is over.
        yield session

        session.close()
        # This command reverts the changes
        transaction.rollback()
        # To apply the changes to db, you would do:
        # transaction.commit()

        # Close this connection with database
        connection.close()

