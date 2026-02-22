# Online Exam System (MVP)

A complete, full-stack Django application for conducting online multiple-choice exams.

## Features
- **Student Authentication**: Register and login as a student.
- **Admin Dashboard**: Manage exams and questions via Django Admin.
- **Exam Interface**: 
  - MCQ questions with 4 options.
  - Live countdown timer.
  - Dynamic progress tracking (answered vs total).
  - Randomized question order per attempt.
  - Auto-submission on timer expiry.
- **Results Tracking**: View scores and history of past attempts.
- **Modern UI**: Built with Tailwind CSS (CDN-based for zero-setup styling).

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- Python 3.10 or higher.
- `pip` (Python package manager).

### 2. Setup (Beginner Friendly)

Open your terminal/command prompt in the project root and run:

```bash
# 1. Create a virtual environment
python -m venv venv

# 2. Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Apply Database Migrations
python manage.py makemigrations exam_app
python manage.py migrate

# 5. Seed Sample Data (Creates Superuser and Exams)
python manage.py seed_data

# 6. Start the Server
python manage.py runserver
```

### 3. Usage

- **Access the App**: Go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Admin Access**: Go to [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
  - **Username**: `admin`
  - **Password**: `adminpass`
- **Student Registration**: Click "Register" on the top right to create a new student account.

---

## 🧪 Running Tests
To verify the scoring logic and system health, run:
```bash
python manage.py test
```

---

## 🛠 Project Structure
- `online_exam/`: Project settings and main URL configuration.
- `exam_app/`: Main application logic (Models, Views, Templates).
  - `models.py`: Defines `Exam`, `Question`, and `Attempt`.
  - `views.py`: Logic for starting, submitting, and scoring exams.
  - `templates/`: HTML files with Tailwind CSS integration.
- `requirements.txt`: List of Python dependencies.

## Switching to PostgreSQL
To switch from SQLite to PostgreSQL:
1. Install `psycopg2-binary`.
2. Update the `DATABASES` setting in `online_exam/settings.py`.
3. Provide your DB credentials (HOST, PORT, NAME, USER, PASSWORD).
