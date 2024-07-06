"""
Flask Entrypoint
"""

import os
from flask import  jsonify, request
from flask_injector import FlaskInjector
from flask_migrate import Migrate
from runner import create_app, db
from flask_jwt_extended import  create_access_token
app = create_app(os.getenv("FLASK_CONFIG","development"))

migrate = Migrate(app,db)


@app.shell_context_processor
def make_shell_context():
    return {
        "app":app,
        "db":db
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8091)