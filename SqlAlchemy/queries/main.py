

from flask_cors import CORS
from flask import jsonify

from train.ORM.initialize import app, db
from train.ORM.models.user import User
from train.pydantic.schemas.user import UserSchema

CORS(app)

@app.route('/get-users', methods=['GET'])
def get_users():
    try:

        users = (
            db.session.query(User)
            .all()
        )

        result = []
        for user in users:
            item = UserSchema.model_validate(user).model_dump(mode="json")
            result.append(item)

        return jsonify(result), 200

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4000, debug=True, use_reloader=False)
