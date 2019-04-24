# pylint: disable=no-self-use,locally-disabled

from flask_jwt_extended import jwt_required
from flask_restplus import Resource

from doxapi.managers import FoldersManager, DocumentsManager

from doxapi.api.api import api
from doxapi.api.documents.models import (
    document_data,
    document_dump,
    document_post_data,
    document_ref,
)

document = api.namespace("documents")


@document.route("")
class DocumentsEndpoint(Resource):
    @document.doc(description="Get documents list")
    @document.response(200, "Success", document_ref)
    @jwt_required
    def get(self):
        return [doc.dump_ref() for doc in DocumentsManager.get_all()]

    @document.doc(description="Create new document")
    @document.expect(document_post_data, validate=True)
    @document.response(201, "Document created", document_ref)
    @document.response(409, "Document with given title already exists")
    @jwt_required
    def post(self):
        if "folder" in api.payload:
            folder = FoldersManager.get(api.payload["folder"])
            del api.payload["folder"]
        else:
            folder = FoldersManager.get_root()

        document = DocumentsManager.create(folder, **api.payload)
        return document.dump_ref(), 201


@document.route("/<int:document_id>")
@document.response(404, "Document with given ID doesn't exists")
@document.param("document_id", "Document unique identifier")
class DocumentEndpoint(Resource):
    @document.doc(description="Get document")
    @document.response(200, "Success", document_dump)
    @jwt_required
    def get(self, document_id):
        return DocumentsManager.get_dump(document_id)

    @document.doc(description="Update document")
    @document.expect(document_data, validate=True)
    @document.response(200, "Document updated")
    @document.response(409, "Document with given title already exists")
    @jwt_required
    def put(self, document_id):
        document = DocumentsManager.get(document_id)
        DocumentsManager.update(document, **api.payload)

    @document.doc(description="Delete document")
    @document.response(200, "Document deleted")
    @jwt_required
    def delete(self, document_id):
        DocumentsManager.delete(document_id)
