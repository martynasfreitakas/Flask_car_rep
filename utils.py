from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User


def create_user(name, username, email, password, phone_number):
    user = User.query.filter_by(username=username).first()
    if user is None:
        user = User(name=name, username=username, email=email, password=generate_password_hash(password),
                    phone_number=phone_number)
        db.session.add(user)
        db.session.commit()
        return True
    else:
        return False


def check_user(username, password):
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        return user
    return None
