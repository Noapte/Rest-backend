from datetime import datetime

import pytest

from werkzeug.exceptions import NotFound, Conflict

from doxapi.app import db
from doxapi.managers import DocumentsManager
from doxapi.models import Document


@pytest.fixture
def sample_doc(folder, doc_data):
    return DocumentsManager.create(folder, **doc_data)


@pytest.mark.usefixtures("db_session", "current_user_context")
class TestDocumentsManager:
    def teardown(self):
        Document.query.delete()
        db.session.commit()

    def test_create_returns_new_doc(self, folder, sample_doc, doc_data, user):
        assert isinstance(sample_doc, Document)
        assert sample_doc.id >= 1
        assert sample_doc.title == doc_data["title"]
        assert sample_doc.description == doc_data["description"]
        assert sample_doc.payload == doc_data["payload"]

        assert sample_doc.created < datetime.now()
        assert sample_doc.author == user

        assert sample_doc.editor is None
        assert sample_doc.updated is None

        assert sample_doc.folder == folder
        assert sample_doc in folder.documents

        assert sample_doc == Document.query.first()

    def test_create_raises_conflict_error_for_duplicated_title(
        self, folder, sample_doc
    ):
        with pytest.raises(Conflict):
            DocumentsManager.create(folder, title=sample_doc.title)

    @pytest.mark.parametrize(
        "modified_properties",
        [
            {"title": "modified"},
            {"payload": "modified"},
            {"description": "modified"},
            {
                "title": "modified",
                "description": "modified too",
                "payload": "also modified",
            },
        ],
    )
    def test_update_modifies_existing_document(
        self, sample_doc, modified_properties, user
    ):
        orig_title = sample_doc.title
        orig_payload = sample_doc.payload
        orig_description = sample_doc.description

        DocumentsManager.update(sample_doc, **modified_properties)

        assert sample_doc.title == modified_properties.get("title", orig_title)
        assert sample_doc.payload == modified_properties.get("payload", orig_payload)
        assert sample_doc.description == modified_properties.get(
            "description", orig_description
        )
        assert sample_doc.created < sample_doc.updated
        assert sample_doc.editor == user
        assert sample_doc == Document.query.get(sample_doc.id)

    def test_update_moves_document_to_another_folder(self, sample_doc, home_folder):
        assert sample_doc not in home_folder.documents

        DocumentsManager.update(sample_doc, folder=home_folder.id)

        assert sample_doc.folder == home_folder
        assert sample_doc in home_folder.documents

    def test_update_ignores_empty_data(self, mocker, sample_doc, other_user):
        orig_title = sample_doc.title
        orig_description = sample_doc.description
        orig_editor = sample_doc.editor
        orig_updated = sample_doc.updated
        with mocker.patch("doxapi.managers.get_current_user", return_value=other_user):
            DocumentsManager.update(sample_doc)

        assert sample_doc.title == orig_title
        assert sample_doc.description == orig_description
        assert sample_doc.editor == orig_editor
        assert sample_doc.updated == orig_updated

    def test_update_raises_conflict_error_for_duplicated_title(
        self, folder, sample_doc
    ):
        test_doc = DocumentsManager.create(folder, title="Do not duplicate")
        with pytest.raises(Conflict):
            DocumentsManager.update(sample_doc, title=test_doc.title)

    def test_get_returns_doc(self, sample_doc):
        result = DocumentsManager.get(sample_doc.id)
        assert result == sample_doc

    def test_get_raises_not_found_error_for_non_existing_doc(self):
        with pytest.raises(NotFound):
            DocumentsManager.get(1)

    def test_get_all_returns_empty_list(self):
        result = DocumentsManager.get_all()
        assert result == []

    def test_get_all_returns_doc_list(self, sample_doc):
        result = DocumentsManager.get_all()
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0] == sample_doc
