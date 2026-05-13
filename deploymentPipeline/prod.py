

from flask import Flask, jsonify

app = Flask(__name__)

# ---- PRODUCTION ENDPOINTS ----

@app.get("/get-users")
def get_users():
    return jsonify([
        {"id": 1, "name": "Alice", "role": "customer"},
        {"id": 2, "name": "Bob", "role": "provider"}
    ])


@app.get("/get-activity")
def get_activity():
    return jsonify({
        "id": "A1",
        "title": "Jet Ski",
        "price": 100,
        "details": {
            "location": "Miami Beach",
            "duration": 60
        }
    })


if __name__ == "__main__":
    app.run(port=8000, debug=False)
