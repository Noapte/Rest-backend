import pytest

from doxapi.models import Document


def test_get_returns_status_200_and_documents_list(mocker, auth_client, documents_url):
    mocker.patch("doxapi.managers.DocumentsManager.get_all", return_value=[])
    resp = auth_client.get(documents_url)
    assert resp.status_code == 200
    assert isinstance(resp.json, list)


def test_get_returns_status_200_and_document_data(
    auth_client, sample_doc, sample_doc_url
):
    resp = auth_client.get(sample_doc_url)
    assert resp.status_code == 200
    assert resp.json == sample_doc.dump()


@pytest.mark.parametrize(
    "invalid_data",
    [
        0,
        {},
        {"title": ""},
        {"title": " "},
        {"title": "\ntitle"},
        {"title": "title "},
        {"title": "Too long" * 20},
        {"description": "Missing title"},
        {"title": "OK", "description": "Too long" * 100},
    ],
)
def test_post_returns_status_400_on_invalid_data(
    auth_client, documents_url, invalid_data
):
    resp = auth_client.post(documents_url, invalid_data)
    assert resp.status_code == 400


def test_post_returns_status_201_and_new_item_ref(
    mocker, home_folder, auth_client, documents_url
):
    test_data = {"title": "Test", "description": "test"}
    test_doc = Document(**test_data)

    mocker.patch("doxapi.managers.DocumentsManager.create", return_value=test_doc)

    resp = auth_client.post(documents_url, test_data)
    assert resp.status_code == 201
    assert resp.json == test_doc.dump_ref()


@pytest.mark.parametrize(
    "invalid_data",
    [
        0,
        {"title": ""},
        {"title": " "},
        {"title": "\ntitle"},
        {"title": "title "},
        {"title": "Too long" * 20},
        {"description": "Too long" * 100},
    ],
)
def test_put_returns_status_400_on_invalid_data(
    auth_client, sample_doc_url, invalid_data
):
    resp = auth_client.put(sample_doc_url, invalid_data)
    assert resp.status_code == 400


def test_put_returns_status_200_and_no_data(mocker, auth_client, sample_doc_url):
    mocker.patch("doxapi.managers.DocumentsManager.update")
    resp = auth_client.put(sample_doc_url, {"title": "Test"})
    assert resp.status_code == 200
    assert resp.json is None


def test_delete_returns_status_200_and_no_data(mocker, auth_client, sample_doc_url):
    mocker.patch("doxapi.managers.DocumentsManager.delete")
    resp = auth_client.delete(sample_doc_url)
    assert resp.status_code == 200
    assert resp.json is None
