#!/bin/bash

# Capital Compass Property Dashboard - Reliable Startup Script
# This script uses the tested working method to start the dashboard

echo "🏢 Capital Compass Property Dashboard - Reliable Start"
echo "====================================================="

# Navigate to the correct directory
cd /Users/teddyjames/Desktop/Property_Dashboard

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment not found. Creating one..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install dependencies if needed
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Run migrations
echo "🗃️  Running database migrations..."
python3 manage.py makemigrations --noinput
python3 manage.py migrate --noinput

# Kill any existing server on port 8000
echo "🔄 Stopping any existing server..."
pkill -f "python3 manage.py runserver"

# Start the server in background (tested working method)
echo "🚀 Starting Django server in background..."
nohup python3 manage.py runserver 127.0.0.1:8000 > server.log 2>&1 &

# Wait for server to start
echo "⏳ Waiting for server to start..."
sleep 3

# Test the server
echo "🧪 Testing server connection..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8000/dashboard/)

if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ Server started successfully!"
    echo "📱 Dashboard available at: http://127.0.0.1:8000/dashboard/"
    echo "📊 All sections working:"
    echo "   • Dashboard: http://127.0.0.1:8000/dashboard/"
    echo "   • Portfolio Performance: http://127.0.0.1:8000/portfolio_performance/"
    echo "   • Property Deep Dive: http://127.0.0.1:8000/property_deepdive/"
    echo "   • Tenancy Schedule: http://127.0.0.1:8000/tenancy_schedule/"
    echo "   • Financial Modelling: http://127.0.0.1:8000/financial_modelling/"
    echo "   • Debt Management: http://127.0.0.1:8000/debt/"
    echo "   • Income & Expenses: http://127.0.0.1:8000/income_and_expenses/"
    echo "   • Forecasting: http://127.0.0.1:8000/forecasting/"
    echo ""
    echo "📋 Server logs: tail -f server.log"
    echo "🛑 To stop server: pkill -f 'python3 manage.py runserver'"
else
    echo "❌ Server failed to start. Check server.log for details."
    tail -n 10 server.log
fi