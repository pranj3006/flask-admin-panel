"""
Flask Entrypoint
"""

import os
from flask import  jsonify, request
from flask_injector import FlaskInjector
from flask_migrate import Migrate
from runner import create_app, db
from flask_jwt_extended import  create_access_token
from flask_socketio import SocketIO
from socketio_def import socketio
app = create_app(os.getenv("FLASK_CONFIG","development"))
socketio.init_app(app)

migrate = Migrate(app,db)

# Sample user data
users = {
    "system1": {"password": '07776fe6177de4f1e46414d8'},
    "system2": {"password": '45b1b60cc22ece0ef40016d2'}
}

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    user = users.get(username)
    
    if user and user['password'] == password:
        access_token = create_access_token(identity={"username": username})
        return jsonify(access_token=access_token), 200
    return jsonify({"msg": "Bad credentials"}), 401

@app.shell_context_processor
def make_shell_context():
    return {
        "app":app,
        "db":db
    }

if __name__ == "__main__":
    socketio.run(app,host="0.0.0.0",port=8091,debug=True,allow_unsafe_werkzeug=True)