from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

# =====================
# USER
# =====================
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )


# =====================
# CLASS (NEW)
# =====================
class Classroom(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    class_name = db.Column(
        db.String(100),
        nullable=False
    )

    
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False
    )

    students = db.relationship(
        'Student',
        backref='classroom',
        lazy=True,
        cascade='all, delete'
    )


# =====================
# STUDENT (UPDATED)
# =====================
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(100),
        nullable=False
    )

    roll_number = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    # OLD: course
    # NEW: class relation
    classroom_id = db.Column(
        db.Integer,
        db.ForeignKey('classroom.id'),
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False
    )

    attendance_records = db.relationship(
        'Attendance',
        backref='student',
        lazy=True,
        cascade='all, delete'
    )


# =====================
# ATTENDANCE (SAME BUT CLEAN)
# =====================
class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(
        db.Integer,
        db.ForeignKey('student.id'),
        nullable=False
    )

    date = db.Column(
        db.String(50),
        nullable=False
    )

    status = db.Column(
        db.String(20),
        nullable=False
    )