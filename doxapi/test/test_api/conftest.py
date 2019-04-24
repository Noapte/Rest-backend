import pytest

from doxapi.app import app
from doxapi.models import Folder, Document

from doxapi.test.test_api.utils import ApiClient, ApiAuthClient


@pytest.fixture(scope="module")
def client():
    with app.app_context():
        yield app.test_client()


@pytest.fixture(scope="module")
def api_client(client):
    return ApiClient(client)


@pytest.fixture(scope="module")
def auth_client(client, user):
    return ApiAuthClient(client, email=user.email, password=user.password)


@pytest.fixture
def documents_url():
    return "/documents"


@pytest.fixture
def home_folder(mocker):
    home_folder = Folder(id=1, name="Home")
    mocker.patch("doxapi.managers.FoldersManager.get_root", return_value=home_folder)
    return home_folder


@pytest.fixture
def sample_folder(mocker, home_folder):
    folder = Folder(id=1, name="Sample folder", parent=home_folder)
    mocker.patch("doxapi.managers.FoldersManager.get", return_value=folder)
    return folder


@pytest.fixture
def sample_doc(mocker, sample_folder):
    doc = Document(id=1, title="test", folder=sample_folder)
    mocker.patch("doxapi.managers.DocumentsManager.get", return_value=doc)
    return doc


@pytest.fixture
def sample_doc_url(documents_url, sample_doc):
    return "{}/{}".format(documents_url, sample_doc.id)
