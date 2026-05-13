
from flask import request, jsonify


class AnalyticsService:
    """
    Fake service representing some external system.
    We will mock this in the test.
    """

    @staticmethod
    def send_event(event_name, properties):
        print(f"Sending event {event_name} with properties {properties}")


def create_note():
    try:

        # Simulate authenticated user
        user_auth_id = request.user_auth_id

        data = request.json

        title = data.get("title")
        content = data.get("content")

        if not title:
            return jsonify({"error": "title is required"}), 400

        # Simulate db_setup insert
        note = {
            "id": 1,
            "title": title,
            "content": content,
            "owner": user_auth_id
        }

        # External service call
        AnalyticsService.send_event(
            event_name="note_created",
            properties={"title": title}
        )

        return jsonify(note), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500