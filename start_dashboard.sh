#!/bin/bash

# Capital Compass Property Dashboard Startup Script
# This script helps you easily start the Django development server

echo "🏢 Capital Compass Property Dashboard"
echo "======================================"

# Navigate to the correct directory
cd /Users/teddyjames/Desktop/Property_Dashboard

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment not found. Creating one..."
    python -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install dependencies if needed
echo "📦 Checking dependencies..."
pip install -r requirements.txt

# Run migrations if needed
echo "🗃️  Applying database migrations..."
python manage.py makemigrations
python manage.py migrate

# Start the development server
echo "🚀 Starting Django development server..."
echo "📱 Dashboard will be available at: http://127.0.0.1:8000/dashboard/"
echo "⏹️  Press Ctrl+C to stop the server"
echo ""

python manage.py runserver