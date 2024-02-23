from django.db import models

class Property(models.Model):
    property_id = models.CharField(max_length=100, unique=True)
    year = models.IntegerField()
    quarter = models.CharField(max_length=2)
    month = models.CharField(max_length=2)
    title = models.CharField(max_length=255)
    address = models.TextField()
    city = models.CharField(max_length=100)
    postcode = models.CharField(max_length=20)
    sector = models.CharField(max_length=100)
    sub_sector = models.CharField(max_length=100)
    portfolio = models.CharField(max_length=100)
    sq_ft = models.DecimalField(max_digits=10, decimal_places=2)
    acreage = models.DecimalField(max_digits=10, decimal_places=2)
    date_acquired = models.DateField()
    net_acquisition_price = models.DecimalField(max_digits=15, decimal_places=2)
    acquisition_costs = models.DecimalField(max_digits=15, decimal_places=2)
    tenure = models.CharField(max_length=100)
    total_gross_income = models.DecimalField(max_digits=15, decimal_places=2)
    operating_expenses = models.DecimalField(max_digits=15, decimal_places=2)
    estimated_rental_value = models.DecimalField(max_digits=15, decimal_places=2)
    valuation = models.DecimalField(max_digits=15, decimal_places=2)
    occupancy = models.DecimalField(max_digits=5, decimal_places=2)
    capital_expenditure = models.DecimalField(max_digits=15, decimal_places=2)
    total_debt = models.DecimalField(max_digits=15, decimal_places=2)
    loan_term_years = models.IntegerField()
    interest_only = models.BooleanField()
    interest_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    amortisation_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    debt_arrangement_fee_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    refinance = models.BooleanField()
    refinance_date = models.DateField(null=True, blank=True)
    valuation_at_refinance = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    refinance_loan_term_years = models.IntegerField(null=True, blank=True)
    refinance_interest_only = models.BooleanField(null=True, blank=True)
    refinance_interest_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    refinance_amortisation_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    refinance_debt_arrangement_fee_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    number_of_tenants = models.IntegerField()
    valuation_fees = models.DecimalField(max_digits=15, decimal_places=2)
    date_sold = models.DateField(null=True, blank=True)
    net_sales_price = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    disposal_costs_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    cluster = models.CharField(max_length=100)
    strategy = models.CharField(max_length=100)
    
    def __str__(self):
        return self.title

class Tenant(models.Model):
    FRI_CHOICES = [
        ('FRI', 'Full Repairing and Insuring'),
        ('EFRI', 'Effective Full Repairing and Insuring'),
        ('IRI', 'Internal Repairing and Insuring'),
    ]
    LETTING_STATUS_CHOICES = [
        ('Let', 'Let'),
        ('Void', 'Void'),
        ('Under Offer', 'Under Offer'),
        ('Terms Out', 'Terms Out'),
        ('Refurbishing', 'Refurbishing'),
        ('Kept Back', 'Kept Back'),
    ]
    ACT_STATUS_CHOICES = [
        ('Inside', 'Inside the Act'),
        ('Outside', 'Outside the Act'),
    ]
    EPC_RATING_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('E', 'E'),
        ('F', 'F'),
        ('G', 'G'),
    ]

    property_id = models.ForeignKey(Property, on_delete=models.CASCADE)
    year = models.IntegerField()
    quarter = models.CharField(max_length=2)
    month = models.CharField(max_length=2)
    floor = models.CharField(max_length=100)
    tenant_name = models.CharField(max_length=255)
    vacant = models.BooleanField()
    letting_status = models.CharField(max_length=20, choices=LETTING_STATUS_CHOICES)
    fri_status = models.CharField(max_length=4, choices=FRI_CHOICES)
    area_sq_ft = models.DecimalField(max_digits=10, decimal_places=2)
    inside_outside_act = models.CharField(max_length=7, choices=ACT_STATUS_CHOICES)
    rent_deposit = models.DecimalField(max_digits=15, decimal_places=2)
    rent_free = models.CharField(max_length=100)
    lease_start = models.DateField()
    lease_end = models.DateField()
    break_option = models.CharField(max_length=100)
    rent_review = models.CharField(max_length=100)
    contracted_rent = models.DecimalField(max_digits=15, decimal_places=2)
    passing_rent = models.DecimalField(max_digits=15, decimal_places=2)
    erv = models.DecimalField(max_digits=15, decimal_places=2)
    epc_rating = models.CharField(max_length=1, choices=EPC_RATING_CHOICES)
    epc_score = models.CharField(max_length=10)
    epc_expiry = models.DateField()
    main_heating_fuel = models.CharField(max_length=100)
    refurbished_lighting = models.BooleanField()
    ev_charging = models.BooleanField()
    green_lease = models.BooleanField()
    solar_panels = models.BooleanField()
    service_charge = models.DecimalField(max_digits=15, decimal_places=2)
    rateable_value = models.DecimalField(max_digits=15, decimal_places=2)
    rates_payable = models.DecimalField(max_digits=15, decimal_places=2)
    total_occupational_cost = models.DecimalField(max_digits=15, decimal_places=2)
    experian_score = models.CharField(max_length=100)
    tenant_sector = models.CharField(max_length=100)
    property_sector = models.CharField(max_length=100)
    property_sector_2 = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100)
    capital_expenditure = models.DecimalField(max_digits=15, decimal_places=2)

    # Add any other fields relevant to your tenant data

    def __str__(self):
        return f"{self.tenant_name} on {self.floor}"

    
class OperatingExpenses(models.Model):
    property_id = models.ForeignKey(Property, on_delete=models.CASCADE)
    year = models.IntegerField()
    quarter = models.CharField(max_length=2)
    month = models.CharField(max_length=2)
    title = models.CharField(max_length=255)
    floor = models.CharField(max_length=100)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    legal_fees = models.DecimalField(max_digits=10, decimal_places=2)
    managing_agent_fees = models.DecimalField(max_digits=10, decimal_places=2)
    marketing_costs = models.DecimalField(max_digits=10, decimal_places=2)
    void_rates = models.DecimalField(max_digits=10, decimal_places=2)
    service_charge_shortfall = models.DecimalField(max_digits=10, decimal_places=2)
    real_estate_taxes = models.DecimalField(max_digits=10, decimal_places=2)
    repairs_and_maintenance = models.DecimalField(max_digits=10, decimal_places=2)
    security = models.DecimalField(max_digits=10, decimal_places=2)
    planning = models.DecimalField(max_digits=10, decimal_places=2)
    letting_fees = models.DecimalField(max_digits=10, decimal_places=2)
    professional_fees = models.DecimalField(max_digits=10, decimal_places=2)
    electricity = models.DecimalField(max_digits=10, decimal_places=2)
    gas = models.DecimalField(max_digits=10, decimal_places=2)
    insurance = models.DecimalField(max_digits=10, decimal_places=2)
    environmental = models.DecimalField(max_digits=10, decimal_places=2)
    dilapidations = models.DecimalField(max_digits=10, decimal_places=2)
    water = models.DecimalField(max_digits=10, decimal_places=2)
    lease_surrender = models.DecimalField(max_digits=10, decimal_places=2)
    deposit = models.DecimalField(max_digits=10, decimal_places=2)
    ground_rent = models.DecimalField(max_digits=10, decimal_places=2)
    fire_risk = models.DecimalField(max_digits=10, decimal_places=2)
    specific_bad_debt = models.DecimalField(max_digits=10, decimal_places=2)
    ppm = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
        return f"Expenses for {self.tenant} on {self.floor}"
from django.db import models


