#!/usr/bin/env python
"""
Test script to simulate the login process and check session handling
"""
import os
import sys
import django
from django.test import Client
from django.conf import settings

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

def test_login_session():
    """Test the login process and session handling"""
    print("Testing Login Session...")
    print("=" * 50)
    
    # Create a test client
    client = Client()
    
    # Test data
    test_data = {
        'username': 'testuser123',
        'password': 'TestUser123'
    }
    
    print(f"Attempting login with username: {test_data['username']}")
    
    # Make a POST request to the login endpoint
    response = client.post('/', test_data)
    
    print(f"Response status code: {response.status_code}")
    print(f"Response redirect URL: {response.get('Location', 'No redirect')}")
    
    # Check if session was created
    session = client.session
    print(f"Session keys: {list(session.keys())}")
    
    if 'is_logged_in' in session:
        print("✓ Session created successfully!")
        print(f"   User ID: {session.get('user_id')}")
        print(f"   Username: {session.get('username')}")
        print(f"   Hospital: {session.get('hospital_name')}")
        print(f"   Logged in: {session.get('is_logged_in')}")
    else:
        print("✗ Session not created!")
        
    # Test access to hospital page
    print("\nTesting access to hospital page...")
    hospital_response = client.get('/hospital')
    print(f"Hospital page status: {hospital_response.status_code}")
    
    if hospital_response.status_code == 200:
        print("✓ Hospital page accessible!")
        # Check if the response contains the expected content
        content = hospital_response.content.decode('utf-8')
        if 'HOSPITAL DASHBOARD' in content:
            print("✓ Hospital dashboard loaded successfully!")
        else:
            print("✗ Hospital dashboard content not found!")
    else:
        print("✗ Hospital page not accessible!")
    
    print("\n" + "=" * 50)
    return True

if __name__ == "__main__":
    test_login_session()
