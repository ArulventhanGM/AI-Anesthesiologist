#!/usr/bin/env python3
"""
CSV Database Viewer - Multiple ways to view your CSV user database
"""

import csv
import pandas as pd
import json
import sys
import os
from pathlib import Path
from datetime import datetime

# Add the core directory to the Python path
sys.path.append(str(Path(__file__).parent / 'core'))

try:
    from csv_user_manager import CSVUserManager
except ImportError:
    print("csv_user_manager.py not found. Make sure it's in the core directory.")
    sys.exit(1)

def view_csv_raw(csv_file_path):
    """View CSV file in raw format."""
    print("=== Raw CSV Content ===")
    try:
        with open(csv_file_path, 'r', newline='', encoding='utf-8') as file:
            content = file.read()
            print(content)
    except FileNotFoundError:
        print(f"CSV file not found: {csv_file_path}")
    except Exception as e:
        print(f"Error reading CSV file: {e}")

def view_csv_formatted(csv_file_path):
    """View CSV file in formatted table."""
    print("\n=== Formatted CSV Content ===")
    try:
        with open(csv_file_path, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            rows = list(reader)
            
            if not rows:
                print("No data found in CSV file.")
                return
            
            # Get headers
            headers = rows[0].keys()
            
            # Calculate column widths
            col_widths = {}
            for header in headers:
                col_widths[header] = max(len(header), 
                                       max(len(str(row.get(header, ''))) for row in rows))
            
            # Print header
            header_line = " | ".join(header.ljust(col_widths[header]) for header in headers)
            print(header_line)
            print("-" * len(header_line))
            
            # Print rows
            for row in rows:
                row_line = " | ".join(str(row.get(header, '')).ljust(col_widths[header]) for header in headers)
                print(row_line)
                
    except FileNotFoundError:
        print(f"CSV file not found: {csv_file_path}")
    except Exception as e:
        print(f"Error reading CSV file: {e}")

def view_csv_with_pandas(csv_file_path):
    """View CSV file using pandas (if available)."""
    print("\n=== Pandas DataFrame View ===")
    try:
        df = pd.read_csv(csv_file_path)
        print(df.to_string(index=False))
        
        print(f"\nDataFrame Info:")
        print(f"Shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        print(f"Data types:\n{df.dtypes}")
        
    except ImportError:
        print("Pandas not available. Install with: pip install pandas")
    except FileNotFoundError:
        print(f"CSV file not found: {csv_file_path}")
    except Exception as e:
        print(f"Error reading CSV file with pandas: {e}")

def view_csv_with_manager(csv_file_path):
    """View CSV file using the CSVUserManager."""
    print("\n=== Using CSVUserManager ===")
    try:
        manager = CSVUserManager(csv_file_path)
        
        # List all users
        result = manager.list_users(active_only=False)
        
        if result['success']:
            users = result['users']
            print(f"Total users: {len(users)}")
            
            if users:
                print("\nUsers:")
                for i, user in enumerate(users, 1):
                    print(f"\n{i}. User ID: {user['id']}")
                    print(f"   Username: {user['username']}")
                    print(f"   Email: {user['email']}")
                    print(f"   Hospital: {user['hospital_name']}")
                    print(f"   Hospital ID: {user['hospital_id']}")
                    print(f"   License ID: {user['license_id']}")
                    print(f"   Created: {user['created_at']}")
                    print(f"   Updated: {user['updated_at']}")
                    print(f"   Status: {'Active' if user['is_active'] == 'true' else 'Inactive'}")
            else:
                print("No users found in the database.")
        else:
            print(f"Error: {result['message']}")
            
    except Exception as e:
        print(f"Error using CSVUserManager: {e}")

def view_csv_summary(csv_file_path):
    """View CSV file summary statistics."""
    print("\n=== CSV Summary ===")
    try:
        with open(csv_file_path, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            rows = list(reader)
            
            if not rows:
                print("No data found in CSV file.")
                return
            
            total_users = len(rows)
            active_users = sum(1 for row in rows if row.get('is_active') == 'true')
            inactive_users = total_users - active_users
            
            print(f"Total users: {total_users}")
            print(f"Active users: {active_users}")
            print(f"Inactive users: {inactive_users}")
            
            # Get unique hospitals
            hospitals = set(row.get('hospital_name', '') for row in rows if row.get('hospital_name'))
            print(f"Unique hospitals: {len(hospitals)}")
            
            # Get creation dates
            creation_dates = [row.get('created_at', '') for row in rows if row.get('created_at')]
            if creation_dates:
                print(f"Date range: {min(creation_dates)} to {max(creation_dates)}")
            
            print("\nHospitals:")
            for hospital in sorted(hospitals):
                if hospital:
                    print(f"  - {hospital}")
                    
    except FileNotFoundError:
        print(f"CSV file not found: {csv_file_path}")
    except Exception as e:
        print(f"Error reading CSV file: {e}")

def view_csv_json(csv_file_path):
    """View CSV file as JSON format."""
    print("\n=== JSON Format ===")
    try:
        with open(csv_file_path, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            rows = list(reader)
            
            # Remove sensitive information for display
            safe_rows = []
            for row in rows:
                safe_row = {k: v for k, v in row.items() 
                          if k not in ['password_hash', 'salt']}
                safe_rows.append(safe_row)
            
            print(json.dumps(safe_rows, indent=2))
            
    except FileNotFoundError:
        print(f"CSV file not found: {csv_file_path}")
    except Exception as e:
        print(f"Error reading CSV file: {e}")

def interactive_viewer(csv_file_path):
    """Interactive CSV viewer with menu options."""
    while True:
        print("\n" + "="*50)
        print("CSV Database Viewer")
        print("="*50)
        print("1. View raw CSV content")
        print("2. View formatted table")
        print("3. View with pandas (if available)")
        print("4. View using CSVUserManager")
        print("5. View summary statistics")
        print("6. View as JSON")
        print("7. Search users")
        print("8. Exit")
        
        choice = input("\nEnter your choice (1-8): ").strip()
        
        if choice == '1':
            view_csv_raw(csv_file_path)
        elif choice == '2':
            view_csv_formatted(csv_file_path)
        elif choice == '3':
            view_csv_with_pandas(csv_file_path)
        elif choice == '4':
            view_csv_with_manager(csv_file_path)
        elif choice == '5':
            view_csv_summary(csv_file_path)
        elif choice == '6':
            view_csv_json(csv_file_path)
        elif choice == '7':
            search_users(csv_file_path)
        elif choice == '8':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
        
        input("\nPress Enter to continue...")

def search_users(csv_file_path):
    """Search for users in the CSV file."""
    print("\n=== Search Users ===")
    search_term = input("Enter search term (username, email, or hospital): ").strip().lower()
    
    if not search_term:
        print("No search term provided.")
        return
    
    try:
        with open(csv_file_path, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            matching_users = []
            
            for row in reader:
                # Search in username, email, and hospital_name
                if (search_term in row.get('username', '').lower() or
                    search_term in row.get('email', '').lower() or
                    search_term in row.get('hospital_name', '').lower()):
                    matching_users.append(row)
            
            if matching_users:
                print(f"\nFound {len(matching_users)} matching user(s):")
                for i, user in enumerate(matching_users, 1):
                    print(f"\n{i}. User ID: {user['id']}")
                    print(f"   Username: {user['username']}")
                    print(f"   Email: {user['email']}")
                    print(f"   Hospital: {user['hospital_name']}")
                    print(f"   Status: {'Active' if user['is_active'] == 'true' else 'Inactive'}")
            else:
                print("No matching users found.")
                
    except FileNotFoundError:
        print(f"CSV file not found: {csv_file_path}")
    except Exception as e:
        print(f"Error searching CSV file: {e}")

def main():
    """Main function to run the CSV viewer."""
    print("CSV Database Viewer")
    print("==================")
    
    # Default CSV file path
    default_csv_path = 'users.csv'
    
    # Check if CSV file exists in common locations
    possible_paths = [
        'users.csv',
        'data/users.csv',
        'core/users.csv',
        'demo_users.csv',
        'flask_users.csv'
    ]
    
    csv_file_path = None
    for path in possible_paths:
        if os.path.exists(path):
            csv_file_path = path
            break
    
    if not csv_file_path:
        csv_file_path = input(f"Enter CSV file path (default: {default_csv_path}): ").strip()
        if not csv_file_path:
            csv_file_path = default_csv_path
    
    print(f"Using CSV file: {csv_file_path}")
    
    if not os.path.exists(csv_file_path):
        print(f"CSV file not found: {csv_file_path}")
        print("Creating a sample CSV file for demonstration...")
        
        # Create sample CSV file
        create_sample_csv(csv_file_path)
    
    # Check if running interactively
    if len(sys.argv) > 1 and sys.argv[1] == '--interactive':
        interactive_viewer(csv_file_path)
    else:
        # Show all views
        view_csv_raw(csv_file_path)
        view_csv_formatted(csv_file_path)
        view_csv_with_pandas(csv_file_path)
        view_csv_with_manager(csv_file_path)
        view_csv_summary(csv_file_path)
        
        print("\n" + "="*50)
        print("For interactive mode, run:")
        print(f"python {sys.argv[0]} --interactive")

def create_sample_csv(csv_file_path):
    """Create a sample CSV file for demonstration."""
    try:
        manager = CSVUserManager(csv_file_path)
        
        # Create sample users
        sample_users = [
            {
                'username': 'city_hospital',
                'email': 'admin@cityhospital.com',
                'password': 'hospital123',
                'hospital_name': 'City General Hospital',
                'hospital_id': 'CGH001',
                'license_id': 'LIC001'
            },
            {
                'username': 'regional_medical',
                'email': 'info@regionalmedical.com',
                'password': 'regional456',
                'hospital_name': 'Regional Medical Center',
                'hospital_id': 'RMC002',
                'license_id': 'LIC002'
            },
            {
                'username': 'metro_health',
                'email': 'contact@metrohealth.com',
                'password': 'metro789',
                'hospital_name': 'Metro Health System',
                'hospital_id': 'MHS003',
                'license_id': 'LIC003'
            }
        ]
        
        for user_data in sample_users:
            result = manager.create_user(user_data)
            if result['success']:
                print(f"Created sample user: {user_data['username']}")
            else:
                print(f"Failed to create user: {result['errors']}")
        
        print(f"Sample CSV file created: {csv_file_path}")
        
    except Exception as e:
        print(f"Error creating sample CSV: {e}")

if __name__ == '__main__':
    main()
