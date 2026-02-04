#!/bin/bash

echo "📦 Packaging AFCON 2027 Project..."

# Create temp directory
mkdir -p afcon_project_deploy
cd afcon_project_deploy

# Copy project files
cp -r ../your-project-folder/* .
cp ../your-project-folder/.gitignore .

# Remove sensitive data
rm -f db.sqlite3
rm -rf __pycache__
rm -rf */__pycache__
rm -rf media/
rm -rf staticfiles/

# Create requirements.txt
pip freeze > requirements.txt

# Create setup instructions
cat > SETUP_GUIDE.md << 'SETUP'
# AFCON 2027 Hotel Management System - Setup Guide

## Quick Start:
1. Extract this folder
2. Open terminal in the folder
3. Run: python -m venv venv
4. Run: venv\Scripts\activate (Windows) OR source venv/bin/activate (Mac/Linux)
5. Run: pip install -r requirements.txt
6. Run: python manage.py migrate
7. Run: python manage.py createsuperuser
8. Run: python manage.py runserver
9. Open: http://localhost:8000

## Admin Access:
- Username: admin
- Password: admin123 (change after login)

## Features:
- Hotel Management
- Tourism Attractions
- Booking System
- AFCON 2027 Events
SETUP

# Create run script
cat > run_project.bat << 'BAT'
@echo off
echo Starting AFCON 2027 System...
venv\Scripts\activate
python manage.py runserver
pause
BAT

cat > run_project.sh << 'SH'
#!/bin/bash
echo "Starting AFCON 2027 System..."
source venv/bin/activate
python manage.py runserver
SH

# Make scripts executable (Linux/Mac)
chmod +x run_project.sh
chmod +x package_project.sh

# Create zip
cd ..
zip -r afcon_2027_project.zip afcon_project_deploy/

echo "✅ Project packaged: afcon_2027_project.zip"
echo "📁 Size:" $(du -sh afcon_2027_project.zip)
