import csv
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_date
from Property_Dashboard_app.models import Property, Tenant, OperatingExpenses

class Command(BaseCommand):
    help = 'Import Properties, Tenants, and Operating Expenses from CSV files.'

    def add_arguments(self, parser):
        parser.add_argument('--properties', type=str, help='Path to the properties CSV file.')
        parser.add_argument('--tenants', type=str, help='Path to the tenants CSV file.')
        parser.add_argument('--expenses', type=str, help='Path to the operating expenses CSV file.')

    def handle(self, *args, **kwargs):
        if kwargs['properties']:
            self.import_properties(kwargs['properties'])
        if kwargs['tenants']:
            self.import_tenants(kwargs['tenants'])
        if kwargs['expenses']:
            self.import_operating_expenses(kwargs['expenses'])

    def import_properties(self, csv_file):
        with open(csv_file, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                property, created = Property.objects.update_or_create(
                    property_id=row['property_id'],
                    defaults={
                        # Assuming all fields are correctly represented in the CSV
                        'year': int(row['year']),
                        'quarter': row['quarter'],
                        'month': row['month'],
                        'title': row['title'],
                        'address': row['address'],
                        'city': row['city'],
                        'postcode': row['postcode'],
                        'sector': row['sector'],
                        'sub_sector': row['sub_sector'],
                        'portfolio': row['portfolio'],
                        'sq_ft': float(row['sq_ft']),
                        'acreage': float(row['acreage']),
                        'date_acquired': parse_date(row['date_acquired']),
                        'net_acquisition_price': float(row['net_acquisition_price']),
                        'acquisition_costs': float(row['acquisition_costs']),
                        'tenure': row['tenure'],
                        'total_gross_income': float(row['total_gross_income']),
                        'operating_expenses': float(row['operating_expenses']),
                        'estimated_rental_value': float(row['estimated_rental_value']),
                        'valuation': float(row['valuation']),
                        'occupancy': float(row['occupancy']),
                        'capital_expenditure': float(row['capital_expenditure']),
                        'total_debt': float(row['total_debt']),
                        'loan_term_years': int(row['loan_term_years']),
                        'interest_only': row['interest_only'].lower() in ('true', 't', '1'),
                        'interest_percentage': float(row['interest_percentage']),
                        'amortisation_percentage': float(row['amortisation_percentage']),
                        'debt_arrangement_fee_percentage': float(row['debt_arrangement_fee_percentage']),
                        'refinance': row['refinance'].lower() in ('true', 't', '1'),
                        'refinance_date': parse_date(row['refinance_date']) if row['refinance_date'] else None,
                        'valuation_at_refinance': float(row['valuation_at_refinance']) if row['valuation_at_refinance'] else None,
                        'refinance_loan_term_years': int(row['refinance_loan_term_years']) if row['refinance_loan_term_years'] else None,
                        'refinance_interest_only': row['refinance_interest_only'].lower() in ('true', 't', '1') if row['refinance_interest_only'] else None,
                        'refinance_interest_percentage': float(row['refinance_interest_percentage']) if row['refinance_interest_percentage'] else None,
                        'refinance_amortisation_percentage': float(row['refinance_amortisation_percentage']) if row['refinance_amortisation_percentage'] else None,
                        'refinance_debt_arrangement_fee_percentage': float(row['refinance_debt_arrangement_fee_percentage']) if row['refinance_debt_arrangement_fee_percentage'] else None,
                        'number_of_tenants': int(row['number_of_tenants']),
                        'valuation_fees': float(row['valuation_fees']),
                        'date_sold': parse_date(row['date_sold']) if row['date_sold'] else None,
                        'net_sales_price': float(row['net_sales_price']) if row['net_sales_price'] else None,
                        'disposal_costs_percentage': float(row['disposal_costs_percentage']) if row['disposal_costs_percentage'] else None,
                        'cluster': row['cluster'],
                        'strategy': row['strategy'],
                    }
                )
                self.stdout.write(self.style.SUCCESS(f"{'Created' if created else 'Updated'} property {property.property_id}"))

    def import_tenants(self, csv_file):
        with open(csv_file, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                property_instance = Property.objects.get(property_id=row['property_id'])
                tenant, created = Tenant.objects.update_or_create(
                    tenant_name=row['tenant_name'],
                    property_id=property_instance,
                    defaults={
                        'year': int(row['year']),
                        'quarter': row['quarter'],
                        'month': row['month'],
                        'floor': row['floor'],
                        'vacant': row['vacant'].lower() in ('true', 't', '1'),
                        'letting_status': row['letting_status'],
                        'fri_status': row['fri_status'],
                        'area_sq_ft': float(row['area_sq_ft']),
                        'inside_outside_act': row['inside_outside_act'],
                        'rent_deposit': float(row['rent_deposit']),
                        'rent_free': row['rent_free'],
                        'lease_start': parse_date(row['lease_start']),
                        'lease_end': parse_date(row['lease_end']),
                        'break_option': row['break_option'],
                        'rent_review': row['rent_review'],
                        'contracted_rent': float(row['contracted_rent']),
                        'passing_rent': float(row['passing_rent']),
                        'erv': float(row['erv']),
                        'epc_rating': row['epc_rating'],
                        'epc_score': row['epc_score'],
                        'epc_expiry': parse_date(row['epc_expiry']),
                        'main_heating_fuel': row['main_heating_fuel'],
                        'refurbished_lighting': row['refurbished_lighting'].lower() in ('true', 't', '1'),
                        'ev_charging': row['ev_charging'].lower() in ('true', 't', '1'),
                        'green_lease': row['green_lease'].lower() in ('true', 't', '1'),
                        'solar_panels': row['solar_panels'].lower() in ('true', 't', '1'),
                        'service_charge': float(row['service_charge']),
                        'rateable_value': float(row['rateable_value']),
                        'rates_payable': float(row['rates_payable']),
                        'total_occupational_cost': float(row['total_occupational_cost']),
                        'experian_score': row['experian_score'],
                        'tenant_sector': row['tenant_sector'],
                        'property_sector': row['property_sector'],
                        'property_sector_2': row.get('property_sector_2', ''),
                        'location': row['location'],
                        'capital_expenditure': float(row['capital_expenditure']),
                    }
                )
                self.stdout.write(self.style.SUCCESS(f"{'Created' if created else 'Updated'} tenant {tenant.tenant_name}"))

    def import_operating_expenses(self, csv_file):
        with open(csv_file, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                property_instance = Property.objects.get(property_id=row['property_id'])
                tenant_instance = Tenant.objects.get(tenant_name=row['tenant_name'])
                expense, created = OperatingExpenses.objects.update_or_create(
                    title=row['title'],
                    property_id=property_instance,
                    tenant=tenant_instance,
                    defaults={
                        'year': int(row['year']),
                        'quarter': row['quarter'],
                        'month': row['month'],
                        'floor': row['floor'],
                        'legal_fees': float(row['legal_fees']),
                        'managing_agent_fees': float(row['managing_agent_fees']),
                        'marketing_costs': float(row['marketing_costs']),
                        'void_rates': float(row['void_rates']),
                        'service_charge_shortfall': float(row['service_charge_shortfall']),
                        'real_estate_taxes': float(row['real_estate_taxes']),
                        'repairs_and_maintenance': float(row['repairs_and_maintenance']),
                        'security': float(row['security']),
                        'planning': float(row['planning']),
                        'letting_fees': float(row['letting_fees']),
                        'professional_fees': float(row['professional_fees']),
                        'electricity': float(row['electricity']),
                        'gas': float(row['gas']),
                        'insurance': float(row['insurance']),
                        'environmental': float(row['environmental']),
                        'dilapidations': float(row['dilapidations']),
                        'water': float(row['water']),
                        'lease_surrender': float(row['lease_surrender']),
                        'deposit': float(row['deposit']),
                        'ground_rent': float(row['ground_rent']),
                        'fire_risk': float(row['fire_risk']),
                        'specific_bad_debt': float(row['specific_bad_debt']),
                        'ppm': float(row['ppm']),
                    }
                )
                self.stdout.write(self.style.SUCCESS(f"{'Created' if created else 'Updated'} operating expense for {expense.title}"))
