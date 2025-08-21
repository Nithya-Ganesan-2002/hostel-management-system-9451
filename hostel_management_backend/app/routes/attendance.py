from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required

from app import db
from app.models import Attendance, Student
from app.schemas import AttendanceSchema, AttendanceUpdateSchema
from app.decorators import admin_required

blp = Blueprint("Attendance", "attendance", url_prefix="/attendance", description="Operations on attendance")

@blp.route("/")
class AttendanceList(MethodView):

    @jwt_required()
    @admin_required()
    @blp.response(200, AttendanceSchema(many=True))
    def get(self):
        """List all attendance records"""
        return Attendance.query.all()

    @jwt_required()
    @admin_required()
    @blp.arguments(AttendanceSchema)
    @blp.response(201, AttendanceSchema)
    def post(self, attendance_data):
        """Mark attendance for a student"""
        student = Student.query.get(attendance_data["student_id"])
        if not student:
            abort(404, message=f"Student with id {attendance_data['student_id']} not found.")
        
        existing_attendance = Attendance.query.filter_by(
            student_id=attendance_data["student_id"],
            date=attendance_data["date"]
        ).first()

        if existing_attendance:
            abort(409, message="Attendance for this student on this date has already been marked.")

        attendance = Attendance(**attendance_data)
        db.session.add(attendance)
        db.session.commit()
        return attendance

@blp.route("/<int:attendance_id>")
class AttendanceDetail(MethodView):

    @jwt_required()
    @admin_required()
    @blp.response(200, AttendanceSchema)
    def get(self, attendance_id):
        """Get a single attendance record"""
        attendance = Attendance.query.get_or_404(attendance_id)
        return attendance

    @jwt_required()
    @admin_required()
    @blp.arguments(AttendanceUpdateSchema)
    @blp.response(200, AttendanceSchema)
    def put(self, attendance_data, attendance_id):
        """Update an attendance record"""
        attendance = Attendance.query.get_or_404(attendance_id)
        
        if "date" in attendance_data:
            attendance.date = attendance_data["date"]
        if "present" in attendance_data:
            attendance.present = attendance_data["present"]
        
        db.session.add(attendance)
        db.session.commit()
        return attendance

    @jwt_required()
    @admin_required()
    @blp.response(204)
    def delete(self, attendance_id):
        """Delete an attendance record"""
        attendance = Attendance.query.get_or_404(attendance_id)
        db.session.delete(attendance)
        db.session.commit()
        return
