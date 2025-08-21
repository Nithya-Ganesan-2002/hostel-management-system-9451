from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)
    role = fields.Str(dump_only=True)

class LoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)

class RoomSchema(Schema):
    id = fields.Int(dump_only=True)
    room_number = fields.Str(required=True)
    capacity = fields.Int(required=True)
    occupancy = fields.Int(dump_only=True)

class RoomUpdateSchema(Schema):
    capacity = fields.Int()
    occupancy = fields.Int()

class StudentSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    user = fields.Nested(UserSchema, dump_only=True)
    name = fields.Str(required=True)
    father_name = fields.Str()
    address = fields.Str()
    dob = fields.Date()
    phone_number = fields.Str()
    room_id = fields.Int()

class StudentUpdateSchema(Schema):
    name = fields.Str()
    father_name = fields.Str()
    address = fields.Str()
    dob = fields.Date()
    phone_number = fields.Str()
    room_id = fields.Int()
