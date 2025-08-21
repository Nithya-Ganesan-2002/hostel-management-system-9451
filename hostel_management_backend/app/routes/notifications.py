from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import db
from app.models import Notification
from app.schemas import NotificationSchema, NotificationUpdateSchema

blp = Blueprint("Notifications", "notifications", url_prefix="/notifications", description="Operations on notifications")

@blp.route("/")
class NotificationList(MethodView):

    @jwt_required()
    @blp.response(200, NotificationSchema(many=True))
    def get(self):
        """List all notifications for the current user"""
        user_id = get_jwt_identity()
        return Notification.query.filter_by(user_id=user_id).order_by(Notification.timestamp.desc()).all()

@blp.route("/<int:notification_id>/read")
class NotificationRead(MethodView):

    @jwt_required()
    @blp.arguments(NotificationUpdateSchema)
    @blp.response(200, NotificationSchema)
    def put(self, notification_data, notification_id):
        """Mark a notification as read or unread"""
        user_id = get_jwt_identity()
        notification = Notification.query.filter_by(id=notification_id, user_id=user_id).first_or_404()
        
        notification.is_read = notification_data["is_read"]
        
        db.session.add(notification)
        db.session.commit()
        return notification

@blp.route("/read-all")
class ReadAllNotifications(MethodView):

    @jwt_required()
    @blp.response(204)
    def put(self):
        """Mark all notifications as read for the current user"""
        user_id = get_jwt_identity()
        notifications = Notification.query.filter_by(user_id=user_id, is_read=False)
        for notification in notifications:
            notification.is_read = True
        
        db.session.commit()
        return
