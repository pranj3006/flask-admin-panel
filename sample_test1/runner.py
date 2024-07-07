"""
Top level module

This module creates app and registers extensions
"""

import sys
import logger_config
from configs import config_by_name

from extensions import  db, adminpnl
from flask import Flask

def create_app(config_name:str):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    cli= sys.modules["flask.cli"]
    cli.show_server_banner = lambda *x: None

    # logger_config.configure_logging()

    register_extensions(app)
    return app


def register_extensions(app):
    """ Register flask extensions """
    db.init_app(app)
    # ma.init_app(app)
    # jwt.init_app(app)
    # bcrypt.init_app(app)
    # cors.init_app(app)
    adminpnl.init_app(app,db)
