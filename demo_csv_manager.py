#!/usr/bin/env python3
"""
Example script demonstrating CSV User Management System
This script shows how to use the CSVUserManager class for various operations.
"""

import sys
import os
from pathlib import Path

# Add the core directory to the Python path
sys.path.append(str(Path(__file__).parent / 'core'))

from csv_user_manager import CSVUserManager

def main():
    """Demonstrate CSV User Management operations."""
    
    print("=== CSV User Management System Demo ===\n")
    
    # Initialize the CSV manager
    csv_manager = CSVUserManager(
        csv_file_path='demo_users.csv',
        backup_dir='demo_backups'
    )
    
    # 1. Create users
    print("1. Creating users...")
    
    users_to_create = [
        {
            'username': 'hospital_alpha',
            'email': 'alpha@example.com',
            'password': 'secure_password_123',
            'hospital_name': 'Alpha Medical Center',
            'hospital_id': 'AMC001',
            'license_id': 'LIC123456'
        },
        {
            'username': 'hospital_beta',
            'email': 'beta@example.com',
            'password': 'another_secure_pass',
            'hospital_name': 'Beta General Hospital',
            'hospital_id': 'BGH002',
            'license_id': 'LIC789012'
        },
        {
            'username': 'hospital_gamma',
            'email': 'gamma@example.com',
            'password': 'gamma_password_456',
            'hospital_name': 'Gamma Regional Hospital',
            'hospital_id': 'GRH003',
            'license_id': 'LIC345678'
        }
    ]
    
    for user_data in users_to_create:
        result = csv_manager.create_user(user_data)
        if result['success']:
            print(f"✓ Created user: {user_data['username']} (ID: {result['user_id']})")
        else:
            print(f"✗ Failed to create user {user_data['username']}: {result['errors']}")
    
    print()
    
    # 2. List all users
    print("2. Listing all users...")
    result = csv_manager.list_users()
    if result['success']:
        for user in result['users']:
            print(f"   - {user['username']} ({user['email']}) - {user['hospital_name']}")
    else:
        print(f"✗ Failed to list users: {result['message']}")
    
    print()
    
    # 3. Authentication test
    print("3. Testing authentication...")
    
    # Test valid credentials
    auth_result = csv_manager.authenticate_user('hospital_alpha', 'secure_password_123')
    if auth_result['success']:
        print("✓ Authentication successful for hospital_alpha")
        print(f"   User info: {auth_result['user']['hospital_name']}")
    else:
        print(f"✗ Authentication failed: {auth_result['message']}")
    
    # Test invalid credentials
    auth_result = csv_manager.authenticate_user('hospital_alpha', 'wrong_password')
    if auth_result['success']:
        print("✗ Authentication should have failed but succeeded")
    else:
        print("✓ Authentication correctly failed for wrong password")
    
    print()
    
    # 4. Get user by username
    print("4. Getting user by username...")
    user_result = csv_manager.get_user(username='hospital_beta')
    if user_result['success']:
        user = user_result['user']
        print(f"✓ Found user: {user['username']}")
        print(f"   Email: {user['email']}")
        print(f"   Hospital: {user['hospital_name']}")
        print(f"   Created: {user['created_at']}")
    else:
        print(f"✗ Failed to get user: {user_result['message']}")
    
    print()
    
    # 5. Update user
    print("5. Updating user information...")
    update_result = csv_manager.update_user(
        user_id='2',  # Assuming this is hospital_beta's ID
        update_data={
            'hospital_name': 'Beta General Hospital - Updated',
            'email': 'beta_updated@example.com'
        }
    )
    if update_result['success']:
        print("✓ User updated successfully")
        
        # Verify the update
        user_result = csv_manager.get_user(user_id='2')
        if user_result['success']:
            user = user_result['user']
            print(f"   Updated hospital name: {user['hospital_name']}")
            print(f"   Updated email: {user['email']}")
    else:
        print(f"✗ Failed to update user: {update_result['message']}")
    
    print()
    
    # 6. Demonstrate input validation
    print("6. Testing input validation...")
    
    # Test with invalid email
    invalid_user = {
        'username': 'test_user',
        'email': 'invalid_email',
        'password': 'password123'
    }
    
    result = csv_manager.create_user(invalid_user)
    if result['success']:
        print("✗ Should have failed validation but succeeded")
    else:
        print("✓ Input validation working correctly")
        for error in result['errors']:
            print(f"   - {error}")
    
    print()
    
    # 7. Test CSV injection protection
    print("7. Testing CSV injection protection...")
    
    # Test with dangerous characters
    dangerous_user = {
        'username': 'test=user',
        'email': 'test@example.com',
        'password': 'password"123'
    }
    
    result = csv_manager.create_user(dangerous_user)
    if result['success']:
        print("✗ Should have failed CSV injection check but succeeded")
    else:
        print("✓ CSV injection protection working correctly")
        for error in result['errors']:
            print(f"   - {error}")
    
    print()
    
    # 8. Delete user (soft delete)
    print("8. Deleting user (soft delete)...")
    delete_result = csv_manager.delete_user('3')  # Assuming this is hospital_gamma's ID
    if delete_result['success']:
        print("✓ User deleted successfully")
        
        # Verify deletion
        result = csv_manager.list_users(active_only=True)
        if result['success']:
            print(f"   Active users after deletion: {len(result['users'])}")
    else:
        print(f"✗ Failed to delete user: {delete_result['message']}")
    
    print()
    
    # 9. List all users including inactive
    print("9. Listing all users (including inactive)...")
    result = csv_manager.list_users(active_only=False)
    if result['success']:
        for user in result['users']:
            status = "Active" if user['is_active'] == 'true' else "Inactive"
            print(f"   - {user['username']} ({status})")
    else:
        print(f"✗ Failed to list users: {result['message']}")
    
    print("\n=== Demo completed ===")
    print(f"Check the 'demo_users.csv' file and 'demo_backups' directory for results.")

if __name__ == '__main__':
    main()
