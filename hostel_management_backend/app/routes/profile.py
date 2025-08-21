from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import db
from app.models import Student
from app.schemas import StudentSchema, ProfileUpdateSchema

blp = Blueprint("Profile", "profile", url_prefix="/profile", description="Operations on user profile")

@blp.route("/")
class UserProfile(MethodView):

    @jwt_required()
    @blp.response(200, StudentSchema)
    def get(self):
        """Get the current user's profile"""
        user_id = get_jwt_identity()
        student = Student.query.filter_by(user_id=user_id).first_or_404()
        return student

    @jwt_required()
    @blp.arguments(ProfileUpdateSchema)
    @blp.response(200, StudentSchema)
    def put(self, profile_data):
        """Update the current user's profile"""
        user_id = get_jwt_identity()
        student = Student.query.filter_by(user_id=user_id).first_or_404()

        for key, value in profile_data.items():
            setattr(student, key, value)

        db.session.commit()
        return student
