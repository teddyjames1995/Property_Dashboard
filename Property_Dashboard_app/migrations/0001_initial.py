# Generated by Django 4.2.10 on 2024-02-21 00:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('property_id', models.CharField(max_length=100, unique=True)),
                ('year', models.IntegerField()),
                ('quarter', models.CharField(max_length=2)),
                ('month', models.CharField(max_length=2)),
                ('title', models.CharField(max_length=255)),
                ('address', models.TextField()),
                ('city', models.CharField(max_length=100)),
                ('postcode', models.CharField(max_length=20)),
                ('sector', models.CharField(max_length=100)),
                ('sub_sector', models.CharField(max_length=100)),
                ('portfolio', models.CharField(max_length=100)),
                ('sq_ft', models.DecimalField(decimal_places=2, max_digits=10)),
                ('acreage', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date_acquired', models.DateField()),
                ('net_acquisition_price', models.DecimalField(decimal_places=2, max_digits=15)),
                ('acquisition_costs', models.DecimalField(decimal_places=2, max_digits=15)),
                ('tenure', models.CharField(max_length=100)),
                ('total_gross_income', models.DecimalField(decimal_places=2, max_digits=15)),
                ('operating_expenses', models.DecimalField(decimal_places=2, max_digits=15)),
                ('estimated_rental_value', models.DecimalField(decimal_places=2, max_digits=15)),
                ('valuation', models.DecimalField(decimal_places=2, max_digits=15)),
                ('occupancy', models.DecimalField(decimal_places=2, max_digits=5)),
                ('capital_expenditure', models.DecimalField(decimal_places=2, max_digits=15)),
                ('total_debt', models.DecimalField(decimal_places=2, max_digits=15)),
                ('loan_term_years', models.IntegerField()),
                ('interest_only', models.BooleanField()),
                ('interest_percentage', models.DecimalField(decimal_places=2, max_digits=5)),
                ('amortisation_percentage', models.DecimalField(decimal_places=2, max_digits=5)),
                ('debt_arrangement_fee_percentage', models.DecimalField(decimal_places=2, max_digits=5)),
                ('refinance', models.BooleanField()),
                ('refinance_date', models.DateField(blank=True, null=True)),
                ('valuation_at_refinance', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('refinance_loan_term_years', models.IntegerField(blank=True, null=True)),
                ('refinance_interest_only', models.BooleanField(blank=True, null=True)),
                ('refinance_interest_percentage', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('refinance_amortisation_percentage', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('refinance_debt_arrangement_fee_percentage', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('number_of_tenants', models.IntegerField()),
                ('valuation_fees', models.DecimalField(decimal_places=2, max_digits=15)),
                ('date_sold', models.DateField(blank=True, null=True)),
                ('net_sales_price', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('disposal_costs_percentage', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('cluster', models.CharField(max_length=100)),
                ('strategy', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Tenant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('quarter', models.CharField(max_length=2)),
                ('month', models.CharField(max_length=2)),
                ('floor', models.CharField(max_length=100)),
                ('tenant_name', models.CharField(max_length=255)),
                ('vacant', models.BooleanField()),
                ('letting_status', models.CharField(choices=[('Let', 'Let'), ('Void', 'Void'), ('Under Offer', 'Under Offer'), ('Terms Out', 'Terms Out'), ('Refurbishing', 'Refurbishing'), ('Kept Back', 'Kept Back')], max_length=20)),
                ('fri_status', models.CharField(choices=[('FRI', 'Full Repairing and Insuring'), ('EFRI', 'Effective Full Repairing and Insuring'), ('IRI', 'Internal Repairing and Insuring')], max_length=4)),
                ('area_sq_ft', models.DecimalField(decimal_places=2, max_digits=10)),
                ('inside_outside_act', models.CharField(choices=[('Inside', 'Inside the Act'), ('Outside', 'Outside the Act')], max_length=7)),
                ('rent_deposit', models.DecimalField(decimal_places=2, max_digits=15)),
                ('rent_free', models.CharField(max_length=100)),
                ('lease_start', models.DateField()),
                ('lease_end', models.DateField()),
                ('break_option', models.CharField(max_length=100)),
                ('rent_review', models.CharField(max_length=100)),
                ('contracted_rent', models.DecimalField(decimal_places=2, max_digits=15)),
                ('passing_rent', models.DecimalField(decimal_places=2, max_digits=15)),
                ('erv', models.DecimalField(decimal_places=2, max_digits=15)),
                ('epc_rating', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'), ('F', 'F'), ('G', 'G')], max_length=1)),
                ('epc_score', models.CharField(max_length=10)),
                ('epc_expiry', models.DateField()),
                ('main_heating_fuel', models.CharField(max_length=100)),
                ('refurbished_lighting', models.BooleanField()),
                ('ev_charging', models.BooleanField()),
                ('green_lease', models.BooleanField()),
                ('solar_panels', models.BooleanField()),
                ('service_charge', models.DecimalField(decimal_places=2, max_digits=15)),
                ('rateable_value', models.DecimalField(decimal_places=2, max_digits=15)),
                ('rates_payable', models.DecimalField(decimal_places=2, max_digits=15)),
                ('total_occupational_cost', models.DecimalField(decimal_places=2, max_digits=15)),
                ('experian_score', models.CharField(max_length=100)),
                ('tenant_sector', models.CharField(max_length=100)),
                ('property_sector', models.CharField(max_length=100)),
                ('property_sector_2', models.CharField(blank=True, max_length=100, null=True)),
                ('location', models.CharField(max_length=100)),
                ('capital_expenditure', models.DecimalField(decimal_places=2, max_digits=15)),
                ('property_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Property_Dashboard_app.property')),
            ],
        ),
        migrations.CreateModel(
            name='OperatingExpenses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('quarter', models.CharField(max_length=2)),
                ('month', models.CharField(max_length=2)),
                ('title', models.CharField(max_length=255)),
                ('floor', models.CharField(max_length=100)),
                ('legal_fees', models.DecimalField(decimal_places=2, max_digits=10)),
                ('managing_agent_fees', models.DecimalField(decimal_places=2, max_digits=10)),
                ('marketing_costs', models.DecimalField(decimal_places=2, max_digits=10)),
                ('void_rates', models.DecimalField(decimal_places=2, max_digits=10)),
                ('service_charge_shortfall', models.DecimalField(decimal_places=2, max_digits=10)),
                ('real_estate_taxes', models.DecimalField(decimal_places=2, max_digits=10)),
                ('repairs_and_maintenance', models.DecimalField(decimal_places=2, max_digits=10)),
                ('security', models.DecimalField(decimal_places=2, max_digits=10)),
                ('planning', models.DecimalField(decimal_places=2, max_digits=10)),
                ('letting_fees', models.DecimalField(decimal_places=2, max_digits=10)),
                ('professional_fees', models.DecimalField(decimal_places=2, max_digits=10)),
                ('electricity', models.DecimalField(decimal_places=2, max_digits=10)),
                ('gas', models.DecimalField(decimal_places=2, max_digits=10)),
                ('insurance', models.DecimalField(decimal_places=2, max_digits=10)),
                ('environmental', models.DecimalField(decimal_places=2, max_digits=10)),
                ('dilapidations', models.DecimalField(decimal_places=2, max_digits=10)),
                ('water', models.DecimalField(decimal_places=2, max_digits=10)),
                ('lease_surrender', models.DecimalField(decimal_places=2, max_digits=10)),
                ('deposit', models.DecimalField(decimal_places=2, max_digits=10)),
                ('ground_rent', models.DecimalField(decimal_places=2, max_digits=10)),
                ('fire_risk', models.DecimalField(decimal_places=2, max_digits=10)),
                ('specific_bad_debt', models.DecimalField(decimal_places=2, max_digits=10)),
                ('ppm', models.DecimalField(decimal_places=2, max_digits=10)),
                ('property_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Property_Dashboard_app.property')),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Property_Dashboard_app.tenant')),
            ],
        ),
    ]
