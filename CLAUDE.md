# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Django-based Property Dashboard application called "Capital Compass" - a comprehensive real estate portfolio management system. The application provides detailed analytics, financial modeling, and reporting capabilities for property investment management.

## Core Technology Stack

- **Backend**: Django 5.0.2 (Python web framework)
- **Frontend**: HTML templates with Chart.js for data visualization
- **Database**: SQLite (default Django database)
- **Styling**: Custom CSS with dark theme
- **Charts**: Chart.js for interactive visualizations
- **Icons**: Google Material Symbols

## Development Commands

```bash
# Set up virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Database operations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver

# Collect static files (for production)
python manage.py collectstatic

# Import CSV data (custom command)
python manage.py import_csv_data
```

## Project Structure

```
Property_Dashboard/
├── Property_Dashboard/          # Django project settings
│   ├── settings.py             # Main settings file
│   ├── urls.py                 # Root URL configuration
│   └── wsgi.py                 # WSGI configuration
├── Property_Dashboard_app/      # Main Django app
│   ├── models.py               # Database models
│   ├── views.py                # View functions
│   ├── urls.py                 # App URL patterns
│   ├── templates/              # HTML templates
│   │   ├── base.html           # Base template with navigation
│   │   ├── dashboard.html      # Main dashboard
│   │   ├── debt.html           # Debt management page
│   │   ├── financial_modelling.html
│   │   ├── portfolio_performance.html
│   │   ├── property_deepdive.html
│   │   ├── tenancy_schedule.html
│   │   ├── income_and_expenses.html
│   │   ├── forecasting.html
│   │   └── artificial_intelligence.html
│   ├── management/commands/    # Custom Django commands
│   │   └── import_csv_data.py  # CSV data import utility
│   └── migrations/             # Database migrations
├── static/
│   ├── css/
│   │   └── styles.css          # Main stylesheet
│   └── js/
│       └── dashboard.js        # Dashboard JavaScript
├── db.sqlite3                  # SQLite database
├── manage.py                   # Django management script
└── requirements.txt            # Python dependencies
```

## Key Features & Pages

### Navigation Structure (from base.html)
- **Dashboard**: Main overview with metrics, charts, and property listings
- **Portfolio Performance**: Performance analytics and reporting
- **Property Deep Dive**: Detailed property analysis
- **Tenancy Schedule**: Lease management and tenant information
- **Financial Modelling**: Financial analysis and projections
- **Debt Management**: Debt tracking and maturity analysis
- **Income & Expenses**: Revenue and cost management
- **Forecasting**: Predictive analytics
- **AI Insights**: Artificial intelligence features

### Dashboard Features
- **Key Metrics**: Properties, Square Footage, Tenants, Occupancy, Income, Yield, Valuation, Capex, Interest
- **Sector Allocation**: Interactive pie chart showing property type distribution
- **Property Rankings**: Top 5 properties by valuation
- **Tenant Analysis**: Top 5 tenants by income with credit ratings
- **Lease Expiry Chart**: Bar chart showing lease expiration timeline
- **Debt Maturity Chart**: Visualization of debt payment schedule

## Database Models

The application includes models for:
- Properties (with valuation, square footage, etc.)
- Tenants (with rental income and credit information)
- Operating Expenses
- Financial metrics and calculations

## Styling & UI

- **Theme**: Dark theme with professional color scheme
- **Typography**: Inter font family for clean, modern appearance
- **Icons**: Google Material Symbols for consistent iconography
- **Layout**: Sidebar navigation with responsive design
- **Charts**: Chart.js with dark theme configuration

## Data Management

- **CSV Import**: Custom management command for importing property data
- **Database**: SQLite for development (easily switchable to PostgreSQL/MySQL for production)
- **Migrations**: Standard Django migration system for database schema changes

## Development Guidelines

### Adding New Features
1. Create new views in `Property_Dashboard_app/views.py`
2. Add URL patterns in `Property_Dashboard_app/urls.py`
3. Create corresponding HTML templates in `templates/`
4. Update navigation in `base.html` if needed

### Database Changes
1. Modify models in `models.py`
2. Run `python manage.py makemigrations`
3. Run `python manage.py migrate`

### Static Files
- CSS modifications go in `static/css/styles.css`
- JavaScript files in `static/js/`
- Use `{% load static %}` in templates
- Use `{% static 'path/to/file' %}` for static file references

## Chart.js Integration

The dashboard uses Chart.js for data visualization with:
- Dark theme configuration
- Responsive design
- Interactive hover effects
- Custom color schemes for different chart types

## Current Status

The application appears to be in active development with:
- Basic structure and navigation implemented
- Main dashboard with working charts and metrics
- Multiple page templates created
- Database models defined
- Custom data import functionality

Most feature pages currently show placeholder content and need implementation.

## Common Development Tasks

- To add new dashboard widgets, modify `dashboard.html` and update corresponding view
- To add new navigation items, update `base.html` sidebar navigation
- To modify chart data, update the chart configuration in JavaScript blocks
- To add new database fields, modify models and create migrations
- To import data, use the custom management command or create new import scripts