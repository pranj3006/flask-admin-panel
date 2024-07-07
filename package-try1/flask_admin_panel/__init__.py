# from flask_admin_panel.controllers import admin_panel_ns
# from flask_admin_panel.middlewares import mdw_authtoken
# from flask import Blueprint
# from flask_restx import Api
# from flask_admin_panel.controllers.admin_panel_controller import AdminPanelIndexController
# from flask_admin_panel.middlewares import mdw_authtoken
# from flask import Blueprint
# from flask_restx import Api
from injector import singleton, Binder,Injector,provider,Module
# from flask_admin_panel.services import AdminPanelService
from flask_injector import FlaskInjector
from flask_restx import Api
# from flask_sqlalchemy import SQLAlchemy
# from flask import Flask

# class AdminPanelModule(Module):
#     """
#     AdminPanel Injector Class definition
#     """    
#     def __init__(self, app: Flask, db: SQLAlchemy):
#         self.app = app
#         self.db = db

#     def configure(self, binder: Binder) -> None:
#         binder.bind(
#             Flask, 
#             to=self.app, 
#             scope=singleton)
        
#         binder.bind(
#             SQLAlchemy, 
#             to=self.db, 
#             scope=singleton)
        
#         binder.bind(
#             AdminPanelService, 
#             to=AdminPanelService, 
#             scope=singleton)

# class AppModule(Module):
#     @singleton
#     @provider
#     def provide_serv(self, app: Flask, db:SQLAlchemy) -> AdminPanelService:
#         return Injector([AdminPanelModule(app,db)]).get(AdminPanelService)

# admin_panel_bp = Blueprint(
#     "flask_admin_panel",
#     __name__,
#     template_folder="../templates/")

# admin_panel_bp.before_request(mdw_authtoken.middleware_method)

# admin_panel_api = Api(
#     admin_panel_bp,
#     title="flask_admin_panel",
#     description="Admin Panel",
#     doc="/swagger/"
# )

# def configure(binder):
#     binder.install(AppModule())

class FlaskAdminPanel:
    def __init__(self, app=None,db=None) -> None:
        if app is not None and db is not None:
            self.init_app(app,db)

    def init_app(self, app,db):
        from flask_admin_panel.blueprints import admin_panel_bp
        from flask_admin_panel.injectors import AdminPanelModule
        from flask_admin_panel.services import AdminPanelService
        with app.app_context():
            app.register_blueprint(admin_panel_bp)

        # Injector([AdminPanelModule(app, db)]).get(AdminPanelService)
        # Store SomeService instance in Flask's g object
        serv_admin_panel = Injector([AdminPanelModule(app, db)]).get(AdminPanelService)
        app.extensions['flask_admin_panel'] = serv_admin_panel
        
        
#         # admin_panel_api.add_namespace(admin_panel_ns)
        
#         # FlaskInjector(app=app, modules=[configure])
        

#         # admin_panel_bp = Blueprint(
#         #     "flask_admin_panel",
#         #     __name__,
#         #     template_folder="../templates/")
#         # admin_panel_bp.before_request(mdw_authtoken.middleware_method)
#         # admin_panel_api = Api(app)
#         # def register_resources(app, api, serv):
            
        
        
#         # admin_panel_api = Api(
#         #     admin_panel_bp,
#         #     title="admin_panel",
#         #     description="Admin Panel",
#         #     doc="/swagger/"
#         # )

#         # admin_panel_api.add_namespace(admin_panel_ns)
#         # app.register_blueprint(admin_panel_bp)
#         # # admin_panel_api.init_app(app)
#         # # app.register_blueprint(admin_panel_bp)
#         # self.register_resources(app)
        # app.config['TEMPLATES_AUTO_RELOAD'] = True
        return app

#     def register_resources(self,app):
        
#         admin_panel_ns.add_resource(
#             AdminPanelIndexController, 
#             "/", 
#             resource_class_kwargs={
#                 'serv_admin_panel': injector.get(AdminPanelService)
#                 }
#         )
__all__ = ['init_app','app','db']