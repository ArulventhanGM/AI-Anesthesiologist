"""
CSV-based User Management System for Django
This module provides secure CRUD operations for user data using CSV files.
"""

import csv
import os
import hashlib
import secrets
import threading
import time
import shutil
from datetime import datetime
from typing import Dict, List, Optional, Union
from pathlib import Path
import re

class CSVUserManager:
    """
    A secure CSV-based user management system with file locking,
    password hashing, and data validation.
    """
    
    def __init__(self, csv_file_path: str = 'users.csv', backup_dir: str = 'backups'):
        """
        Initialize the CSV User Manager.
        
        Args:
            csv_file_path: Path to the CSV file
            backup_dir: Directory for backup files
        """
        self.csv_file_path = Path(csv_file_path)
        self.backup_dir = Path(backup_dir)
        self.lock = threading.Lock()
        
        # Create necessary directories
        self.csv_file_path.parent.mkdir(parents=True, exist_ok=True)
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        # CSV headers
        self.headers = [
            'id', 'username', 'email', 'password_hash', 'salt',
            'hospital_name', 'hospital_id', 'license_id', 
            'created_at', 'updated_at', 'is_active'
        ]
        
        # Initialize CSV file if it doesn't exist
        self._initialize_csv()
    
    def _initialize_csv(self):
        """Initialize the CSV file with headers if it doesn't exist."""
        if not self.csv_file_path.exists():
            with open(self.csv_file_path, 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=self.headers)
                writer.writeheader()
    
    def _generate_salt(self) -> str:
        """Generate a random salt for password hashing."""
        return secrets.token_hex(32)
    
    def _hash_password(self, password: str, salt: str) -> str:
        """Hash a password with salt using SHA-256."""
        return hashlib.sha256((password + salt).encode()).hexdigest()
    
    def _validate_input(self, data: Dict) -> List[str]:
        """
        Validate input data for CSV injection and required fields.
        
        Returns:
            List of validation errors
        """
        errors = []
        
        # Check for required fields
        required_fields = ['username', 'email', 'password']
        for field in required_fields:
            if not data.get(field):
                errors.append(f"{field} is required")
        
        # Validate email format
        if data.get('email'):
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, data['email']):
                errors.append("Invalid email format")
        
        # Check for CSV injection attempts
        dangerous_chars = ['"', "'", '=', '+', '-', '@', '\t', '\r', '\n']
        for key, value in data.items():
            if isinstance(value, str):
                # Remove dangerous characters or escape them
                for char in dangerous_chars:
                    if char in value:
                        errors.append(f"Invalid character '{char}' in {key}")
        
        # Validate username (alphanumeric and underscore only)
        if data.get('username'):
            if not re.match(r'^[a-zA-Z0-9_]+$', data['username']):
                errors.append("Username can only contain letters, numbers, and underscores")
        
        return errors
    
    def _create_backup(self):
        """Create a backup of the current CSV file."""
        if self.csv_file_path.exists():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = self.backup_dir / f"users_backup_{timestamp}.csv"
            shutil.copy2(self.csv_file_path, backup_path)
            
            # Keep only the last 10 backups
            backups = sorted(self.backup_dir.glob("users_backup_*.csv"))
            if len(backups) > 10:
                for old_backup in backups[:-10]:
                    old_backup.unlink()
    
    def _read_all_users(self) -> List[Dict]:
        """Read all users from the CSV file."""
        users = []
        try:
            with open(self.csv_file_path, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                users = list(reader)
        except FileNotFoundError:
            pass
        return users
    
    def _write_all_users(self, users: List[Dict]):
        """Write all users to the CSV file."""
        with open(self.csv_file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=self.headers)
            writer.writeheader()
            writer.writerows(users)
    
    def _generate_user_id(self) -> str:
        """Generate a unique user ID."""
        users = self._read_all_users()
        if not users:
            return "1"
        
        # Find the highest ID and increment
        max_id = max(int(user.get('id', 0)) for user in users)
        return str(max_id + 1)
    
    def create_user(self, user_data: Dict) -> Dict:
        """
        Create a new user in the CSV file.
        
        Args:
            user_data: Dictionary containing user information
            
        Returns:
            Dictionary with success status and message
        """
        with self.lock:
            try:
                # Validate input
                errors = self._validate_input(user_data)
                if errors:
                    return {'success': False, 'errors': errors}
                
                # Check if user already exists
                users = self._read_all_users()
                
                # Check for duplicate username or email
                for user in users:
                    if user.get('username') == user_data['username']:
                        return {'success': False, 'errors': ['Username already exists']}
                    if user.get('email') == user_data['email']:
                        return {'success': False, 'errors': ['Email already exists']}
                
                # Create backup before modification
                self._create_backup()
                
                # Prepare user data
                salt = self._generate_salt()
                password_hash = self._hash_password(user_data['password'], salt)
                current_time = datetime.now().isoformat()
                
                new_user = {
                    'id': self._generate_user_id(),
                    'username': user_data['username'],
                    'email': user_data['email'],
                    'password_hash': password_hash,
                    'salt': salt,
                    'hospital_name': user_data.get('hospital_name', ''),
                    'hospital_id': user_data.get('hospital_id', ''),
                    'license_id': user_data.get('license_id', ''),
                    'created_at': current_time,
                    'updated_at': current_time,
                    'is_active': 'true'
                }
                
                # Add new user to the list
                users.append(new_user)
                
                # Write back to CSV
                self._write_all_users(users)
                
                return {
                    'success': True, 
                    'message': 'User created successfully',
                    'user_id': new_user['id']
                }
                
            except Exception as e:
                return {'success': False, 'errors': [f'Error creating user: {str(e)}']}
    
    def authenticate_user(self, username: str, password: str) -> Dict:
        """
        Authenticate a user by username and password.
        
        Args:
            username: User's username
            password: User's plain text password
            
        Returns:
            Dictionary with authentication result
        """
        with self.lock:
            try:
                users = self._read_all_users()
                
                for user in users:
                    if (user.get('username') == username and 
                        user.get('is_active') == 'true'):
                        
                        # Verify password
                        stored_hash = user.get('password_hash')
                        salt = user.get('salt')
                        
                        if stored_hash and salt:
                            computed_hash = self._hash_password(password, salt)
                            if computed_hash == stored_hash:
                                # Remove sensitive information
                                safe_user = {k: v for k, v in user.items() 
                                           if k not in ['password_hash', 'salt']}
                                return {
                                    'success': True,
                                    'user': safe_user,
                                    'message': 'Authentication successful'
                                }
                
                return {'success': False, 'message': 'Invalid username or password'}
                
            except Exception as e:
                return {'success': False, 'message': f'Authentication error: {str(e)}'}
    
    def get_user(self, user_id: str = None, username: str = None) -> Dict:
        """
        Get a user by ID or username.
        
        Args:
            user_id: User's ID
            username: User's username
            
        Returns:
            Dictionary with user data or error message
        """
        with self.lock:
            try:
                users = self._read_all_users()
                
                for user in users:
                    if ((user_id and user.get('id') == user_id) or 
                        (username and user.get('username') == username)):
                        
                        # Remove sensitive information
                        safe_user = {k: v for k, v in user.items() 
                                   if k not in ['password_hash', 'salt']}
                        return {'success': True, 'user': safe_user}
                
                return {'success': False, 'message': 'User not found'}
                
            except Exception as e:
                return {'success': False, 'message': f'Error retrieving user: {str(e)}'}
    
    def update_user(self, user_id: str, update_data: Dict) -> Dict:
        """
        Update a user's information.
        
        Args:
            user_id: User's ID
            update_data: Dictionary containing fields to update
            
        Returns:
            Dictionary with update result
        """
        with self.lock:
            try:
                users = self._read_all_users()
                user_found = False
                
                for i, user in enumerate(users):
                    if user.get('id') == user_id:
                        user_found = True
                        
                        # Create backup before modification
                        self._create_backup()
                        
                        # Update allowed fields
                        updatable_fields = ['hospital_name', 'hospital_id', 'license_id', 'email']
                        for field in updatable_fields:
                            if field in update_data:
                                user[field] = update_data[field]
                        
                        # Update password if provided
                        if 'password' in update_data:
                            salt = self._generate_salt()
                            password_hash = self._hash_password(update_data['password'], salt)
                            user['password_hash'] = password_hash
                            user['salt'] = salt
                        
                        user['updated_at'] = datetime.now().isoformat()
                        users[i] = user
                        break
                
                if not user_found:
                    return {'success': False, 'message': 'User not found'}
                
                # Write back to CSV
                self._write_all_users(users)
                
                return {'success': True, 'message': 'User updated successfully'}
                
            except Exception as e:
                return {'success': False, 'message': f'Error updating user: {str(e)}'}
    
    def delete_user(self, user_id: str) -> Dict:
        """
        Delete a user (soft delete by setting is_active to false).
        
        Args:
            user_id: User's ID
            
        Returns:
            Dictionary with deletion result
        """
        with self.lock:
            try:
                users = self._read_all_users()
                user_found = False
                
                for i, user in enumerate(users):
                    if user.get('id') == user_id:
                        user_found = True
                        
                        # Create backup before modification
                        self._create_backup()
                        
                        # Soft delete
                        user['is_active'] = 'false'
                        user['updated_at'] = datetime.now().isoformat()
                        users[i] = user
                        break
                
                if not user_found:
                    return {'success': False, 'message': 'User not found'}
                
                # Write back to CSV
                self._write_all_users(users)
                
                return {'success': True, 'message': 'User deleted successfully'}
                
            except Exception as e:
                return {'success': False, 'message': f'Error deleting user: {str(e)}'}
    
    def list_users(self, active_only: bool = True) -> Dict:
        """
        List all users.
        
        Args:
            active_only: If True, return only active users
            
        Returns:
            Dictionary with user list
        """
        with self.lock:
            try:
                users = self._read_all_users()
                
                if active_only:
                    users = [user for user in users if user.get('is_active') == 'true']
                
                # Remove sensitive information
                safe_users = []
                for user in users:
                    safe_user = {k: v for k, v in user.items() 
                               if k not in ['password_hash', 'salt']}
                    safe_users.append(safe_user)
                
                return {'success': True, 'users': safe_users}
                
            except Exception as e:
                return {'success': False, 'message': f'Error listing users: {str(e)}'}
