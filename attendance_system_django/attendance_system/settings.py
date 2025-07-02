import dj_database_url
import os

# Detect Railway environment
if 'RAILWAY_ENVIRONMENT' in os.environ or 'DATABASE_URL' in os.environ:
    DEBUG = False
    
    # Security settings first
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    # Safe database configuration
    if 'DATABASE_URL' in os.environ:
        DATABASES['default'] = dj_database_url.parse(
            os.environ['DATABASE_URL'],
            conn_max_age=600,
            conn_health_checks=True,
        )
    else:
        # Fallback to SQLite if no DATABASE_URL (during initial deploy)
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }
    
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
    
    # Channel Layers for production (use Redis if available, fallback to InMemory)
    redis_url = os.environ.get('REDIS_URL')
    if redis_url:
        CHANNEL_LAYERS = {
            'default': {
                'BACKEND': 'channels_redis.core.RedisChannelLayer',
                'CONFIG': {
                    "hosts": [redis_url],
                },
            },
        }
    else:
        CHANNEL_LAYERS = {
            'default': {
                'BACKEND': 'channels.layers.InMemoryChannelLayer'
            }
        }
    
    # Logging configuration for Railway
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
        },
        'loggers': {
            'django': {
                'handlers': ['console'],
                'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
                'propagate': False,
            },
        },
    }