from django.shortcuts import render

def home_view(request):
    # Updated template path
    return render(request, 'home.html', {})

def dashboard_view(request):
    # Add any logic to gather data for the dashboard here
    context = {}  # For now, we'll use an empty context
    return render(request, 'Property_Dashboard_app/dashboard.html', context)

def financial_modelling_view(request):
    # Add any logic to gather data for the dashboard here
    context = {}  # For now, we'll use an empty context
    return render(request, 'Property_Dashboard_app/financial_modelling.html', context)

def property_deepdive_view(request):
    # Add any logic to gather data for the dashboard here
    context = {}  # For now, we'll use an empty context
    return render(request, 'Property_Dashboard_app/property_deepdive.html', context)

def tenancy_schedule_view(request):
    # Add any logic to gather data for the dashboard here
    context = {}  # For now, we'll use an empty context
    return render(request, 'Property_Dashboard_app/tenancy_schedule.html', context)

def portfolio_performance_view(request):
    # Add any logic to gather data for the dashboard here
    context = {}  # For now, we'll use an empty context
    return render(request, 'Property_Dashboard_app/portfolio_performance.html', context)

def debt_view(request):
    # Add any logic to gather data for the dashboard here
    context = {}  # For now, we'll use an empty context
    return render(request, 'Property_Dashboard_app/debt.html', context)

def income_and_expenses_view(request):
    # Add any logic to gather data for the dashboard here
    context = {}  # For now, we'll use an empty context
    return render(request, 'Property_Dashboard_app/income_and_expenses.html', context)

def artificial_intelligence_view(request):
    # Add any logic to gather data for the dashboard here
    context = {}  # For now, we'll use an empty context
    return render(request, 'Property_Dashboard_app/artificial_intelligence.html', context)

def forecasting_view(request):
    # Add any logic to gather data for the dashboard here
    context = {}  # For now, we'll use an empty context
    return render(request, 'Property_Dashboard_app/forecasting.html', context)
