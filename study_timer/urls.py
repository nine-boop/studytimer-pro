from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Your core app pages (Dashboard, etc.)
    path('', include('core.urls')), 
    
    # The new django-allauth routes for Google Login
    path('accounts/', include('allauth.urls')),
]