# pylint: disable=no-self-use,locally-disabled

from flask_jwt_extended import jwt_required, create_access_token, current_user
from flask_restplus import Resource
from flask_security.utils import verify_password

from doxapi.models import User

from doxapi.api.api import api
from doxapi.api.models import user_data

from doxapi.api.auth.models import creadentials, auth_response


auth = api.namespace("auth")


@auth.route("")
class AuthorizationEndpoint(Resource):
    @auth.doc(description="Get user identity")
    @auth.response(200, "Success", user_data)
    @auth.response(401, "Unauthorized")
    @jwt_required
    def get(self):
        return current_user.dump()

    @auth.doc(description="Authorize")
    @auth.expect(creadentials, validate=True)
    @auth.response(200, "Success", auth_response)
    @auth.response(401, "Invalid credentials")
    def post(self):
        user = User.query.filter(User.email == api.payload["email"]).first()
        are_credentials_valid = user and verify_password(
            api.payload["password"], user.password
        )
        if not are_credentials_valid:
            return {"message": "Invalid credentials"}, 401

        access_token = create_access_token(identity=user)
        return {"access_token": access_token, "user": user.dump()}
