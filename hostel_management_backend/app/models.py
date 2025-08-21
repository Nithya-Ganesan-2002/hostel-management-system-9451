import enum
from datetime import datetime
from app import db

class UserRole(enum.Enum):
    STUDENT = "student"
    ADMIN = "admin"

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.Enum(UserRole), default=UserRole.STUDENT, nullable=False)
    student = db.relationship('Student', back_populates='user', uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<User {self.username}>'

class Room(db.Model):
    __tablename__ = 'rooms'
    id = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.String(10), unique=True, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    occupancy = db.Column(db.Integer, default=0)
    students = db.relationship('Student', backref='room', lazy=True)

    def __repr__(self):
        return f'<Room {self.room_number}>'

class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    user = db.relationship('User', back_populates='student')
    
    name = db.Column(db.String(120), nullable=False)
    father_name = db.Column(db.String(120))
    address = db.Column(db.String(255))
    dob = db.Column(db.Date)
    phone_number = db.Column(db.String(20))
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'))
    
    payments = db.relationship('Payment', backref='student', lazy=True, cascade="all, delete-orphan")
    attendances = db.relationship('Attendance', backref='student', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Student {self.name}>'

class Payment(db.Model):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    status = db.Column(db.String(20), default='Pending') # e.g., Pending, Paid, Overdue

    def __repr__(self):
        return f'<Payment {self.id} for Student {self.student_id}>'

class Attendance(db.Model):
    __tablename__ = 'attendances'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    present = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Attendance {self.id} for Student {self.student_id} on {self.date}>'

class Notification(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) # Can be for admin or student
    message = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)
    user = db.relationship('User', backref=db.backref('notifications', lazy=True, cascade="all, delete-orphan"))


    def __repr__(self):
        return f'<Notification {self.id} for User {self.user_id}>'
