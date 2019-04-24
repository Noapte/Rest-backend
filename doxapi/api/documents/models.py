from flask_restplus import fields

from doxapi.models import Document

from doxapi.api.api import api
from doxapi.api.models import user_data


def document_title_field(**optional_properties):
    return fields.String(
        example="Sample document",
        pattern=r"^(?!\s).+(?<!\s)$",
        max_length=Document.title.type.length,
        **optional_properties
    )


document_id = fields.Integer(readOnly=True, required=True, example=1)

document_desc = fields.String(
    example="Sample document for testing purposes",
    max_length=Document.description.type.length,
)

documet_payload = fields.String(example="Lorem ipsum dolor sit amet")


document_ref = api.model(
    "DocumentDump",
    {
        "id": document_id,
        "title": document_title_field(),
        "description": document_desc,
        "author": fields.Nested(user_data, allow_null=True),
        "created": fields.DateTime(
            readOnly=True, example="2015-07-07T15:49:51.230+02:00"
        ),
        "editor": fields.Nested(user_data, allow_null=True),
        "updated": fields.DateTime(
            readOnly=True, example="2015-07-07T15:49:51.230+02:00"
        ),
    },
)


document_dump = api.model(
    "DocumentDump",
    {"id": document_id, "title": document_title_field(), "payload": documet_payload},
)

document_data = api.model(
    "DocumentData",
    {
        "title": document_title_field(),
        "description": document_desc,
        "payload": documet_payload,
        "folder": fields.Integer(example=1),
    },
)

document_post_data = api.inherit(
    "DocumentPostData", document_data, {"title": document_title_field(required=True)}
)
