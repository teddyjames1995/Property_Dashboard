from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),  # Assuming you have a home_view in your views.py
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('financial_modelling/', views.financial_modelling_view, name='financial_modelling'),
    path('property_deepdive/', views.property_deepdive_view, name='property_deepdive'),
    path('portfolio_performance/', views.portfolio_performance_view, name='portfolio_performance'),
    path('debt/', views.debt_view, name='debt'),  # Added missing trailing slash
    path('income_and_expenses/', views.income_and_expenses_view, name='income_and_expenses'),  # Added missing trailing slash
    path('artificial_intelligence/', views.artificial_intelligence_view, name='artificial_intelligence'),
    path('forecasting/', views.forecasting_view, name='forecasting'),
]
