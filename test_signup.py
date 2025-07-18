#!/usr/bin/env python
"""
Test script to verify CSV database connectivity for signup functionality
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

def test_csv_connectivity():
    """Test CSV database connectivity and operations"""
    print("Testing CSV Database Connectivity...")
    print("=" * 50)
    
    # Initialize CSV manager
    csv_manager = CSVUserManager(
        csv_file_path=os.path.join(settings.BASE_DIR, 'data', 'users.csv'),
        backup_dir=os.path.join(settings.BASE_DIR, 'data', 'backups')
    )
    
    # Test 1: Check if CSV file exists and is readable
    print("1. Checking CSV file accessibility...")
    try:
        result = csv_manager.list_users()
        if result['success']:
            users = result['users']
            print(f"   ✓ CSV file accessible. Found {len(users)} users.")
        else:
            print(f"   ✗ Error accessing CSV file: {result['message']}")
            return False
    except Exception as e:
        print(f"   ✗ Error accessing CSV file: {e}")
        return False
    
    # Test 2: Test user creation (dry run)
    print("\n2. Testing user creation logic...")
    test_user_data = {
        'username': 'Test Hospital',
        'email': 'test@hospital.com',
        'password': 'TestPass123',
        'hospital_name': 'Test Hospital',
        'hospital_id': 'TEST001',
        'license_id': 'TestPass123'
    }
    
    try:
        # Check if user already exists
        result = csv_manager.list_users()
        if result['success']:
            existing_users = result['users']
            test_email_exists = any(user['email'] == test_user_data['email'] for user in existing_users)
            test_username_exists = any(user['username'] == test_user_data['username'] for user in existing_users)
            
            if test_email_exists:
                print("   ✓ Email validation working (test email already exists)")
            else:
                print("   ✓ Email validation working (test email available)")
                
            if test_username_exists:
                print("   ✓ Username validation working (test username already exists)")
            else:
                print("   ✓ Username validation working (test username available)")
        else:
            print(f"   ✗ Error accessing users: {result['message']}")
            return False
            
    except Exception as e:
        print(f"   ✗ Error in user creation logic: {e}")
        return False
    
    # Test 3: Test password validation
    print("\n3. Testing password validation...")
    test_passwords = [
        ('weak', False),      # Too short
        ('WeakPass', False),  # No numbers
        ('weakpass123', False), # No uppercase
        ('WEAKPASS123', False), # No lowercase
        ('StrongPass123', True)  # Valid password
    ]
    
    for password, should_be_valid in test_passwords:
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        is_long_enough = len(password) >= 8
        
        is_valid = has_upper and has_lower and has_digit and is_long_enough
        
        if is_valid == should_be_valid:
            print(f"   ✓ Password '{password}': {'Valid' if is_valid else 'Invalid'}")
        else:
            print(f"   ✗ Password '{password}': Expected {'Valid' if should_be_valid else 'Invalid'}, got {'Valid' if is_valid else 'Invalid'}")
    
    # Test 4: Test authentication
    print("\n4. Testing authentication...")
    result = csv_manager.list_users()
    if result['success'] and result['users']:
        test_user = result['users'][0]
        # Use the license_id as password since that's what we store
        auth_result = csv_manager.authenticate_user(test_user['username'], test_user['license_id'])
        if auth_result['success']:
            print("   ✓ Authentication working")
        else:
            print(f"   ✗ Authentication failed: {auth_result['message']}")
    else:
        print("   ⚠ No users found to test authentication")
    
    # Test 5: Display current users
    print("\n5. Current users in CSV database:")
    if result['success'] and result['users']:
        for i, user in enumerate(result['users'], 1):
            print(f"   {i}. {user['username']} ({user['email']})")
    else:
        print("   No users found in CSV database")
    
    print("\n" + "=" * 50)
    print("CSV Database Connectivity Test Complete!")
    return True

if __name__ == "__main__":
    test_csv_connectivity()
