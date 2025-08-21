import os
from flask import Flask
from flask_cors import CORS
from flask_smorest import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from .routes.health import blp
from .routes.auth import blp as auth_blp
from .routes.rooms import blp as rooms_blp
from .routes.students import blp as students_blp
from .routes.payments import blp as payments_blp
from .routes.attendance import blp as attendance_blp


app = Flask(__name__)
app.url_map.strict_.slashes = False
CORS(app, resources={r"/*": {"origins": "*"}})

# JWT Configuration
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "super-secret") # Change this in production
jwt = JWTManager(app)

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///data.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["API_TITLE"] = "Hostel Management API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config['OPENAPI_URL_PREFIX'] = '/docs'
app.config["OPENAPI_SWAGGER_UI_PATH"] = ""
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

db = SQLAlchemy(app)
migrate = Migrate(app, db)

api = Api(app)
api.register_blueprint(blp)
api.register_blueprint(auth_blp)
api.register_blueprint(rooms_blp)
api.register_blueprint(students_blp)
api.register_blueprint(payments_blp)
api.register_blueprint(attendance_blp)

# Import models to ensure they are registered with SQLAlchemy
from . import models
