from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from datetime import date, timedelta
import json
import random
from .models import Distraction, StudySession

@login_required(login_url='login')
def dashboard_view(request):
    if request.user.is_staff or request.user.is_superuser:
        total_users = User.objects.filter(is_staff=False).count()
        all_students = User.objects.filter(is_staff=False)
        context = {'total_users': total_users, 'students': all_students}
        return render(request, 'admin_dashboard.html', context)
    
    today_date_str = timezone.now().strftime("%A, %B %d, %Y")
    today = date.today()

    # Calculate real stats
    today_sessions = StudySession.objects.filter(user=request.user, session_type='study', date_completed__date=today)
    pomodoros_today = today_sessions.count()
    total_minutes = sum(s.duration_minutes for s in today_sessions)
    focus_time_str = f"{total_minutes // 60}h {total_minutes % 60}m"

    today_distractions = Distraction.objects.filter(user=request.user, time_logged__date=today)
    distractions_today = today_distractions.count()

    # Calculate streak
    sessions = StudySession.objects.filter(user=request.user, session_type='study').values_list('date_completed', flat=True).order_by('-date_completed')
    completed_dates = sorted(list(set([timezone.localdate(d) for d in sessions])), reverse=True)
    current_streak = 0
    yesterday = today - timedelta(days=1)
    
    if completed_dates:
        if completed_dates[0] == today or completed_dates[0] == yesterday:
            current_streak = 1
            for i in range(len(completed_dates) - 1):
                if completed_dates[i] - completed_dates[i+1] == timedelta(days=1):
                    current_streak += 1
                else:
                    break

    all_distractions = Distraction.objects.filter(user=request.user).order_by('-time_logged')
    recent_distractions = all_distractions[:5]
    
    context = {
        'distractions': recent_distractions,
        'all_distractions_export': all_distractions,
        'current_streak': current_streak,
        'today_date': today_date_str,
        'focus_time': focus_time_str,
        'pomodoros_today': pomodoros_today,
        'distractions_today': distractions_today
    }
    return render(request, 'dashboard.html', context)

@login_required
def update_settings(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        new_username = data.get('username')
        new_email = data.get('email')
        new_password = data.get('password')
        
        user = request.user
        if new_username and new_username != user.username:
            if User.objects.filter(username=new_username).exists():
                return JsonResponse({'status': 'error', 'message': 'Username already taken!'})
            user.username = new_username
        
        if new_email:
            user.email = new_email
            
        if new_password and new_password.strip() != "":
            user.set_password(new_password)
            user.save()
            from django.contrib.auth import update_session_auth_hash
            update_session_auth_hash(request, user)
        else:
            user.save()
            
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def save_distraction(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        distraction_text = data.get('text')
        category_label = data.get('category', 'Other')
        dist = Distraction.objects.create(user=request.user, name=distraction_text, category=category_label)
        return JsonResponse({'status': 'success', 'time': dist.time_logged.strftime("%I:%M %p")})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def save_session(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        duration = data.get('duration', 25)
        sType = data.get('type', 'study')
        StudySession.objects.create(user=request.user, duration_minutes=duration, session_type=sType)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        otp_code = str(random.randint(1000, 9999))
        request.session['temp_user'] = {'username': username, 'email': email, 'password': password}
        request.session['registration_otp'] = otp_code
        return redirect('verify_otp')
    return render(request, 'register.html')

def verify_otp_view(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp1','') + request.POST.get('otp2','') + request.POST.get('otp3','') + request.POST.get('otp4','')
        if entered_otp == request.session.get('registration_otp'):
            user_data = request.session.get('temp_user')
            user = User.objects.create_user(username=user_data['username'], email=user_data['email'], password=user_data['password'])
            user.save()
            return redirect('login')
    return render(request, 'verify_otp.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def forgot_password_view(request):
    return render(request, 'forgot_password.html')