"""
Django views using CSV-based user management system.
"""

from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.conf import settings
import os
from .csv_user_manager import CSVUserManager

# Initialize CSV User Manager
csv_manager = CSVUserManager(
    csv_file_path=os.path.join(settings.BASE_DIR, 'data', 'users.csv'),
    backup_dir=os.path.join(settings.BASE_DIR, 'data', 'backups')
)

def ex_data(req, data):
    """Extract data from POST request."""
    return req.POST.get(data, "").strip()

def index(request):
    """Login view with CSV authentication."""
    if request.method == 'POST':
        username = ex_data(request, "username")
        password = ex_data(request, "password")
        
        if not username or not password:
            messages.error(request, 'Please enter both username and password.')
            return render(request, 'login.html')
        
        try:
            # Authenticate using CSV manager
            result = csv_manager.authenticate_user(username, password)
            
            if result['success']:
                # Store user info in session
                request.session['user_id'] = result['user']['id']
                request.session['username'] = result['user']['username']
                request.session['hospital_name'] = result['user']['hospital_name']
                request.session['is_logged_in'] = True
                
                messages.success(request, f'Welcome back, {username}!')
                return redirect('hos')
            else:
                messages.error(request, result['message'])
                return render(request, 'login.html')
                
        except Exception as e:
            messages.error(request, f'Login error: {str(e)}')
            return render(request, 'login.html')
    
    return render(request, 'login.html')

def go(request):
    """Alternative login view (same as index)."""
    return index(request)

def hospital(request):
    """Hospital dashboard view."""
    if not request.session.get('is_logged_in'):
        messages.error(request, 'Please login to access this page.')
        return redirect('login')
    
    return render(request, 'hospital.html')

def prediction(request):
    """Prediction view."""
    if not request.session.get('is_logged_in'):
        messages.error(request, 'Please login to access this page.')
        return redirect('login')
    
    return render(request, 'prediction.html')

def out(request):
    """Logout view."""
    # Clear session data
    request.session.flush()
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')

def signup(request):
    """User registration view using CSV storage."""
    if request.method == 'POST':
        hospital_name = ex_data(request, "hospital_name")
        hospital_id = ex_data(request, "hospital_id")
        license_id = ex_data(request, "license_id")
        email_id = ex_data(request, "email_id")
        
        # Basic validation
        if not all([hospital_name, hospital_id, license_id, email_id]):
            messages.error(request, 'All fields are required.')
            return render(request, 'signup.html')
        
        # Prepare user data
        user_data = {
            'username': hospital_name,
            'email': email_id,
            'password': license_id,
            'hospital_name': hospital_name,
            'hospital_id': hospital_id,
            'license_id': license_id
        }
        
        try:
            # Create user using CSV manager
            result = csv_manager.create_user(user_data)
            
            if result['success']:
                messages.success(request, 
                    f'Account created successfully! You can now login with Hospital Name: {hospital_name}')
                return redirect('login')
            else:
                # Display validation errors
                for error in result.get('errors', []):
                    messages.error(request, error)
                return render(request, 'signup.html')
                
        except Exception as e:
            messages.error(request, f'Error creating account: {str(e)}')
            return render(request, 'signup.html')
    
    return render(request, 'signup.html')

def profile(request):
    """User profile view."""
    if not request.session.get('is_logged_in'):
        messages.error(request, 'Please login to access this page.')
        return redirect('login')
    
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, 'Session expired. Please login again.')
        return redirect('login')
    
    # Get user data
    result = csv_manager.get_user(user_id=user_id)
    
    if result['success']:
        context = {'user': result['user']}
        return render(request, 'profile.html', context)
    else:
        messages.error(request, 'Could not load profile.')
        return redirect('hos')

def update_profile(request):
    """Update user profile."""
    if not request.session.get('is_logged_in'):
        messages.error(request, 'Please login to access this page.')
        return redirect('login')
    
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, 'Session expired. Please login again.')
        return redirect('login')
    
    if request.method == 'POST':
        update_data = {}
        
        # Get fields to update
        if ex_data(request, "hospital_name"):
            update_data['hospital_name'] = ex_data(request, "hospital_name")
        if ex_data(request, "hospital_id"):
            update_data['hospital_id'] = ex_data(request, "hospital_id")
        if ex_data(request, "email_id"):
            update_data['email'] = ex_data(request, "email_id")
        if ex_data(request, "new_password"):
            update_data['password'] = ex_data(request, "new_password")
        
        if update_data:
            result = csv_manager.update_user(user_id, update_data)
            
            if result['success']:
                messages.success(request, 'Profile updated successfully!')
                
                # Update session data if username changed
                if 'hospital_name' in update_data:
                    request.session['hospital_name'] = update_data['hospital_name']
                
                return redirect('profile')
            else:
                messages.error(request, result['message'])
        else:
            messages.error(request, 'No changes were made.')
    
    return redirect('profile')

def admin_users(request):
    """Admin view to list all users (for demonstration purposes)."""
    if not request.session.get('is_logged_in'):
        messages.error(request, 'Please login to access this page.')
        return redirect('login')
    
    # In a real application, you'd check for admin privileges
    result = csv_manager.list_users()
    
    if result['success']:
        context = {'users': result['users']}
        return render(request, 'admin_users.html', context)
    else:
        messages.error(request, 'Could not load users.')
        return redirect('hos')

def delete_user(request, user_id):
    """Delete a user (admin function)."""
    if not request.session.get('is_logged_in'):
        messages.error(request, 'Please login to access this page.')
        return redirect('login')
    
    # In a real application, you'd check for admin privileges
    result = csv_manager.delete_user(user_id)
    
    if result['success']:
        messages.success(request, 'User deleted successfully.')
    else:
        messages.error(request, result['message'])
    
    return redirect('admin_users')
