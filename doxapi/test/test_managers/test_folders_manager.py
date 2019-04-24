from datetime import datetime

import pytest

from werkzeug.exceptions import Conflict, Forbidden, NotFound

from doxapi.app import db
from doxapi.managers import FoldersManager, Document
from doxapi.models import Folder

from doxapi.test.utils import commit


@pytest.fixture
def sample_folder(home_folder):
    return FoldersManager.create(name="sample_folder", parent=home_folder.id)


@pytest.fixture
def sample_subfolder(sample_folder):
    return FoldersManager.create(name="sample_subfolder", parent=sample_folder.id)


@pytest.mark.usefixtures("db_session", "current_user_context")
class TestFoldersManager:
    def teardown(self):
        Folder.query.filter(Folder.name != "Home").delete(synchronize_session="fetch")
        db.session.commit()

    def test_get_root_returns_home_folder(self, home_folder):
        result = FoldersManager.get_root()
        assert result == home_folder

    def test_create_returns_new_folder(self, sample_folder):
        test_folder = FoldersManager.create(
            name=sample_folder.name, parent=sample_folder.id
        )

        assert isinstance(test_folder, Folder)

        assert test_folder.id > 1
        assert test_folder.name == sample_folder.name
        assert test_folder.created < datetime.utcnow()

        assert test_folder.parent == sample_folder
        assert test_folder in sample_folder.folders

    def test_create_raises_conflict_error_for_duplicated_name_and_parent(
        self, sample_folder
    ):
        with pytest.raises(Conflict):
            FoldersManager.create(
                name=sample_folder.name, parent=sample_folder.parent.id
            )

    def test_create_raises_not_found_error_for_non_existing_parent(self):
        with pytest.raises(NotFound):
            FoldersManager.create(name="Test", parent=99)

    @pytest.mark.parametrize("modified_props", [{}, {"name": "modified"}])
    def test_update_modifies_folder_properties(self, sample_subfolder, modified_props):
        orig_name = sample_subfolder.name
        FoldersManager.update(sample_subfolder, **modified_props)
        assert sample_subfolder.name == modified_props.get("name", orig_name)

    def test_update_moves_folder_to_another(self, sample_subfolder, home_folder):
        assert sample_subfolder not in home_folder.folders

        FoldersManager.update(sample_subfolder, parent=home_folder.id)

        assert sample_subfolder.parent == home_folder
        assert sample_subfolder in home_folder.folders

    def test_update_raises_conflict_error_for_duplicated_name_and_parent(
        self, sample_folder, sample_subfolder
    ):
        with pytest.raises(Conflict):
            FoldersManager.update(
                sample_subfolder,
                name=sample_folder.name,
                parent=sample_folder.parent.id,
            )

    def test_update_raises_conflict_error_for_circular_parent_dependency(
        self, sample_folder, sample_subfolder
    ):
        with pytest.raises(Conflict):
            FoldersManager.update(sample_folder, parent=sample_folder.id)

        with pytest.raises(Conflict):
            FoldersManager.update(sample_folder, parent=sample_subfolder.id)

    @pytest.mark.parametrize(
        "modified_props",
        [{"name": "modified"}, {"parent": 99}, {"name": "modified", "parent": 99}],
    )
    def test_delete_raises_forbidden_error_for_home_folder(
        self, home_folder, modified_props
    ):
        with pytest.raises(Forbidden):
            FoldersManager.update(home_folder, **modified_props)

    def test_delete_removes_folder_with_items(self, sample_folder, sample_subfolder):
        sample_doc = commit(Document(folder=sample_folder, title="Test"))
        FoldersManager.delete(sample_folder.id)
        assert Folder.query.get(sample_folder.id) is None
        assert Folder.query.get(sample_subfolder.id) is None
        assert Document.query.get(sample_doc.id) is None

    def test_delete_raises_forbidden_error_on_home_folder_delete(self, home_folder):
        with pytest.raises(Forbidden):
            FoldersManager.delete(home_folder.id)
