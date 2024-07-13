"""
Flask Entrypoint
"""

import os
from flask import  jsonify, request
from flask_injector import FlaskInjector
from flask_migrate import Migrate
from runner import create_app, db,adminpanel
from flask_jwt_extended import  create_access_token
app = create_app(os.getenv("FLASK_CONFIG","development"))

migrate = Migrate(app,db)


@app.shell_context_processor
def make_shell_context():
    return {
        "app":app,
        "db":db
    }

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

# with app.app_context():
#     db.create_all()

adminpanel.serv_admin_panel.register_model_for_admin_panel("User",User)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8091)