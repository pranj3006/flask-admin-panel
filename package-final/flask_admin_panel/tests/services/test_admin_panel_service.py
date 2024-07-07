import pytest
from unittest.mock import MagicMock, create_autospec, patch
from datetime import datetime
from flask import Flask, request
from werkzeug.datastructures import MultiDict
from flask_sqlalchemy import SQLAlchemy
from flask_admin_panel.services.admin_panel_service import (
    AdminPanelService,
)  # Replace with your actual module import
from flask_admin_panel.exceptions.exceptions_classes import ModelNotFoundException


@pytest.fixture
def app():
    """Create and return a Flask app instance for testing."""
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    return app


@pytest.fixture
def db(app):
    """Create and return a SQLAlchemy database instance for testing."""
    db = SQLAlchemy(app)
    return db


@pytest.fixture
def service(app, db):
    """Create and return an instance of AdminPanelService for testing."""
    return AdminPanelService(app, db)


@pytest.fixture
def mock_model():
    model_cls = MagicMock()
    columns_mock = MagicMock()
    columns_mock.keys.return_value = ["id", "name", "email"]
    model_cls.__table__ = MagicMock(columns=columns_mock)
    records = [
        {"id": 1, "name": "abc", "email": "abc@xyz.com"},
        {"id": 2, "name": "pqr", "email": "pqr@xyz.com"},
    ]
    model_cls.query.all.return_value = records
    return model_cls


@pytest.fixture
def mock_form_instance():
    return MagicMock(validate=lambda: True, populate_obj=lambda obj: None)


@pytest.fixture
def mock_form_class(mock_form_instance):
    return MagicMock(return_value=mock_form_instance)


@pytest.fixture
def client(app, db):
    """Create a test client for the Flask app."""
    with app.test_client() as client:
        with app.app_context():
            yield client


def test_register_model_for_admin_panel(service, mock_model):
    """Test registering a model for admin panel."""

    service.register_model_for_admin_panel("TestModel", mock_model)
    assert "TestModel" in service.models_for_admin_panel


def test_list_records_success(client, db, service):
    """Test listing all records of a registered model."""

    # Create a test model class
    class TestModel(db.Model):
        __tablename__ = "test_model"
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(50), nullable=False)

    # Create all tables for the models
    db.create_all()
    # Register the model with the service
    service.register_model_for_admin_panel("TestModel", TestModel)

    # Create test records
    test_record_1 = TestModel(name="Record 1")
    test_record_2 = TestModel(name="Record 2")
    db.session.add_all([test_record_1, test_record_2])
    db.session.commit()

    # Call the list_records method
    records, columns = service.list_records("TestModel")

    # Assertions
    assert len(records) == 2
    assert columns == ["id", "name"]  # Assuming 'id' and 'name' are columns


def test_list_records_model_not_found(service):
    """Test ModelNotFoundException when listing records of an unregistered model."""
    # Mock request and form data
    with pytest.raises(ModelNotFoundException):
        service.list_records("NonExistentModel")


def test_add_record_success(client, db, service):
    """Test adding a record to a registered model."""

    # Create a test model class
    class TestModel(db.Model):
        __tablename__ = "test_model"
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(50), nullable=False)

    # Create all tables for the models
    db.create_all()
    # Register the model with the service
    service.register_model_for_admin_panel("TestModel", TestModel)

    # Mock request and form data
    form_data = MultiDict([("name", "New Record")])  # Use MultiDict for form data
    with client.application.test_request_context(method="POST", data=form_data):
        # Call the add_record method
        success, model_name, form = service.add_record(request, "TestModel")

        # Assertions
        assert success is True
        assert model_name == "TestModel"
        assert form.errors == {}

        # Verify that the record was added to the database
        records = TestModel.query.all()
        assert len(records) == 1
        assert records[0].name == "New Record"


def test_add_record_invalid_form(client, db, service):
    """Test adding a record with invalid form data."""

    # Create a test model class
    class TestModel(db.Model):
        __tablename__ = "test_model"
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(50), nullable=False)

    # Create all tables for the models
    db.create_all()
    # Register the model with the service
    service.register_model_for_admin_panel("TestModel", TestModel)

    # Mock request and invalid form data
    invalid_form_data = MultiDict([("name", "")])  # Use MultiDict for invalid form data
    with client.application.test_request_context(method="POST", data=invalid_form_data):
        # Call the add_record method
        success, model_name, form = service.add_record(request, "TestModel")

        # Assertions
        assert success is False
        assert model_name == "TestModel"
        assert form.errors != {}  # Form should have validation errors


def test_add_record_model_not_found(service):
    """Test ModelNotFoundException when adding a record to an unregistered model."""
    # Mock request and form data
    with pytest.raises(ModelNotFoundException):
        service.add_record(
            None, "NonExistentModel"
        )  # Pass None for request since we expect exception


def test_edit_record_success(client, db, service):
    """Test editing an existing record successfully."""

    # Create a test model class
    class TestModel(db.Model):
        __tablename__ = "test_model"
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(50), nullable=False)

    # Create all tables for the models
    db.create_all()
    # Register the model with the service
    service.register_model_for_admin_panel("TestModel", TestModel)

    # Create a test record
    test_record = TestModel(name="Initial Name")
    db.session.add(test_record)
    db.session.commit()

    # Mock request and form data
    new_name = "Updated Name"
    form_data = MultiDict([("name", new_name)])  # Use MultiDict for form data
    with client.application.test_request_context(method="POST", data=form_data):
        # Call the edit_record method
        success, model_name, form = service.edit_record(
            request, "TestModel", test_record.id
        )

        # Assertions
        assert success is True
        assert model_name == "TestModel"
        assert form.errors == {}

        # Verify that the record was updated in the database
        updated_record = TestModel.query.get(test_record.id)
        assert updated_record.name == new_name


def test_edit_record_invalid_form(client, db, service):
    """Test editing an existing record with invalid form data."""

    # Create a test model class
    class TestModel(db.Model):
        __tablename__ = "test_model"
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(50), nullable=False)

    # Create all tables for the models
    db.create_all()
    # Register the model with the service
    service.register_model_for_admin_panel("TestModel", TestModel)

    # Create a test record
    test_record = TestModel(name="Initial Name")
    db.session.add(test_record)
    db.session.commit()

    # Mock request and invalid form data
    invalid_form_data = MultiDict([("name", "")])  # Use MultiDict for invalid form data
    with client.application.test_request_context(method="POST", data=invalid_form_data):
        # Call the edit_record method
        success, model_name, form = service.edit_record(
            request, "TestModel", test_record.id
        )

        # Assertions
        assert success is False
        assert model_name == "TestModel"
        assert form.errors != {}  # Form should have validation errors


def test_edit_record_model_not_found(service):
    """Test ModelNotFoundException when editing a record of an unregistered model."""
    # Mock request and form data
    with pytest.raises(ModelNotFoundException):
        service.edit_record(
            None, "NonExistentModel", 1
        )  # Pass None for request since we expect exception


def test_delete_record_success(client, db, service):
    """Test deleting a record from the model."""

    # Create a test model class
    class TestModel(db.Model):
        __tablename__ = "test_model"
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(50), nullable=False)

    # Create all tables for the models
    db.create_all()
    # Register the model with the service
    service.register_model_for_admin_panel("TestModel", TestModel)

    # Create a test record
    test_record = TestModel(name="Record to Delete")
    db.session.add(test_record)
    db.session.commit()

    # Call the delete_record method
    success, model_name, deleted_instance = service.delete_record(
        request, "TestModel", test_record.id
    )

    # Assertions
    assert success is True
    assert model_name == "TestModel"
    assert deleted_instance.name == "Record to Delete"
    assert (
        TestModel.query.get(test_record.id) is None
    )  # Verify that the record was deleted


def test_delete_record_model_not_found(service):
    """Test ModelNotFoundException when deleting a record from an unregistered model."""
    # Mock request and form data
    with pytest.raises(ModelNotFoundException):
        service.delete_record(
            None, "NonExistentModel", 1
        )  # Pass None for request since we expect exception


def test_model_not_found_exception(service):
    """Test ModelNotFoundException when accessing unregistered model."""
    with pytest.raises(ModelNotFoundException):
        service.list_records("NonExistentModel")
