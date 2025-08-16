from django.shortcuts import render
from django.core.serializers.json import DjangoJSONEncoder
import json
from .models import Property, Tenant, OperatingExpenses
from django.core.mail import send_mail
from django.db.models import Sum, Count, Avg, F, ExpressionWrapper, DecimalField
from datetime import datetime, timedelta
import locale

# Set locale for currency formatting
try:
    locale.setlocale(locale.LC_ALL, 'en_GB.UTF-8')
except locale.Error:
    try:
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    except locale.Error:
        pass  # Use default locale if none work

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
    # check_for_reminders()  # Commented out to prevent BrokenPipeError

    # Aggregate data for key portfolio facts
    total_properties_value = Property.objects.count()
    total_tenants_value = Tenant.objects.count()
    total_income_value = Tenant.objects.aggregate(total_rental_income=Sum('contracted_rent'))['total_rental_income'] or 0
    total_valuation_value = Property.objects.aggregate(total_valuation=Sum('valuation'))['total_valuation'] or 0
    total_sq_ft_value = Property.objects.aggregate(total_sq_ft=Sum('sq_ft'))['total_sq_ft'] or 0
    total_capex = Property.objects.aggregate(total_capex=Sum('capital_expenditure'))['total_capex'] or 0
    total_occupancy_by_erv = Property.objects.filter(occupancy__gt=0).aggregate(avg_occupancy=Avg('occupancy'))['avg_occupancy'] or 0

    # Keep raw numeric values for portfolio analysis
    total_yield_raw = (total_income_value / total_valuation_value) * 100 if total_valuation_value > 0 else 0
    total_debt_ltv_raw = Property.objects.aggregate(debt_ltv=Sum('total_debt') / Sum('valuation') * 100)['debt_ltv'] or 0
    total_interest_raw = Property.objects.annotate(
        weighted_interest_part=ExpressionWrapper(
            F('interest_percentage') * F('total_debt'), 
            output_field=DecimalField()
        )
    ).aggregate(
        weighted_interest=Sum('weighted_interest_part', output_field=DecimalField()) / Sum('total_debt', output_field=DecimalField())
    )['weighted_interest'] or 0

    # Format for display
    total_properties = format_number(total_properties_value)
    total_tenants = format_number(total_tenants_value)
    total_sq_ft = format_number(total_sq_ft_value)
    total_yield = "{:.2f}".format(total_yield_raw)
    total_occupancy_by_erv = "{:.1f}".format(total_occupancy_by_erv)
    total_debt_ltv = "{:.1f}".format(total_debt_ltv_raw)
    total_interest = "{:.2f}".format(total_interest_raw)

    total_valuation = format_currency(total_valuation_value)
    total_income = format_currency(total_income_value)
    total_capex_formatted = format_currency(total_capex)

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

    # Generate sector allocation data from actual properties
    sector_allocation_valuation = Property.objects.values('sector').annotate(
        valuation_sum=Sum('valuation')
    ).order_by('-valuation_sum')
    
    sector_labels = []
    sector_values = []
    sector_colors = ['#3b82f6', '#8b5cf6', '#10b981', '#f59e0b', '#ef4444']
    
    for i, sector in enumerate(sector_allocation_valuation):
        sector_labels.append(sector['sector'])
        sector_values.append(float(sector['valuation_sum']) / 1000000)  # Convert to millions
    
    sector_allocation_data = {
        'labels': sector_labels,
        'data': sector_values,
        'backgroundColor': sector_colors[:len(sector_labels)],
    }

    # Generate yearly lease expiry data with rent amounts and percentages
    from datetime import datetime, timedelta
    
    current_year = datetime.now().year
    
    # Calculate total rent for percentage calculations
    total_rent = Tenant.objects.aggregate(total_rent=Sum('contracted_rent'))['total_rent'] or 0
    
    # Define year ranges for lease expiry analysis
    year_labels = ['2025', '2026', '2027', '2028', '2029', '2030+']
    year_data = []
    year_rent_data = []
    year_percentages = []
    
    for i, year_label in enumerate(year_labels):
        if year_label == '2030+':
            # For 2030+, get all leases expiring from 2030 onwards
            year_rent = Tenant.objects.filter(
                lease_end__year__gte=2030
            ).aggregate(rent_sum=Sum('contracted_rent'))['rent_sum'] or 0
        else:
            # For specific years
            target_year = int(year_label)
            year_rent = Tenant.objects.filter(
                lease_end__year=target_year
            ).aggregate(rent_sum=Sum('contracted_rent'))['rent_sum'] or 0
        
        # Calculate percentage of total rent
        percentage = (year_rent / total_rent * 100) if total_rent > 0 else 0
        
        year_data.append(float(year_rent))
        year_rent_data.append(float(year_rent))
        year_percentages.append(round(percentage, 1))
    
    lease_expiry_data = {
        'labels': year_labels,
        'data': year_percentages,  # Percentage data for chart display
        'rent_data': year_rent_data,  # Actual rent amounts for tooltips
        'total_rent': float(total_rent)
    }

    # Generate debt maturity data starting from current year
    current_year = datetime.now().year
    debt_years = [str(current_year + i) for i in range(4)]  # Current year + 3 more years
    debt_years[-1] = debt_years[-1] + "+"  # Last year gets a "+" suffix
    
    # Query actual debt data by maturity year - all zeros since no debt
    debt_amounts = []
    for year in debt_years[:-1]:  # Exclude the "++" year
        year_debt = Property.objects.filter(
            year__lte=int(year)
        ).aggregate(total_debt=Sum('total_debt'))['total_debt'] or 0
        debt_amounts.append(float(year_debt) / 1000000)  # Convert to millions
    
    # Add zero for the "+" year as well
    debt_amounts.append(0)
    
    debt_wall_data = {
        'labels': debt_years,
        'data': debt_amounts,  # Real debt data (all zeros since no debt)
    }

    sector_allocation_data_json = json.dumps(sector_allocation_data, cls=DjangoJSONEncoder)
    lease_expiry_data_json = json.dumps(lease_expiry_data, cls=DjangoJSONEncoder)
    debt_wall_data_json = json.dumps(debt_wall_data, cls=DjangoJSONEncoder)

    # Portfolio Analysis Rules Engine
    def analyze_portfolio():
        analysis_findings = []
        current_date = datetime.now().date()
        
        # Use raw numeric values for comparisons (before string formatting)
        yield_raw = total_yield_raw  # Raw numeric value from line 70
        ltv_raw = total_debt_ltv_raw  # Raw numeric value from line 71
        
        # 1. Lease Risk Analysis - Check if >20% of rent expires in any single year
        for i, year_label in enumerate(year_labels):
            percentage = year_percentages[i]
            if percentage > 20:
                rent_amount = year_rent_data[i] / 1000000  # Convert to millions for display
                analysis_findings.append({
                    'category': 'Lease Risk',
                    'finding': f'{percentage:.1f}% of total rent (£{rent_amount:.1f}M) expires in {year_label}',
                    'impact': 'High' if percentage > 50 else 'Medium',
                    'recommendation': 'Prioritize lease renewal negotiations - major portfolio exposure',
                    'action': f'Schedule renewal meetings for £{rent_amount:.1f}M expiring rent',
                    'chart_reference': 'lease-expiry'
                })
        
        # 1b. Multi-year lease risk analysis
        # Check for combined 2-year periods with high exposure
        for i in range(len(year_labels) - 1):
            combined_percentage = year_percentages[i] + year_percentages[i + 1]
            if combined_percentage > 40:
                year1, year2 = year_labels[i], year_labels[i + 1]
                pct1, pct2 = year_percentages[i], year_percentages[i + 1]
                analysis_findings.append({
                    'category': 'Lease Risk',
                    'finding': f'Combined {pct1:.1f}% + {pct2:.1f}% = {combined_percentage:.1f}% expires in {year1}-{year2}',
                    'impact': 'High',
                    'recommendation': 'Stagger renewal negotiations across both years to spread risk',
                    'action': 'Develop 2-year renewal strategy',
                    'chart_reference': 'lease-expiry'
                })
        
        # 2. Concentration Risk Analysis - Check sector allocation
        total_valuation_check = sum(sector_values) * 1000000  # Convert back from millions
        for i, sector_label in enumerate(sector_labels):
            sector_percentage = (sector_values[i] * 1000000 / total_valuation_check) * 100 if total_valuation_check > 0 else 0
            if sector_percentage > 40:
                analysis_findings.append({
                    'category': 'Concentration',
                    'finding': f'{sector_label} represents {sector_percentage:.1f}% of portfolio value',
                    'impact': 'High',
                    'recommendation': 'Diversify sector allocation to reduce concentration risk',
                    'action': 'Review acquisition strategy',
                    'chart_reference': 'sector-allocation'
                })
        
        # 3. Tenant Quality Analysis - Check credit ratings
        poor_credit_tenants = Tenant.objects.filter(
            experian_score__in=['Very Poor', 'Poor', 'Below Average']
        ).count()
        total_tenants_count = Tenant.objects.count()
        
        if total_tenants_count > 0:
            poor_credit_percentage = (poor_credit_tenants / total_tenants_count) * 100
            if poor_credit_percentage > 15:
                analysis_findings.append({
                    'category': 'Tenant Quality',
                    'finding': f'{poor_credit_percentage:.1f}% of tenants have poor credit ratings',
                    'impact': 'Medium',
                    'recommendation': 'Review tenant covenant strength and consider rent guarantees',
                    'action': 'Credit assessment review',
                    'chart_reference': 'tenant-analysis'
                })
        
        # 4. Portfolio Diversification Analysis - Check property count by sector
        sector_property_counts = Property.objects.values('sector').annotate(count=Count('id'))
        total_properties_count = Property.objects.count()
        
        for sector_data in sector_property_counts:
            if total_properties_count > 0:
                property_percentage = (sector_data['count'] / total_properties_count) * 100
                if property_percentage > 50:
                    analysis_findings.append({
                        'category': 'Diversification',
                        'finding': f'{sector_data["sector"]} sector has {property_percentage:.1f}% of properties',
                        'impact': 'Medium',
                        'recommendation': 'Consider geographic and sector diversification',
                        'action': 'Strategic review meeting',
                        'chart_reference': 'sector-allocation'
                    })
        
        # 5. Income Trends Analysis - Check occupancy levels
        low_occupancy_properties = Property.objects.filter(occupancy__lt=85).count()
        if total_properties_count > 0:
            low_occupancy_percentage = (low_occupancy_properties / total_properties_count) * 100
            if low_occupancy_percentage > 20:
                analysis_findings.append({
                    'category': 'Income Trends',
                    'finding': f'{low_occupancy_percentage:.1f}% of properties have occupancy below 85%',
                    'impact': 'Medium',
                    'recommendation': 'Focus on letting vacant spaces and tenant retention',
                    'action': 'Marketing campaign',
                    'chart_reference': 'occupancy-metrics'
                })
        
        # 6. Positive findings - Portfolio strengths (use raw numeric value)
        if yield_raw > 6:
            analysis_findings.append({
                'category': 'Income Trends',
                'finding': f'Strong portfolio yield of {yield_raw:.1f}%',
                'impact': 'Positive',
                'recommendation': 'Maintain current asset management strategy',
                'action': 'Continue monitoring',
                'chart_reference': 'yield-metrics'
            })
        
        # 7. Debt analysis if applicable (use raw numeric value)
        if ltv_raw and float(ltv_raw) > 0:
            if float(ltv_raw) > 70:
                analysis_findings.append({
                    'category': 'Financial',
                    'finding': f'High LTV ratio of {ltv_raw:.1f}%',
                    'impact': 'High',
                    'recommendation': 'Consider debt reduction or refinancing options',
                    'action': 'Meet with lenders',
                    'chart_reference': 'debt-wall'
                })
        
        return analysis_findings
    
    # Generate portfolio analysis
    portfolio_analysis = analyze_portfolio()
    portfolio_analysis_json = json.dumps(portfolio_analysis, cls=DjangoJSONEncoder)

    context = {
        'total_properties': total_properties,
        'total_tenants': total_tenants,
        'total_income': total_income,
        'total_valuation': total_valuation,
        'total_sq_ft': total_sq_ft,
        'total_occupancy_by_erv': total_occupancy_by_erv,
        'total_yield': total_yield,
        'total_capex': total_capex_formatted,
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
        'portfolio_analysis': portfolio_analysis,
        'portfolio_analysis_json': portfolio_analysis_json,
    }

    return render(request, 'dashboard.html', context)


# Temporarily commented out - focusing on portfolio dashboard
# def financial_modelling_view(request):
#     # Add any logic to gather data for the dashboard here
#     context = {}  # For now, we'll use an empty context
#     return render(request, 'financial_modelling.html', context)

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

# Temporarily commented out - focusing on portfolio dashboard
# def deals_view(request):
#     # Add any logic to gather data for the deals dashboard here
#     context = {}  # For now, we'll use an empty context
#     return render(request, 'deals.html', context)

def asset_management_view(request):
    # Add any logic to gather data for the asset management dashboard here
    context = {}  # For now, we'll use an empty context
    return render(request, 'asset_management.html', context)

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