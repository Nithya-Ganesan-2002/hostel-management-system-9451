from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required

from app import db
from app.models import Student, User, Room
from app.schemas import StudentSchema, StudentUpdateSchema
from app.decorators import admin_required

blp = Blueprint("Students", "students", url_prefix="/students", description="Operations on students")

@blp.route("/")
class StudentList(MethodView):

    @jwt_required()
    @admin_required()
    @blp.response(200, StudentSchema(many=True))
    def get(self):
        """List all students"""
        return Student.query.all()

    @jwt_required()
    @admin_required()
    @blp.arguments(StudentSchema)
    @blp.response(201, StudentSchema)
    def post(self, student_data):
        """Create a new student"""
        user = User.query.get(student_data["user_id"])
        if not user:
            abort(404, message=f"User with id {student_data['user_id']} not found.")
        
        if student_data.get("room_id"):
            room = Room.query.get(student_data["room_id"])
            if not room:
                abort(404, message=f"Room with id {student_data['room_id']} not found.")
            if room.occupancy >= room.capacity:
                abort(400, message="Room is already full.")
            room.occupancy += 1

        student = Student(**student_data)
        db.session.add(student)
        db.session.commit()
        
        return student

@blp.route("/<int:student_id>")
class StudentDetail(MethodView):

    @jwt_required()
    @admin_required()
    @blp.response(200, StudentSchema)
    def get(self, student_id):
        """Get a single student's details"""
        student = Student.query.get_or_404(student_id)
        return student

    @jwt_required()
    @admin_required()
    @blp.arguments(StudentUpdateSchema)
    @blp.response(200, StudentSchema)
    def put(self, student_data, student_id):
        """Update a student's details"""
        student = Student.query.get_or_404(student_id)

        # Handle room change
        if "room_id" in student_data and student_data["room_id"] != student.room_id:
            if student.room: # Decrement occupancy of old room
                student.room.occupancy -= 1
            
            new_room = Room.query.get(student_data["room_id"])
            if not new_room:
                 abort(404, message=f"Room with id {student_data['room_id']} not found.")
            if new_room.occupancy >= new_room.capacity:
                abort(400, message="New room is already full.")
            new_room.occupancy += 1
            student.room_id = student_data["room_id"]

        for key, value in student_data.items():
            if key != "room_id":
                setattr(student, key, value)

        db.session.commit()
        return student

    @jwt_required()
    @admin_required()
    @blp.response(204)
    def delete(self, student_id):
        """Delete a student"""
        student = Student.query.get_or_404(student_id)
        if student.room:
            student.room.occupancy -= 1
        db.session.delete(student)
        db.session.commit()
        return
