#import all the libraries that are to be used in the program
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
import os
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'd8a8e8ff6b624d5e9b1543f28f6c3fadc31a2bb8e92d3a5e541fdff09c1234fe' #sets key for flask cryptographic operations

#login
login_manager = LoginManager() #instance of loginmanager class
login_manager.init_app(app) #intializes login manager
login_manager.login_view = 'login' #This attribute specifies the name of the view (or route) that handles the login page.

# Set the database URI
base_dir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(base_dir, 'app.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Create database and tables
def setup_database():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    setup_database()

class User(UserMixin): #User class inherits the UserMixin class containing several methods for managing user sessions
    def __init__(self, id, username, role): #defines the constructor of the class, called whenever a new instance of this class is created
        self.id = id
        self.username = username
        self.role = role

# User loader callback for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, role FROM users WHERE id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return User(id=result[0], username=result[1], role=result[2])
    return None

#@app.route("/", methods=["GET", "POST"])
#def login():
    

 #   if request.method == "POST":
  #      username = request.form["username"]
  #      password = request.form["password"]

 #       conn = sqlite3.connect("app.db")
  #      cursor = conn.cursor()
   #     cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    #    user_data = cursor.fetchone()
    #   conn.close()
 #       if user_data and check_password_hash(user_data[2], password):
  #          user = User(id=user_data[0], username=user_data[1], password=user_data[2])
   #         user.role = user_data[3]  # Store the role
    #        login_user(user)
     #       return redirect("/home")
      #     flash("Invalid credentials. Please try again.", "error")
       #     return redirect(url_for("login"))
    
    #return render_template("login.html")
@app.route("/", methods=["GET", "POST"])
def login():
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, hash, role) VALUES (?,?,?)", ("admin",generate_password_hash("admin"), "admin"))
    conn.close()
    if current_user.is_authenticated:
        return redirect("/home")                #when the user opens the site in the same cookie session
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")  # Get the entered password

        # Query the database for the user
        conn = sqlite3.connect("app.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user_data = cursor.fetchone()                                                   
        conn.close()

        if user_data and user_data[2]==password:
            # If the user exists and the password matches
            user = User(id=user_data[0], username=user_data[1], role= user_data[3])                             #set user identity
            login_user(user)
            return redirect("/home")
        else:
            flash("Invalid username or password. Please try again.", "error")

    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))

@app.route("/home")
@login_required
def home():
    return render_template("index.html")

@app.route("/students")
@login_required
def students():                                                                     #get all the students and their id's from the database
    # In your Flask route:
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM students")
    students = cursor.fetchall()
    #return render_template('index.html', title = "Pahal Foundation")
    return render_template('dashboard.html', students=students, title = "Pahal Foundation")

@app.route("/student_profile/<int:student_id>", methods=["POST","GET"])                           #display the profile of the student specified by their id
@login_required
def student_profile(student_id):
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    # Fetch student profile
    cursor.execute("SELECT id, name, gender, age, guardian_contact FROM students WHERE id = ?", [student_id])
    student = cursor.fetchone()
    
    # Fetch student progress
    cursor.execute("SELECT hindi, english, mathematics, other FROM progress WHERE student_id = ?", [student_id])
    progress = cursor.fetchone()
    
    # Fetch student attendance
    cursor.execute("""
        SELECT date, status FROM attendance
        WHERE student_id = ?
        ORDER BY date DESC
    """, [student_id])
    attendance = cursor.fetchall()

    attendance_records = [{"date": record[0], "status": record[1]} for record in attendance]
    
    conn.close()
    return render_template("student_profile.html", student=student, progress=progress, attendance=attendance_records)

@app.route("/add_student", methods=["GET", "POST"])             #add a new student
@login_required
def add_student():
    

    if request.method == "POST":
        
       
        name = request.form.get("name")
        gender = request.form.get("gender")
        age = request.form.get("age")
        guardian_contact = request.form.get("guardian_contact")
        conn = sqlite3.connect("app.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO students (name, gender, age, guardian_contact)
            VALUES (?, ?, ?, ?)
        """, (name, gender, age, guardian_contact))
        conn.commit()
        conn.close()

        flash("Student added successfully!", "success")
        return redirect(url_for("students"))
    
    return render_template("add_student.html")


@app.route("/delete_student/<int:student_id>", methods=["POST"])       #delete a stident
@login_required
def delete_student(student_id):

    if current_user.role != "admin":
        flash("You are not authorized to delete students.", "error")
        return redirect(url_for("students"))

    try:
        conn = sqlite3.connect("app.db")
        cursor = conn.cursor()

        # Delete related records from progress and attendance tables
        cursor.execute("DELETE FROM progress WHERE student_id = ?", (student_id,))
        cursor.execute("DELETE FROM attendance WHERE student_id = ?", (student_id,))

        # Delete the student record
        cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))

        conn.commit()
        conn.close()

        flash("Student and all related records deleted successfully.", "success")
    except sqlite3.Error as e:
        flash(f"An error occurred: {e}", "error")
        if conn:
            conn.rollback()

    return redirect(url_for("students"))

@app.route("/attendance", methods = ["POST","GET"])
@login_required
def attendance():
    return render_template("attendance.html")


@app.route("/check_attendance", methods=["POST", "GET"])
@login_required
def check_attendance():
    if request.method == 'POST':
        selected_date = request.form.get('date')
        conn = sqlite3.connect("app.db")
        cursor = conn.cursor()

        # Query to get students and their attendance status for the selected date
        query = """
            SELECT students.name, attendance.status 
            FROM students
            LEFT JOIN attendance ON students.id = attendance.student_id
            WHERE attendance.date = ?
        """
        cursor.execute(query, (selected_date,))
        students = cursor.fetchall()
        attendance_status = [{"name": record[0], "status": record[1]} for record in students]
        conn.close()
        return render_template('check_attendance.html', students=attendance_status, selected_date=selected_date)
    return render_template('check_attendance.html')

@app.route("/add_attendance", methods=["GET", "POST"])
@login_required
def add_attendance():
    conn = sqlite3.connect("app.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    if request.method == "POST":
        selected_date = request.form.get("date")

        # Validate selected date (ensure it’s not in the future)
        today_date = datetime.now().date()
        selected_date_obj = datetime.strptime(selected_date, "%Y-%m-%d").date() #datetime format

        if selected_date_obj > today_date:
            conn.close()
            flash("You cannot select a future date for attendance.", "error")
            return redirect(url_for("add_attendance"))

        # Process attendance data
        attendance_data = request.form.to_dict(flat=False)
        for student_id, statuses in attendance_data.items():
            if student_id == "date":
                continue
            # Insert or update attendance for the selected day only
            cursor.execute("""
                INSERT INTO attendance (student_id, date, status)
                VALUES (?, ?, ?)
                ON CONFLICT(student_id, date) DO UPDATE SET status = excluded.status
            """, (student_id, selected_date, statuses[0]))

        conn.commit()
        conn.close()
        flash("Attendance successfully uploaded!", "success")
        return redirect(url_for("check_attendance"))

    # Pass current date for the date picker max attribute
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Fetch all students for the form
    cursor.execute("SELECT id, name FROM students")
    students = cursor.fetchall()
    conn.close()

    return render_template("add_attendance.html", students=students, current_date=current_date)

@app.route("/update_progress/<int:student_id>", methods=["POST"])
@login_required
def update_progress(student_id):
    if request.method == "POST":
        # Get progress values from the form
        hindi = request.form.get("hindi")
        english = request.form.get("english")
        math = request.form.get("math")
        other = request.form.get("other")

        # Connect to the database
        conn = sqlite3.connect("app.db")
        cursor = conn.cursor()

        try:
            # Check if an entry for the student already exists
            cursor.execute("SELECT * FROM progress WHERE student_id = ?", (student_id,))
            existing_progress = cursor.fetchone()

            if existing_progress:
                # If an entry exists, update it
                query = """
                    UPDATE progress 
                    SET hindi = ?, english = ?, mathematics = ?, other = ? 
                    WHERE student_id = ?
                """
                cursor.execute(query, (hindi, english, math, other, student_id))
                flash("Progress updated successfully!", "success")
            else:
                # If no entry exists, insert a new record
                query = """
                    INSERT INTO progress (student_id, hindi, english, mathematics, other)
                    VALUES (?, ?, ?, ?, ?)
                """
                cursor.execute(query, (student_id, hindi, english, math, other))
                flash("Progress added successfully!", "success")

            # Commit the transaction and close the connection
            conn.commit()

        except sqlite3.Error as e:
            # If any error occurs, flash an error message
            flash(f"Error: {e}", "error")
        finally:
            conn.close()

        return redirect(url_for("student_profile", student_id=student_id))
    

@app.route("/timeline", methods=["GET", "POST"])
@login_required
def timeline():
    if request.method == "POST":
        # Only admins can add events
        if current_user.role != "admin":
            flash("You are not authorized to add events.", "error")
            return redirect(url_for("timeline"))

        title = request.form.get("title")
        description = request.form.get("description")
        event_date = request.form.get("event_date")

        if not title or not event_date:
            flash("Title and Event Date are required.", "error")
            return redirect(url_for("timeline"))

        try:
            conn = sqlite3.connect("app.db")
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO events (title, description, event_date)
                VALUES (?, ?, ?)
            """, (title, description, event_date))
            conn.commit()
            conn.close()

            flash("Event added successfully!", "success")
        except sqlite3.Error as e:
            flash(f"An error occurred: {e}", "error")

        return redirect(url_for("timeline"))

    # Fetch all events sorted by date
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, description, event_date FROM events ORDER BY event_date ASC")
    events = cursor.fetchall()
    conn.close()

    return render_template("timeline.html", events=events)

@app.route("/delete_event/<int:event_id>", methods=["POST"], endpoint="delete_event")
@login_required
def delete_event(event_id):
    if current_user.role != "admin":
        flash("You are not authorized to delete events.", "error")
        return redirect(url_for("timeline"))

    try:
        conn = sqlite3.connect("app.db")
        cursor = conn.cursor()

        # Delete the event from the events table
        cursor.execute("DELETE FROM events WHERE id = ?", (event_id,))
        conn.commit()
        conn.close()

        flash("Event deleted successfully.", "success")
    except sqlite3.Error as e:
        flash(f"An error occurred: {e}", "error")
        if conn:
            conn.rollback()

    return redirect(url_for("timeline"))

@app.route("/manage_users", methods=["GET", "POST"])
@login_required
def manage_users():
    if current_user.role != "admin":
        flash("You are not authorized to manage users.", "error")
        return redirect(url_for("home"))

    if request.method == "POST":
        # Handle user creation form submission
        username = request.form.get("username")
        password = request.form.get("password")
        role = request.form.get("role")

        if username and password and role:
            # Hash the password before saving
            hashed_password = generate_password_hash(password)
            
            conn = sqlite3.connect("app.db")
            cursor = conn.cursor()

            cursor.execute("INSERT INTO users (username, hash, role) VALUES (?, ?, ?)", 
                           (username, hashed_password, role))
            conn.commit()
            conn.close()

            flash(f"User {username} created successfully.", "success")
            return redirect(url_for("manage_users"))
    
    # Fetch all users for display
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, role FROM users")
    users = cursor.fetchall()
    conn.close()

    return render_template("manage_users.html", users=users)

@app.route("/delete_user/<int:user_id>", methods=["POST"])
@login_required
def delete_user(user_id):
    if current_user.role != "admin":
        flash("You are not authorized to delete users.", "error")
        return redirect(url_for("home"))

    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        flash("User deleted successfully.", "success")
    except sqlite3.Error as e:
        flash(f"An error occurred: {e}", "error")
    finally:
        conn.close()

    return redirect(url_for("manage_users"))



if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)