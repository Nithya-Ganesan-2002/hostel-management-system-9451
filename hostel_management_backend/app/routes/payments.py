from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required

from app import db
from app.models import Payment, Student
from app.schemas import PaymentSchema, PaymentUpdateSchema
from app.decorators import admin_required

blp = Blueprint("Payments", "payments", url_prefix="/payments", description="Operations on payments")

@blp.route("/")
class PaymentList(MethodView):

    @jwt_required()
    @admin_required()
    @blp.response(200, PaymentSchema(many=True))
    def get(self):
        """List all payments"""
        return Payment.query.all()

    @jwt_required()
    @admin_required()
    @blp.arguments(PaymentSchema)
    @blp.response(201, PaymentSchema)
    def post(self, payment_data):
        """Create a new payment"""
        student = Student.query.get(payment_data["student_id"])
        if not student:
            abort(404, message=f"Student with id {payment_data['student_id']} not found.")
        
        payment = Payment(**payment_data)
        db.session.add(payment)
        db.session.commit()
        return payment

@blp.route("/<int:payment_id>")
class PaymentDetail(MethodView):

    @jwt_required()
    @admin_required()
    @blp.response(200, PaymentSchema)
    def get(self, payment_id):
        """Get a single payment's details"""
        payment = Payment.query.get_or_404(payment_id)
        return payment

    @jwt_required()
    @admin_required()
    @blp.arguments(PaymentUpdateSchema)
    @blp.response(200, PaymentSchema)
    def put(self, payment_data, payment_id):
        """Update a payment's details"""
        payment = Payment.query.get_or_404(payment_id)
        
        if "amount" in payment_data:
            payment.amount = payment_data["amount"]
        if "status" in payment_data:
            payment.status = payment_data["status"]
        
        db.session.add(payment)
        db.session.commit()
        return payment

    @jwt_required()
    @admin_required()
    @blp.response(204)
    def delete(self, payment_id):
        """Delete a payment"""
        payment = Payment.query.get_or_404(payment_id)
        db.session.delete(payment)
        db.session.commit()
        return
