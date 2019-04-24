import pytest

from doxapi.models import Folder, Document
from doxapi.test.utils import commit


@pytest.fixture
def current_user_context(mocker, user):
    mocker.patch("doxapi.managers.get_current_user", return_value=user)


@pytest.fixture(scope="module")
def home_folder():
    return commit(Folder(id=1, name="Home"))


@pytest.fixture(scope="module")
def folder(home_folder):
    return commit(Folder(name="Folder", parent=home_folder))


@pytest.fixture(scope="module")
def doc_data():
    return {
        "title": "Test document",
        "description": "Document for testing purposes",
        "payload": "Lorem ipsum dolor sit amet",
    }


@pytest.fixture(scope="module")
def doc(home_folder, doc_data):
    return commit(Document(folder=home_folder, **doc_data))
