from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('properties/', include('Property_Dashboard_app.urls')),  # Include your app's URLs
]
