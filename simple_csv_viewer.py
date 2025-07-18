#!/usr/bin/env python3
"""
Simple CSV Database Viewer - No external dependencies
"""

import csv
import json
import os
from pathlib import Path

def view_csv_table(csv_file_path):
    """View CSV file in a formatted table."""
    print("\n" + "="*80)
    print("CSV DATABASE VIEWER")
    print("="*80)
    
    try:
        with open(csv_file_path, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            rows = list(reader)
            
            if not rows:
                print("No data found in CSV file.")
                return
            
            print(f"📊 File: {csv_file_path}")
            print(f"📁 Size: {os.path.getsize(csv_file_path)} bytes")
            print(f"👥 Records: {len(rows)}")
            print("-" * 80)
            
            # Display headers
            headers = rows[0].keys()
            print(f"{'ID':>3} | {'Username':<15} | {'Email':<25} | {'Hospital':<20} | {'Status':<8}")
            print("-" * 80)
            
            # Display rows
            for row in rows:
                status = "Active" if row.get('is_active') == 'true' else "Inactive"
                print(f"{row.get('id', ''):<3} | {row.get('username', ''):<15} | {row.get('email', ''):<25} | {row.get('hospital_name', ''):<20} | {status:<8}")
            
            print("-" * 80)
            
            # Statistics
            active_count = sum(1 for row in rows if row.get('is_active') == 'true')
            inactive_count = len(rows) - active_count
            
            print(f"📈 Statistics:")
            print(f"   ✅ Active users: {active_count}")
            print(f"   ❌ Inactive users: {inactive_count}")
            
            # Unique hospitals
            hospitals = set(row.get('hospital_name', '').strip() for row in rows)
            hospitals.discard('')
            
            if hospitals:
                print(f"   🏥 Hospitals: {len(hospitals)}")
                for hospital in sorted(hospitals):
                    print(f"      - {hospital}")
                    
    except FileNotFoundError:
        print(f"❌ CSV file not found: {csv_file_path}")
    except Exception as e:
        print(f"❌ Error reading CSV file: {e}")

def view_csv_raw(csv_file_path):
    """View raw CSV content."""
    print("\n" + "="*80)
    print("RAW CSV CONTENT")
    print("="*80)
    
    try:
        with open(csv_file_path, 'r', newline='', encoding='utf-8') as file:
            content = file.read()
            print(content)
    except FileNotFoundError:
        print(f"❌ CSV file not found: {csv_file_path}")
    except Exception as e:
        print(f"❌ Error reading CSV file: {e}")

def view_csv_json(csv_file_path):
    """View CSV as JSON."""
    print("\n" + "="*80)
    print("JSON FORMAT")
    print("="*80)
    
    try:
        with open(csv_file_path, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            rows = list(reader)
            
            # Remove sensitive data
            safe_rows = []
            for row in rows:
                safe_row = {k: v for k, v in row.items() 
                          if k not in ['password_hash', 'salt']}
                safe_rows.append(safe_row)
            
            print(json.dumps(safe_rows, indent=2))
            
    except FileNotFoundError:
        print(f"❌ CSV file not found: {csv_file_path}")
    except Exception as e:
        print(f"❌ Error reading CSV file: {e}")

def main():
    """Main function."""
    # Check for CSV file
    csv_paths = ['data/users.csv', 'users.csv', 'demo_users.csv', 'flask_users.csv']
    
    csv_file = None
    for path in csv_paths:
        if os.path.exists(path):
            csv_file = path
            break
    
    if not csv_file:
        print("❌ No CSV file found in default locations")
        return
    
    print("📋 CSV Database Viewer")
    print("Choose viewing option:")
    print("1. Table view")
    print("2. Raw CSV")
    print("3. JSON format")
    print("4. All formats")
    
    choice = input("Enter choice (1-4): ").strip()
    
    if choice == '1':
        view_csv_table(csv_file)
    elif choice == '2':
        view_csv_raw(csv_file)
    elif choice == '3':
        view_csv_json(csv_file)
    elif choice == '4':
        view_csv_table(csv_file)
        view_csv_raw(csv_file)
        view_csv_json(csv_file)
    else:
        print("❌ Invalid choice")

if __name__ == '__main__':
    main()
