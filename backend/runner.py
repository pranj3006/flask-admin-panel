"""
Top level module

This module creates app and registers extensions
"""

import sys
import logger_config
from configs import config_by_name

from extensions import bcrypt, cors, db, jwt, ma,adminpanel
from flask import Flask

def create_app(config_name:str):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    cli= sys.modules["flask.cli"]
    cli.show_server_banner = lambda *x: None

    logger_config.configure_logging()

    register_extensions(app)
    register_blueprints(app)
    return app

def register_blueprints(app):
    from apps.healthcheck.blueprints import healthcheck_bp,healthcheck_token_bp    
    from apps.admin_panel.blueprints import admin_panel_bp
    
    app.register_blueprint(healthcheck_bp,url_prefix="/api/healthcheck/")
    app.register_blueprint(healthcheck_token_bp,url_prefix="/api/token/healthcheck/")
    # app.register_blueprint(admin_panel_bp,url_prefix="/api/admin_panel/")    


def register_extensions(app):
    """ Register flask extensions """
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    cors.init_app(app)
    adminpanel.init_app(app,db)
