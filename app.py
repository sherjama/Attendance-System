import os
import io
import matplotlib
matplotlib.use('Agg')

import pymysql
pymysql.install_as_MySQLdb()

from flask import Flask, render_template, redirect, url_for, request, flash, send_file

from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user
)

from werkzeug.security import generate_password_hash, check_password_hash

from config import Config
from models import db, User, Student, Attendance, Classroom

import matplotlib.pyplot as plt
from datetime import datetime, date


# =========================
# APP INIT
# =========================
app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

with app.app_context():
    db.create_all()


# =========================
# LOGIN MANAGER
# =========================
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# =========================
# HOME
# =========================
@app.route('/')
def home():
    return redirect(url_for('login'))


# =========================
# REGISTER
# =========================
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('register'))

        user = User(
            username=username,
            password=generate_password_hash(password)
        )

        db.session.add(user)
        db.session.commit()

        flash('Registration Successful')
        return redirect(url_for('login'))

    return render_template('register.html')


# =========================
# LOGIN
# =========================
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))

        flash('Invalid Credentials')

    return render_template('login.html')


# =========================
# LOGOUT
# =========================
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# =========================
# DASHBOARD
# =========================
@app.route('/dashboard')
@login_required
def dashboard():

    total_students = Student.query.filter_by(user_id=current_user.id).count()

    total_attendance = Attendance.query.join(Student).filter(
        Student.user_id == current_user.id
    ).count()

    present_count = Attendance.query.join(Student).filter(
        Student.user_id == current_user.id,
        Attendance.status == 'Present'
    ).count()

    absent_count = Attendance.query.join(Student).filter(
        Student.user_id == current_user.id,
        Attendance.status == 'Absent'
    ).count()

    return render_template(
        'dashboard.html',
        total_students=total_students,
        total_attendance=total_attendance,
        present_count=present_count,
        absent_count=absent_count
    )


# =========================
# CLASSES
# =========================
@app.route('/classes')
@login_required
def classes():

    classes = Classroom.query.filter_by(user_id=current_user.id).all()

    return render_template('classes.html', classes=classes)


@app.route('/add_class', methods=['GET', 'POST'])
@login_required
def add_class():

    if request.method == 'POST':

        new_class = Classroom(
            class_name=request.form['class_name'],
            user_id=current_user.id
        )

        db.session.add(new_class)
        db.session.commit()

        flash('Class Created Successfully')
        return redirect(url_for('classes'))

    return render_template('add_class.html')


@app.route('/class/<int:id>')
@login_required
def class_details(id):

    classroom = Classroom.query.filter_by(
        id=id,
        user_id=current_user.id
    ).first_or_404()

    students = Student.query.filter_by(
        classroom_id=id,
        user_id=current_user.id
    ).all()

    return render_template(
        'class_details.html',
        classroom=classroom,
        students=students
    )


# =========================
# STUDENTS
# =========================
@app.route('/students')
@login_required
def students():

    students = Student.query.filter_by(user_id=current_user.id).all()

    return render_template('students.html', students=students)


@app.route('/add_student/<int:class_id>', methods=['GET', 'POST'])
@login_required
def add_student(class_id):

    classroom = Classroom.query.filter_by(
        id=class_id,
        user_id=current_user.id
    ).first_or_404()

    if request.method == 'POST':

        student = Student(
            name=request.form['name'],
            roll_number=request.form['roll_number'],
            classroom_id=class_id,
            user_id=current_user.id
        )

        db.session.add(student)
        db.session.commit()

        flash('Student Added Successfully')
        return redirect(url_for('class_details', id=class_id))

    return render_template('add_student.html', classroom=classroom)


@app.route('/delete_student/<int:id>')
@login_required
def delete_student(id):

    student = Student.query.filter_by(
        id=id,
        user_id=current_user.id
    ).first_or_404()

    db.session.delete(student)
    db.session.commit()

    flash('Student Deleted')
    return redirect(url_for('students'))


# =========================
# STUDENT PROFILE
# =========================
@app.route('/student/<int:id>')
@login_required
def student_profile(id):

    student = Student.query.filter_by(
        id=id,
        user_id=current_user.id
    ).first_or_404()

    present_count = Attendance.query.filter_by(
        student_id=id,
        status='Present'
    ).count()

    absent_count = Attendance.query.filter_by(
        student_id=id,
        status='Absent'
    ).count()

    total_attendance = present_count + absent_count

    return render_template(
        'student_profile.html',
        student=student,
        present_count=present_count,
        absent_count=absent_count,
        total_attendance=total_attendance
    )


# =========================
# ATTENDANCE CALENDAR
# =========================
@app.route('/attendance')
@login_required
def attendance():

    records = Attendance.query.join(Student).filter(
        Student.user_id == current_user.id
    ).all()

    events = []

    for r in records:
        d = r.date
        date_str = d.strftime("%Y-%m-%d") if hasattr(d, 'strftime') else str(d)

        events.append({
            "title": r.student.name,
            "start": date_str,
            "color": "#22c55e" if r.status == "Present" else "#ef4444",
            "display": "block"
        })

    return render_template("attendance.html", events=events)


@app.route('/attendance/<date_str>')
@login_required
def attendance_by_date(date_str):

    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return "Invalid date format", 400

    records = Attendance.query.join(Student).filter(
        Attendance.date == date_str,
        Student.user_id == current_user.id
    ).all()

    return render_template(
        'attendance_details.html',
        records=records,
        selected_date=date_str
    )


@app.route('/mark_attendance', methods=['GET', 'POST'])
@login_required
def mark_attendance():

    students = Student.query.filter_by(user_id=current_user.id).all()

    if request.method == 'POST':

        attendance = Attendance(
            student_id=request.form['student_id'],
            date=request.form['date'],
            status=request.form['status']
        )

        db.session.add(attendance)
        db.session.commit()

        flash('Attendance Marked Successfully')
        return redirect(url_for('mark_attendance'))

    return render_template('mark_attendance.html', students=students)


# =========================
# ANALYTICS
# =========================
@app.route('/analytics')
@login_required
def analytics():

    os.makedirs('static/charts', exist_ok=True)

    present = Attendance.query.join(Student).filter(
        Student.user_id == current_user.id,
        Attendance.status == 'Present'
    ).count()

    absent = Attendance.query.join(Student).filter(
        Student.user_id == current_user.id,
        Attendance.status == 'Absent'
    ).count()

    plt.figure(figsize=(5, 5))

    plt.pie(
        [present, absent],
        labels=['Present', 'Absent'],
        autopct='%1.1f%%'
    )

    chart_path = 'static/charts/attendance_chart.png'

    plt.savefig(chart_path)
    plt.close()

    return render_template('analytics.html', chart=chart_path)


# =========================
# PDF REPORT
# =========================
@app.route('/download_report')
@login_required
def download_report():

    buffer = io.BytesIO()

    from reportlab.pdfgen import canvas

    p = canvas.Canvas(buffer)

    y = 800

    p.drawString(200, 820, 'Attendance Report')

    records = Attendance.query.join(Student).filter(
        Student.user_id == current_user.id
    ).all()

    for r in records:

        text = f'{r.student.name} | {r.date} | {r.status}'
        p.drawString(50, y, text)

        y -= 20

        if y < 50:
            p.showPage()
            y = 800

    p.save()
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name='attendance_report.pdf',
        mimetype='application/pdf'
    )


# =========================
# RUN APP
# =========================
if __name__ == '__main__':
    app.run(debug=True)