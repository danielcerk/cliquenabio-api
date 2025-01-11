from pathlib import Path
from urllib.parse import urlparse
from datetime import timedelta
import os

from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'api',
    'api.analytics',
    'api.auth',
    'api.links',
    'api.product',
    'api.profile_user',
    'api.subscriptions',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    'dj_rest_auth'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

AUTH_USER_MODEL = 'api_custom_auth.UserProfile'

WSGI_APPLICATION = 'app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

if DEBUG:

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

else:

    tmpPostgres = urlparse(os.getenv("DATABASE_URL"))

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': tmpPostgres.path.replace('/', ''),
            'USER': tmpPostgres.username,
            'PASSWORD': tmpPostgres.password,
            'HOST': tmpPostgres.hostname,
            'PORT': 5432,
        }
    }


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'suporteconstsoft@gmail.com'
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True

STATIC_URL = 'static/'

DATE_FORMAT = 'd/m/Y' 
DATETIME_FORMAT = 'd/m/Y às H:i:s'

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [

    'http://localhost:5173'

]

if DEBUG:

    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False

else:

    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

CSRF_TRUSTED_ORIGINS = ['http://localhost:5173']

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 5
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=180),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=50),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',

    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

if DEBUG:

    STRIPE_TEST_PUBLIC_KEY = 'pk_test_51Pk3r3RtCzJ3GhkZLAt3ExMMW58j7x7GGZcBFftxpwjBjPk7oUW7PY8IhVjHd4xzfdcoSke8vCchWjrMJj7gJB3200594SyOXM'
    STRIPE_TEST_SECRET_KEY = 'sk_test_51Pk3r3RtCzJ3GhkZQNM5EUlMrRAvdULQ9Fsylw5ib5C1PN1o3VyP6hSIkQJWgjpIyZsY2rZKSGIzCQDnvvN18Fq000X0BQZm8J'

    # STRIPE_PRICING_TABLE_ID_PT = "prctbl_1Q5bRuRtCzJ3GhkZ2ihhOcbt"
    # STRIPE_PRICING_TABLE_ID_EN = "prctbl_1Q5bUJRtCzJ3GhkZnB8VKPuS"

    STRIPE_LIVE_MODE = False

    STRIPE_PUBLIC_KEY = STRIPE_TEST_PUBLIC_KEY
    STRIPE_SECRET_KEY = STRIPE_TEST_SECRET_KEY

    STRIPE_ENDPOINT_SECRET = 'whsec_4e6e00b81344ac1ca8aaac4f5ea07d78c6d7da97f65d356509067e1daf5803ad'

    PLAN_CONEXAO_PROD_ID = 'price_1QenYmRtCzJ3GhkZR6gpJWAM'
    PLAN_INFLUENCIA_PROD_ID = 'price_1Qena9RtCzJ3GhkZurfW7vG8'

else:

    STRIPE_LIVE_PUBLIC_KEY ='pk_live_51Pk3r3RtCzJ3GhkZwr5qWgm7mPdwba0WPgysGC8po3OogywN80I0nL1aaF5U7z0hKTXkA4vIOdBmFGn1973QLnJm000O7tEFCg'
    STRIPE_LIVE_SECRET_KEY ='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'

    # STRIPE_PRICING_TABLE_ID_PT = "prctbl_1Q5cYkRtCzJ3GhkZGAdbkpcM"
    # STRIPE_PRICING_TABLE_ID_EN = "prctbl_1Q5cZZRtCzJ3GhkZDZ70MdJE"

    STRIPE_LIVE_MODE = True

    STRIPE_PUBLIC_KEY = STRIPE_LIVE_PUBLIC_KEY
    STRIPE_SECRET_KEY = STRIPE_LIVE_SECRET_KEY

    PLAN_CONEXAO_PROD_ID = 'price_1QenaDRtCzJ3GhkZXDPz4J12'
    PLAN_INFLUENCIA_PROD_ID = 'price_1Qena9RtCzJ3GhkZurfW7vG8'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
