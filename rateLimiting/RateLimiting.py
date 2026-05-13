



# server.py
from flask import Flask, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_limiter.errors import RateLimitExceeded

app = Flask(__name__)

# ---------------------- #
#  Setup Flask-Limiter
# ---------------------- #
limiter = Limiter(
    key_func=get_remote_address,   # identify client by IP address
    default_limits=["100 per minute"]  # limit all routes to 5 req/min
)
limiter.init_app(app)

# ---------------------- #
#  Custom rate limit error
# ---------------------- #
@app.errorhandler(RateLimitExceeded)
def handle_rate_limit(e):
    print(f"Rate Limit reached: {e}")
    return jsonify({str("Too many requests")}), 429


# ---------------------- #
#  Example route
# ---------------------- #
@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"message": "Pong! ✅"}), 200

@app.route("/test", methods=["GET"])
def test():
    return jsonify({"message": "Pong! ✅"}), 200

@app.route("/go", methods=["GET"])
@limiter.limit("50 per minute")  # optional, overrides default
def go():
    return jsonify({"message": "Pong! ✅"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6000, debug=True)

