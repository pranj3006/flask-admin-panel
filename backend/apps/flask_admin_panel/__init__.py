from flask import Flask
from flask_restx import Api, Namespace
from flask_sqlalchemy import SQLAlchemy
from flask_injector import FlaskInjector
from injector import Binder, inject, singleton, Injector
from apps.flask_admin_panel.injectors import AdminPanelModule
from apps.flask_admin_panel.services import AdminPanelService
from apps.flask_admin_panel.blueprints.admin_panel_blueprint import (
    admin_panel_api,
    admin_panel_bp,
)
from apps.flask_admin_panel.controllers.admin_panel_controller import (
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


class FlaskAdminPanel:

    def __init__(self, app=None, db=None) -> None:
        self.serv_admin_panel: AdminPanelService = None
        if app is not None and db is not None:
            self.init_app(app, db)

    def init_app(self, app, db):

        def configure(binder: Binder, app: Flask, db: SQLAlchemy, api: Api) -> None:
            binder.bind(Flask, to=app, scope=singleton)
            binder.bind(SQLAlchemy, to=db, scope=singleton)
            binder.bind(Api, to=admin_panel_api, scope=singleton)

        self.serv_admin_panel = Injector([AdminPanelModule(app, db)]).get(
            AdminPanelService
        )

        # Initialize FlaskInjector
        FlaskInjector(
            app=app,
            modules=[lambda binder: configure(binder, app, db, admin_panel_api)],
        )

        # Create a namespace
        _admin_panel_ns = Namespace(
            "flask_admin_panel", description="Admin Panel Index Operations"
        )

        # Add the resources to the namespace
        admin_panel_api.add_resource(
            AdminPanelIndexController,
            "/home",
            resource_class_kwargs={"serv_admin_panel": self.serv_admin_panel},
        )
        admin_panel_api.add_resource(
            AdminPanelLoginPageController,
            "/page/login",
            resource_class_kwargs={"serv_admin_panel": self.serv_admin_panel},
        )
        admin_panel_api.add_resource(
            AdminPanelLoginController,
            "/login/",
            resource_class_kwargs={"serv_admin_panel": self.serv_admin_panel},
        )
        admin_panel_api.add_resource(
            AdminPanelRefreshTokenController,
            "/refresh_token/",
            resource_class_kwargs={"serv_admin_panel": self.serv_admin_panel},
        )

        admin_panel_api.add_resource(
            AdminPanelListModelController,
            "/list_models/",
            resource_class_kwargs={"serv_admin_panel": self.serv_admin_panel},
        )
        admin_panel_api.add_resource(
            AdminPanelListRecordsController,
            "/list_records/<model_name>/",
            resource_class_kwargs={"serv_admin_panel": self.serv_admin_panel},
        )
        admin_panel_api.add_resource(
            AdminPanelEditRecordController,
            "/<model_name>/edit_record/<int:id>",
            methods=["GET", "POST"],
            resource_class_kwargs={"serv_admin_panel": self.serv_admin_panel},
        )
        admin_panel_api.add_resource(
            AdminPanelAddRecordController,
            "/add_record/<model_name>/",
            methods=["GET", "POST"],
            resource_class_kwargs={"serv_admin_panel": self.serv_admin_panel},
        )
        admin_panel_api.add_resource(
            AdminPanelDeleteRecordController,
            "/<model_name>/delete_record/<int:id>",
            methods=["POST"],
            resource_class_kwargs={"serv_admin_panel": self.serv_admin_panel},
        )

        # Add the namespace to the API
        admin_panel_api.add_namespace(_admin_panel_ns)

        # Register the blueprint
        app.register_blueprint(admin_panel_bp, url_prefix="/flask_admin_panel")

        return app
