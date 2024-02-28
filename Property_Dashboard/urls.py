from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Property_Dashboard_app.urls')),  # Directly include your app's URLs
]
