from django.shortcuts import render
from django.core.serializers.json import DjangoJSONEncoder
import json
from .models import Property, Tenant, OperatingExpenses
from django.core.mail import send_mail
from django.db.models import Sum, Count, Avg, F, ExpressionWrapper, DecimalField
from datetime import datetime, timedelta
import locale

# Set locale for currency formatting
locale.setlocale(locale.LC_ALL, 'en_GB.UTF-8')

def format_currency(value):
    if value < 0:
        return f"[Red](£{abs(value):,.0f})"
    else:
        return f"£{value:,.0f}"

def format_number(value):
    if value < 0:
        return f"[Red]({abs(value):,})"
    else:
        return f"{value:,}"

# Reminder Logic Function
def send_reminder_email(tenant):
    if tenant.property:
        if hasattr(tenant, 'email') and tenant.email:  # Ensure tenant has an email field and it's not empty
            message = (
                f'This is a reminder that tenant {tenant.tenant_name} in property {tenant.property.title} '
                'is approaching a critical lease date (lease expiry or break option).'
            )
            # Code to send email goes here, if you have a valid email
        else:
            print(f'Tenant {tenant.tenant_name} does not have an email address.')
    else:
        print(f'Tenant {tenant.tenant_name} has no associated property.')

# Function to check for reminders and send email notifications
def check_for_reminders():
    today = datetime.now().date()
    six_months_from_today = today + timedelta(days=180)

    tenants = Tenant.objects.filter(lease_end__lte=six_months_from_today)  # Assuming Tenant model has a 'lease_end' field

    for tenant in tenants:
        send_reminder_email(tenant)

# Dashboard View
def dashboard_view(request):
    # Check for reminders whenever the dashboard is accessed
    check_for_reminders()

    # Aggregate data for key portfolio facts
    total_properties_value = Property.objects.count()
    total_tenants_value = Tenant.objects.count()
    total_income_value = Tenant.objects.aggregate(total_rental_income=Sum('contracted_rent'))['total_rental_income'] or 0
    total_valuation_value = Property.objects.aggregate(total_valuation=Sum('valuation'))['total_valuation'] or 0
    total_sq_ft_value = Property.objects.aggregate(total_sq_ft=Sum('sq_ft'))['total_sq_ft'] or 0
    total_capex = Property.objects.aggregate(total_capex=Sum('capital_expenditure'))['total_capex'] or 0
    total_occupancy_by_erv = Property.objects.filter(occupancy__gt=0).aggregate(avg_occupancy=Avg('occupancy'))['avg_occupancy'] or 0

    total_yield = (total_income_value / total_valuation_value) * 100 if total_valuation_value > 0 else 0
    total_debt_ltv = Property.objects.aggregate(debt_ltv=Sum('total_debt') / Sum('valuation') * 100)['debt_ltv'] or 0
    total_interest = Property.objects.annotate(
        weighted_interest_part=ExpressionWrapper(
            F('interest_percentage') * F('total_debt'), 
            output_field=DecimalField()
        )
    ).aggregate(
        weighted_interest=Sum('weighted_interest_part', output_field=DecimalField()) / Sum('total_debt', output_field=DecimalField())
    )['weighted_interest'] or 0

    total_properties = format_number(total_properties_value)
    total_tenants = format_number(total_tenants_value)
    total_sq_ft = format_number(total_sq_ft_value)
    total_yield = "{:.2f}".format(total_yield)
    total_occupancy_by_erv = "{:.1f}".format(total_occupancy_by_erv)
    total_debt_ltv = "{:.1f}".format(total_debt_ltv)
    total_interest = "{:.2f}".format(total_interest)

    total_valuation = format_currency(total_valuation_value)
    total_income = format_currency(total_income_value)

    top_properties_by_valuation = Property.objects.order_by('-valuation')[:5]
    top_properties = []
    for property in top_properties_by_valuation:
        property_percentage = (property.valuation / total_valuation_value) * 100 if total_valuation_value > 0 else 0
        top_properties.append({
            'id': property.id,
            'name': property.title,
            'valuation': format_currency(property.valuation),
            'percentage': "{:.1f}".format(property_percentage)
        })

    total_rental_income = Tenant.objects.aggregate(total_rent=Sum('contracted_rent'))['total_rent'] or 0
    top_tenants_by_income = Tenant.objects.order_by('-contracted_rent')[:5]
    top_tenants = []
    for tenant in top_tenants_by_income:
        tenant_percentage = (tenant.contracted_rent / total_rental_income) * 100 if total_rental_income > 0 else 0
        top_tenants.append({
            'id': tenant.id,
            'tenant_name': tenant.tenant_name,
            'total_rent': format_currency(tenant.contracted_rent),
            'percentage': "{:.1f}".format(tenant_percentage)
        })

    sector_allocation_valuation = Property.objects.values('sector').annotate(
        valuation_sum=Sum('valuation')
    ).order_by('-valuation_sum')

    pie_chart_data = [
        {'sector': sector['sector'], 'valuation': sector['valuation_sum']}
        for sector in sector_allocation_valuation
    ]

    lease_expiry_breakdown = Tenant.objects.values('year').annotate(
        count=Count('id')
    ).order_by('year')

    debt_wall_breakdown = Property.objects.values('year').annotate(
        debt_sum=Sum('total_debt')
    ).order_by('year')

    sector_allocation_data = {
        'labels': ['Industrial', 'Offices', 'Retail'],
        'data': [30, 25, 45],
        'backgroundColor': ['#FF6384', '#36A2EB', '#FFCE56'],
    }

    lease_expiry_data = {
        'labels': ['2024', '2025', '2026'],
        'data': [5, 10, 15],
    }

    debt_wall_data = {
        'labels': ['2024', '2025', '2026'],
        'data': [200000, 300000, 400000],
    }

    sector_allocation_data_json = json.dumps(sector_allocation_data, cls=DjangoJSONEncoder)
    lease_expiry_data_json = json.dumps(lease_expiry_data, cls=DjangoJSONEncoder)
    debt_wall_data_json = json.dumps(debt_wall_data, cls=DjangoJSONEncoder)

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
        'top_properties': top_properties,
        'top_tenants_by_income': top_tenants,
        'pie_chart_data': pie_chart_data,
        'lease_expiry_breakdown': lease_expiry_breakdown,
        'debt_wall_breakdown': debt_wall_breakdown,
        'sector_allocation_data_json': sector_allocation_data_json,
        'lease_expiry_data_json': lease_expiry_data_json,
        'debt_wall_data_json': debt_wall_data_json,
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
    # Get all properties with their tenants
    properties = Property.objects.all()[:5]  # Get all properties

    # Prepare data
    property_list = []
    for property in properties:
        tenants = Tenant.objects.filter(property=property)[:4]  # Use the 'property' ForeignKey to filter tenants
        property_data = {
            'name': property.title,  # Change based on your model field
            'tenants': tenants,
        }
        property_list.append(property_data)

    # Render the template
    context = {
        'properties': property_list,
    }
    return render(request, 'tenancy_schedule.html', context)

def portfolio_performance_view(request):
    # Add any logic to gather data for the dashboard here
    context = {}  # For now, we'll use an empty context
    return render(request, 'portfolio_performance.html', context)

def portfolio_report_view(request):
    # Add any logic to gather data for the report here
    from datetime import datetime
    context = {
        'current_date': datetime.now().strftime('%B %Y')
    }
    return render(request, 'portfolio_report.html', context)

def debt_view(request):
    # Add any logic to gather data for the dashboard here
    context = {}  # For now, we'll use an empty context
    return render(request, 'debt_dashboard.html', context)

def income_and_expenses_view(request):
    # Add any logic to gather data for the dashboard here
    context = {}  # For now, we'll use an empty context
    return render(request, 'income_expenses.html', context)

def artificial_intelligence_view(request):
    # Add any logic to gather data for the dashboard here
    context = {}  # For now, we'll use an empty context
    return render(request, 'artificial_intelligence.html', context)

def forecasting_view(request):
    # Add any logic to gather data for the dashboard here
    context = {}  # For now, we'll use an empty context
    return render(request, 'forecasting.html', context)

def login_view(request):
    # Basic login view function
    return render(request, 'login.html')  # Make sure you have a login.html template

def register_view(request):
    # Basic register view function
    return render(request, 'register.html')  # Make sure you have a register.html template

def home_view(request):
    return render(request, 'home.html', {})