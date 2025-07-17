# Capital Compass Property Dashboard - User Guide

## 🚀 How to Start the Dashboard

### Method 1: Reliable Startup Script (Recommended)
```bash
cd /Users/teddyjames/Desktop/Property_Dashboard
./start_dashboard_reliable.sh
```

### Method 2: Manual Background Start
```bash
cd /Users/teddyjames/Desktop/Property_Dashboard
nohup python3 manage.py runserver 127.0.0.1:8000 > server.log 2>&1 &
```

### Method 3: Manual Foreground Start
```bash
cd /Users/teddyjames/Desktop/Property_Dashboard
python3 manage.py runserver 127.0.0.1:8000
```

## 📱 Dashboard URLs

Once the server is running, access these URLs:

- **Main Dashboard**: http://127.0.0.1:8000/dashboard/
- **Portfolio Performance**: http://127.0.0.1:8000/portfolio_performance/
- **Property Deep Dive**: http://127.0.0.1:8000/property_deepdive/
- **Tenancy Schedule**: http://127.0.0.1:8000/tenancy_schedule/
- **Financial Modelling**: http://127.0.0.1:8000/financial_modelling/
- **Debt Management**: http://127.0.0.1:8000/debt/
- **Income & Expenses**: http://127.0.0.1:8000/income_and_expenses/
- **Forecasting**: http://127.0.0.1:8000/forecasting/

## 🔧 Server Management

### Check if Server is Running
```bash
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8000/dashboard/
# Should return: 200
```

### View Server Logs
```bash
tail -f server.log
```

### Stop the Server
```bash
pkill -f "python3 manage.py runserver"
```

### Check Server Process
```bash
ps aux | grep "python3 manage.py runserver"
```

## 🗃️ Database Management

### Run Migrations
```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

### Import Data (if needed)
```bash
python3 manage.py import_csv_data
```

## 🎯 Troubleshooting

### If Dashboard Won't Load
1. Check if server is running: `curl -I http://127.0.0.1:8000/dashboard/`
2. Check server logs: `tail -f server.log`
3. Restart server: `./start_dashboard_reliable.sh`

### If Server Keeps Stopping
- Use the background method: `nohup python3 manage.py runserver 127.0.0.1:8000 > server.log 2>&1 &`
- Check for errors in `server.log`

### If Port 8000 is Busy
```bash
# Find process using port 8000
lsof -i :8000

# Kill process if needed
pkill -f "python3 manage.py runserver"
```

## 💾 Saving Your Work

### Commit Changes
```bash
git add .
git commit -m "Your changes description"
```

### Push to Remote (if configured)
```bash
git push origin templates
```

## 🏗️ Project Structure

```
Property_Dashboard/
├── Property_Dashboard/          # Django settings
├── Property_Dashboard_app/      # Main application
│   ├── templates/              # HTML templates
│   ├── models.py               # Database models
│   ├── views.py                # Application logic
│   └── urls.py                 # URL routing
├── static/                     # CSS, JS, images
├── db.sqlite3                  # Database
├── manage.py                   # Django management
├── requirements.txt            # Python dependencies
├── server.log                  # Server logs
├── start_dashboard_reliable.sh # Startup script
└── CLAUDE.md                   # Development guide
```

## 🎨 Features

### Working Dashboard Sections
- ✅ **Dashboard**: Main overview with charts and metrics
- ✅ **Portfolio Performance**: Performance analytics
- ✅ **Property Deep Dive**: Detailed property analysis
- ✅ **Tenancy Schedule**: Lease management
- ✅ **Financial Modelling**: Financial projections
- ✅ **Debt Management**: Debt tracking
- ✅ **Income & Expenses**: Revenue management
- ✅ **Forecasting**: Predictive analytics

### Technical Features
- Dark theme UI with professional styling
- Interactive Chart.js visualizations
- Responsive design with sidebar navigation
- SQLite database with Django ORM
- Custom management commands
- Material Design icons

## 🔮 Future Development

To add new features:
1. Modify templates in `Property_Dashboard_app/templates/`
2. Update views in `Property_Dashboard_app/views.py`
3. Add URL patterns in `Property_Dashboard_app/urls.py`
4. Update models in `Property_Dashboard_app/models.py` if needed
5. Run migrations: `python3 manage.py makemigrations && python3 manage.py migrate`

---

**Last Updated**: July 17, 2025
**Status**: ✅ Fully Working
**Server Method**: Background with nohup (tested reliable)