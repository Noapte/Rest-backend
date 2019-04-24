import pytest

from doxapi.models import Folder


FOLDERS_URL = "/folders"
HOME_FOLDER_URL = FOLDERS_URL + "/home"


@pytest.fixture
def sample_folder_url(sample_folder):
    return "{}/{}".format(FOLDERS_URL, sample_folder.id)


def test_get_returns_home_folder_dump(auth_client, home_folder):
    resp = auth_client.get(HOME_FOLDER_URL)
    assert resp.status_code == 200
    assert resp.json == home_folder.dump()


def test_get_returns_folder_dump(auth_client, sample_folder, sample_folder_url):
    resp = auth_client.get(sample_folder_url)
    assert resp.status_code == 200
    assert resp.json == sample_folder.dump()


@pytest.mark.parametrize(
    "invalid_data",
    [
        0,
        {},
        {"name": "New folder"},  # missing parent
        {"parent": 1},  # missing name
        {"parent": 1, "name": ""},
        {"parent": 1, "name": " "},
        {"parent": 1, "name": "\nNew folder"},
        {"parent": 1, "name": "New folder "},
        {"parent": 1, "name": "Too long" * 20},
        {"name": "New folder", "parent": None},
        {"name": "New folder", "parent": "invalid"},
    ],
)
def test_post_returns_status_400_on_invalid_data(auth_client, invalid_data):
    resp = auth_client.post(FOLDERS_URL, invalid_data)
    assert resp.status_code == 400


def test_post_returns_status_201_and_new_folder_ref(mocker, auth_client, home_folder):
    test_name = "New folder"
    test_folder = Folder(name=test_name, parent=home_folder)

    mocker.patch("doxapi.managers.FoldersManager.create", return_value=test_folder)

    resp = auth_client.post(FOLDERS_URL, {"name": test_name, "parent": home_folder.id})
    assert resp.status_code == 201
    assert resp.json == test_folder.dump_ref()


@pytest.mark.parametrize(
    "invalid_data",
    [
        0,
        {"name": ""},
        {"name": " "},
        {"name": "\nNew folder"},
        {"name": "New folder "},
        {"name": "Too long" * 20},
        {"parent": "invalid"},
    ],
)
def test_put_returns_status_400_on_invalid_data(
    auth_client, sample_folder_url, invalid_data
):
    resp = auth_client.put(sample_folder_url, invalid_data)
    assert resp.status_code == 400


def test_put_returns_status_200_and_no_data(mocker, auth_client, sample_folder_url):
    mocker.patch("doxapi.managers.FoldersManager.update")
    resp = auth_client.put(sample_folder_url, {"name": "New name"})
    assert resp.status_code == 200
    assert resp.json is None


def test_delete_returns_status_200_and_no_data(mocker, auth_client, sample_folder_url):
    mocker.patch("doxapi.managers.FoldersManager.delete")
    resp = auth_client.delete(sample_folder_url)
    assert resp.status_code == 200
    assert resp.json is None
