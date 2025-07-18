
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.http import HttpResponse
from django.conf import settings
import os

# Import CSV User Manager
from .csv_user_manager import CSVUserManager

# Initialize CSV User Manager
csv_manager = CSVUserManager(
    csv_file_path=os.path.join(settings.BASE_DIR, 'data', 'users.csv'),
    backup_dir=os.path.join(settings.BASE_DIR, 'data', 'backups')
)

def ex_data(req,data):
    return req.POST.get(data,"")

def index(request):
    if request.POST:
        username = ex_data(request,"username")
        password = ex_data(request,"password")
        
        if not username or not password:
            messages.error(request, 'Please enter both username and password.')
            return render(request,'login.html')
        
        try:
            # Use CSV manager for authentication
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
                return render(request,'login.html')
                
        except Exception as e:
            messages.error(request, f'Login error: {str(e)}')
            return render(request,'login.html')
    else:
        return render(request,'login.html')

def go(request):
    if request.POST:
        username = ex_data(request,"username")
        password = ex_data(request,"password")
        
        if not username or not password:
            messages.error(request, 'Please enter both username and password.')
            return render(request,'login.html')
        
        try:
            # Use CSV manager for authentication
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
                return render(request,'login.html')
                
        except Exception as e:
            messages.error(request, f'Login error: {str(e)}')
            return render(request,'login.html')
    else:
        return render(request,'login.html')

def hospital(request):
    if not request.session.get('is_logged_in'):
        messages.error(request, 'Please login to access this page.')
        return redirect('login')
    
    return render(request, 'hospital.html') 

def prediction(request):
    if not request.session.get('is_logged_in'):
        messages.error(request, 'Please login to access this page.')
        return redirect('login')
    
    return render(request,'prediction.html')    

def out(request):
    # Clear session data
    request.session.flush()
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')       

def signup(request):
    if request.POST:
        # Get form data
        hospital_name = ex_data(request,"hospital_name").strip()
        hospital_id = ex_data(request,"hospital_id").strip()
        username = ex_data(request,"username").strip()
        license_id = ex_data(request,"license_id").strip()
        email_id = ex_data(request,"email_id").strip().lower()
        
        # Enhanced validation
        errors = []
        
        # Check required fields
        if not hospital_name:
            errors.append('Hospital name is required.')
        elif len(hospital_name) < 3:
            errors.append('Hospital name must be at least 3 characters long.')
            
        if not hospital_id:
            errors.append('Hospital ID is required.')
        elif len(hospital_id) < 3:
            errors.append('Hospital ID must be at least 3 characters long.')
            
        if not username:
            errors.append('Username is required.')
        elif len(username) < 3:
            errors.append('Username must be at least 3 characters long.')
        elif not username.replace('_', '').isalnum():
            errors.append('Username can only contain letters, numbers, and underscores.')
            
        if not license_id:
            errors.append('License ID (password) is required.')
        elif len(license_id) < 8:
            errors.append('Password must be at least 8 characters long.')
        else:
            # Check password strength
            has_upper = any(c.isupper() for c in license_id)
            has_lower = any(c.islower() for c in license_id)
            has_digit = any(c.isdigit() for c in license_id)
            
            if not has_upper:
                errors.append('Password must contain at least one uppercase letter.')
            if not has_lower:
                errors.append('Password must contain at least one lowercase letter.')
            if not has_digit:
                errors.append('Password must contain at least one number.')
            
        if not email_id:
            errors.append('Email address is required.')
        elif '@' not in email_id or '.' not in email_id:
            errors.append('Please enter a valid email address.')
            
        # If there are validation errors, display them
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request,'signup.html')
        
        # Prepare user data for CSV manager
        user_data = {
            'username': username,
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
                    f'Account created successfully! Welcome {username}. You can now login with your username and password.')
                return redirect('login')
            else:
                # Display validation errors from CSV manager
                for error in result.get('errors', []):
                    messages.error(request, error)
                return render(request,'signup.html')
                
        except Exception as e:
            messages.error(request, f'Error creating account: {str(e)}')
            return render(request,'signup.html')
    
    return render(request,'signup.html')    
