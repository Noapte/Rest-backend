from flask_restplus import fields

from doxapi.api.api import api


class NullableStringField(fields.String):
    __schema_type__ = ["string", "null"]
    __schema_example__ = "null"


user_data = api.model(
    "UserData",
    {
        "id": fields.Integer(example=1),
        "name": fields.String(example="John Doe"),
        "email": fields.String(example="john.doe@example.com"),
        "can_edit": fields.Boolean(example=True),
    },
)
