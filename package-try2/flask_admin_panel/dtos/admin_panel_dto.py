"""
DTO for AdminPanelDto
"""

from flask_restx import Namespace, fields


class AdminPanelDto:
    """
    AdminPanelDto DTO definition
    """

    api = Namespace("flask_admin_panel", description="Admin panel all models")
    