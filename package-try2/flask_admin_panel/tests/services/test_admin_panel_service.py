import datetime
from unittest.mock import MagicMock, create_autospec, patch

import pytest
from flask_admin_panel.services.admin_panel_service import (  # assuming the service is in admin_panel_service.py
    AdminPanelService,
)
from flask_admin_panel.exceptions.exceptions_classes import ModelNotFoundException
from extensions import db
from flask_wtf import FlaskForm
from sqlalchemy import inspect
from wtforms import (
    BooleanField,
    DateField,
    DateTimeField,
    FloatField,
    IntegerField,
    StringField,
)
from wtforms.validators import DataRequired, Optional


@pytest.fixture
def mock_db_session(mocker):
    return mocker.patch.object(db, "session")


@pytest.fixture
def admin_panel_service():
    return AdminPanelService()


def test_get_model_columnnames(admin_panel_service):
    model_cls = MagicMock()
    columns_mock = MagicMock()
    columns_mock.keys.return_value = ["id", "name", "email"]
    model_cls.__table__ = MagicMock(columns=columns_mock)

    columns = admin_panel_service.get_model_columnnames(model_cls)
    assert columns == ["id", "name", "email"]


def test_get_model_properties(admin_panel_service):
    class TestModel:
        @property
        def computed_property(self):
            return "value"

        query = None

    properties = admin_panel_service.get_model_properties(TestModel)
    assert properties == ["computed_property"]


def test_list_records(admin_panel_service):
    model_cls = MagicMock()
    columns_mock = MagicMock()
    columns_mock.keys.return_value = ["id", "name", "email"]
    model_cls.__table__ = MagicMock(columns=columns_mock)
    model_cls.query.all.return_value = [MagicMock(id=1), MagicMock(id=2)]
    admin_panel_service.register_model_for_admin_panel("TestModel", model_cls)
    records, columns = admin_panel_service.list_records("TestModel")
    assert len(records) == 2
    assert columns == model_cls.__table__.columns.keys() + []


def test_list_records_model_not_found(admin_panel_service):
    with pytest.raises(ModelNotFoundException):
        admin_panel_service.list_records("NonExistentModel")


def test_get_a_records(admin_panel_service):
    model_cls = MagicMock()
    columns_mock = MagicMock()
    columns_mock.keys.return_value = ["id", "name", "email"]
    model_cls.__table__ = MagicMock(columns=columns_mock)
    model_cls.query.get.return_value = MagicMock(id=1)
    record = admin_panel_service.get_a_records(model_cls, 1)
    assert record.id == 1


def test_add_record(admin_panel_service):
    model_cls = MagicMock()
    columns_mock = MagicMock()
    columns_mock.keys.return_value = ["id", "name", "email"]
    model_cls.__table__ = MagicMock(columns=columns_mock)
    form_instance = MagicMock(validate=lambda: True, populate_obj=lambda obj: None)
    form_class = MagicMock(return_value=form_instance)
    model_cls.query.all.return_value = []
    admin_panel_service.register_model_for_admin_panel("TestModel", model_cls)
    admin_panel_service.models_for_admin_panel["TestModel"]["form"] = form_class

    with patch("extensions.db.session.add") as mock_add, patch(
        "extensions.db.session.commit"
    ) as mock_commit:
        request = MagicMock(method="POST", form={})
        success, model_name, form = admin_panel_service.add_record(request, "TestModel")
        assert success
        assert model_name == "TestModel"
        assert form == form_instance
        mock_add.assert_called_once()
        mock_commit.assert_called_once()


def test_edit_record(admin_panel_service):
    model_cls = MagicMock()
    columns_mock = MagicMock()
    columns_mock.keys.return_value = ["id", "name", "email"]
    model_cls.__table__ = MagicMock(columns=columns_mock)
    instance = MagicMock(id=1)
    form_instance = MagicMock(validate=lambda: True, populate_obj=lambda obj: None)
    form_class = MagicMock(return_value=form_instance)
    model_cls.query.get.return_value = instance
    admin_panel_service.register_model_for_admin_panel("TestModel", model_cls)
    admin_panel_service.models_for_admin_panel["TestModel"]["form"] = form_class

    with patch("extensions.db.session.commit") as mock_commit:
        request = MagicMock(method="POST", form={})
        success, model_name, form = admin_panel_service.edit_record(
            request, "TestModel", 1
        )
        assert success
        assert model_name == "TestModel"
        assert form == form_instance
        mock_commit.assert_called_once()


def test_delete_record(admin_panel_service):
    model_cls = MagicMock()
    columns_mock = MagicMock()
    columns_mock.keys.return_value = ["id", "name", "email"]
    model_cls.__table__ = MagicMock(columns=columns_mock)
    instance = MagicMock(id=1)
    model_cls.query.get.return_value = instance
    admin_panel_service.register_model_for_admin_panel("TestModel", model_cls)

    with patch("extensions.db.session.delete") as mock_delete, patch(
        "extensions.db.session.commit"
    ) as mock_commit:
        request = MagicMock()
        success, model_name, deleted_instance = admin_panel_service.delete_record(
            request, "TestModel", 1
        )
        assert success
        assert model_name == "TestModel"
        assert deleted_instance == instance
        mock_delete.assert_called_once_with(instance)
        mock_commit.assert_called_once()


def test_delete_record_model_not_found(admin_panel_service):
    with pytest.raises(ModelNotFoundException):
        admin_panel_service.delete_record(MagicMock(), "NonExistentModel", 1)