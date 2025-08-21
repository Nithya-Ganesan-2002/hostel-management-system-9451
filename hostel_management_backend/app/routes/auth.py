from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.models import User, UserRole
from app.schemas import UserSchema, LoginSchema

blp = Blueprint("Auth", "auth", url_prefix="/auth", description="Operations on users")


@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        if User.query.filter(User.username == user_data["username"]).first():
            abort(409, message="A user with that username already exists.")

        if User.query.filter(User.email == user_data["email"]).first():
            abort(409, message="A user with that email already exists.")

        user = User(
            username=user_data["username"],
            email=user_data["email"],
            password=generate_password_hash(user_data["password"]),
            role=user_data.get("role", UserRole.STUDENT)
        )
        db.session.add(user)
        db.session.commit()

        return {"message": "User created successfully."}, 201


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(LoginSchema)
    def post(self, user_data):
        user = User.query.filter(
            User.username == user_data["username"]
        ).first()

        if user and check_password_hash(user.password, user_data["password"]):
            additional_claims = {"is_admin": user.role == UserRole.ADMIN}
            access_token = create_access_token(identity=user.id, additional_claims=additional_claims)
            return {"access_token": access_token}

        abort(401, message="Invalid credentials.")
