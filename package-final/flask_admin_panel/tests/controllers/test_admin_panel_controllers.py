import pytest
from injector import Injector
from flask import Flask, jsonify
from flask.testing import FlaskClient
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api, Namespace
from werkzeug.datastructures import MultiDict
from unittest.mock import patch
from injector import Binder, singleton, inject
from flask_admin_panel.controllers.admin_panel_controller import (
    AdminPanelIndexController,
    AdminPanelLoginPageController,
    AdminPanelLoginController,
    AdminPanelRefreshTokenController,
    AdminPanelListModelController,
    AdminPanelListRecordsController,
    AdminPanelEditRecordController,
    AdminPanelAddRecordController,
    AdminPanelDeleteRecordController,
    AdminPanelService,
)
from flask_admin_panel.blueprints.admin_panel_blueprint import (
    admin_panel_api,
    admin_panel_bp,
)


@pytest.fixture(scope="module")
def app():
    """Create and return a Flask app instance for testing."""
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["TESTING"] = True
    # app.template_folder = '../templates/'

    # Initialize SQLAlchemy
    db = SQLAlchemy(app)

    def configure(
        binder: Binder, app: Flask, db: SQLAlchemy, admin_panel_api: Api
    ) -> None:
        """Configure bindings for dependency injection."""
        binder.bind(Flask, to=app, scope=singleton)
        binder.bind(SQLAlchemy, to=db, scope=singleton)
        binder.bind(Api, to=admin_panel_api, scope=singleton)

    # Bind dependencies
    injector = Injector([lambda binder: configure(binder, app, db, admin_panel_api)])
    serv_admin_panel = injector.get(AdminPanelService)
    _admin_panel_ns = Namespace(
        "flask_admin_panel", description="Admin Panel Index Operations"
    )

    # Register controllers with API
    from flask_admin_panel.controllers.admin_panel_controller import (
        AdminPanelIndexController,
        AdminPanelLoginPageController,
        AdminPanelLoginController,
        AdminPanelRefreshTokenController,
        AdminPanelListModelController,
        AdminPanelListRecordsController,
        AdminPanelEditRecordController,
        AdminPanelAddRecordController,
        AdminPanelDeleteRecordController,
    )

    admin_panel_api.add_resource(
        AdminPanelIndexController,
        "/home",
        resource_class_kwargs={"serv_admin_panel": serv_admin_panel},
    )
    admin_panel_api.add_resource(
        AdminPanelLoginPageController,
        "/page/login",
        resource_class_kwargs={"serv_admin_panel": serv_admin_panel},
    )
    admin_panel_api.add_resource(
        AdminPanelLoginController,
        "/login/",
        resource_class_kwargs={"serv_admin_panel": serv_admin_panel},
    )
    admin_panel_api.add_resource(
        AdminPanelRefreshTokenController,
        "/refresh_token/",
        resource_class_kwargs={"serv_admin_panel": serv_admin_panel},
    )
    admin_panel_api.add_resource(
        AdminPanelListModelController,
        "/list_models/",
        resource_class_kwargs={"serv_admin_panel": serv_admin_panel},
    )
    admin_panel_api.add_resource(
        AdminPanelListRecordsController,
        "/list_records/<model_name>/",
        resource_class_kwargs={"serv_admin_panel": serv_admin_panel},
    )
    admin_panel_api.add_resource(
        AdminPanelEditRecordController,
        "/<model_name>/edit_record/<int:id>",
        methods=["GET", "POST"],
        resource_class_kwargs={"serv_admin_panel": serv_admin_panel},
    )
    admin_panel_api.add_resource(
        AdminPanelAddRecordController,
        "/add_record/<model_name>/",
        methods=["GET", "POST"],
        resource_class_kwargs={"serv_admin_panel": serv_admin_panel},
    )
    admin_panel_api.add_resource(
        AdminPanelDeleteRecordController,
        "/<model_name>/delete_record/<int:id>",
        methods=["POST"],
        resource_class_kwargs={"serv_admin_panel": serv_admin_panel},
    )

    admin_panel_api.add_namespace(_admin_panel_ns)
    app.register_blueprint(admin_panel_bp, url_prefix="/flask_admin_panel")

    class TestModel(db.Model):
        __tablename__ = "test_model"
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(50), nullable=False)

    with app.app_context():
        # Create all tables for the models
        db.create_all()
        # Register the model with the service
        serv_admin_panel.register_model_for_admin_panel("TestModel", TestModel)

        # Create test records
        test_record_1 = TestModel(name="Record 1")
        test_record_2 = TestModel(name="Record 2")
        db.session.add_all([test_record_1, test_record_2])
        db.session.commit()

    yield app


@pytest.fixture
def client(app):
    """Create a test client for the Flask app."""
    with app.test_client() as client:
        with app.app_context():
            yield client


def test_admin_panel_index_controller_get(client: FlaskClient):
    """Test GET request to AdminPanelIndexController."""
    response = client.get("/flask_admin_panel/home")
    assert response.status_code == 200
    assert "App Admin Panel" in response.data.decode("utf-8")


def test_admin_panel_login_page_controller_get(client: FlaskClient):
    """Test GET request to AdminPanelLoginPageController."""

    response = client.get("/flask_admin_panel/page/login")
    assert response.status_code == 200
    assert "text/html" in response.headers["Content-Type"]


def test_admin_panel_list_model_controller_get(client: FlaskClient):
    """Test GET request to AdminPanelListModelController."""
    response = client.get("/flask_admin_panel/list_models/")
    response_text = response.data.decode("utf-8")

    # Check if the expected text is in the response
    assert response.status_code == 200
    assert "text/html" in response.headers["Content-Type"]
    assert "TestModel" in response_text


def test_admin_panel_list_record_controller_get(client: FlaskClient):
    """Test GET request to AdminPanelListRecordsController."""
    response = client.get("/flask_admin_panel/list_records/TestModel/")
    response_text = response.data.decode("utf-8")
    assert response.status_code == 200
    assert "Record 1" in response_text


def test_admin_panel_edit_record_controller_get(client: FlaskClient):
    """Test POST request to AdminPanelEditRecordController."""
    response = client.get("/flask_admin_panel/TestModel/edit_record/1")
    response_text = response.data.decode("utf-8")
    assert response.status_code == 200
    assert "TestModel Edit Form" in response_text
    assert "Record 1" in response_text


def test_admin_panel_edit_record_controller_post(client: FlaskClient):
    """Test POST request to AdminPanelEditRecordController."""
    data = {"name": "name", "value": "Record 2"}
    response = client.post("/flask_admin_panel/TestModel/edit_record/1", data=data)
    response_text = response.data.decode("utf-8")
    assert response.status_code == 302
    assert "/flask_admin_panel/list_records/TestModel/" in response_text


def test_admin_panel_add_record_controller_post(client: FlaskClient):
    """Test POST request to AdminPanelAddRecordController."""
    data = {"name": "name3", "value": "Record 3"}
    response = client.post("/flask_admin_panel/add_record/TestModel/", data=data)
    response_text = response.data.decode("utf-8")
    assert response.status_code == 302
    assert "/flask_admin_panel/list_records/TestModel/" in response_text


def test_admin_panel_delete_record_controller_post(client: FlaskClient):
    """Test POST request to AdminPanelDeleteRecordController."""
    response = client.post("/flask_admin_panel/TestModel/delete_record/1")
    response_text = response.data.decode("utf-8")
    assert response.status_code == 302
    assert "/flask_admin_panel/list_records/TestModel/" in response_text
