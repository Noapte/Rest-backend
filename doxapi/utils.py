# pylint: disable=too-many-arguments,locally-disabled
from flask_security.utils import encrypt_password

from doxapi.app import db
from doxapi.models import user_datastore


def create_user(name, email, password, admin=False, readonly=False):
    user = user_datastore.create_user(
        name=name, email=email, password=encrypt_password(password)
    )
    if admin:
        user_datastore.add_role_to_user(user, user_datastore.find_role("Admin"))
    if not readonly:
        user_datastore.add_role_to_user(user, user_datastore.find_role("Editor"))
    db.session.commit()


def reset_password(email, new_password):
    user = user_datastore.find_user(email=email)
    if not user:
        print(f"User with email: '{email}' not found")
        return
    user.password = encrypt_password(new_password)
    db.session.commit()
