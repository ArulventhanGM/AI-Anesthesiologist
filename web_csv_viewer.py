#!/usr/bin/env python3
"""
Web-based CSV Database Viewer
A simple Flask app to view your CSV database in a web browser.
"""

from flask import Flask, render_template_string, request, jsonify
import csv
import os
import sys
from pathlib import Path

# Add the core directory to the Python path
sys.path.append(str(Path(__file__).parent / 'core'))

try:
    from csv_user_manager import CSVUserManager
except ImportError:
    print("csv_user_manager.py not found. Make sure it's in the core directory.")
    sys.exit(1)

app = Flask(__name__)

# Configuration
CSV_FILE_PATH = 'users.csv'
BACKUP_DIR = 'backups'

# Initialize CSV manager
csv_manager = CSVUserManager(CSV_FILE_PATH, BACKUP_DIR)

# HTML Template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CSV Database Viewer</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            text-align: center;
            margin-bottom: 30px;
        }
        .stats {
            display: flex;
            justify-content: space-around;
            margin-bottom: 30px;
        }
        .stat-item {
            text-align: center;
            padding: 15px;
            background-color: #f8f9fa;
            border-radius: 5px;
            min-width: 100px;
        }
        .stat-number {
            font-size: 24px;
            font-weight: bold;
            color: #007bff;
        }
        .stat-label {
            font-size: 14px;
            color: #666;
        }
        .search-box {
            margin-bottom: 20px;
        }
        .search-box input {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 16px;
        }
        .table-container {
            overflow-x: auto;
            border: 1px solid #ddd;
            border-radius: 5px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 0;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #f8f9fa;
            font-weight: bold;
            position: sticky;
            top: 0;
        }
        tr:hover {
            background-color: #f5f5f5;
        }
        .status-active {
            color: #28a745;
            font-weight: bold;
        }
        .status-inactive {
            color: #dc3545;
            font-weight: bold;
        }
        .btn {
            padding: 8px 16px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            margin: 5px;
        }
        .btn-primary {
            background-color: #007bff;
            color: white;
        }
        .btn-secondary {
            background-color: #6c757d;
            color: white;
        }
        .btn:hover {
            opacity: 0.8;
        }
        .actions {
            text-align: center;
            margin: 20px 0;
        }
        .user-details {
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
        }
        .user-details h3 {
            margin-top: 0;
            color: #333;
        }
        .user-details p {
            margin: 5px 0;
        }
        .refresh-btn {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background-color: #28a745;
            color: white;
            border: none;
            border-radius: 50%;
            width: 60px;
            height: 60px;
            font-size: 20px;
            cursor: pointer;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        }
        .refresh-btn:hover {
            background-color: #218838;
        }
        .no-data {
            text-align: center;
            padding: 40px;
            color: #666;
        }
        .file-info {
            background-color: #e9ecef;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 20px;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>CSV Database Viewer</h1>
        
        <div class="file-info">
            <strong>CSV File:</strong> {{ csv_file_path }}<br>
            <strong>Last Updated:</strong> {{ last_updated }}<br>
            <strong>File Size:</strong> {{ file_size }}
        </div>
        
        <div class="stats">
            <div class="stat-item">
                <div class="stat-number">{{ total_users }}</div>
                <div class="stat-label">Total Users</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">{{ active_users }}</div>
                <div class="stat-label">Active Users</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">{{ inactive_users }}</div>
                <div class="stat-label">Inactive Users</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">{{ unique_hospitals }}</div>
                <div class="stat-label">Hospitals</div>
            </div>
        </div>
        
        <div class="search-box">
            <input type="text" id="searchInput" placeholder="Search users by username, email, or hospital name..." onkeyup="searchUsers()">
        </div>
        
        <div class="actions">
            <a href="/raw" class="btn btn-secondary">View Raw CSV</a>
            <a href="/json" class="btn btn-secondary">View as JSON</a>
            <a href="/export" class="btn btn-secondary">Export Data</a>
        </div>
        
        {% if users %}
        <div class="table-container">
            <table id="usersTable">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Username</th>
                        <th>Email</th>
                        <th>Hospital Name</th>
                        <th>Hospital ID</th>
                        <th>License ID</th>
                        <th>Created</th>
                        <th>Updated</th>
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
                        <td>{{ user.hospital_id }}</td>
                        <td>{{ user.license_id }}</td>
                        <td>{{ user.created_at[:10] if user.created_at else '' }}</td>
                        <td>{{ user.updated_at[:10] if user.updated_at else '' }}</td>
                        <td>
                            {% if user.is_active == 'true' %}
                                <span class="status-active">Active</span>
                            {% else %}
                                <span class="status-inactive">Inactive</span>
                            {% endif %}
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        {% else %}
        <div class="no-data">
            <h3>No users found in the database</h3>
            <p>The CSV file is empty or doesn't exist.</p>
        </div>
        {% endif %}
        
        <button class="refresh-btn" onclick="location.reload()" title="Refresh Data">↻</button>
    </div>
    
    <script>
        function searchUsers() {
            var input = document.getElementById('searchInput');
            var filter = input.value.toLowerCase();
            var table = document.getElementById('usersTable');
            var rows = table.getElementsByTagName('tr');
            
            for (var i = 1; i < rows.length; i++) {
                var cells = rows[i].getElementsByTagName('td');
                var match = false;
                
                for (var j = 0; j < cells.length; j++) {
                    if (cells[j].textContent.toLowerCase().indexOf(filter) > -1) {
                        match = true;
                        break;
                    }
                }
                
                rows[i].style.display = match ? '' : 'none';
            }
        }
        
        // Auto-refresh every 30 seconds
        setInterval(function() {
            location.reload();
        }, 30000);
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    """Main dashboard showing all users."""
    try:
        # Get all users
        result = csv_manager.list_users(active_only=False)
        
        if result['success']:
            users = result['users']
            
            # Calculate statistics
            total_users = len(users)
            active_users = sum(1 for user in users if user['is_active'] == 'true')
            inactive_users = total_users - active_users
            unique_hospitals = len(set(user['hospital_name'] for user in users if user['hospital_name']))
            
            # File information
            file_size = "N/A"
            last_updated = "N/A"
            
            try:
                if os.path.exists(CSV_FILE_PATH):
                    stat = os.stat(CSV_FILE_PATH)
                    file_size = f"{stat.st_size} bytes"
                    last_updated = str(stat.st_mtime)
            except:
                pass
            
            return render_template_string(HTML_TEMPLATE,
                                        users=users,
                                        total_users=total_users,
                                        active_users=active_users,
                                        inactive_users=inactive_users,
                                        unique_hospitals=unique_hospitals,
                                        csv_file_path=CSV_FILE_PATH,
                                        file_size=file_size,
                                        last_updated=last_updated)
        else:
            return render_template_string(HTML_TEMPLATE,
                                        users=[],
                                        total_users=0,
                                        active_users=0,
                                        inactive_users=0,
                                        unique_hospitals=0,
                                        csv_file_path=CSV_FILE_PATH,
                                        file_size="N/A",
                                        last_updated="N/A")
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/raw')
def raw_csv():
    """View raw CSV content."""
    try:
        if os.path.exists(CSV_FILE_PATH):
            with open(CSV_FILE_PATH, 'r', newline='', encoding='utf-8') as file:
                content = file.read()
                return f"<pre>{content}</pre>", 200, {'Content-Type': 'text/html'}
        else:
            return "CSV file not found", 404
    except Exception as e:
        return f"Error reading CSV file: {str(e)}", 500

@app.route('/json')
def json_data():
    """View data as JSON."""
    try:
        result = csv_manager.list_users(active_only=False)
        if result['success']:
            return jsonify(result['users'])
        else:
            return jsonify({"error": result['message']}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/export')
def export_data():
    """Export data as downloadable CSV."""
    try:
        if os.path.exists(CSV_FILE_PATH):
            with open(CSV_FILE_PATH, 'r', newline='', encoding='utf-8') as file:
                content = file.read()
                
                from flask import Response
                return Response(
                    content,
                    mimetype='text/csv',
                    headers={'Content-Disposition': f'attachment; filename=users_export.csv'}
                )
        else:
            return "CSV file not found", 404
    except Exception as e:
        return f"Error exporting CSV file: {str(e)}", 500

@app.route('/api/users')
def api_users():
    """API endpoint to get users data."""
    try:
        result = csv_manager.list_users(active_only=False)
        if result['success']:
            return jsonify({
                'success': True,
                'users': result['users'],
                'total': len(result['users'])
            })
        else:
            return jsonify({
                'success': False,
                'message': result['message']
            }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/api/search')
def api_search():
    """API endpoint to search users."""
    query = request.args.get('q', '').lower()
    
    if not query:
        return jsonify({'success': False, 'message': 'No search query provided'}), 400
    
    try:
        result = csv_manager.list_users(active_only=False)
        if result['success']:
            # Filter users based on search query
            filtered_users = []
            for user in result['users']:
                if (query in user.get('username', '').lower() or
                    query in user.get('email', '').lower() or
                    query in user.get('hospital_name', '').lower()):
                    filtered_users.append(user)
            
            return jsonify({
                'success': True,
                'users': filtered_users,
                'total': len(filtered_users)
            })
        else:
            return jsonify({
                'success': False,
                'message': result['message']
            }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

def create_sample_data():
    """Create sample data if CSV file doesn't exist."""
    if not os.path.exists(CSV_FILE_PATH):
        print("Creating sample data...")
        
        sample_users = [
            {
                'username': 'general_hospital',
                'email': 'admin@generalhospital.com',
                'password': 'hospital123',
                'hospital_name': 'General Hospital',
                'hospital_id': 'GH001',
                'license_id': 'LIC001'
            },
            {
                'username': 'medical_center',
                'email': 'info@medicalcenter.com',
                'password': 'medical456',
                'hospital_name': 'Medical Center',
                'hospital_id': 'MC002',
                'license_id': 'LIC002'
            },
            {
                'username': 'health_clinic',
                'email': 'contact@healthclinic.com',
                'password': 'clinic789',
                'hospital_name': 'Health Clinic',
                'hospital_id': 'HC003',
                'license_id': 'LIC003'
            }
        ]
        
        for user_data in sample_users:
            result = csv_manager.create_user(user_data)
            if result['success']:
                print(f"Created sample user: {user_data['username']}")

if __name__ == '__main__':
    print("Starting CSV Database Viewer...")
    print("="*50)
    
    # Create sample data if needed
    create_sample_data()
    
    print(f"CSV File: {CSV_FILE_PATH}")
    print(f"Backup Directory: {BACKUP_DIR}")
    print("="*50)
    print("Available endpoints:")
    print("  http://localhost:5000/        - Main dashboard")
    print("  http://localhost:5000/raw     - Raw CSV content")
    print("  http://localhost:5000/json    - JSON format")
    print("  http://localhost:5000/export  - Download CSV")
    print("  http://localhost:5000/api/users - API endpoint")
    print("="*50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
