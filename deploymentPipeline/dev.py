
from flask import Flask, jsonify

app = Flask(__name__)

# ---- DEV ENDPOINTS WITH BREAKING CHANGES ----

@app.get("/get-users")
def get_users():
    # ❌ Removed "role" — BREAKING CHANGE
    return jsonify([
        {"id": 1, "name": "Alice", "role": "customer", "age": 23},
        {"id": 2, "name": "Bob", "role": "customer", "age": 25}
    ])


@app.get("/get-activity")
def get_activity():
    # ❌ Renamed "title" → "name" — BREAKING CHANGE
    # ❌ Changed price from number → string — BREAKING CHANGE
    return jsonify({
        "id": "A1",
        "name": "Jet Ski",      # previously "title"
        "price": "100",         # previously number
        "details": {
            "location": "Miami Beach",
            "duration": 60
        }
    })


if __name__ == "__main__":
    app.run(port=9000, debug=False)
