# pylint: disable=unused-argument,locally-disabled

import pytest

from doxapi.app import db
from doxapi.models import User, Role
from doxapi.test.utils import commit


@pytest.fixture(scope="module")
def db_session():
    db.create_all()
    yield
    db.drop_all()


@pytest.fixture(scope="module")
def editor_role(db_session):
    return commit(Role(name="Editor"))


@pytest.fixture(scope="module")
def user(editor_role):
    return commit(
        User(
            name="John Doe",
            email="john.doe@example.com",
            password="test",
            roles=[editor_role],
        )
    )


@pytest.fixture(scope="module")
def other_user(editor_role):
    return commit(
        User(
            name="Other John Doe",
            email="other.john.doe@example.com",
            password="test",
            roles=[editor_role],
        )
    )
