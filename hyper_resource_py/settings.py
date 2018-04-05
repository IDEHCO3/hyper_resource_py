"""
Django settings for hyper_resource_py project.

Generated by 'django-admin startproject' using Django 1.11.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-&t&pd%%((qdof5m#=cp-=-3q+_+pjmu(ru_b%e+6u#ft!yb$$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

APPEND_SLASH = True
# Application definition
TOKEN_NEED= False

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'rest_framework',
    'rest_framework_gis',
    'corsheaders',
    'hyper_resource',
    'user_management',
    'controle_adesao',
    'controle',
    'bcim',
]

MIDDLEWARE_CLASSES = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'hyper_resource_py.urls'

CORS_ALLOW_HEADERS = (
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'content-location',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'link',
)
CORS_ORIGIN_ALLOW_ALL = True
CORS_EXPOSE_HEADERS = ['accept',
                       'accept-encoding',
                       'authorization',
                       'content-type',
                       'content-location',
                       'dnt',
                       'origin',
                       'user-agent',
                       'x-csrftoken',
                       'x-requested-with',
                       'x-access-token',
                       'access-control-allow-origin',
                       'link',
                       ]

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

WSGI_APPLICATION = 'hyper_resource_py.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

if not 'IP_SGBD' in os.environ:
    #os.environ['IP_SGBD'] = '127.0.0.1'
    os.environ['IP_SGBD'] = '172.30.10.86'

if not 'PORT_SGBD' in os.environ:
    #os.environ['PORT_SGBD'] = '2345'
    os.environ['PORT_SGBD'] = '54322'

if not 'DB_NAME' in os.environ:
    #os.environ['DB_NAME'] = 'postgres'
    os.environ['DB_NAME'] = 'gis'

if not 'DB_USERNAME' in os.environ:
    #os.environ['DB_USERNAME'] = 'postgres'
    os.environ['DB_USERNAME'] = 'ccar_prod'

if not 'DB_PASSWORD' in os.environ:
    #os.environ['DB_PASSWORD'] = 'desenv'
    os.environ['DB_PASSWORD'] = 'ccar_prod'

ip_sgbd = os.environ['IP_SGBD']
port_sgbd = os.environ['PORT_SGBD']
db_name = os.environ['DB_NAME']
user = os.environ['DB_USERNAME']
password = os.environ['DB_PASSWORD']


DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'OPTIONS': {
            'options': '-c search_path=ggt,bcim,public,administrativo,user_management',

        },

        'HOST': ip_sgbd,
        'PORT': port_sgbd,
        'NAME': db_name,
        'USER': user,
        'PASSWORD': password
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}
REST_FRAMEWORK = {
    #'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',)
}
