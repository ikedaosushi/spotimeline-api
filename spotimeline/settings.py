import os
import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'r3+$wti2%xz2i1mt!b&eeeai(%4*t#hulpzkg2m&hle(&v8#!0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["spotimeline-api.herokuapp.com"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_social_auth',
    'djoser',
    'social_django',
    'django_extensions',
    "django_cron",
    'timeline',
    'user_profile',
    'apiv1'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

CRON_CLASSES = [
    'timeline.cron.FetchTracks',
]

CORS_ORIGIN_ALLOW_ALL = False

CORS_ORIGIN_WHITELIST = (
    os.environ['WEB_ORIGIN'],
)

REST_FRAMEWORK = {
    # 'DEFAULT_PERMISSION_CLASSES': [
    #     'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    # ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ]
}
from datetime import timedelta

SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("JWT",),
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30)
}

ROOT_URLCONF = 'spotimeline.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'spotimeline.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

if os.environ['SPOTIMELINE_ENV'] == "heroku":
    db_from_env = dj_database_url.config(conn_max_age=600, ssl_require=True)
    DATABASES = {
        'default': db_from_env
    }
    # DATABASES['default'].update(db_from_env)
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'

AUTHENTICATION_BACKENDS = {
    'django.contrib.auth.backends.ModelBackend',
    'social_core.backends.spotify.SpotifyOAuth2'
}

SOCIAL_AUTH_URL_NAMESPACE = 'social'

SOCIAL_AUTH_SPOTIFY_KEY = os.environ['SPOTIFY_CLIENT_ID']
SOCIAL_AUTH_SPOTIFY_SECRET = os.environ['SPOTIFY_CLIENT_SECRET']
# SOCIAL_AUTH_SPOTIFY_SCOPE = ['user-read-email', 'user-library-read']
REST_SOCIAL_OAUTH_ABSOLUTE_REDIRECT_URI = os.environ['WEB_ORIGIN'] + "/auth/complete"
REST_SOCIAL_DOMAIN_FROM_ORIGIN = False

LOGIN_URL = '/'
LOGIN_REDIRECT_URL = '/api/v1/auth/users/me'
