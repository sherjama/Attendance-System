# 📋 AttendPro — Attendance Management System

A professional, multi-user attendance management web application built with **Flask** and **MySQL**. Each teacher/user has their own isolated data — classes, students, and attendance records are completely private per account.

---

## ✨ Features

- 🔐 **Multi-user Authentication** — Register & login with hashed passwords. Each user's data is fully isolated.
- 🏫 **Class Management** — Create and manage multiple classes/batches.
- 👥 **Student Management** — Add students to classes, view profiles, delete records.
- 📅 **Attendance Calendar** — Interactive FullCalendar view with color-coded present/absent events.
- ✅ **Mark Attendance** — Mark any student present or absent for any date.
- 📊 **Analytics** — Pie chart showing overall present vs absent distribution.
- 📄 **PDF Reports** — Download a full attendance report as a PDF file.
- 📱 **Responsive UI** — Professional dark-themed interface that works on all screen sizes.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3, Flask |
| Database | MySQL (via PyMySQL) |
| ORM | Flask-SQLAlchemy |
| Auth | Flask-Login, Werkzeug |
| Frontend | Jinja2, Bootstrap 5, Bootstrap Icons |
| Calendar | FullCalendar 6 |
| Charts | Matplotlib |
| PDF | ReportLab |
| Fonts | Google Fonts (Outfit, JetBrains Mono) |

---

## 📁 Project Structure

```
attendance-system/
│
├── app.py                  # Main Flask app & all routes
├── models.py               # SQLAlchemy database models
├── config.py               # App configuration (DB URI, secret key)
│
├── templates/              # Jinja2 HTML templates
│   ├── base.html           # Base layout (sidebar, navbar, flash messages)
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── classes.html
│   ├── add_class.html
│   ├── class_details.html
│   ├── students.html
│   ├── add_student.html
│   ├── student_profile.html
│   ├── attendance.html
│   ├── attendance_details.html
│   ├── mark_attendance.html
│   └── analytics.html
│
├── static/
│   ├── style.css           # Custom styles
│   └── charts/             # Auto-generated chart images
│
└── README.md
```

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/attendpro.git
cd attendpro
```

### 2. Create a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install flask flask-sqlalchemy flask-login pymysql werkzeug matplotlib reportlab
```

### 4. Configure the database

Create a `config.py` file in the root directory:

```python
class Config:
    SECRET_KEY = 'your-secret-key-here'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username:password@localhost/attendpro_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

Then create the MySQL database:

```sql
CREATE DATABASE attendpro_db;
```

### 5. Run the app

```bash
python app.py
```

Open your browser and go to: **http://127.0.0.1:5000**

> The database tables are created automatically on first run via `db.create_all()`.

---

## 🗄️ Database Schema

```
User
├── id (PK)
├── username (unique)
└── password (hashed)

Classroom
├── id (PK)
├── class_name
├── user_id (FK → User)
└── students → [Student]

Student
├── id (PK)
├── name
├── roll_number
├── classroom_id (FK → Classroom)
├── user_id (FK → User)
└── attendance_records → [Attendance]

Attendance
├── id (PK)
├── student_id (FK → Student)
├── date (YYYY-MM-DD)
└── status (Present / Absent)
```

---

## 🔗 Application Routes

| Method | Route | Description |
|---|---|---|
| GET/POST | `/register` | Create a new account |
| GET/POST | `/login` | Login to your account |
| GET | `/logout` | Logout |
| GET | `/dashboard` | Overview stats |
| GET | `/classes` | List all your classes |
| GET/POST | `/add_class` | Create a new class |
| GET | `/class/<id>` | View students in a class |
| GET/POST | `/add_student/<class_id>` | Add student to a class |
| GET | `/students` | List all students |
| GET | `/student/<id>` | Student profile & attendance stats |
| GET | `/delete_student/<id>` | Delete a student |
| GET | `/attendance` | Attendance calendar view |
| GET | `/attendance/<date>` | Attendance details for a specific date |
| GET/POST | `/mark_attendance` | Mark a student present/absent |
| GET | `/analytics` | Pie chart analytics |
| GET | `/download_report` | Download PDF report |

---

## 👤 How to Use

1. **Register** a new account at `/register`
2. **Create a Class** from the Classes section
3. **Add Students** to the class
4. **Mark Attendance** daily from the Mark Attendance page
5. **View Calendar** to see color-coded attendance (🟢 Present, 🔴 Absent)
6. **Click any date** on the calendar to see who was present/absent
7. **Download PDF** report from the Dashboard or Analytics page

---

## 🔒 Security Notes

- Passwords are hashed using **Werkzeug's `generate_password_hash`** — never stored in plain text.
- All routes (except login/register) are protected with `@login_required`.
- Every database query filters by `current_user.id` — users **cannot** access each other's data.
- Student delete is protected — only the owner can delete their own students.

---

## 📦 Dependencies

```
flask
flask-sqlalchemy
flask-login
pymysql
werkzeug
matplotlib
reportlab
```

Install all at once:

```bash
pip install flask flask-sqlalchemy flask-login pymysql werkzeug matplotlib reportlab
```

---

## 🚀 Deployment Tips

- Set `DEBUG = False` in production
- Use a strong random `SECRET_KEY`
- Use **Gunicorn** as the WSGI server:
  ```bash
  gunicorn -w 4 app:app
  ```
- Use **Nginx** as a reverse proxy
- Store your DB credentials in environment variables, not in `config.py`

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

> Built with ❤️ using Flask & Python
