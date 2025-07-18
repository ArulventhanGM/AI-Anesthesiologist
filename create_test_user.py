#!/usr/bin/env python
"""
Test script to create a test user and verify signup functionality
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

def create_test_user():
    """Create a test user to verify signup functionality"""
    print("Creating Test User...")
    print("=" * 50)
    
    # Initialize CSV manager
    csv_manager = CSVUserManager(
        csv_file_path=os.path.join(settings.BASE_DIR, 'data', 'users.csv'),
        backup_dir=os.path.join(settings.BASE_DIR, 'data', 'backups')
    )
    
    # Test user data
    test_user_data = {
        'username': 'Modern Test Hospital',
        'email': 'moderntest@hospital.com',
        'password': 'ModernTest123',
        'hospital_name': 'Modern Test Hospital',
        'hospital_id': 'MTH001',
        'license_id': 'ModernTest123'
    }
    
    print("Creating user with the following data:")
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
            
            # Test authentication immediately
            print("\nTesting authentication...")
            auth_result = csv_manager.authenticate_user(
                test_user_data['username'], 
                test_user_data['password']
            )
            
            if auth_result['success']:
                print("✓ Authentication successful!")
                print(f"   Authenticated user: {auth_result['user']['username']}")
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
    create_test_user()
