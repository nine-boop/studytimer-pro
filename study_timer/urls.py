from django.contrib import admin
from django.urls import path, include
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard_view, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('verify-otp/', views.verify_otp_view, name='verify_otp'),
    path('logout/', views.logout_view, name='logout'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('save-distraction/', views.save_distraction, name='save_distraction'),
    path('save-session/', views.save_session, name='save_session'),
    path('update-settings/', views.update_settings, name='update_settings'),
    
    # --- NEW: The Data Analytics Dashboard! 📊 ---
    path('reports/', views.reports_view, name='reports'),
    
    path('accounts/', include('allauth.urls')),
]
