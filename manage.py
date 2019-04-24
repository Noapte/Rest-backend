from flask_migrate import MigrateCommand
from flask_script import Manager, prompt_pass

from doxapi import app
from doxapi.utils import create_user, reset_password

manager = Manager(app)
manager.add_command("db", MigrateCommand)


@manager.command
def createuser(name, email, admin=False, readonly=False):
    password = prompt_pass("Enter password")
    create_user(name, email, password, admin, readonly)


@manager.command
def passwd(email, new_password):
    reset_password(email, new_password)


if __name__ == "__main__":
    manager.run()
