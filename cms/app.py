import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import MySQLdb.cursors

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'my_secret_key_12345')

# Database Config
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', 'Tanishh#123')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'g1b2')

mysql = MySQL(app)


# Flask-Login gives central management  
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'



# User Model for Flask-Login
class User(UserMixin):
    def __init__(self, user_id, username, email, password, role, phone=None, active=True):
        self.id = user_id
        self.username = username
        self.email = email
        self.password = password
        self.role = role
        self.phone = phone
        self._active = active  # Use _active to avoid conflict with UserMixin
    
    def is_admin(self):
        return self.role == 'Admin'
    
    def is_instructor(self):
        return self.role == 'Instructor'
    
    def is_student(self):
        return self.role == 'Student'
    
    # Override UserMixin's is_active property
    def is_active(self):
        return self._active

# Course Model
class Course:
    def __init__(self, course_id, course_code, course_name, description, credits, 
                 instructor_id, start_date, end_date, department, max_students, status):
        self.course_id = course_id
        self.course_code = course_code
        self.course_name = course_name
        self.description = description
        self.credits = credits
        self.instructor_id = instructor_id
        self.start_date = start_date
        self.end_date = end_date
        self.department = department
        self.max_students = max_students
        self.status = status

# Assignment Model
class Assignment:
    def __init__(self, assignment_id, course_id, title, description, due_date, 
                 max_points, assignment_type, is_published):
        self.assignment_id = assignment_id
        self.course_id = course_id
        self.title = title
        self.description = description
        self.due_date = due_date
        self.max_points = max_points
        self.assignment_type = assignment_type
        self.is_published = is_published

# Enrollment Model
class Enrollment:
    def __init__(self, enrollment_id, student_id, course_id, enrollment_date, status, grade):
        self.enrollment_id = enrollment_id
        self.student_id = student_id
        self.course_id = course_id
        self.enrollment_date = enrollment_date
        self.status = status
        self.grade = grade


@login_manager.user_loader
def load_user(user_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM Users WHERE user_id = %s", (user_id,))
    user_data = cursor.fetchone()
    cursor.close()
    
    if user_data:
        return User(
            user_data['user_id'], 
            user_data['username'], 
            user_data['email'], 
            user_data['password'],
            user_data['role'],
            user_data.get('phone'),
            user_data.get('is_active', True)
        )
    return None


@app.route('/')
def index():
    return render_template('index.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM Users WHERE username = %s AND is_active = TRUE", (username,))
        user_data = cursor.fetchone()
        
        if user_data and check_password_hash(user_data['password'], password):
            user = User(
                user_data['user_id'], 
                user_data['username'], 
                user_data['email'], 
                user_data['password'],
                user_data['role'],
                user_data.get('phone'),
                user_data.get('is_active', True)
            )
            login_user(user)
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password!', 'error')
    
    return render_template('login.html')




@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form.get('role', 'Student')  # Default to Student
        phone = request.form.get('phone', '')
        
        # Hash password
        hashed_password = generate_password_hash(password)
        
        cursor = mysql.connection.cursor()
        try:
            cursor.execute("""
                INSERT INTO Users (username, email, password, role, phone) 
                VALUES (%s, %s, %s, %s, %s)
            """, (username, email, hashed_password, role, phone if phone else None))
            mysql.connection.commit()
            cursor.close()
            
            flash('Account created successfully! Please login.')
            return redirect(url_for('login'))
        except Exception as e:
            flash('Username or email already exists!', 'error')
            cursor.close()
    
    return render_template('signup.html')




@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_admin():
        # Get admin statistics
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        # Get total users
        cursor.execute("SELECT COUNT(*) as count FROM Users")
        total_users = cursor.fetchone()['count']
        
        # Get total courses
        cursor.execute("SELECT COUNT(*) as count FROM Courses")
        total_courses = cursor.fetchone()['count']
        
        # Get active courses
        cursor.execute("SELECT COUNT(*) as count FROM Courses WHERE status = 'Active'")
        active_courses = cursor.fetchone()['count']
        
        # Get total enrollments
        cursor.execute("SELECT COUNT(*) as count FROM Enrollments")
        total_enrollments = cursor.fetchone()['count']
        
        # Get recent activity
        cursor.execute("""
            SELECT c.course_name as title, c.created_at as date, u.username as user, 'Created' as status
            FROM Courses c
            JOIN Users u ON c.instructor_id = u.user_id
            ORDER BY c.created_at DESC
            LIMIT 5
        """)
        recent_activity = cursor.fetchall()
        
        cursor.close()
        
        stats = {
            'total_users': total_users,
            'total_courses': total_courses,
            'active_courses': active_courses,
            'total_enrollments': total_enrollments
        }
        
        return render_template('admin_dashboard.html', 
                         username=current_user.username, 
                         stats=stats, 
                         recent_activity=recent_activity)
    else:
        return render_template('dashboard.html', username=current_user.username)



# Course Management Routes
@app.route('/test_courses')
def test_courses():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM Courses ORDER BY course_name")
    courses = cursor.fetchall()
    cursor.close()
    
    return f"<h1>Courses in Database: {len(courses)}</h1><pre>" + "\n".join([f"ID: {c['course_id']}, Code: {c['course_code']}, Name: {c['course_name']}" for c in courses]) + "</pre>"

@app.route('/create_test_course')
def create_test_course():
    cursor = mysql.connection.cursor()
    try:
        cursor.execute("""
            INSERT INTO Courses (course_code, course_name, description, credits, instructor_id, department, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, ('TEST101', 'Test Course', 'This is a test course to verify database connection', 3, 1, 'Computer Science', 'Active'))
        mysql.connection.commit()
        cursor.close()
        return "<h1>Test Course Created Successfully!</h1><a href='/test_courses'>View Courses</a>"
    except Exception as e:
        cursor.close()
        return f"<h1>Error creating test course: {str(e)}</h1>"

@app.route('/courses')
@login_required
def courses():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    if current_user.is_student():
        # Students can see active courses
        cursor.execute("""
            SELECT c.*, u.username as instructor_name 
            FROM Courses c 
            LEFT JOIN Users u ON c.instructor_id = u.user_id 
            WHERE c.status = 'Active'
            ORDER BY c.course_name
        """)
    elif current_user.is_instructor():
        # Instructors can see their courses
        cursor.execute("""
            SELECT c.*, u.username as instructor_name 
            FROM Courses c 
            LEFT JOIN Users u ON c.instructor_id = u.user_id 
            WHERE c.instructor_id = %s OR c.instructor_id IS NULL
            ORDER BY c.course_name
        """, (current_user.id,))
    else:  # Admin
        # Admins can see all courses
        cursor.execute("""
            SELECT c.*, u.username as instructor_name 
            FROM Courses c 
            LEFT JOIN Users u ON c.instructor_id = u.user_id 
            ORDER BY c.course_name
        """)
    
    courses = cursor.fetchall()
    cursor.close()
    
    return render_template('courses.html', courses=courses)





@app.route('/create_course', methods=['GET', 'POST'])
@login_required
def create_course():
    if not current_user.is_instructor() and not current_user.is_admin():
        flash('Only instructors and admins can create courses!', 'error')
        return redirect(url_for('courses'))
    
    if request.method == 'POST':
        course_code = request.form['course_code']
        course_name = request.form['course_name']
        description = request.form['description']
        credits = request.form['credits']
        department = request.form['department']
        max_students = request.form.get('max_students')
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        
        cursor = mysql.connection.cursor()
        try:
            cursor.execute("""
                INSERT INTO Courses (course_code, course_name, description, credits, 
                                  instructor_id, department, max_students, start_date, end_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (course_code, course_name, description, credits, 
                  current_user.id if current_user.is_instructor() else None,
                  department, max_students, start_date, end_date))
            mysql.connection.commit()
            flash('Course created successfully!', 'success')
            return redirect(url_for('courses'))
        except Exception as e:
            flash('Error creating course. Course code may already exist!', 'error')
        finally:
            cursor.close()
    
    return render_template('create_course.html')





@app.route('/course/<int:course_id>')
@login_required
def course_details(course_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    # Get course details
    cursor.execute("""
        SELECT c.*, u.username as instructor_name 
        FROM Courses c 
        LEFT JOIN Users u ON c.instructor_id = u.user_id 
        WHERE c.course_id = %s
    """, (course_id,))
    course = cursor.fetchone()
    
    if not course:
        flash('Course not found!', 'error')
        return redirect(url_for('courses'))
    
    # Get assignments for this course
    cursor.execute("""
        SELECT * FROM Assignments 
        WHERE course_id = %s 
        ORDER BY due_date
    """, (course_id,))
    assignments = cursor.fetchall()
    
    # Check if user is enrolled (for students)
    is_enrolled = False
    if current_user.is_student():
        cursor.execute("""
            SELECT * FROM Enrollments 
            WHERE student_id = %s AND course_id = %s
        """, (current_user.id, course_id))
        is_enrolled = cursor.fetchone() is not None
    
    cursor.close()
    
    return render_template('course_details.html', course=course, assignments=assignments, is_enrolled=is_enrolled)


@app.route('/enroll/<int:course_id>')
@login_required
def enroll_course(course_id):
    if not current_user.is_student():
        flash('Only students can enroll in courses!', 'error')
        return redirect(url_for('courses'))
    
    cursor = mysql.connection.cursor()
    try:
        cursor.execute("""
            INSERT INTO Enrollments (student_id, course_id, status)
            VALUES (%s, %s, 'Enrolled')
        """, (current_user.id, course_id))
        mysql.connection.commit()
        flash('Successfully enrolled in course!', 'success')
    except Exception as e:
        flash('You are already enrolled in this course!', 'error')
    finally:
        cursor.close()
    
    return redirect(url_for('course_details', course_id=course_id))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)