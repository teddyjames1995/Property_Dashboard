import os
import django
from faker import Faker
from random import choice, randint, uniform
from datetime import date, timedelta


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Property_Dashboard.settings')


from Property_Dashboard_app.models import Property  # Adjust the import according to your app structure

fake = Faker()

def create_properties(n):
    sectors = ['Industrial', 'Office', 'Retail']
    sub_sectors = ['Warehouse', 'Data Center', 'Shopping Mall']
    strategies = ['Core', 'Value-Add', 'Opportunistic']
    for _ in range(n):
        acquisition_date = fake.date_between(start_date='-10y', end_date='today')
        refinance_date = acquisition_date + timedelta(days=randint(100, 1000))
        Property.objects.create(
            title=fake.company(),
            address=fake.address(),
            city=fake.city(),
            postcode=fake.postcode(),
            sector=choice(sectors),
            sub_sector=choice(sub_sectors),
            portfolio=fake.word(),
            sq_ft=randint(1000, 50000),
            acreage=uniform(0.5, 10.0),
            date_acquired=acquisition_date,
            net_acquisition_price=randint(100000, 5000000),
            acquisition_costs=uniform(1.0, 5.0),
            tenure=fake.word(),
            total_gross_income=randint(50000, 1000000),
            operating_expenses=randint(10000, 500000),
            estimated_rental_value=randint(50000, 1000000),
            valuation=randint(100000, 5000000),
            occupancy=uniform(0, 100),
            capital_expenditure=randint(1000, 100000),
            total_debt=randint(50000, 2000000),
            loan_term_years=randint(1, 30),
            interest_only=choice([True, False]),
            interest=uniform(1.0, 5.0),
            amortisation=uniform(0, 100),
            debt_arrangement_fee=uniform(0, 5),
            refinance=choice([True, False]),
            refinance_date=refinance_date if choice([True, False]) else None,
            valuation_at_refinance=randint(100000, 5000000) if choice([True, False]) else None,
            refinance_loan_term_years=randint(1, 30) if choice([True, False]) else None,
            refinance_interest_only=choice([True, False]) if choice([True, False]) else None,
            refinance_interest=uniform(1.0, 5.0) if choice([True, False]) else None,
            refinance_amortisation=uniform(0, 100) if choice([True, False]) else None,
            refinance_debt_arrangement_fee=uniform(0, 5) if choice([True, False]) else None,
            number_of_tenants=randint(1, 10),
            valuation_fees=uniform(0.1, 1.0) * randint(1000, 10000),
            date_sold=fake.date_between(start_date=refinance_date, end_date='today') if choice([True, False]) else None,
            net_sales_price=randint(100000, 5000000) if choice([True, False]) else None,
            disposal_costs=uniform(0, 5) if choice([True, False]) else None,
            cluster=fake.word(),
            strategy=choice(strategies),
        )

if __name__ == '__main__':
    num_properties = 100  # Number of properties to create
    create_properties(num_properties)

from Property_Dashboard_app.models import Tenant, Property

def create_tenants(n):
    tenant_sectors = ['Technology', 'Finance', 'Healthcare']
    for _ in range(n):
        property = choice(Property.objects.all())
        Tenant.objects.create(
            property=property,
            year=randint(2015, 2023),
            quarter=choice(['Q1', 'Q2', 'Q3', 'Q4']),
            month=choice(range(1, 13)),
            floor=randint(1, 10),
            tenant=fake.company(),
            vacant=choice([True, False]),
            letting_status=choice(['Let', 'Available']),
            fri_or_efri=choice(['FRI', 'EFRI']),
            area_sq_ft=randint(500, 20000),
            inside_or_outside_act=choice([True, False]),
            rent_deposit=randint(1000, 20000),
            rent_free=choice([0, 1, 2, 3, 6]),
            lease_start=fake.past_date(),
            lease_end=fake.future_date(),
            break_option=choice([None, fake.future_date()]),
            rent_review=choice([None, fake.future_date()]),
            contracted_rent=randint(1000, 20000),
            passing_rent=randint(1000, 20000),
            erv=randint(1000, 20000),
            epc_rating=choice(['A', 'B', 'C', 'D', 'E']),
            epc_score=randint(1, 100),
            epc_expiry=fake.future_date(),
            main_heating_fuel=choice(['Gas', 'Electric', 'Oil']),
            refurbished_lighting=choice([True, False]),
            ev_charging=choice([True, False]),
            green_lease=choice([True, False]),
            solar_panels=choice([True, False]),
            service_charge=randint(100, 5000),
            rateable_value=randint(1000, 100000),
            rates_payable=randint(100, 5000),
            total_occupational_cost=randint(1000, 50000),
            experian_score=randint(1, 100),
            tenant_sector=choice(tenant_sectors),
            property_sector=property.sector,
            location=fake.city(),
            capital_expenditure=randint(1000, 50000),
        )

if __name__ == '__main__':
    num_tenants = 300  # Number of tenants to create
    create_tenants(num_tenants)

from Property_Dashboard_app.models import OperatingExpenses, Property

# Completion of Operating Expenses Data Generation Script
def create_operating_expenses(n):
    for _ in range(n):
        property = choice(Property.objects.all())
        OperatingExpenses.objects.create(
            property=property,
            year=randint(2015, 2023),
            quarter=choice(['Q1', 'Q2', 'Q3', 'Q4']),
            month=choice(range(1, 13)),
            title=fake.sentence(),
            legal_fees=randint(100, 10000),
            managing_agent_fees=randint(100, 10000),
            marketing_costs=randint(100, 10000),
            void_rates=randint(0, 10000),
            service_charge_shortfall=randint(0, 10000),
            real_estate_taxes=randint(100, 10000),
            repairs_and_maintenance=randint(100, 10000),
            security=randint(100, 5000),
            planning=randint(100, 5000),
            letting_fees=randint(100, 5000),
            professional_fees=randint(100, 5000),
            electricity=randint(100, 5000),
            gas=randint(100, 5000),
            insurance=randint(100, 5000),
            environmental=randint(100, 5000),
            dilapidations=randint(100, 5000),
            water=randint(100, 5000),
            lease_surrender=randint(0, 10000),
            deposit=randint(0, 10000),
            ground_rent=randint(0, 10000),
            fire_risk=randint(0, 10000),
            specific_bad_debt=randint(0, 5000),
            ppm=randint(100, 5000)
        )

if __name__ == '__main__':
    num_properties = 100  # Adjust as needed
    num_tenants = 300  # Adjust as needed
    num_operating_expenses = 400  # Adjust as needed

    print("Creating Properties...")
    create_properties(num_properties)
    print("Creating Tenants...")
    create_tenants(num_tenants, list(Property.objects.all()))
    print("Creating Operating Expenses...")
    create_operating_expenses(num_operating_expenses)

    print("Data generation completed.")
