from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from apps.flask_admin_panel import FlaskAdminPanel
db = SQLAlchemy()
bcrypt =Bcrypt()
migrate = Migrate()
cors = CORS()

jwt =JWTManager()
ma = Marshmallow()

adminpanel = FlaskAdminPanel()