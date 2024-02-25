from django.contrib import admin
from .models import Property, Tenant, OperatingExpenses

admin.site.register(Property)
admin.site.register(Tenant)
admin.site.register(OperatingExpenses)
