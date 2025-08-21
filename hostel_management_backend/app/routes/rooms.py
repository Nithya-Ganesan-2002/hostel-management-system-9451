from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required

from app import db
from app.models import Room
from app.schemas import RoomSchema, RoomUpdateSchema
from app.decorators import admin_required

blp = Blueprint("Rooms", "rooms", url_prefix="/rooms", description="Operations on rooms")

@blp.route("/")
class RoomList(MethodView):

    @jwt_required()
    @admin_required()
    @blp.response(200, RoomSchema(many=True))
    def get(self):
        """List all rooms"""
        return Room.query.all()

    @jwt_required()
    @admin_required()
    @blp.arguments(RoomSchema)
    @blp.response(201, RoomSchema)
    def post(self, room_data):
        """Create a new room"""
        if Room.query.filter(Room.room_number == room_data["room_number"]).first():
            abort(409, message="A room with that room number already exists.")
        
        room = Room(**room_data)
        db.session.add(room)
        db.session.commit()
        return room

@blp.route("/<int:room_id>")
class RoomDetail(MethodView):

    @jwt_required()
    @admin_required()
    @blp.response(200, RoomSchema)
    def get(self, room_id):
        """Get a single room's details"""
        room = Room.query.get_or_404(room_id)
        return room

    @jwt_required()
    @admin_required()
    @blp.arguments(RoomUpdateSchema)
    @blp.response(200, RoomSchema)
    def put(self, room_data, room_id):
        """Update a room's details"""
        room = Room.query.get_or_404(room_id)
        if "capacity" in room_data:
            room.capacity = room_data["capacity"]
        if "occupancy" in room_data:
            room.occupancy = room_data["occupancy"]
        
        db.session.add(room)
        db.session.commit()
        return room

    @jwt_required()
    @admin_required()
    @blp.response(204)
    def delete(self, room_id):
        """Delete a room"""
        room = Room.query.get_or_404(room_id)
        if room.students:
            abort(400, message="Cannot delete room with assigned students.")
        db.session.delete(room)
        db.session.commit()
        return
