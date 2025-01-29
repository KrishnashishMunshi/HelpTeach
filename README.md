# 📚 HelpTeach
#### Video Demo:  <URL HERE>

A web-based platform for managing student data, attendance, and performance, designed to support the educational efforts of underprivileged children. The system allows **admins** and **teachers** to efficiently track progress, monitor attendance, and manage users with role-based access control.

## 🚀 Features

### 🏫 Student Management
- **Admins** can add, view, update, and delete student profiles.
- Track student progress across subjects like **Hindi, English, and Math**.
- Delete a student and remove all related records.

### 📊 Progress Tracking
- Teachers can **view and update** student progress in various subjects.
- Securely stored in the database for review.

### ✅ Attendance Management
- Teachers can **mark student attendance** daily.
- Attendance records are stored and can be reviewed by **date**.

### 📅 Event Timeline
- **Admins** can create, view, and delete events.
- Events related to school activities are shown in a **timeline format**.

### 👤 User Management
- **Admins** can create and delete teacher accounts.
- Role-based access: **Admins have full access, teachers have limited access**.

### 🔐 Authentication & Session Management
- Users **stay logged in** even after closing the browser.
- Role-based authentication and clearance with **Flask-Login**.

---

## 🛠️ Tech Stack

| Technology    | Description |
|--------------|------------|
| **Flask**    | Backend framework |
| **SQLite**   | Local database (can be migrated to PostgreSQL for production) |
| **Tailwind CSS** | Frontend styling |
| **Flask-Login** | Authentication & session management |
| **Jinja2**   | Templating engine |

---

## ⚙️ Setup Instructions

### 📌 Prerequisites
Ensure you have **Python 3.13.1 and `pip` installed:
```bash
python 3.13.1
pip 24.3.1
```


### ⚙️ Setup
```
git clone <repo_url>
cd <repo_directory>
pip install -r requirements.txt
```


### Database
```
python init_db.py
```

## Run the Flask app

```
python app.py
```

Access the application at your local server.


## 🎨 UI Enhancements
- Responsive: Tailwind CSS ensures adaptability across devices.
- Modern UI: Professional, minimalistic design with interactive elements.
- Confirmation Dialogs: Prevent accidental deletions with pop-ups.

## 🔮 Future Enhancements
- 📩 User Notifications: Notify teachers about important updates.
- 📊 Data Analytics: Visual graphs for student performance trends.
- ☁ Cloud Database Migration: Move to PostgreSQL for scalability.




# Conclusion
- This is a project I have made with love and excitement, both for learning as well as for using my skills for the good of my community. This happens to be my final project for CS50x course, and I couldn't have been more excited to start my journey in the world of programming with this code. I plan to revisit this project quite regularly in the future as well, maybe perhaps only to add a comment or two or tweak some function. If you went through my project I would be very grateful if you could drop me your thoughts and suggestions on what could be improved. 
My details are available on my github.




