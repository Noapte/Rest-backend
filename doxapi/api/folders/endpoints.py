# pylint: disable=no-self-use,locally-disabled

from flask_jwt_extended import jwt_required
from flask_restplus import Resource

from doxapi.managers import FoldersManager

from doxapi.api.api import api
from doxapi.api.folders.models import (
    folder_ref,
    folder_dump,
    folder_put_data,
    folder_post_data,
)

folders = api.namespace("folders")


@folders.route("")
class FoldersEndpoint(Resource):
    @folders.doc(description="Create new folder")
    @folders.expect(folder_post_data, validate=True)
    @folders.response(201, "Folder created", folder_ref)
    @folders.response(404, "Parent folder with given ID not found")
    @folders.response(409, "Folder with given name already exists")
    @jwt_required
    def post(self):
        folder = FoldersManager.create(**api.payload)
        return folder.dump_ref(), 201


@folders.route("/home")
class HomeFolderEndpoint(Resource):
    @folders.doc(description="Get home folder dump")
    @folders.response(200, "Success", folder_dump)
    @jwt_required
    def get(self):
        return FoldersManager.get_root().dump()


@folders.route("/<int:folder_id>")
@folders.response(404, "Folder with given ID doesn't exists")
@folders.param("folder_id", "Folder unique identifier")
class FolderEndpoint(Resource):
    @folders.doc(description="Get folder dump")
    @folders.response(200, "Success", folder_dump)
    @jwt_required
    def get(self, folder_id):
        return FoldersManager.get(folder_id).dump()

    @folders.doc(description="Update folder")
    @folders.expect(folder_put_data, validate=True)
    @folders.response(200, "Folder updated")
    @folders.response(404, "Parent folder with given ID not found")
    @folders.response(409, "Folder with given name already exists")
    @jwt_required
    def put(self, folder_id):
        folder = FoldersManager.get(folder_id)
        FoldersManager.update(folder, **api.payload)

    @folders.doc(description="Delete folder")
    @folders.response(200, "Folder deleted")
    @jwt_required
    def delete(self, folder_id):
        FoldersManager.delete(folder_id)
