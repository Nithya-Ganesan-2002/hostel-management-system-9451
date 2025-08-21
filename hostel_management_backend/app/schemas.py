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

class PaymentSchema(Schema):
    id = fields.Int(dump_only=True)
    student_id = fields.Int(required=True)
    amount = fields.Float(required=True)
    date = fields.DateTime(dump_only=True)
    status = fields.Str()

class PaymentUpdateSchema(Schema):
    amount = fields.Float()
    status = fields.Str()

class AttendanceSchema(Schema):
    id = fields.Int(dump_only=True)
    student_id = fields.Int(required=True)
    date = fields.Date(required=True)
    present = fields.Boolean(required=True)

class AttendanceUpdateSchema(Schema):
    date = fields.Date()
    present = fields.Boolean()


class NotificationSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(dump_only=True)
    message = fields.Str(dump_only=True)
    timestamp = fields.DateTime(dump_only=True)
    is_read = fields.Boolean()

class NotificationUpdateSchema(Schema):
    is_read = fields.Boolean(required=True)

class ProfileUpdateSchema(Schema):
    name = fields.Str()
    father_name = fields.Str()
    address = fields.Str()
    dob = fields.Date()
    phone_number = fields.Str()
