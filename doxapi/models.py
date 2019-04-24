from flask_security import SQLAlchemyUserDatastore, UserMixin, RoleMixin
from sqlalchemy.sql import func

from doxapi.app import db


class Document(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    payload = db.Column(db.Text())
    created = db.Column(db.DateTime(), default=func.now())
    updated = db.Column(db.DateTime())
    author_id = db.Column(db.Integer(), db.ForeignKey("user.id"))
    editor_id = db.Column(db.Integer(), db.ForeignKey("user.id"))
    folder_id = db.Column(db.Integer(), db.ForeignKey("folder.id"), nullable=False)

    __table_args__ = (db.UniqueConstraint("folder_id", "title", name="_unique_title"),)

    author = db.relationship("User", foreign_keys=[author_id])
    editor = db.relationship("User", foreign_keys=[editor_id])
    folder = db.relationship("Folder", back_populates="documents")

    def dump_ref(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "created": self.created.isoformat() if self.created else None,
            "updated": self.updated.isoformat() if self.updated else None,
            "author": self.author.dump() if self.author else None,
            "editor": self.editor.dump() if self.editor else None,
        }

    def dump(self):
        return {"id": self.id, "title": self.title, "payload": self.payload}


class Folder(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    created = db.Column(db.DateTime(), default=func.now())
    parent_id = db.Column(db.Integer(), db.ForeignKey("folder.id"))

    __table_args__ = (db.UniqueConstraint("parent_id", "name", name="_unique_name"),)

    parent = db.relationship("Folder", remote_side=[id])

    folders = db.relationship(
        "Folder",
        lazy="joined",
        join_depth=1,
        cascade="all, delete-orphan",
        order_by=created.desc(),
    )

    documents = db.relationship(
        "Document",
        back_populates="folder",
        cascade="all, delete-orphan",
        order_by=Document.created.desc(),
    )

    def dump_ref(self):
        return {
            "id": self.id,
            "name": self.name,
            "created": self.created.isoformat() if self.created else None,
        }

    def dump(self):
        result = self.dump_ref()
        result["folders"] = [folder.dump_ref() for folder in self.folders]
        result["documents"] = [doc.dump_ref() for doc in self.documents]
        result["parents"] = [
            parent_folder.dump_ref() for parent_folder in self.iter_parents()
        ]
        return result

    def iter_parents(self):
        if self.parent is None:
            return

        yield self.parent
        yield from self.parent.iter_parents()


roles_users = db.Table(
    "roles_users",
    db.Column("user_id", db.Integer(), db.ForeignKey("user.id")),
    db.Column("role_id", db.Integer(), db.ForeignKey("role.id")),
)


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean(), default=True)
    roles = db.relationship(
        "Role", secondary=roles_users, backref=db.backref("users", lazy="dynamic")
    )

    def is_active_admin(self):
        return self.is_active and self.has_role("Admin")

    def is_active_editor(self):
        return self.is_active and self.has_role("Editor")

    def dump(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "can_edit": self.is_active_editor(),
        }

    def __str__(self):
        return "{} <{}>".format(self.name, self.email)


user_datastore = SQLAlchemyUserDatastore(db, User, Role)
