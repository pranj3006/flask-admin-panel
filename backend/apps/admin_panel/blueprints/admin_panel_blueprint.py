"""
Admin Panel Blueprint
"""

from apps.admin_panel.controllers import admin_panel_ns
from apps.admin_panel.middlewares import mdw_authtoken
from flask import Blueprint
from flask_restx import Api

admin_panel_bp = Blueprint(
    "admin_panel",
    __name__,
    template_folder="../templates/")

admin_panel_bp.before_request(mdw_authtoken.middleware_method)

admin_panel_api = Api(
    admin_panel_bp,
    title="admin_panel",
    description="Admin Panel",
    doc="/swagger/"
)

admin_panel_api.add_namespace(admin_panel_ns)