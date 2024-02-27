from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Property_Dashboard_app/', include('Property_Dashboard_app.urls')),  # Updated path
]
