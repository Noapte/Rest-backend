from flask_restplus import fields

from doxapi.api.api import api
from doxapi.api.models import user_data


creadentials = api.model(
    "Creadentials",
    {
        "email": fields.String(required=True, example="john.doe@example.com"),
        "password": fields.String(required=True, example="qwerty"),
    },
)

auth_response = api.model(
    "AuthResponse",
    {
        "access_token": fields.String(example="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9"),
        "identity": fields.Nested(user_data),
    },
)
