from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('properties/', include('Property_Dashboard_app.urls')),
    re_path(r'^$', RedirectView.as_view(url='/properties/', permanent=False)),
]
