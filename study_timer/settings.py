from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Security Warning: Keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-safe-pastel-key-replace-me-in-strict-production'

# Security Warning: Don't run with debug turned on in production!
DEBUG = True

# --- PRODUCTION HOST MANAGEMENT 🌸 ---
# Allows your local machine and your future Render web link to run the app safely.
ALLOWED_HOSTS = ['.onrender.com', '127.0.0.1', 'localhost']


# --- 1. INSTALLED APPLICATION REGISTRY ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Core Feature App
    'core',
    
    # Google Allauth Secure Framework Packages 🎀
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
]


# --- 2. MIDDLEWARE PIPELINE ---
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Production static styling pipeline injector ☁️
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    # Allauth Identity Session Management Middleware
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'study_timer.urls'


# --- 3. TEMPLATES ENGINE CONFIGURATION ---
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'study_timer.wsgi.application'


# --- 4. INTERNAL SQLITE CORE DATABASE ENGINE 🍓 ---
# Bulletproof data layer engine mapped directly within the Pathlib project directory tree.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# --- 5. PASSWORD VALIDATION ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]


# --- 6. INTERNATIONALIZATION CONFIGS ---
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# --- 7. STATIC AND STYLING ASSET TRACKERS ---
STATIC_URL = 'static/'
# Directory where WhiteNoise gathers all static styles during live deployment build triggers
STATIC_ROOT = BASE_DIR / 'staticfiles'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ========================================================
# 8. GOOGLE OAUTH SECURITY PROFILE CONSTANTS 🐾
# ========================================================
SITE_ID = 1

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Destination routes mapped following active credentials authorization state updates
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'login'

# Skips strict verification redirects to create immediate login records smoothly
SOCIALACCOUNT_LOGIN_ON_GET = True
ACCOUNT_EMAIL_VERIFICATION = 'none'
# --- Bypassing SQLite for Google Login ---
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': os.environ.get('GOOGLE_CLIENT_ID', ''),
            'secret': os.environ.get('GOOGLE_CLIENT_SECRET', ''),
            'key': ''
        }
    }
}
}
