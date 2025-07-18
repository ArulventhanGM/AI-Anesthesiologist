# Anesthesia Drug Prediction System

## Project Overview

The Anesthesia Drug Prediction System is a web-based application designed to assist medical professionals in determining appropriate anesthesia drug dosages during different types of surgeries. The system utilizes patient-specific data to calculate recommended dosages, enhancing precision in anesthesia administration and improving patient safety during surgical procedures.

## Key Features

- **Hospital User Authentication**: Secure login system for hospital staff
- **Hospital Dashboard**: Centralized interface for accessing prediction tools
- **Multiple Surgery Type Support**: 
  - General Surgery Anesthesia Prediction
  - Spinal Surgery Anesthesia Prediction
  - Local Surgery Anesthesia Prediction
- **Patient-specific Dosage Calculation**: Considers factors like weight, age, medical history, and vital signs
- **Responsive Web Interface**: User-friendly design for seamless experience across devices

## Technology Stack

- **Backend**: Django (Python web framework)
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite
- **Authentication**: Django built-in authentication system

## Prerequisites

Before setting up the project, ensure you have the following installed:

1. Python (version 3.8+ recommended)
2. pip (Python package installer)
3. Git (optional, for cloning the repository)

## Setup and Installation Guide

### Step 1: Clone the Repository (or Download)

```bash
git clone https://github.com/yourusername/Anesthesia-Drug-Prediction-System.git
cd Anesthesia-Drug-Prediction-System
```

Alternatively, download and extract the ZIP file from the repository.

### Step 2: Create and Activate a Virtual Environment (Optional but Recommended)

#### For Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

#### For macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Required Dependencies

```bash
pip install django
```

### Step 4: Apply Database Migrations

```bash
python manage.py migrate
```

### Step 5: Create an Admin User (Optional)

```bash
python manage.py createsuperuser
```
Follow the prompts to create your admin username, email, and password.

### Step 6: Run the Development Server

```bash
python manage.py runserver
```

The server will start running at `http://127.0.0.1:8000/`

## Using the Application

1. **Access the Application**: Open your web browser and navigate to `http://127.0.0.1:8000/`

2. **Sign Up/Login**:
   - For first-time users, click on "SIGNUP" to register your hospital
   - Fill in required details (Hospital Name, Hospital ID, License ID, Email)
   - Once registered, use your Hospital Name as username and License ID as password to log in

3. **Navigate the Dashboard**:
   - After logging in, you'll be directed to the hospital dashboard
   - Click on "PREDICT NOW" to access prediction tools

4. **Select Surgery Type**:
   - Choose from "GENERAL SURGERY", "SPINAL SURGERY", or "LOCAL SURGERY"
   - Each option leads to a specialized prediction form

5. **Enter Patient Data**:
   - Fill in all required patient information:
     - Patient demographics (name, age, weight)
     - Doctor information
     - Surgery details
     - Vital signs (heart rate, blood pressure, respiration rate)
     - Medical history and current medications

6. **Get Prediction**:
   - Click "Predict" to receive anesthesia drug recommendations
   - The system will calculate appropriate drug dosages based on the input data

7. **Review Results**:
   - Review the recommended drugs and dosages
   - Use "Clear" to reset the form for a new prediction

## Project Structure

```
Anesthesia-Drug-Prediction-System/
├── manage.py                # Django management script
├── backend/                 # Project settings and configuration
│   ├── settings.py          # Django settings
│   ├── urls.py              # Project URL configuration
│   └── ...                  # Other Django files
├── core/                    # Main application
│   ├── views.py             # View functions
│   ├── models.py            # Database models
│   ├── urls.py              # App URL routing
│   └── static/              # Static files (CSS, JS, images)
│       ├── generalprediction.html
│       ├── localprediction.html
│       ├── spinalprediction.html
│       └── ...
├── static/                  # Global static files
│   └── ...
└── templates/               # HTML templates
    ├── hospital.html
    ├── index.html
    ├── login.html
    ├── prediction.html
    └── signup.html
```

## Troubleshooting

1. **Installation Issues**:
   - Ensure you have the correct Python version (3.8+)
   - Try upgrading pip: `python -m pip install --upgrade pip`

2. **Database Migration Errors**:
   - Delete the db.sqlite3 file and run migrations again
   - Ensure there are no syntax errors in models.py

3. **Server Won't Start**:
   - Check if another service is using port 8000
   - Try a different port: `python manage.py runserver 8080`

4. **Login Problems**:
   - Make sure you're using the correct credentials
   - Try resetting your password via the admin interface

## Development and Contribution

To contribute to this project:

1. Fork the repository
2. Create a new branch for your feature
3. Make your changes
4. Test thoroughly
5. Submit a pull request with a detailed description of your changes

## License

[Include appropriate license information here]

## Authors

- ELANESAN K
- PRITHEEVE D
- DEO ALESTER S
- ARUN KUMAR S
- KAAVIYA R

Students, Department of Artificial Intelligence and Machine Learning, KRCE-TRICHY