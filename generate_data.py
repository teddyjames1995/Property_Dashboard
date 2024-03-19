import os
import django
import uuid
from faker import Faker
from random import choice, randint, uniform, getrandbits
from datetime import timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Property_Dashboard.settings')
django.setup()

from Property_Dashboard_app.models import Property

fake = Faker()

def create_properties(n):
    sectors = ['Industrial', 'Office', 'Retail']
    sub_sectors = ['Warehouse', 'Data Center', 'Shopping Mall']
    strategies = ['Core', 'Value-Add', 'Opportunistic']
    for _ in range(n):
        acquisition_date = fake.date_between(start_date='-10y', end_date='today')
        # Assign a year based on the acquisition_date
        year = acquisition_date.year

        refinance_date = acquisition_date + timedelta(days=randint(1, 3650))

        if refinance_date <= timezone.now().date():
            refinance = choice([True, False])
            date_sold = fake.date_between(start_date=refinance_date, end_date='today') if refinance and choice([True, False]) else None
            net_sales_price = randint(100000, 5000000) if date_sold else None
            disposal_costs_percentage = uniform(0, 5) if date_sold else None
        else:
            refinance = False
            date_sold = None
            net_sales_price = None
            disposal_costs_percentage = None

        Property.objects.create(
             property_id=str(uuid.uuid4()),  # Generate a unique UUID for property_id
            year=year,
            quarter=f'Q{choice([1, 2, 3, 4])}',
            month=str(acquisition_date.month).zfill(2),
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
            interest_percentage=uniform(1.0, 5.0),
            amortisation_percentage=uniform(0, 100),
            debt_arrangement_fee_percentage=uniform(0, 5),
            refinance=refinance,
            refinance_date=refinance_date if refinance else None,
            valuation_at_refinance=randint(100000, 5000000) if refinance else None,
            refinance_loan_term_years=randint(1, 30) if refinance else None,
            refinance_interest_only=choice([True, False]) if refinance else None,
            refinance_interest_percentage=uniform(1.0, 5.0) if refinance else None,
            refinance_amortisation_percentage=uniform(0, 100) if refinance else None,
            refinance_debt_arrangement_fee_percentage=uniform(0, 5) if refinance else None,
            number_of_tenants=randint(1, 10),
            valuation_fees=uniform(0.1, 1.0) * randint(1000, 10000),
            date_sold=date_sold,
            net_sales_price=net_sales_price,
            disposal_costs_percentage=disposal_costs_percentage,
            cluster=fake.word(),
            strategy=choice(strategies),
        )

if __name__ == '__main__':
    num_properties = 100  # Number of properties to create
    create_properties(num_properties)

from Property_Dashboard_app.models import Tenant, Property

def create_tenants(n, properties):
    LETTING_STATUS_CHOICES = ['Let', 'Void', 'Under Offer', 'Terms Out', 'Refurbishing', 'Kept Back']
    FRI_CHOICES = ['FRI', 'EFRI', 'IRI']
    ACT_STATUS_CHOICES = ['Inside', 'Outside']
    EPC_RATING_CHOICES = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

    for _ in range(n):
        property_instance = choice(properties)
        lease_start_date = fake.date_between(start_date='-10y', end_date='today')
        lease_end_date = lease_start_date + timedelta(days=randint(1000, 2000))

        Tenant.objects.create(
            property_id=property_instance,
            year=lease_start_date.year,
            quarter=choice(['Q1', 'Q2', 'Q3', 'Q4']),
            month=str(lease_start_date.month).zfill(2),
            floor=fake.random_int(min=1, max=10),
            tenant_name=fake.company(),
            vacant=bool(getrandbits(1)),
            letting_status=choice(LETTING_STATUS_CHOICES),
            fri_status=choice(FRI_CHOICES),
            area_sq_ft=uniform(1000, 20000),
            inside_outside_act=choice(ACT_STATUS_CHOICES),
            rent_deposit=uniform(1000, 10000),
            rent_free=f"{randint(0, 6)} months",
            lease_start=lease_start_date,
            lease_end=lease_end_date,
            break_option=f"{randint(0, 5)} years",
            rent_review=f"{randint(1, 5)} years",
            contracted_rent=uniform(5000, 20000),
            passing_rent=uniform(5000, 20000),
            erv=uniform(5000, 20000),
            epc_rating=choice(EPC_RATING_CHOICES),
            epc_score=f"{randint(1, 100)}",
            epc_expiry=lease_end_date + timedelta(days=365),
            main_heating_fuel=choice(['Gas', 'Electric', 'Oil']),
            refurbished_lighting=bool(getrandbits(1)),
            ev_charging=bool(getrandbits(1)),
            green_lease=bool(getrandbits(1)),
            solar_panels=bool(getrandbits(1)),
            service_charge=uniform(100, 5000),
            rateable_value=uniform(5000, 20000),
            rates_payable=uniform(1000, 10000),
            total_occupational_cost=uniform(5000, 20000),
            experian_score=f"{randint(1, 100)}",
            tenant_sector=fake.word(),
            property_sector=property_instance.sector,
            location=fake.city(),
            capital_expenditure=uniform(1000, 50000),
        )

if __name__ == '__main__':
    num_tenants = 300  # Adjust as needed
    properties = list(Property.objects.all())
    create_tenants(num_tenants, properties)


from Property_Dashboard_app.models import OperatingExpenses, Property

# Completion of Operating Expenses Data Generation Script
def create_operating_expenses(n, properties, tenants):
    for _ in range(n):
        property_instance = choice(properties)
        tenant_instance = choice(tenants)

        OperatingExpenses.objects.create(
            property_id=property_instance,
            tenant=tenant_instance,
            year=randint(2015, 2023),
            quarter=choice(['Q1', 'Q2', 'Q3', 'Q4']),
            month=str(randint(1, 12)).zfill(2),
            title=fake.sentence(),
            floor=str(randint(1, 20)),  # Adjust according to your data
            legal_fees=uniform(100, 10000),
            managing_agent_fees=uniform(100, 10000),
            marketing_costs=uniform(100, 10000),
            void_rates=uniform(0, 10000),
            service_charge_shortfall=uniform(0, 10000),
            real_estate_taxes=uniform(100, 10000),
            repairs_and_maintenance=uniform(100, 10000),
            security=uniform(100, 5000),
            planning=uniform(100, 5000),
            letting_fees=uniform(100, 5000),
            professional_fees=uniform(100, 5000),
            electricity=uniform(100, 5000),
            gas=uniform(100, 5000),
            insurance=uniform(100, 5000),
            environmental=uniform(100, 5000),
            dilapidations=uniform(100, 5000),
            water=uniform(100, 5000),
            lease_surrender=uniform(0, 10000),
            deposit=uniform(0, 10000),
            ground_rent=uniform(0, 10000),
            fire_risk=uniform(0, 10000),
            specific_bad_debt=uniform(0, 5000),
            ppm=uniform(100, 5000),
        )

if __name__ == '__main__':
    num_properties = 100  # Adjust as needed
    num_tenants = 300  # Adjust as needed
    num_operating_expenses = 400  # Adjust as needed
    properties = list(Property.objects.all())
    tenants = list(Tenant.objects.all())

    print("Creating Properties...")
    create_properties(num_properties)
    print("Creating Tenants...")
    create_tenants(num_tenants, properties)
    print("Creating Operating Expenses...")
    create_operating_expenses(num_operating_expenses, properties, tenants)

    print("Data generation completed.")
