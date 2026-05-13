from train.ORM.initialize import app, db
from train.ORM.models.user import User


# -----------------------------------
# 1️⃣ Basic Delete (by authentication_id)
# -----------------------------------
def delete1_user(authentication_id):

    user = db.session.query(User).filter_by(
        authentication_id=authentication_id
    ).first()

    if not user:
        print("User not found")
        return

    db.session.delete(user)
    db.session.commit()

    print("User deleted successfully")
    return user


# -----------------------------------
# Fully Generic Delete
# -----------------------------------
def delete_record(model_class, id):

    instance = db.session.query(model_class).filter_by(
       id=id
    ).first()

    if not instance:
        print("Record not found")
        return

    db.session.delete(instance)
    db.session.commit()

    print(f"{instance} deleted successfully")

    return instance


if __name__ == "__main__":

    with app.app_context():

        # Example 1
        delete1_user("auth_999")


        # Example 3 (Fully generic)
        delete_record(User, {
            "id": 5
        })