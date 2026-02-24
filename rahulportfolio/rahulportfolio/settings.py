"""
Django settings for rahulportfolio project.
Production-ready configuration for Render deployment.
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
# Load SECRET_KEY from environment variable
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-fallback-dev-key-change-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False').lower() in ('true', '1', 'yes')

# ALLOWED_HOSTS - Configure for Render deployment
# Get from environment variable or use Render's default domain
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS = [RENDER_EXTERNAL_HOSTNAME, 'localhost', '127.0.0.1']
else:
    # Fallback for local development - add your custom domains here
    ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Application definition

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

# Database configuration for production
# Uses SQLite by default, but can be configured for PostgreSQL on Render
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# For PostgreSQL on Render, uncomment and configure below:
# import dj_database_url
# DATABASES = {
#     'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
# }

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

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
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Authentication settings
LOGIN_URL = 'portfolio:login'
LOGIN_REDIRECT_URL = 'portfolio:dashboard'
LOGOUT_REDIRECT_URL = 'portfolio:home'

# Session settings
SESSION_COOKIE_AGE = 60 * 60 * 24 * 7  # 1 week
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# =============================================================================
# SECURITY SETTINGS FOR PRODUCTION (Required by check --deploy)
# =============================================================================

# Force HTTPS/SSL - Redirect all HTTP requests to HTTPS
SECURE_SSL_REDIRECT = os.environ.get('SECRET_SSL_REDIRECT', 'True').lower() in ('true', '1', 'yes')

# HSTS (HTTP Strict Transport Security) - Forces browsers to use HTTPS
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Secure cookies - Only send cookies over HTTPS
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Prevent content type sniffing
SECURE_CONTENT_TYPE_NOSNIFF = True

# Browser's X-Frame-Options for clickjacking protection
X_FRAME_OPTIONS = 'DENY'

# HTTPS for the entire session (optional - uncomment if needed)
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
