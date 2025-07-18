#!/usr/bin/env python3
"""
Migration script to move users from Django database to CSV format
"""

import os
import sys
import django
from pathlib import Path

# Add the current directory to the path and set up Django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth.models import User
from core.csv_user_manager import CSVUserManager

def migrate_users():
    """Migrate users from Django database to CSV format."""
    
    # Initialize CSV manager
    csv_manager = CSVUserManager(
        csv_file_path='data/users.csv',
        backup_dir='data/backups'
    )
    
    # Get all Django users
    django_users = User.objects.all()
    
    print(f"Found {django_users.count()} users in Django database")
    print("Starting migration to CSV format...")
    print("=" * 50)
    
    migrated_count = 0
    skipped_count = 0
    
    for django_user in django_users:
        # Prepare user data for CSV
        user_data = {
            'username': django_user.username,
            'email': django_user.email if django_user.email else f"{django_user.username}@example.com",
            'password': 'migrated_password_123',  # Default password for migrated users
            'hospital_name': django_user.username,  # Use username as hospital name
            'hospital_id': django_user.first_name if django_user.first_name else f"H{django_user.id:03d}",
            'license_id': f"LIC{django_user.id:03d}"
        }
        
        # Try to create user in CSV
        result = csv_manager.create_user(user_data)
        
        if result['success']:
            print(f"✅ Migrated: {django_user.username} ({django_user.email})")
            migrated_count += 1
        else:
            print(f"❌ Skipped: {django_user.username} - {result.get('errors', ['Unknown error'])}")
            skipped_count += 1
    
    print("=" * 50)
    print(f"Migration completed:")
    print(f"  ✅ Migrated: {migrated_count} users")
    print(f"  ❌ Skipped: {skipped_count} users")
    print(f"  📁 CSV file: data/users.csv")
    
    # Show CSV content
    print("\nCSV Database content:")
    result = csv_manager.list_users(active_only=False)
    if result['success']:
        for user in result['users']:
            print(f"  - {user['username']} ({user['email']}) - {user['hospital_name']}")
    
    print("\n🔑 Important: All migrated users have the password 'migrated_password_123'")
    print("   Users should change their passwords after first login.")

if __name__ == '__main__':
    migrate_users()
