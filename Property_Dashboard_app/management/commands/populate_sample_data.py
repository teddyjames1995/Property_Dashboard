from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
from Property_Dashboard_app.models import Property, Tenant
from decimal import Decimal
import random

class Command(BaseCommand):
    help = 'Populate database with sample portfolio data: £120m portfolio with 5 assets, no debt'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample portfolio data...')
        
        # Clear existing data
        Property.objects.all().delete()
        Tenant.objects.all().delete()
        
        # Portfolio data - 5 properties totaling £120m
        properties_data = [
            {
                'title': 'Prime Office Complex London',
                'address': '123 Canary Wharf, London',
                'city': 'London',
                'postcode': 'E14 5AB',
                'sector': 'Office',
                'sub_sector': 'Prime Office',
                'valuation': Decimal('35000000'),  # £35m
                'sq_ft': Decimal('95000'),
                'acreage': Decimal('2.18'),
            },
            {
                'title': 'Industrial Distribution Center',
                'address': '456 Industrial Estate, Manchester',
                'city': 'Manchester',
                'postcode': 'M50 2UU',
                'sector': 'Industrial',
                'sub_sector': 'Distribution',
                'valuation': Decimal('28000000'),  # £28m
                'sq_ft': Decimal('180000'),
                'acreage': Decimal('4.13'),
            },
            {
                'title': 'Retail Park Birmingham',
                'address': '789 Shopping Centre, Birmingham',
                'city': 'Birmingham',
                'postcode': 'B42 1NT',
                'sector': 'Retail',
                'sub_sector': 'Retail Park',
                'valuation': Decimal('25000000'),  # £25m
                'sq_ft': Decimal('120000'),
                'acreage': Decimal('2.75'),
            },
            {
                'title': 'Mixed Use Development Leeds',
                'address': '321 City Centre, Leeds',
                'city': 'Leeds',
                'postcode': 'LS1 4AP',
                'sector': 'Mixed Use',
                'sub_sector': 'City Centre',
                'valuation': Decimal('20000000'),  # £20m
                'sq_ft': Decimal('85000'),
                'acreage': Decimal('1.95'),
            },
            {
                'title': 'Business Park Bristol',
                'address': '654 Technology Park, Bristol',
                'city': 'Bristol',
                'postcode': 'BS34 8QZ',
                'sector': 'Office',
                'sub_sector': 'Business Park',
                'valuation': Decimal('12000000'),  # £12m
                'sq_ft': Decimal('65000'),
                'acreage': Decimal('1.49'),
            },
        ]
        
        created_properties = []
        current_date = datetime.now()
        
        for i, prop_data in enumerate(properties_data):
            # Calculate rental values based on property type
            valuation = prop_data['valuation']
            sq_ft = prop_data['sq_ft']
            
            # Different yields by sector
            if prop_data['sector'] == 'Office':
                yield_pct = Decimal('0.055')  # 5.5% yield
            elif prop_data['sector'] == 'Industrial':
                yield_pct = Decimal('0.065')  # 6.5% yield
            elif prop_data['sector'] == 'Retail':
                yield_pct = Decimal('0.060')  # 6.0% yield
            else:
                yield_pct = Decimal('0.058')  # 5.8% yield
            
            gross_income = valuation * yield_pct
            erv = gross_income * Decimal('1.05')  # ERV slightly higher than passing rent
            
            property_obj = Property.objects.create(
                property_id=f'PROP-{i+1:03d}',
                year=current_date.year,
                quarter=f'Q{(current_date.month-1)//3 + 1}',
                month=f'{current_date.month:02d}',
                title=prop_data['title'],
                address=prop_data['address'],
                city=prop_data['city'],
                postcode=prop_data['postcode'],
                sector=prop_data['sector'],
                sub_sector=prop_data['sub_sector'],
                portfolio='Core Portfolio',
                sq_ft=sq_ft,
                acreage=prop_data['acreage'],
                date_acquired=current_date.date() - timedelta(days=random.randint(365, 1825)),  # 1-5 years ago
                net_acquisition_price=valuation * Decimal('0.92'),  # Acquired below current valuation
                acquisition_costs=valuation * Decimal('0.03'),  # 3% acquisition costs
                tenure='Freehold',
                total_gross_income=gross_income,
                operating_expenses=gross_income * Decimal('0.15'),  # 15% operating expenses
                estimated_rental_value=erv,
                valuation=valuation,
                occupancy=Decimal(random.randint(85, 100)),  # 85-100% occupancy
                capital_expenditure=Decimal(random.randint(50000, 200000)),
                total_debt=Decimal('0'),  # NO DEBT as requested
                loan_term_years=0,
                interest_only=False,
                interest_percentage=Decimal('0'),
                amortisation_percentage=Decimal('0'),
                debt_arrangement_fee_percentage=Decimal('0'),
                refinance=False,
                number_of_tenants=random.randint(1, 4),
                valuation_fees=Decimal(random.randint(5000, 15000)),
                cluster='Core Assets',
                strategy='Hold & Manage',
            )
            created_properties.append(property_obj)
            
            # Create tenants for each property
            num_tenants = property_obj.number_of_tenants
            for tenant_idx in range(num_tenants):
                tenant_names = [
                    'Amazon UK Services Ltd', 'HSBC UK Bank Plc', 'Tesco Stores Limited',
                    'British Telecommunications Plc', 'Marks & Spencer Plc', 'John Lewis Partnership',
                    'Lloyds Banking Group Plc', 'Vodafone Limited', 'Next Retail Ltd',
                    'Sainsbury\'s Supermarkets Ltd', 'DHL Supply Chain Ltd', 'FedEx UK',
                    'Barclays Bank Plc', 'Microsoft Limited', 'Google UK Limited',
                    'Accenture UK Limited', 'Deloitte LLP', 'PwC UK', 'KPMG LLP',
                    'EY UK', 'Whitbread Group Plc', 'Premier Inn Hotels'
                ]
                
                tenant_name = random.choice(tenant_names)
                
                # Calculate tenant's share of the building
                tenant_area = sq_ft / num_tenants
                tenant_rent = gross_income / num_tenants
                
                # Generate lease dates with variety across the next 24 months
                lease_start = current_date.date() - timedelta(days=random.randint(30, 1095))  # Started 1 month to 3 years ago
                lease_length_months = random.choice([12, 24, 36, 60, 120])  # Various lease lengths
                lease_end = lease_start + timedelta(days=lease_length_months * 30)
                
                # Ensure some leases expire in the next 12 months for chart data
                if tenant_idx == 0:  # First tenant expires soon
                    months_until_expiry = random.randint(1, 12)
                    lease_end = current_date.date() + timedelta(days=months_until_expiry * 30)
                
                Tenant.objects.create(
                    property=property_obj,
                    year=current_date.year,
                    quarter=f'Q{(current_date.month-1)//3 + 1}',
                    month=f'{current_date.month:02d}',
                    floor=f'Floor {tenant_idx + 1}' if num_tenants > 1 else 'Whole Building',
                    tenant_name=tenant_name,
                    vacant=False,
                    letting_status='Let',
                    fri_status='FRI',
                    area_sq_ft=tenant_area,
                    inside_outside_act='Inside',
                    rent_deposit=tenant_rent * Decimal('0.25'),  # 3 months deposit
                    rent_free='None',
                    lease_start=lease_start,
                    lease_end=lease_end,
                    break_option='None' if random.random() > 0.3 else f'Year {random.randint(3, 5)}',
                    rent_review='Annual',
                    contracted_rent=tenant_rent,
                    passing_rent=tenant_rent,
                    erv=tenant_rent * Decimal('1.05'),
                    epc_rating=random.choice(['A', 'B', 'C', 'D']),
                    epc_score=str(random.randint(21, 92)),
                    epc_expiry=current_date.date() + timedelta(days=random.randint(365, 3650)),
                    main_heating_fuel='Gas',
                    refurbished_lighting=random.choice([True, False]),
                    ev_charging=random.choice([True, False]),
                    green_lease=random.choice([True, False]),
                    solar_panels=random.choice([True, False]),
                    service_charge=tenant_rent * Decimal('0.08'),  # 8% service charge
                    rateable_value=tenant_area * Decimal('12'),
                    rates_payable=tenant_area * Decimal('6'),
                    total_occupational_cost=tenant_rent + (tenant_area * Decimal('18')),
                    experian_score=random.choice(['Excellent', 'Good', 'Fair']),
                    tenant_sector=prop_data['sector'],
                    property_sector=prop_data['sector'],
                    location=prop_data['city'],
                    capital_expenditure=Decimal(random.randint(5000, 25000)),
                )
        
        # Print summary
        total_valuation = sum(prop.valuation for prop in created_properties)
        total_income = sum(prop.total_gross_income for prop in created_properties)
        total_sq_ft = sum(prop.sq_ft for prop in created_properties)
        total_tenants = Tenant.objects.count()
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created sample portfolio data:'))
        self.stdout.write(f'• Properties: {len(created_properties)}')
        self.stdout.write(f'• Total Valuation: £{total_valuation:,.0f}')
        self.stdout.write(f'• Total Income: £{total_income:,.0f}')
        self.stdout.write(f'• Total Sq Ft: {total_sq_ft:,.0f}')
        self.stdout.write(f'• Total Tenants: {total_tenants}')
        self.stdout.write(f'• Total Debt: £0 (as requested)')
        self.stdout.write(f'• Average Yield: {(total_income/total_valuation*100):.1f}%')