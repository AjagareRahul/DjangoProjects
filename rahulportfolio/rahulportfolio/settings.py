"""
Django settings for rahulportfolio project.
Production-ready configuration for Render deployment.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# =============================================================================
# SECRET KEY - Load from environment variable (REQUIRED for production)
# =============================================================================
# SECURITY WARNING: keep the secret key used in production secret!
# Load SECRET_KEY from environment variable - MUST be set in production!
# For local development, use a default key
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-development-key-change-in-production')

# =============================================================================
# DEBUG MODE - Disable in production
# =============================================================================
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False').lower() in ('true', '1', 'yes')

# =============================================================================
# ALLOWED_HOSTS - Configure for Render deployment
# =============================================================================
# Get from environment variable or use Render's default domain
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS = [RENDER_EXTERNAL_HOSTNAME, 'localhost', '127.0.0.1']
else:
    # Fallback for local development - add your custom domains here
    allowed_hosts_env = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1')
    ALLOWED_HOSTS = [host.strip() for host in allowed_hosts_env.split(',') if host.strip()]

# =============================================================================
# Application definition
# =============================================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    # Local apps
    'portfolio',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # For static file serving
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Custom middleware
    'rahulportfolio.middleware.VisitorCountMiddleware',
    'rahulportfolio.middleware.LastVisitMiddleware',
]

ROOT_URLCONF = 'rahulportfolio.urls'

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
                # Custom context processors
                'rahulportfolio.context_processors.site_info',
                'rahulportfolio.context_processors.social_links',
                'rahulportfolio.context_processors.visitor_count',
            ],
            'libraries': {
                'portfolio_tags': 'portfolio.templatetags.portfolio_tags',
            },
        },
    },
]

WSGI_APPLICATION = 'rahulportfolio.wsgi.application'

# =============================================================================
# Database configuration for production (PostgreSQL on Render)
# =============================================================================
# Uses SQLite by default for development, PostgreSQL for production on Render
import dj_database_url

# Get the DATABASE_URL from environment variable (provided by Render for PostgreSQL)
DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    # PostgreSQL on Render - parse the DATABASE_URL
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600)
    }
else:
    # Fallback to SQLite for local development
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# =============================================================================
# Password validation
# =============================================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# =============================================================================
# Internationalization
# =============================================================================

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True

# =============================================================================
# Static files (CSS, JavaScript, Images)
# =============================================================================

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# WhiteNoise configuration for serving static files in production
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# =============================================================================
# Authentication settings
# =============================================================================

LOGIN_URL = 'portfolio:login'
LOGIN_REDIRECT_URL = 'portfolio:dashboard'
LOGOUT_REDIRECT_URL = 'portfolio:home'

# =============================================================================
# Session settings
# =============================================================================

SESSION_COOKIE_AGE = 60 * 60 * 24 * 7  # 1 week
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# =============================================================================
# SECURITY SETTINGS FOR PRODUCTION (Required by check --deploy)
# =============================================================================

# Force HTTPS/SSL - Disabled for local development
SECURE_SSL_REDIRECT = False

# HSTS (HTTP Strict Transport Security) - Disabled for local development
SECURE_HSTS_SECONDS = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False

# Secure cookies - Disabled for local development
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# Prevent content type sniffing - Disabled for local development
SECURE_CONTENT_TYPE_NOSNIFF = False

# Browser's X-Frame-Options for clickjacking protection
X_FRAME_OPTIONS = 'DENY'

# HTTPS for the entire session - Disabled for local development
SECURE_PROXY_SSL_HEADER = None

# =============================================================================
# Admin panel configuration
# =============================================================================

# Django admin panel site header
ADMIN_SITE_HEADER = "Rahul's Portfolio Admin"
ADMIN_SITE_TITLE = "Portfolio Admin"
ADMIN_INDEX_TITLE = "Welcome to Portfolio Admin"

# =============================================================================
# Logging configuration for production
# =============================================================================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
