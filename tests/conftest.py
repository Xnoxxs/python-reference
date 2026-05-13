
import pytest
from flask import Flask


@pytest.fixture
def app():
    """
    Creates a Flask app for testing.
    This fixture is automatically available to all tests_need_fix.
    """

    app = Flask(__name__)

    # Enable testing mode
    app.config["TESTING"] = True

    return app