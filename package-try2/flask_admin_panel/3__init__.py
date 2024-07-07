# # from flask_admin_panel.controllers import admin_panel_ns
# # from flask_admin_panel.middlewares import mdw_authtoken
# # from flask import Blueprint
# # from flask_restx import Api
# # from flask_admin_panel.controllers.admin_panel_controller import AdminPanelIndexController
# # from flask_admin_panel.middlewares import mdw_authtoken
# # from flask import Blueprint
# # from flask_restx import Api
# from injector import singleton, Binder,Injector,provider,Module
# # from flask_admin_panel.services import AdminPanelService
# from flask_injector import FlaskInjector
# from flask_restx import Api
# # from flask_sqlalchemy import SQLAlchemy
# # from flask import Flask

# # class AdminPanelModule(Module):
# #     """
# #     AdminPanel Injector Class definition
# #     """
# #     def __init__(self, app: Flask, db: SQLAlchemy):
# #         self.app = app
# #         self.db = db

# #     def configure(self, binder: Binder) -> None:
# #         binder.bind(
# #             Flask,
# #             to=self.app,
# #             scope=singleton)

# #         binder.bind(
# #             SQLAlchemy,
# #             to=self.db,
# #             scope=singleton)

# #         binder.bind(
# #             AdminPanelService,
# #             to=AdminPanelService,
# #             scope=singleton)

# # class AppModule(Module):
# #     @singleton
# #     @provider
# #     def provide_serv(self, app: Flask, db:SQLAlchemy) -> AdminPanelService:
# #         return Injector([AdminPanelModule(app,db)]).get(AdminPanelService)

# # admin_panel_bp = Blueprint(
# #     "flask_admin_panel",
# #     __name__,
# #     template_folder="../templates/")

# # admin_panel_bp.before_request(mdw_authtoken.middleware_method)

# # admin_panel_api = Api(
# #     admin_panel_bp,
# #     title="flask_admin_panel",
# #     description="Admin Panel",
# #     doc="/swagger/"
# # )

# # def configure(binder):
# #     binder.install(AppModule())

# class FlaskAdminPanel:
#     def __init__(self, app=None,db=None) -> None:
#         if app is not None and db is not None:
#             self.init_app(app,db)

#     def init_app(self, app,db):
#         from flask_admin_panel.blueprints import admin_panel_bp,admin_panel_api
#         from flask_admin_panel.injectors import AdminPanelModule
#         from flask_admin_panel.services import AdminPanelService

#         # Injector([AdminPanelModule(app, db)]).get(AdminPanelService)
#         # Store SomeService instance in Flask's g object
#         serv_admin_panel = Injector([AdminPanelModule(app, db)]).get(AdminPanelService)
#         # app.extensions['flask_admin_panel'] = serv_admin_panel
#         from flask_admin_panel.controllers.admin_panel_controller import AdminPanelIndexController,AdminPanelLoginPangeController,AdminPanelLoginController
#         admin_panel_api.add_resource(AdminPanelIndexController, "/", resource_class_kwargs={'serv_admin_panel': serv_admin_panel})
#         admin_panel_api.add_resource(AdminPanelLoginPangeController, "/page/login", resource_class_kwargs={'serv_admin_panel': serv_admin_panel})
#         admin_panel_api.add_resource(AdminPanelLoginController, "/login/", resource_class_kwargs={'serv_admin_panel': serv_admin_panel})

#         with app.app_context():
#             app.register_blueprint(admin_panel_bp)
#             for rule in app.url_map.iter_rules():
#                 print(f"Endpoint: {rule.endpoint}, URL: {rule.rule}")

# #         # admin_panel_api.add_namespace(admin_panel_ns)

# #         # FlaskInjector(app=app, modules=[configure])


# #         # admin_panel_bp = Blueprint(
# #         #     "flask_admin_panel",
# #         #     __name__,
# #         #     template_folder="../templates/")
# #         # admin_panel_bp.before_request(mdw_authtoken.middleware_method)
# #         # admin_panel_api = Api(app)
# #         # def register_resources(app, api, serv):



# #         # admin_panel_api = Api(
# #         #     admin_panel_bp,
# #         #     title="admin_panel",
# #         #     description="Admin Panel",
# #         #     doc="/swagger/"
# #         # )

# #         # admin_panel_api.add_namespace(admin_panel_ns)
# #         # app.register_blueprint(admin_panel_bp)
# #         # # admin_panel_api.init_app(app)
# #         # # app.register_blueprint(admin_panel_bp)
# #         # self.register_resources(app)
#         # app.config['TEMPLATES_AUTO_RELOAD'] = True
#         return app

# #     def register_resources(self,app):

# #         admin_panel_ns.add_resource(
# #             AdminPanelIndexController,
# #             "/",
# #             resource_class_kwargs={
# #                 'serv_admin_panel': injector.get(AdminPanelService)
# #                 }
# #         )
# __all__ = ['init_app','app','db']


# main.py
from flask import Flask, Blueprint, make_response, render_template
from flask_restx import Api, Namespace, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_injector import FlaskInjector
from injector import Binder, inject, singleton

from flask_admin_panel.services import AdminPanelService

# Resource classes
class AdminPanelIndexController(Resource):
    """Controller for Admin Panel Index"""
    @inject
    def __init__(self, api: Api, serv_admin_panel: AdminPanelService) -> None:
        super().__init__()
        self.api = api
        self.serv_admin_panel = serv_admin_panel

    def get(self):
        """
        Authenticate User and Generate Token
        """
        headers = {"Content-Type": "text/html"}
        html_content = render_template(
            "flask_admin_panel/index.html",
            app_title=self.serv_admin_panel.app_title,
            api_url_prefix=self.api.prefix,
        )
        return make_response(html_content, 200, headers)


class AdminPanelLoginPageController(Resource):
    """Controller for Admin Panel Login Page"""
    @inject
    def __init__(self, api: Api, serv_admin_panel: AdminPanelService) -> None:
        super().__init__()
        self.api = api
        self.serv_admin_panel = serv_admin_panel

    def get(self):
        """
        Authenticate User and Generate Token
        """
        headers = {"Content-Type": "text/html"}
        html_content = render_template(
            "flask_admin_panel/login.html",
            app_title=self.serv_admin_panel.app_title,
            api_url_prefix=self.api.prefix,
        )
        return make_response(html_content, 200, headers)


class FlaskAdminPanel:
    def __init__(self, app=None, db=None) -> None:
        if app is not None and db is not None:
            self.init_app(app, db)

    def init_app(self, app, db):
        def configure(binder: Binder, app: Flask, db: SQLAlchemy,api:Api,serv_admin_panel:AdminPanelService) -> None:
            binder.bind(Flask, to=app, scope=singleton)
            binder.bind(SQLAlchemy, to=db, scope=singleton)
            binder.bind(AdminPanelService, to=serv_admin_panel, scope=singleton)
            binder.bind(Api, to=api, scope=singleton)  # Bind Api instance
        serv_admin_panel=AdminPanelService(app,db)
        # Create a blueprint
        admin_bp = Blueprint('flask_admin_panel', __name__, template_folder="templates/")

        # Create an API instance
        # api = Api(admin_bp,  doc=False)
        admin_panel_api = Api(
            admin_bp,
            title="flask_admin_panel",
            description="Admin Panel",
            doc="/swagger/"
        )
        # Initialize FlaskInjector
        FlaskInjector(app=app, modules=[lambda binder: configure(binder, app, db,admin_panel_api,serv_admin_panel)])
        # Create a namespace
        admin_ns = Namespace('flask_admin_panel', description='Admin Panel Index Operations')

        # Add the resources to the namespace
        api.add_resource(AdminPanelIndexController, '/', resource_class_kwargs={'serv_admin_panel': serv_admin_panel})
        api.add_resource(AdminPanelLoginPageController, '/page/login', resource_class_kwargs={'serv_admin_panel': serv_admin_panel})

        # Add the namespace to the API
        api.add_namespace(admin_ns)

        # Register the blueprint
        app.register_blueprint(admin_bp)

        with app.app_context():
            for rule in app.url_map.iter_rules():
                print(f"Endpoint: {rule.endpoint}, URL: {rule.rule}")
        return app
