#!/usr/bin/env python
"""
Test script to debug login issue
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

def test_login_flow():
    """Test the login flow to debug the issue"""
    print("Testing Login Flow...")
    print("=" * 50)
    
    # Initialize CSV manager
    csv_manager = CSVUserManager(
        csv_file_path=os.path.join(settings.BASE_DIR, 'data', 'users.csv'),
        backup_dir=os.path.join(settings.BASE_DIR, 'data', 'backups')
    )
    
    # Test with a known user
    test_username = "testuser123"
    test_password = "TestUser123"
    
    print(f"Testing login with username: {test_username}")
    print(f"Testing login with password: {test_password}")
    
    try:
        # Test authentication
        result = csv_manager.authenticate_user(test_username, test_password)
        
        if result['success']:
            print("✓ Authentication successful!")
            print(f"   User ID: {result['user']['id']}")
            print(f"   Username: {result['user']['username']}")
            print(f"   Hospital: {result['user']['hospital_name']}")
            print(f"   Email: {result['user']['email']}")
            print(f"   Is Active: {result['user']['is_active']}")
            
            print("\n✓ Login should redirect to hospital dashboard")
            print("   URL: /hospital")
        else:
            print("✗ Authentication failed!")
            print(f"   Message: {result['message']}")
            
    except Exception as e:
        print(f"✗ Error during authentication: {str(e)}")
        
    print("\n" + "=" * 50)
    
    # List all users to verify
    print("Current users in database:")
    result = csv_manager.list_users()
    if result['success']:
        for i, user in enumerate(result['users'], 1):
            print(f"   {i}. {user['username']} - {user['hospital_name']} - Active: {user['is_active']}")
    else:
        print("   Error listing users")
    
    return True

if __name__ == "__main__":
    test_login_flow()
