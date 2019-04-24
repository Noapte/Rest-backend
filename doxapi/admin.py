from flask import abort, url_for, redirect, request
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib import sqla
from flask_security import current_user, utils
from wtforms.fields import PasswordField

from doxapi.app import app, db
from doxapi.models import User


class AdminLoginIndexView(AdminIndexView):
    @expose("/")
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for("security.login"))
        return super(AdminLoginIndexView, self).index()


class AdminModelView(sqla.ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_active_admin()

    def _handle_view(self, name, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for("security.login", next=request.url))
        if not current_user.is_active_admin():
            return abort(403)
        return None


class UsersView(AdminModelView):

    column_exclude_list = ["password"]
    column_searchable_list = ["name", "email"]

    form_excluded_columns = ["documents", "password"]
    form_extra_fields = {"new_password": PasswordField("Password")}

    def __init__(self):
        super(UsersView, self).__init__(User, db.session, name="Users")

    def on_model_change(self, form, model, is_created):
        if form.new_password.data:
            model.password = utils.encrypt_password(form.new_password.data)


admin = Admin(
    app,
    "Documents API",
    index_view=AdminLoginIndexView(),
    base_template="base.html",
    template_mode="bootstrap3",
)

admin.add_view(UsersView())
