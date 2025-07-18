#!/usr/bin/env python3
"""
Quick CSV viewer - Command line tool to quickly view CSV database
Usage: python quick_csv_view.py [csv_file_path]
"""

import sys
import os
import csv
from pathlib import Path

def quick_view(csv_file_path):
    """Quick view of CSV file with basic formatting."""
    
    if not os.path.exists(csv_file_path):
        print(f"❌ CSV file not found: {csv_file_path}")
        return False
    
    try:
        with open(csv_file_path, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            rows = list(reader)
            
            if not rows:
                print("📄 CSV file is empty or has no data rows")
                return True
            
            print(f"📊 CSV Database: {csv_file_path}")
            print(f"📁 File size: {os.path.getsize(csv_file_path)} bytes")
            print(f"👥 Total records: {len(rows)}")
            print("=" * 60)
            
            # Show first few records
            for i, row in enumerate(rows[:5], 1):
                print(f"\n🔹 Record {i}:")
                for key, value in row.items():
                    if key in ['password_hash', 'salt']:
                        value = '*' * 8  # Hide sensitive data
                    print(f"   {key}: {value}")
            
            if len(rows) > 5:
                print(f"\n... and {len(rows) - 5} more records")
            
            # Show statistics
            active_count = sum(1 for row in rows if row.get('is_active') == 'true')
            inactive_count = len(rows) - active_count
            
            print("\n📈 Statistics:")
            print(f"   ✅ Active users: {active_count}")
            print(f"   ❌ Inactive users: {inactive_count}")
            
            # Show unique hospitals
            hospitals = set(row.get('hospital_name', '').strip() for row in rows)
            hospitals.discard('')  # Remove empty strings
            
            if hospitals:
                print(f"   🏥 Unique hospitals: {len(hospitals)}")
                for hospital in sorted(hospitals):
                    print(f"      - {hospital}")
            
            return True
            
    except Exception as e:
        print(f"❌ Error reading CSV file: {e}")
        return False

def main():
    """Main function."""
    # Default CSV file paths to check
    default_paths = [
        'users.csv',
        'data/users.csv',
        'core/users.csv',
        'demo_users.csv',
        'flask_users.csv'
    ]
    
    # Check command line arguments
    if len(sys.argv) > 1:
        csv_file_path = sys.argv[1]
    else:
        # Find existing CSV file
        csv_file_path = None
        for path in default_paths:
            if os.path.exists(path):
                csv_file_path = path
                break
        
        if not csv_file_path:
            print("🔍 No CSV file found in default locations:")
            for path in default_paths:
                print(f"   - {path}")
            
            csv_file_path = input("\n📝 Enter CSV file path: ").strip()
            if not csv_file_path:
                print("❌ No file path provided")
                return
    
    # View the CSV file
    success = quick_view(csv_file_path)
    
    if success:
        print("\n✅ CSV file viewed successfully!")
        print(f"\n💡 Tips:")
        print(f"   - Use 'python csv_viewer.py' for more viewing options")
        print(f"   - Use 'python web_csv_viewer.py' for web interface")
        print(f"   - Use 'python demo_csv_manager.py' to test the system")
    else:
        print("\n❌ Failed to view CSV file")

if __name__ == '__main__':
    main()
