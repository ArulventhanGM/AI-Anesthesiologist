# How to View Your CSV Database

## Overview
You now have several tools to view your CSV user database. Here are all the methods available:

## 1. Quick View (Recommended for daily use)
```bash
python quick_csv_view.py
```
- **Best for**: Quick daily checks
- **Shows**: Basic statistics and first few records
- **Features**: Automatic file detection, security-aware (hides passwords)

## 2. Simple Table View
```bash
python simple_csv_viewer.py
```
- **Best for**: Clean table display
- **Shows**: Formatted table with statistics
- **Features**: Multiple viewing formats (table, raw, JSON)

## 3. Comprehensive Viewer
```bash
python csv_viewer.py
```
- **Best for**: Detailed analysis
- **Shows**: Multiple formats with search functionality
- **Features**: Interactive mode, pandas integration (if available)

## 4. Web Interface
```bash
python web_csv_viewer.py
```
- **Best for**: Visual interface and sharing
- **Shows**: Web dashboard with statistics
- **Features**: Real-time updates, search, export options
- **Access**: http://localhost:5000

## 5. Direct File Access
You can also view the CSV file directly:

### Using any text editor:
```bash
notepad data/users.csv          # Windows
nano data/users.csv             # Linux/Mac
code data/users.csv             # VS Code
```

### Using command line:
```bash
# Windows
type data\users.csv

# Linux/Mac
cat data/users.csv
```

## 6. Using Python Built-in CSV Module
```python
import csv
with open('data/users.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        print(row)
```

## 7. Using Excel or Google Sheets
- Open the CSV file directly in Excel
- Import into Google Sheets
- Any spreadsheet application can read CSV files

## CSV File Structure
Your CSV file contains these columns:
- `id`: Unique user identifier
- `username`: Hospital username
- `email`: Contact email
- `password_hash`: Encrypted password (never visible)
- `salt`: Password salt (never visible)
- `hospital_name`: Full hospital name
- `hospital_id`: Hospital identifier
- `license_id`: Medical license ID
- `created_at`: Account creation timestamp
- `updated_at`: Last update timestamp
- `is_active`: Account status (true/false)

## Security Features
- Password hashes and salts are hidden in viewers
- Backup files are created automatically
- File permissions are set securely

## File Locations
The CSV viewers check these locations automatically:
1. `data/users.csv` (recommended)
2. `users.csv`
3. `demo_users.csv`
4. `flask_users.csv`
5. `core/users.csv`

## Tips for Daily Use

### Quick Check
```bash
python quick_csv_view.py
```

### Web Dashboard
```bash
python web_csv_viewer.py
# Then open http://localhost:5000 in your browser
```

### Search for Specific Users
```bash
python csv_viewer.py --interactive
# Then choose option 7 for search
```

### Export Data
- Use the web interface export feature
- Or simply copy the CSV file

## Troubleshooting

### File Not Found
```bash
# Check if file exists
ls data/users.csv     # Linux/Mac
dir data\users.csv    # Windows

# Create sample data
python demo_csv_manager.py
```

### Permission Errors
```bash
# Check file permissions
ls -l data/users.csv  # Linux/Mac

# Fix permissions if needed
chmod 600 data/users.csv
```

### Web Interface Issues
```bash
# Check if Flask is installed
pip install flask

# Use different port if 5000 is busy
python web_csv_viewer.py --port 8080
```

## Summary
- **Quick daily checks**: Use `quick_csv_view.py`
- **Detailed analysis**: Use `csv_viewer.py`
- **Web interface**: Use `web_csv_viewer.py`
- **Direct editing**: Use any text editor
- **Spreadsheet view**: Import into Excel/Google Sheets
