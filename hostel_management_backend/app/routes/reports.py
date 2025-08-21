from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required
from sqlalchemy import func

from app import db
from app.models import Room, Payment, Attendance
from app.decorators import admin_required

blp = Blueprint("Reports", "reports", url_prefix="/reports", description="Generate various reports")

@blp.route("/occupancy")
class OccupancyReport(MethodView):

    @jwt_required()
    @admin_required()
    def get(self):
        """Get a room occupancy report"""
        rooms = Room.query.all()
        report = [
            {
                "room_number": room.room_number,
                "capacity": room.capacity,
                "occupancy": room.occupancy,
                "percentage": (room.occupancy / room.capacity) * 100 if room.capacity > 0 else 0
            } for room in rooms
        ]
        return {"occupancy_report": report}

@blp.route("/payments")
class PaymentsReport(MethodView):
    
    @jwt_required()
    @admin_required()
    def get(self):
        """Get a summary of payments"""
        total_payments = db.session.query(func.sum(Payment.amount)).scalar() or 0.0
        pending_payments = db.session.query(func.sum(Payment.amount)).filter(Payment.status == 'Pending').scalar() or 0.0
        paid_payments = db.session.query(func.sum(Payment.amount)).filter(Payment.status == 'Paid').scalar() or 0.0

        return {
            "total_payments_collected": paid_payments,
            "total_pending_payments": pending_payments,
            "overall_total": total_payments
        }

@blp.route("/attendance")
class AttendanceReport(MethodView):

    @jwt_required()
    @admin_required()
    def get(self):
        """Get an attendance summary report"""
        total_records = Attendance.query.count()
        present_count = Attendance.query.filter_by(present=True).count()
        absent_count = total_records - present_count

        return {
            "total_attendance_records": total_records,
            "present_count": present_count,
            "absent_count": absent_count,
            "presenteeism_rate": (present_count/total_records) * 100 if total_records > 0 else 0
        }
