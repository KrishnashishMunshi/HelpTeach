# 📚 HelpTeach
#### Video Demo: https://youtu.be/MOo3osDb9rs?si=NwRFB-VTRo_eztaF

A web-based platform for managing student data, attendance, and performance, designed to support the educational efforts of underprivileged children. The system allows **admins** and **teachers** to efficiently track progress, monitor attendance, and manage users with role-based access control.

<img width="1362" height="846" alt="Image" src="https://github.com/user-attachments/assets/72d47e7e-cd70-4e2e-9564-29ac952aec22" /> 

## 🚀 Features

### 🏫 Student Management
- **Admins** can add, view, update, and delete student profiles.
- Track student progress across subjects like **Hindi, English, and Math**.
- Delete a student and remove all related records.

### 📊 Progress Tracking
- Teachers can **view and update** student progress in various subjects.
- Securely stored in the database for review.

<img width="1675" height="885" alt="Image" src="https://github.com/user-attachments/assets/6392378a-75a9-4d1f-b312-8fb0f6219373" />

### ✅ Attendance Management
- Teachers can **mark student attendance** daily.
- Attendance records are stored and can be reviewed by **date**.

<img width="1507" height="920" alt="Image" src="https://github.com/user-attachments/assets/57a7be03-506f-47ce-ad43-abc7e6727d4b" />

### 📅 Event Timeline
- **Admins** can create, view, and delete events.
- Events related to school activities are shown in a **timeline format**.

<img width="1376" height="601" alt="Image" src="https://github.com/user-attachments/assets/f86428f4-cb67-46fe-8aa4-cded22905f13" />

### 👤 User Management
- **Admins** can create and delete teacher accounts.
- Role-based access: **Admins have full access, teachers have limited access**.

<img width="1910" height="924" alt="Image" src="https://github.com/user-attachments/assets/b322d059-d11c-403c-b469-e303874e9c00" />

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




