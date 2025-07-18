"""
Deployment Guide for CSV-based User Management System

This guide covers production deployment considerations for the CSV user management system.
"""

# deployment_guide.py

import os
import stat
import shutil
from pathlib import Path
from datetime import datetime

class DeploymentHelper:
    """Helper class for deployment tasks."""
    
    def __init__(self, app_dir: str):
        self.app_dir = Path(app_dir)
        self.data_dir = self.app_dir / 'data'
        self.backups_dir = self.data_dir / 'backups'
        self.logs_dir = self.app_dir / 'logs'
    
    def setup_directories(self):
        """Create necessary directories with proper permissions."""
        directories = [
            self.data_dir,
            self.backups_dir,
            self.logs_dir
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            
            # Set directory permissions (readable/writable by owner only)
            os.chmod(directory, stat.S_IRWXU)
            
            print(f"Created directory: {directory}")
    
    def setup_csv_file(self, csv_filename: str = 'users.csv'):
        """Initialize CSV file with proper permissions."""
        csv_path = self.data_dir / csv_filename
        
        if not csv_path.exists():
            # Create the file with headers
            headers = [
                'id', 'username', 'email', 'password_hash', 'salt',
                'hospital_name', 'hospital_id', 'license_id', 
                'created_at', 'updated_at', 'is_active'
            ]
            
            with open(csv_path, 'w', newline='', encoding='utf-8') as file:
                import csv
                writer = csv.writer(file)
                writer.writerow(headers)
            
            print(f"Created CSV file: {csv_path}")
        
        # Set file permissions (readable/writable by owner only)
        os.chmod(csv_path, stat.S_IRUSR | stat.S_IWUSR)
        
        return csv_path
    
    def create_systemd_service(self, app_name: str, user: str, working_dir: str, 
                             exec_start: str, port: int = 8000):
        """Create a systemd service file for the application."""
        service_content = f"""[Unit]
Description={app_name} Web Application
After=network.target

[Service]
Type=simple
User={user}
WorkingDirectory={working_dir}
ExecStart={exec_start}
Restart=always
RestartSec=10
Environment=PORT={port}
Environment=PYTHONUNBUFFERED=1

# Security settings
NoNewPrivileges=yes
PrivateTmp=yes
ProtectSystem=strict
ProtectHome=yes
ReadWritePaths={working_dir}
CapabilityBoundingSet=CAP_NET_BIND_SERVICE
AmbientCapabilities=CAP_NET_BIND_SERVICE

[Install]
WantedBy=multi-user.target
"""
        
        service_path = f"/etc/systemd/system/{app_name}.service"
        
        print(f"Systemd service file content:")
        print(service_content)
        print(f"\nTo install, run as root:")
        print(f"sudo tee {service_path} > /dev/null << 'EOF'")
        print(service_content)
        print("EOF")
        print(f"sudo systemctl daemon-reload")
        print(f"sudo systemctl enable {app_name}")
        print(f"sudo systemctl start {app_name}")
        
        return service_content
    
    def create_nginx_config(self, app_name: str, domain: str, port: int = 8000):
        """Create nginx configuration for the application."""
        nginx_config = f"""server {{
    listen 80;
    server_name {domain};
    
    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}}

server {{
    listen 443 ssl http2;
    server_name {domain};
    
    # SSL Configuration (you need to obtain SSL certificates)
    ssl_certificate /etc/ssl/certs/{domain}.crt;
    ssl_certificate_key /etc/ssl/private/{domain}.key;
    
    # Security headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    
    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 10240;
    gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;
    
    # Static files
    location /static/ {{
        alias /path/to/your/static/files/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }}
    
    # Main application
    location / {{
        proxy_pass http://127.0.0.1:{port};
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }}
    
    # Health check endpoint
    location /health {{
        proxy_pass http://127.0.0.1:{port}/health;
        access_log off;
    }}
}}
"""
        
        print(f"Nginx configuration for {app_name}:")
        print(nginx_config)
        print(f"\nTo install, save to /etc/nginx/sites-available/{app_name}")
        print(f"Then create symlink: sudo ln -s /etc/nginx/sites-available/{app_name} /etc/nginx/sites-enabled/")
        print(f"Test config: sudo nginx -t")
        print(f"Reload nginx: sudo systemctl reload nginx")
        
        return nginx_config
    
    def setup_log_rotation(self, app_name: str):
        """Create logrotate configuration."""
        logrotate_config = f"""{self.logs_dir}/*.log {{
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    create 0644 {os.getenv('USER', 'www-data')} {os.getenv('USER', 'www-data')}
    postrotate
        systemctl reload {app_name} > /dev/null 2>&1 || true
    endscript
}}
"""
        
        print(f"Logrotate configuration:")
        print(logrotate_config)
        print(f"\nTo install, save to /etc/logrotate.d/{app_name}")
        
        return logrotate_config
    
    def create_backup_script(self, app_name: str):
        """Create a backup script for the CSV data."""
        backup_script = f"""#!/bin/bash
# Backup script for {app_name}

set -e

# Configuration
APP_NAME="{app_name}"
DATA_DIR="{self.data_dir}"
BACKUP_DIR="{self.backups_dir}"
REMOTE_BACKUP_DIR="/path/to/remote/backups"  # Change this
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup filename
BACKUP_FILE="${{APP_NAME}}_backup_${{DATE}}.tar.gz"

echo "Starting backup for ${{APP_NAME}} at $(date)"

# Create local backup
cd "${{DATA_DIR}}"
tar -czf "${{BACKUP_DIR}}/${{BACKUP_FILE}}" users.csv

# Verify backup
if [ -f "${{BACKUP_DIR}}/${{BACKUP_FILE}}" ]; then
    echo "Local backup created: ${{BACKUP_DIR}}/${{BACKUP_FILE}}"
    
    # Copy to remote location (uncomment and configure as needed)
    # rsync -avz "${{BACKUP_DIR}}/${{BACKUP_FILE}}" "${{REMOTE_BACKUP_DIR}}/"
    # echo "Backup copied to remote location"
    
    # Clean up old backups (keep last 30 days)
    find "${{BACKUP_DIR}}" -name "${{APP_NAME}}_backup_*.tar.gz" -mtime +30 -delete
    echo "Old backups cleaned up"
else
    echo "ERROR: Backup failed!" >&2
    exit 1
fi

echo "Backup completed successfully at $(date)"
"""
        
        backup_script_path = self.app_dir / 'backup.sh'
        
        with open(backup_script_path, 'w') as f:
            f.write(backup_script)
        
        # Make executable
        os.chmod(backup_script_path, stat.S_IRWXU)
        
        print(f"Backup script created: {backup_script_path}")
        print(f"To run daily, add to crontab:")
        print(f"0 2 * * * {backup_script_path}")
        
        return backup_script_path
    
    def create_monitoring_script(self, app_name: str, port: int = 8000):
        """Create a monitoring script."""
        monitoring_script = f"""#!/bin/bash
# Monitoring script for {app_name}

set -e

APP_NAME="{app_name}"
PORT={port}
LOG_FILE="{self.logs_dir}/monitoring.log"
PID_FILE="/var/run/{app_name}.pid"

# Function to log messages
log_message() {{
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
}}

# Check if application is running
check_app() {{
    if curl -f -s http://localhost:$PORT/health > /dev/null 2>&1; then
        log_message "Application is running normally"
        return 0
    else
        log_message "ERROR: Application is not responding"
        return 1
    fi
}}

# Check disk space
check_disk_space() {{
    USAGE=$(df {self.data_dir} | tail -1 | awk '{{print $5}}' | sed 's/%//')
    if [ "$USAGE" -gt 90 ]; then
        log_message "WARNING: Disk usage is ${{USAGE}}%"
        return 1
    else
        log_message "Disk usage is normal (${{USAGE}}%)"
        return 0
    fi
}}

# Check CSV file integrity
check_csv_integrity() {{
    CSV_FILE="{self.data_dir}/users.csv"
    if [ -f "$CSV_FILE" ]; then
        # Check if file is readable and has header
        if head -1 "$CSV_FILE" | grep -q "id,username,email"; then
            log_message "CSV file integrity check passed"
            return 0
        else
            log_message "ERROR: CSV file appears to be corrupted"
            return 1
        fi
    else
        log_message "ERROR: CSV file not found"
        return 1
    fi
}}

# Main monitoring function
main() {{
    log_message "Starting monitoring check"
    
    ERRORS=0
    
    if ! check_app; then
        ERRORS=$((ERRORS + 1))
    fi
    
    if ! check_disk_space; then
        ERRORS=$((ERRORS + 1))
    fi
    
    if ! check_csv_integrity; then
        ERRORS=$((ERRORS + 1))
    fi
    
    if [ $ERRORS -eq 0 ]; then
        log_message "All checks passed"
    else
        log_message "Monitoring found $ERRORS issues"
        # Send alert (configure as needed)
        # mail -s "Alert: $APP_NAME monitoring issues" admin@example.com < "$LOG_FILE"
    fi
}}

# Run monitoring
main
"""
        
        monitoring_script_path = self.app_dir / 'monitor.sh'
        
        with open(monitoring_script_path, 'w') as f:
            f.write(monitoring_script)
        
        # Make executable
        os.chmod(monitoring_script_path, stat.S_IRWXU)
        
        print(f"Monitoring script created: {monitoring_script_path}")
        print(f"To run every 5 minutes, add to crontab:")
        print(f"*/5 * * * * {monitoring_script_path}")
        
        return monitoring_script_path

def main():
    """Main deployment setup function."""
    print("=== CSV User Management System Deployment Setup ===\n")
    
    # Get deployment parameters
    app_dir = input("Enter application directory path: ").strip()
    if not app_dir:
        app_dir = "/opt/csv-user-app"
    
    app_name = input("Enter application name (default: csv-user-app): ").strip()
    if not app_name:
        app_name = "csv-user-app"
    
    user = input("Enter system user (default: www-data): ").strip()
    if not user:
        user = "www-data"
    
    domain = input("Enter domain name (default: localhost): ").strip()
    if not domain:
        domain = "localhost"
    
    port = input("Enter port number (default: 8000): ").strip()
    if not port:
        port = 8000
    else:
        port = int(port)
    
    # Initialize deployment helper
    helper = DeploymentHelper(app_dir)
    
    print(f"\nSetting up deployment for {app_name}...")
    print(f"Application directory: {app_dir}")
    print(f"Domain: {domain}")
    print(f"Port: {port}")
    print(f"User: {user}")
    
    # Setup directories
    print("\n1. Setting up directories...")
    helper.setup_directories()
    
    # Setup CSV file
    print("\n2. Setting up CSV file...")
    csv_path = helper.setup_csv_file()
    
    # Create systemd service
    print("\n3. Creating systemd service...")
    exec_start = f"/usr/bin/python3 {app_dir}/app.py"
    helper.create_systemd_service(app_name, user, app_dir, exec_start, port)
    
    # Create nginx config
    print("\n4. Creating nginx configuration...")
    helper.create_nginx_config(app_name, domain, port)
    
    # Setup log rotation
    print("\n5. Setting up log rotation...")
    helper.setup_log_rotation(app_name)
    
    # Create backup script
    print("\n6. Creating backup script...")
    helper.create_backup_script(app_name)
    
    # Create monitoring script
    print("\n7. Creating monitoring script...")
    helper.create_monitoring_script(app_name, port)
    
    # Final instructions
    print("\n=== Deployment Complete ===")
    print("\nNext steps:")
    print("1. Copy your application files to the app directory")
    print("2. Install the systemd service file")
    print("3. Configure nginx with the provided configuration")
    print("4. Set up SSL certificates for HTTPS")
    print("5. Add backup and monitoring scripts to crontab")
    print("6. Test the application thoroughly")
    
    print("\nSecurity considerations:")
    print("- Ensure CSV file has proper permissions (600)")
    print("- Use HTTPS in production")
    print("- Implement rate limiting")
    print("- Regular security updates")
    print("- Monitor application logs")
    print("- Set up proper firewall rules")

if __name__ == '__main__':
    main()
