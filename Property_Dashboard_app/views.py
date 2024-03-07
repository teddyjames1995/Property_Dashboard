from django.db.models import Sum, Count, Avg, F, FloatField
from django.db.models.functions import ExtractYear
from django.shortcuts import render
from .models import Property, Tenant, OperatingExpenses

def home_view(request):
    # Updated template path
    return render(request, 'home.html', {})

def dashboard_view(request):
    # Aggregate data for key portfolio facts
    total_properties = Property.objects.count()
    total_tenants = Tenant.objects.count()
    total_income = Tenant.objects.aggregate(total_rental_income=Sum('contracted_rent'))['total_rental_income'] or 0
    total_valuation = Property.objects.aggregate(total_valuation=Sum('valuation'))['total_valuation'] or 0
    total_sq_ft = Property.objects.aggregate(total_sq_ft=Sum('sq_ft'))['total_sq_ft'] or 0
    total_capex = Property.objects.aggregate(total_capex=Sum('capital_expenditure'))['total_capex'] or 0
    # Calculations for Occupancy by ERV, Yield, Debt LTV, and Interest
    # These are placeholders for your actual calculations. Replace with your own logic.
    total_occupancy_by_erv = Property.objects.filter(occupancy__gt=0).aggregate(avg_occupancy=Avg('occupancy'))['avg_occupancy'] or 0
    total_yield = Property.objects.aggregate(weighted_yield=Sum(F('yield') * F('valuation'), output_field=FloatField()) / Sum('valuation'))['weighted_yield'] or 0
    total_debt_ltv = Property.objects.aggregate(debt_ltv=Sum('total_debt') / Sum('valuation') * 100)['debt_ltv'] or 0
    total_interest = Property.objects.aggregate(weighted_interest=Sum(F('interest_percentage') * F('total_debt'), output_field=FloatField()) / Sum('total_debt'))['weighted_interest'] or 0


    # Get the top 5 properties by valuation
    top_properties_by_valuation = Property.objects.order_by('-valuation')[:5]

    # Get the top 5 tenants by rental income
    top_tenants_by_income = Tenant.objects.order_by('-contracted_rent')[:5]

    # Sector allocation for pie chart
    sector_allocation_valuation = Property.objects.values('sector').annotate(
    valuation_sum=Sum('valuation')
    ).order_by('-valuation_sum')


    # Pie chart data preparation
    pie_chart_data = [
        {'sector': sector['sector'], 'valuation': sector['valuation_sum']}
        for sector in sector_allocation_valuation
    ]

    # Lease expiry and breaks bar chart data
    # Adjust the logic according to your specific requirements
    lease_expiry_breakdown = Tenant.objects.annotate(
        year=ExtractYear('lease_end')
    ).values('year').annotate(
        count=Count('id')
    ).order_by('year')

    # Debt wall bar chart data
    # Adjust the logic according to your specific requirements
    debt_wall_breakdown = Property.objects.annotate(
        year=ExtractYear('debt_expiry_date')
    ).values('year').annotate(
        debt_sum=Sum('total_debt')
    ).order_by('year')

    # Prepare context data for rendering
    context = {
        'total_properties': total_properties,
        'total_tenants': total_tenants,
        'total_income': total_income,
        'total_valuation': total_valuation,
        'total_sq_ft': total_sq_ft,
        'total_occupancy_by_erv': total_occupancy_by_erv,
        'total_yield': total_yield,
        'total_capex': total_capex,
        'total_debt_ltv': total_debt_ltv,
        'total_interest': total_interest,
        'top_properties_by_valuation': top_properties_by_valuation,
        'top_tenants_by_income': top_tenants_by_income,
        'pie_chart_data': pie_chart_data,
        'lease_expiry_breakdown': lease_expiry_breakdown,
        'debt_wall_breakdown': debt_wall_breakdown,
        # Add more context data as needed...
    }
    return render(request, 'dashboard.html', context)

def financial_modelling_view(request):
    # Add any logic to gather data for the dashboard here
    context = {}  # For now, we'll use an empty context
    return render(request, 'financial_modelling.html', context)

def property_deepdive_view(request):
    # Add any logic to gather data for the dashboard here
    context = {}  # For now, we'll use an empty context
    return render(request, 'property_deepdive.html', context)

def tenancy_schedule_view(request):
    # Add any logic to gather data for the dashboard here
    context = {}  # For now, we'll use an empty context
    return render(request, 'tenancy_schedule.html', context)

def portfolio_performance_view(request):
    # Add any logic to gather data for the dashboard here
    context = {}  # For now, we'll use an empty context
    return render(request, 'portfolio_performance.html', context)

def debt_view(request):
    # Add any logic to gather data for the dashboard here
    context = {}  # For now, we'll use an empty context
    return render(request, 'debt.html', context)

def income_and_expenses_view(request):
    # Add any logic to gather data for the dashboard here
    context = {}  # For now, we'll use an empty context
    return render(request, 'income_and_expenses.html', context)

def artificial_intelligence_view(request):
    # Add any logic to gather data for the dashboard here
    context = {}  # For now, we'll use an empty context
    return render(request, 'artificial_intelligence.html', context)

def forecasting_view(request):
    # Add any logic to gather data for the dashboard here
    context = {}  # For now, we'll use an empty context
    return render(request, 'forecasting.html', context)
