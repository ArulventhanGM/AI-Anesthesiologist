#!/usr/bin/env python3
"""
Flask Example using CSV User Management System
This demonstrates how to integrate the CSV user management with Flask.
"""

from flask import Flask, request, render_template_string, redirect, url_for, flash, session
import sys
import os
from pathlib import Path

# Add the core directory to the Python path
sys.path.append(str(Path(__file__).parent / 'core'))

from csv_user_manager import CSVUserManager

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'

# Initialize CSV manager
csv_manager = CSVUserManager(
    csv_file_path='flask_users.csv',
    backup_dir='flask_backups'
)

# HTML Templates
LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Flask CSV User Management - Login</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 400px; margin: 100px auto; padding: 20px; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; }
        input[type="text"], input[type="password"], input[type="email"] { 
            width: 100%; padding: 8px; margin-bottom: 10px; 
        }
        button { background-color: #007bff; color: white; padding: 10px 20px; border: none; cursor: pointer; }
        button:hover { background-color: #0056b3; }
        .alert { padding: 10px; margin: 10px 0; border-radius: 4px; }
        .alert-error { background-color: #f8d7da; color: #721c24; }
        .alert-success { background-color: #d4edda; color: #155724; }
        .links { margin-top: 20px; text-align: center; }
        .links a { margin: 0 10px; }
    </style>
</head>
<body>
    <h2>Login</h2>
    
    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            {% for category, message in messages %}
                <div class="alert alert-{{ category }}">{{ message }}</div>
            {% endfor %}
        {% endif %}
    {% endwith %}
    
    <form method="POST">
        <div class="form-group">
            <label for="username">Username:</label>
            <input type="text" id="username" name="username" required>
        </div>
        
        <div class="form-group">
            <label for="password">Password:</label>
            <input type="password" id="password" name="password" required>
        </div>
        
        <button type="submit">Login</button>
    </form>
    
    <div class="links">
        <a href="{{ url_for('register') }}">Don't have an account? Register here</a>
    </div>
</body>
</html>
"""

REGISTER_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Flask CSV User Management - Register</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 400px; margin: 50px auto; padding: 20px; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; }
        input[type="text"], input[type="password"], input[type="email"] { 
            width: 100%; padding: 8px; margin-bottom: 10px; 
        }
        button { background-color: #28a745; color: white; padding: 10px 20px; border: none; cursor: pointer; }
        button:hover { background-color: #218838; }
        .alert { padding: 10px; margin: 10px 0; border-radius: 4px; }
        .alert-error { background-color: #f8d7da; color: #721c24; }
        .alert-success { background-color: #d4edda; color: #155724; }
        .links { margin-top: 20px; text-align: center; }
        .links a { margin: 0 10px; }
    </style>
</head>
<body>
    <h2>Register</h2>
    
    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            {% for category, message in messages %}
                <div class="alert alert-{{ category }}">{{ message }}</div>
            {% endfor %}
        {% endif %}
    {% endwith %}
    
    <form method="POST">
        <div class="form-group">
            <label for="username">Username:</label>
            <input type="text" id="username" name="username" required>
        </div>
        
        <div class="form-group">
            <label for="email">Email:</label>
            <input type="email" id="email" name="email" required>
        </div>
        
        <div class="form-group">
            <label for="password">Password:</label>
            <input type="password" id="password" name="password" required>
        </div>
        
        <div class="form-group">
            <label for="hospital_name">Hospital Name:</label>
            <input type="text" id="hospital_name" name="hospital_name" required>
        </div>
        
        <div class="form-group">
            <label for="hospital_id">Hospital ID:</label>
            <input type="text" id="hospital_id" name="hospital_id" required>
        </div>
        
        <div class="form-group">
            <label for="license_id">License ID:</label>
            <input type="text" id="license_id" name="license_id" required>
        </div>
        
        <button type="submit">Register</button>
    </form>
    
    <div class="links">
        <a href="{{ url_for('login') }}">Already have an account? Login here</a>
    </div>
</body>
</html>
"""

DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Flask CSV User Management - Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
        .user-info { background-color: #f8f9fa; padding: 20px; margin: 20px 0; border-radius: 5px; }
        .user-info h3 { margin-top: 0; }
        .user-info p { margin: 5px 0; }
        .actions { margin: 20px 0; }
        .actions a { 
            display: inline-block; margin: 5px 10px 5px 0; padding: 10px 20px; 
            background-color: #007bff; color: white; text-decoration: none; border-radius: 4px; 
        }
        .actions a:hover { background-color: #0056b3; }
        .logout { background-color: #dc3545 !important; }
        .logout:hover { background-color: #c82333 !important; }
        .alert { padding: 10px; margin: 10px 0; border-radius: 4px; }
        .alert-error { background-color: #f8d7da; color: #721c24; }
        .alert-success { background-color: #d4edda; color: #155724; }
        .users-table { margin: 20px 0; }
        table { width: 100%; border-collapse: collapse; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
    </style>
</head>
<body>
    <h1>Dashboard</h1>
    
    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            {% for category, message in messages %}
                <div class="alert alert-{{ category }}">{{ message }}</div>
            {% endfor %}
        {% endif %}
    {% endwith %}
    
    <div class="user-info">
        <h3>Welcome, {{ current_user.username }}!</h3>
        <p><strong>Email:</strong> {{ current_user.email }}</p>
        <p><strong>Hospital:</strong> {{ current_user.hospital_name }}</p>
        <p><strong>Hospital ID:</strong> {{ current_user.hospital_id }}</p>
        <p><strong>License ID:</strong> {{ current_user.license_id }}</p>
        <p><strong>Member Since:</strong> {{ current_user.created_at }}</p>
    </div>
    
    <div class="actions">
        <a href="{{ url_for('all_users') }}">View All Users</a>
        <a href="{{ url_for('logout') }}" class="logout">Logout</a>
    </div>
    
    {% if users %}
    <div class="users-table">
        <h3>All Registered Users</h3>
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Username</th>
                    <th>Email</th>
                    <th>Hospital</th>
                    <th>Created</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
                {% for user in users %}
                <tr>
                    <td>{{ user.id }}</td>
                    <td>{{ user.username }}</td>
                    <td>{{ user.email }}</td>
                    <td>{{ user.hospital_name }}</td>
                    <td>{{ user.created_at }}</td>
                    <td>{{ 'Active' if user.is_active == 'true' else 'Inactive' }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
    {% endif %}
</body>
</html>
"""

@app.route('/')
def index():
    """Home page - redirect to login or dashboard."""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login route."""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        if not username or not password:
            flash('Please enter both username and password.', 'error')
            return render_template_string(LOGIN_TEMPLATE)
        
        # Authenticate user
        result = csv_manager.authenticate_user(username, password)
        
        if result['success']:
            # Store user info in session
            session['user_id'] = result['user']['id']
            session['username'] = result['user']['username']
            flash(f'Welcome back, {username}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash(result['message'], 'error')
    
    return render_template_string(LOGIN_TEMPLATE)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registration route."""
    if request.method == 'POST':
        # Get form data
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        hospital_name = request.form.get('hospital_name', '').strip()
        hospital_id = request.form.get('hospital_id', '').strip()
        license_id = request.form.get('license_id', '').strip()
        
        # Basic validation
        if not all([username, email, password, hospital_name, hospital_id, license_id]):
            flash('All fields are required.', 'error')
            return render_template_string(REGISTER_TEMPLATE)
        
        # Prepare user data
        user_data = {
            'username': username,
            'email': email,
            'password': password,
            'hospital_name': hospital_name,
            'hospital_id': hospital_id,
            'license_id': license_id
        }
        
        # Create user
        result = csv_manager.create_user(user_data)
        
        if result['success']:
            flash(f'Account created successfully! You can now login.', 'success')
            return redirect(url_for('login'))
        else:
            # Display validation errors
            for error in result.get('errors', []):
                flash(error, 'error')
    
    return render_template_string(REGISTER_TEMPLATE)

@app.route('/dashboard')
def dashboard():
    """Dashboard route."""
    if 'user_id' not in session:
        flash('Please login to access this page.', 'error')
        return redirect(url_for('login'))
    
    # Get current user info
    user_result = csv_manager.get_user(user_id=session['user_id'])
    
    if not user_result['success']:
        flash('Session expired. Please login again.', 'error')
        return redirect(url_for('login'))
    
    return render_template_string(DASHBOARD_TEMPLATE, current_user=user_result['user'])

@app.route('/users')
def all_users():
    """Show all users."""
    if 'user_id' not in session:
        flash('Please login to access this page.', 'error')
        return redirect(url_for('login'))
    
    # Get current user info
    user_result = csv_manager.get_user(user_id=session['user_id'])
    
    if not user_result['success']:
        flash('Session expired. Please login again.', 'error')
        return redirect(url_for('login'))
    
    # Get all users
    users_result = csv_manager.list_users()
    users = users_result['users'] if users_result['success'] else []
    
    return render_template_string(DASHBOARD_TEMPLATE, 
                                current_user=user_result['user'], 
                                users=users)

@app.route('/logout')
def logout():
    """Logout route."""
    session.clear()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    print("Starting Flask CSV User Management Example...")
    print("Access the application at: http://localhost:5000")
    print("CSV file will be created as: flask_users.csv")
    print("Backups will be stored in: flask_backups/")
    
    # Run the Flask app
    app.run(debug=True, port=5000)
