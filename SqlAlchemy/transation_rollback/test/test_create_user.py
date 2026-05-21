

from config.initialize import app, db
from app.models.user import User

TEST_AUTH_ID = "TEST_UID_123"

# python -m pytest path/transaction_rollback.py -s

def test_create_user(db_transaction):
    """
    When you add db_transaction() fixture from conftest in the test’s parameters:
    This test
    pytest executes test_create_user
        → sees parameters: app, user, db_transaction
        → looks up fixtures with those names (conftest.py)
        → runs fixtures in dependency order
        → So now, db_transaction() creates a connection with the db ( a session )
        → due to yield session in db_transaction(), code in the function is executed within this ( session )
        → after yield, db_transaction() executes the next step, which is rollback
    """
    session = db_transaction

    print("\n=== BEFORE INSERT ===")

    before_user = (
        session.query(User)
        .filter(User.authentication_id == TEST_AUTH_ID)
        .first()
    )
    print(f"User before insert: {before_user}")

    new_user = User(
        authentication_id=TEST_AUTH_ID,
        name="Hamza",
        email="hamza@test.com",
        password="123456",
        photo="https://example.com/photo.png",
        devices_tokens=[],
    )

    session.add(new_user)

    # flush() sends SQL but stays inside the open connection transaction.
    # It does NOT persist until transaction.commit() in the fixture teardown
    # (when PERSIST_TEST_DATA is True). Skipping rollback alone is not enough.
    session.flush()

    print("\n=== AFTER FLUSH (visible in this session until commit/rollback) ===")

    retrieved_user = (
        session.query(User)
        .filter(User.authentication_id == TEST_AUTH_ID)
        .first()
    )
    print(f"Retrieved user: {retrieved_user}")

    assert retrieved_user is not None
    assert retrieved_user.name == "Hamza"
    assert retrieved_user.email == "hamza@test.com"

    print("\n=== USER EXISTS INSIDE TEST ===")
    print(f"User ID: {retrieved_user.id}")
    print(f"User Name: {retrieved_user.name}")


if __name__ == "__main__":
    import pytest

    exit_code = pytest.main([__file__, "-s"])

    with app.app_context():
        user_after_test = (
            db.session.query(User)
            .filter(User.authentication_id == TEST_AUTH_ID)
            .first()
        )
        if ACTIVATE_ROLLBACK:
            expected = "None (rolled back)"
        else:
            expected = "present (committed)"
        print(f"User after test teardown (expect {expected}): {user_after_test}")

    raise SystemExit(exit_code)

