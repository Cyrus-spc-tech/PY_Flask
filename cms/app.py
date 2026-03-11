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
    return render_template('dashboard.html', username=current_user.username)



@app.route('/couses')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)