from flask import url_for
from flask_cors import CORS
from flask_admin import helpers
from flask_jwt_extended import JWTManager
from flask_security import Security
from flask_security.core import _request_loader

from doxapi.app import app
from doxapi.api import api
from doxapi.admin import admin
from doxapi.models import user_datastore


CORS(app, resources={r"/api/*": {"origins": "*"}})


jwt = JWTManager(app)
jwt._set_error_handler_callbacks(api)  # pylint: disable=protected-access


@jwt.user_identity_loader
def get_user_identity(user):
    return user.id


@jwt.user_loader_callback_loader
def load_user(identity):
    return user_datastore.get_user(identity)


security = Security(app, user_datastore)


@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=helpers,
        get_url=url_for,
    )


def request_loader(request):
    if request.is_json:
        return security.login_manager.anonymous_user()
    return _request_loader(request)


security.login_manager.request_loader(request_loader)
