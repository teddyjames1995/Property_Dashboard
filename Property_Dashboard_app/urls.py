from django.urls import path
from Property_Dashboard_app import views  # Change this line

urlpatterns = [
    path('', views.home_view, name='home'),  # This is the home page URL pattern
    path('login/', views.login_view, name='login'),  # Add a login URL pattern
    path('register/', views.register_view, name='register'),  # Add a registration URL pattern
    path('dashboard/', views.dashboard_view, name='dashboard'),
    # Temporarily commented out - focusing on portfolio dashboard
    # path('financial_modelling/', views.financial_modelling_view, name='financial_modelling'),
    path('property_deepdive/', views.property_deepdive_view, name='property_deepdive'),
    path('tenancy_schedule/', views.tenancy_schedule_view, name='tenancy_schedule'),
    # Temporarily commented out - focusing on portfolio dashboard  
    # path('deals/', views.deals_view, name='deals'),
    path('asset_management/', views.asset_management_view, name='asset_management'),
    path('portfolio_performance/', views.portfolio_performance_view, name='portfolio_performance'),
    path('portfolio_report/', views.portfolio_report_view, name='portfolio_report'),
    path('debt/', views.debt_view, name='debt'),  # Added missing trailing slash
    path('income_and_expenses/', views.income_and_expenses_view, name='income_and_expenses'),  # Added missing trailing slash
    # Removed for v2 stripped back version
    # path('artificial_intelligence/', views.artificial_intelligence_view, name='artificial_intelligence'),
    # Removed for v2 stripped back version
    # path('forecasting/', views.forecasting_view, name='forecasting'),
]
