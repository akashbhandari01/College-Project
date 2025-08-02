# 📘 Django Project: StudyBuddy

A web application built with the Django framework.

## 🚀 Features

- User authentication (Sign up, Login, Logout)
- CRUD functionality
- Admin dashboard

---

## 🛠️ Technologies Used

- Python
- Django
- SQLite 
- HTML, CSS, JavaScript, Bootstrap

---

## 📦 Project Setup & Installation

Follow these steps to run this project on your local machine:

### 1. Clone the Repository

```bash
git clone https://github.com/akashbhandari01/College-Project.git
cd College-Project
```

### 2. Create & Activate Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Change The Settings

Change DEBUG = True
<br>
In ALLOWED_HOSTS =["enter your hostname"]

### 5. Apply Migrations

```bash
python manage.py migrate
```

### 6. Create Superuser (Admin Login)

```bash
python manage.py createsuperuser
```

### 7. Run the Server

```bash
python manage.py runserver
```

Now open your browser and go to:  
👉 `http://127.0.0.1:8000/`

---

## 👨‍💻 Admin Panel

Visit: `http://127.0.0.1:8000/admin/`  
Login with your superuser credentials.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🙌 Acknowledgements

- Django Documentation: https://docs.djangoproject.com/
- [List any other tools, templates, or contributors]
