#!/usr/bin/env python
"""
Test script to verify the new signup form with username field
"""
import os
import sys
import django
from django.conf import settings

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from core.csv_user_manager import CSVUserManager

def test_username_signup():
    """Test the new signup form with username field"""
    print("Testing Username Signup Form...")
    print("=" * 50)
    
    # Initialize CSV manager
    csv_manager = CSVUserManager(
        csv_file_path=os.path.join(settings.BASE_DIR, 'data', 'users.csv'),
        backup_dir=os.path.join(settings.BASE_DIR, 'data', 'backups')
    )
    
    # Test user data with username field
    test_user_data = {
        'username': 'testuser123',
        'email': 'testuser123@hospital.com',
        'password': 'TestUser123',
        'hospital_name': 'Test Username Hospital',
        'hospital_id': 'TUH001',
        'license_id': 'TestUser123'
    }
    
    print("Creating user with the following data:")
    print(f"   Username: {test_user_data['username']}")
    print(f"   Hospital Name: {test_user_data['hospital_name']}")
    print(f"   Hospital ID: {test_user_data['hospital_id']}")
    print(f"   Email: {test_user_data['email']}")
    print(f"   Password: {test_user_data['password']}")
    
    try:
        # Create user using CSV manager
        result = csv_manager.create_user(test_user_data)
        
        if result['success']:
            print(f"\n✓ User created successfully!")
            print(f"   User ID: {result['user_id']}")
            
            # Test authentication with username
            print("\nTesting authentication with username...")
            auth_result = csv_manager.authenticate_user(
                test_user_data['username'], 
                test_user_data['password']
            )
            
            if auth_result['success']:
                print("✓ Authentication with username successful!")
                print(f"   Authenticated user: {auth_result['user']['username']}")
                print(f"   Hospital: {auth_result['user']['hospital_name']}")
            else:
                print(f"✗ Authentication failed: {auth_result['message']}")
                
        else:
            print(f"\n✗ User creation failed!")
            for error in result.get('errors', []):
                print(f"   Error: {error}")
                
    except Exception as e:
        print(f"\n✗ Error creating user: {str(e)}")
        return False
    
    print("\n" + "=" * 50)
    return True

if __name__ == "__main__":
    test_username_signup()
