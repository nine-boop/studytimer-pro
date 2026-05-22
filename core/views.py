from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.db.models import Count
from datetime import date, timedelta
import json
import random
from .models import Distraction, StudySession

# ==========================================
# DASHBOARDS & DATA ANALYTICS
# ==========================================

@login_required(login_url='login')
def dashboard_view(request):
    if request.user.is_staff or request.user.is_superuser:
        total_users = User.objects.filter(is_staff=False).count()
        all_students = User.objects.filter(is_staff=False)
        return render(request, 'admin_dashboard.html', {'total_users': total_users, 'students': all_students})
    
    today = date.today()
    today_sessions = StudySession.objects.filter(user=request.user, date_completed__date=today)
    
    context = {
        'today_date': timezone.now().strftime("%A, %B %d, %Y"),
        'pomodoros_today': today_sessions.count(),
        'focus_time': f"{(sum(s.duration_minutes for s in today_sessions)) // 60}h",
    }
    return render(request, 'dashboard.html', context)

@login_required(login_url='login')
def reports_view(request):
    all_sessions = StudySession.objects.filter(user=request.user).order_by('-date_completed')
    total_minutes = sum(session.duration_minutes for session in all_sessions)
    user_distractions = Distraction.objects.filter(user=request.user)
    
    context = {
        'total_hours': round(total_minutes / 60, 1),
        'total_sessions': all_sessions.count(),
        'recent_sessions': all_sessions[:10],
        'distractions_count': user_distractions.count(),
        'top_distractions': user_distractions.values('category').annotate(count=Count('category')).order_by('-count')[:5]
    }
    return render(request, 'reports.html', context)

# ==========================================
# AJAX SAVING & SETTINGS
# ==========================================

@login_required
def update_settings(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = request.user
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        if data.get('password'): user.set_password(data.get('password'))
        user.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def save_distraction(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        Distraction.objects.create(user=request.user, name=data.get('text'), category=data.get('category', 'Other'))
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def save_session(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        StudySession.objects.create(user=request.user, duration_minutes=data.get('duration', 25), session_type=data.get('type', 'study'))
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

# ==========================================
# AUTHENTICATION ENGINE (STABLE)
# ==========================================

def register_view(request):
    if request.method == 'POST':
        username, email, password = request.POST.get('username'), request.POST.get('email'), request.POST.get('password')
        otp_code = str(random.randint(1000, 9999))
        
        # --- MAIL ENGINE DISABLED FOR STABILITY ---
        # We save the OTP to the session so the user can still verify it
        request.session.update({'temp_user': {'username': username, 'email': email, 'password': password}, 'registration_otp': otp_code})
        
        # DURING DEMO: Tell your team the code is in the logs or print it to console
        print(f"DEBUG - Registration OTP: {otp_code}") 
        
        return redirect('verify_otp')
    return render(request, 'register.html')

def verify_otp_view(request):
    if request.method == 'POST':
        entered_otp = "".join([request.POST.get(f'otp{i}', '') for i in range(1, 5)])
        if entered_otp == request.session.get('registration_otp'):
            u = request.session.get('temp_user')
            User.objects.create_user(username=u['username'], email=u['email'], password=u['password']).save()
            return redirect('login')
        messages.error(request, "Invalid code! 🎀")
    return render(request, 'verify_otp.html')

def login_view(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user:
            login(request, user)
            return redirect('dashboard')
        messages.error(request, "Invalid credentials! 🐾")
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def forgot_password_view(request):
    return render(request, 'forgot_password.html')
