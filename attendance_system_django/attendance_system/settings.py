import dj_database_url
import os
from pathlib import Path

# Define BASE_DIR first (required for database path)
BASE_DIR = Path(__file__).resolve().parent.parent

# Detect Railway environment
if 'RAILWAY_ENVIRONMENT' in os.environ or 'DATABASE_URL' in os.environ:
    DEBUG = False
    
    # Security settings first
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    # Define DATABASES first before trying to modify it
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    
    # Safe database configuration
    if 'DATABASE_URL' in os.environ:
        DATABASES['default'] = dj_database_url.parse(
            os.environ['DATABASE_URL'],
            conn_max_age=600,
            conn_health_checks=True,
        )
    
    # Define MIDDLEWARE first before trying to modify it
    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]
    
    # Static files configuration
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    
    # Add whitenoise middleware safely
    if 'whitenoise.middleware.WhiteNoiseMiddleware' not in MIDDLEWARE:
        MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
    
    # Railway-specific hosts
    ALLOWED_HOSTS = [
        '.railway.app',
        '.up.railway.app',
        'localhost',
        '127.0.0.1',
    ]
    
    # Add your specific Railway URL if you know it
    railway_url = os.environ.get('RAILWAY_STATIC_URL', '').replace('https://', '').replace('http://', '')
    if railway_url:
        ALLOWED_HOSTS.append(railway_url)
    
    # CSRF trusted origins (For railway)
    CSRF_TRUSTED_ORIGINS = [
        'https://*.railway.app',
        'https://*.up.railway.app',
    ]
    
    # Channel Layers for production
    redis_url = os.environ.get('REDIS_URL')
    if redis_url:
        print(f"✅ Using Redis for Channel Layers: {redis_url}")
        CHANNEL_LAYERS = {
            'default': {
                'BACKEND': 'channels_redis.core.RedisChannelLayer',
                'CONFIG': {
                    "hosts": [redis_url],
                    "capacity": 1500,
                    "expiry": 10,
                    "group_expiry": 86400,
                    "symmetric_encryption_keys": [SECRET_KEY],
                },
            },
        }
    else:
        print("⚠️ No Redis URL found, using InMemoryChannelLayer")
        CHANNEL_LAYERS = {
            'default': {
                'BACKEND': 'channels.layers.InMemoryChannelLayer',
                'CONFIG': {
                    "capacity": 300,
                    "expiry": 60,
                }
            }
        }
    
    # Enhanced logging for WebSocket debugging
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
                'style': '{',
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'verbose',
            },
        },
        'root': {
            'handlers': ['console'],
        },
        'loggers': {
            'django': {
                'handlers': ['console'],
                'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
                'propagate': False,
            },
            'channels': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': False,
            },
            'daphne': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': False,
            },
            'attendance': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': False,
            },
        },
    }

    # Required Django settings for production-only setup (ADDED DAPHNE)
    INSTALLED_APPS = [
        'daphne', 
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'channels',
        'core',
        'courses',
        'attendance',
        'django_extensions',
    ]

    AUTH_USER_MODEL = 'core.User'
    
    STATIC_URL = '/static/'
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'static_dev'),
    ]
    
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')
    
    FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
    DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
    
    LOGIN_REDIRECT_URL = '/'
    LOGOUT_REDIRECT_URL = '/'
    LOGIN_URL = 'login'
    
    ASGI_APPLICATION = 'attendance_system.asgi.application'
    
    from django.contrib.messages import constants as messages
    MESSAGE_TAGS = {
        messages.DEBUG: 'secondary',
        messages.INFO: 'info',
        messages.SUCCESS: 'success',
        messages.WARNING: 'warning',
        messages.ERROR: 'danger',
    }
    
    ROOT_URLCONF = 'attendance_system.urls'
    
    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [BASE_DIR / 'templates'],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]
    
    WSGI_APPLICATION = 'attendance_system.wsgi.application'
    
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
    
    LANGUAGE_CODE = 'en-us'
    TIME_ZONE = 'Europe/Lisbon'
    USE_I18N = True
    USE_TZ = True
    
    STATIC_URL = 'static/'
    STATICFILES_FINDERS = [
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    ]
    
    DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

else:
    # Fallback: If not in Railway environment, raise an error
    raise RuntimeError(
        "This settings file is for Railway production only. "
        "Set RAILWAY_ENVIRONMENT=production in your environment variables."
    )