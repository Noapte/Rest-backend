from flask_restplus import fields

from doxapi.models import Folder
from doxapi.api.api import api
from doxapi.api.documents.models import document_ref


def folder_name_field(**optional_properties):
    return fields.String(
        example="New folder",
        pattern=r"^(?!\s).+(?<!\s)$",
        max_length=Folder.name.type.length,
        **optional_properties
    )


def folder_parent_field(**optional_properties):
    return fields.Integer(example=1, **optional_properties)


folder_ref = api.model(
    "FolderDumpBase",
    {
        "id": fields.Integer(readOnly=True, required=True, example=1),
        "name": folder_name_field(),
        "created": fields.DateTime(
            readOnly=True, example="2015-07-07T15:49:51.230+02:00"
        ),
    },
)

folder_dump = api.inherit(
    "FolderDump",
    folder_ref,
    {
        "parents": fields.Nested(folder_ref, as_list=True),
        "folders": fields.Nested(folder_ref, as_list=True),
        "documents": fields.Nested(document_ref, as_list=True),
    },
)


folder_put_data = api.model(
    "FolderPutData", {"name": folder_name_field(), "parent": folder_parent_field()}
)

folder_post_data = api.model(
    "FolderPostData",
    {
        "name": folder_name_field(required=True),
        "parent": folder_parent_field(required=True),
    },
)
