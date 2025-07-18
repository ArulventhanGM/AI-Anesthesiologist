
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.http import HttpResponse

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
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user=user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('hos')
            else:
                messages.error(request, 'Invalid username or password. Please try again.')
                return render(request,'login.html')
        except User.DoesNotExist:
            messages.error(request, 'User does not exist. Please check your username or sign up.')
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
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user=user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('hos')
            else:
                messages.error(request, 'Invalid username or password. Please try again.')
                return render(request,'login.html')
        except User.DoesNotExist:
            messages.error(request, 'User does not exist. Please check your username or sign up.')
            return render(request,'login.html')
        except Exception as e:
            messages.error(request, f'Login error: {str(e)}')
            return render(request,'login.html')
    else:
        return render(request,'login.html')

def hospital(request):
    return render(request, 'hospital.html') 

def prediction(request):
    return prediction(request,'prediction.html')    
def out(request):
    logout(request)
    return redirect('login')       

def signup(request):
    
    if request.POST:
        hospital_name = ex_data(request,"hospital_name")
        hospital_id = ex_data(request,"hospital_id")
        license_id = ex_data(request,"license_id")
        email_id = ex_data(request,"email_id")
        
        # Check if user already exists
        if User.objects.filter(username=hospital_name).exists():
            messages.error(request, f'Hospital with name "{hospital_name}" already exists. Please choose a different name.')
            return render(request,'signup.html')
        
        if User.objects.filter(email=email_id).exists():
            messages.error(request, f'Email "{email_id}" is already registered. Please use a different email.')
            return render(request,'signup.html')
        
        try:
            user = User(username=hospital_name, email=email_id, first_name=hospital_id)
            user.set_password(license_id)
            user.save()
            messages.success(request, f'Account created successfully! You can now login with Hospital Name: {hospital_name}')
            return redirect('login')
        except Exception as e:
            messages.error(request, f'Error creating account: {str(e)}')
            return render(request,'signup.html')
    return render(request,'signup.html')    
