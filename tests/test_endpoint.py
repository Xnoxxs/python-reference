
# python -m pytest tests_need_fix/example/test_create_note.py
# python -m pytest tests_need_fix/example/test_create_note.py -s (with print statements)

from unittest.mock import patch
from flask import request

from train.tests.endpoint import create_note


def test_create_note(app):

    # --------------------------------------------------
    # Mock external service
    # --------------------------------------------------

    with patch("actions.actions.example.create_note.AnalyticsService.send_event") as mock_send_event:

        data = {
            "title": "Test note",
            "content": "This is a test note"
        }

        # --------------------------------------------------
        # Simulate HTTP request
        # --------------------------------------------------

        with app.test_request_context(
            "/create_note",
            method="POST",
            json=data
        ):

            # Simulate authentication middleware adding this attribute
            request.user_auth_id = "ZklDmbWXmibm7TcUGpPPNPheakG2"

            response, status = create_note()

        # --------------------------------------------------
        # Verify endpoint response
        # --------------------------------------------------

        assert status == 200

        response_json = response.get_json()

        assert response_json["title"] == "Test note"
        assert response_json["content"] == "This is a test note"
        assert response_json["owner"] == "ZklDmbWXmibm7TcUGpPPNPheakG2"

        # --------------------------------------------------
        # Verify external service was called
        # --------------------------------------------------

        mock_send_event.assert_called_once()

        args, kwargs = mock_send_event.call_args

        assert kwargs["event_name"] == "note_created"
        assert kwargs["properties"]["title"] == "Test note"