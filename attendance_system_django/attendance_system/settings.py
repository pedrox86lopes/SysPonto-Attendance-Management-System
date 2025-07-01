# Railway Production Settings
import os
import dj_database_url

# Detect Railway environment
if 'RAILWAY_ENVIRONMENT' in os.environ or 'DATABASE_URL' in os.environ:
    DEBUG = False
    
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
    
    # Add whitenoise middleware safely
    if 'whitenoise.middleware.WhiteNoiseMiddleware' not in MIDDLEWARE:
        MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
    
    # Security settings
    ALLOWED_HOSTS = [
        '.railway.app',
        'localhost',
        '127.0.0.1',
        '.up.railway.app',  # Railway's new domain
    ]
    
    # Use environment secret key or fallback
    SECRET_KEY = os.environ.get('SECRET_KEY', SECRET_KEY)
    
    # Channel Layers for production
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels.layers.InMemoryChannelLayer'
        }
    }