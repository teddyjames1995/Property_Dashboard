from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('Property_Dashboard_app/', include('Property_Dashboard_app.urls')),
    path('', RedirectView.as_view(url='/Property_Dashboard_app/', permanent=False)),  # Add this line
]
