# pylint: disable=no-member,locally-disabled
from datetime import datetime

from flask_jwt_extended import get_current_user
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound, Conflict, Forbidden

from doxapi.app import db
from doxapi.models import Folder, Document


def editor_role_required(function):
    def _wrap(inst, *args, **kwargs):
        if not get_current_user().is_active_editor():
            raise Forbidden(
                "You are not allowed to edit items. Please contact administrator."
            )
        return function(inst, *args, **kwargs)

    return _wrap


class Manager:

    model = None
    conflict_reason = "Integrity error"

    @classmethod
    @editor_role_required
    def create(cls, *args, **kwargs):
        new_item = cls._create(*args, **kwargs)
        cls._commit(new_item)
        return new_item

    @classmethod
    @editor_role_required
    def update(cls, obj, **properties):
        if not properties:
            return
        cls._assert_edit_allowed(obj)
        cls._update(obj, properties)
        cls._commit(obj)

    @classmethod
    @editor_role_required
    def delete(cls, obj_id, *parent_ids):
        obj = cls.get(obj_id, *parent_ids)
        cls._assert_edit_allowed(obj)
        db.session.delete(obj)
        db.session.commit()

    @classmethod
    def get(cls, obj_id, *parent_ids):
        obj = cls._find(obj_id, *parent_ids)
        if not obj:
            raise NotFound("Matching {} not found".format(cls.model.__name__))
        return obj

    @classmethod
    def _commit(cls, obj):
        try:
            db.session.add(obj)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise Conflict(cls.conflict_reason)

    @classmethod
    def _assert_edit_allowed(cls, obj):
        pass


class FoldersManager(Manager):

    model = Folder
    conflict_reason = "Folder with given name already exists"

    @classmethod
    def get_root(cls):
        return cls.model.query.filter(cls.model.parent_id.is_(None)).first()

    @classmethod
    def _find(cls, folder_id):
        return cls.model.query.get(folder_id)

    @classmethod
    def _create(cls, **properties):
        return cls.model(name=properties["name"], parent=cls.get(properties["parent"]))

    @classmethod
    def _update(cls, folder, properties):
        if "name" in properties:
            folder.name = properties["name"]
        if "parent" in properties:
            parent_id = properties["parent"]
            cls._set_parent_folder(folder, parent_id)

    @classmethod
    def _set_parent_folder(cls, folder, parent_id):
        parent = cls.get(parent_id)
        if parent is folder:
            raise Conflict("Cannot move folder to itself")
        for grand_parent in parent.iter_parents():
            if grand_parent is folder:
                raise Conflict("Cannot move folder to a subfolder of itself")
        folder.parent = parent

    @classmethod
    def _assert_edit_allowed(cls, obj):
        if obj.parent is None:
            raise Forbidden("Cannot delete or modify root folder")


class DocumentsManager(Manager):

    model = Document
    conflict_reason = "Document with given title already exists"

    @classmethod
    def get_all(cls):
        return cls.model.query.all()

    @classmethod
    def get_dump(cls, doc_id):
        return cls.get(doc_id).dump()

    @classmethod
    def _find(cls, doc_id):
        return cls.model.query.get(doc_id)

    @classmethod
    def _create(cls, folder, **properties):
        return cls.model(
            folder=folder,
            title=properties["title"],
            payload=properties.get("payload"),
            description=properties.get("description"),
            author=get_current_user(),
        )

    @classmethod
    def _update(cls, doc, properties):
        if "folder" in properties:
            doc.folder = FoldersManager.get(properties["folder"])
        if "title" in properties:
            doc.title = properties["title"]
        if "payload" in properties:
            doc.payload = properties["payload"]
        if "description" in properties:
            doc.description = properties["description"]
        if properties:
            doc.editor = get_current_user()
            doc.updated = datetime.now()
