from pathlib import Path
import os
import environ

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# env
env = environ.Env()
environ.Env.read_env()


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_6xa1oi)^%lqsl&&k$q#3cembbb+al3l&4xv%-7r$@n4_p1m&5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
]

# CUSTOM_APP = [
#     'mferp.apps.MasterTableConfig',
#     'mferp.apps.UserConfig',
#     'mferp.apps.DropsdownConfig',
#     'mferp.apps.EmployeeConfig',
    
#     # 'mferp.auth.user',
#     'django_extensions',
# ]
CUSTOM_APP = [
    'mferp.apps.MasterTableConfig',
    'mferp.apps.UserConfig',
    'mferp.apps.DropsdownConfig',
    'mferp.apps.AddressConfig',
    'mferp.apps.UploadConfig',
    'hr.apps.HrTableConfig',
    'employee.apps.ProfileConfig',
    # 'mferp.auth.user',
    'django_extensions',
]


THIRD_PARTY_APP = ["rest_framework", "oauth2_provider", "corsheaders", "graphene_django",]
INSTALLED_APPS.extend(CUSTOM_APP)
INSTALLED_APPS.extend(THIRD_PARTY_APP)
MIDDLEWARE = [
    # 'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ops.urls'

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

WSGI_APPLICATION = 'ops.wsgi.application'
AUTH_USER_MODEL = "user.Account"
# AUTH_USER_MODEL = "user.CustomUser"


host = env("DATABASE_HOST")
password = env("PASSWORD")
user = env("USER")
name = env("NAME")

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'kieterp',
#         'USER': 'root',
#         'PASSWORD':'MyStrongPassword1234$',
#         'HOST':'localhost',
#         'PORT':'3306',
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'kieterp2',
        'USER': 'harry',
        'PASSWORD':'MyStrongPassword1234$',
        'HOST':'localhost',
        'PORT':'3306',
    }
}
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': name,
#         'USER': user,
#         'PASSWORD': password,
#         'HOST':host,
#         'PORT':'3306',
#     }
# }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': name,
#         'USER': user,
#         'PASSWORD':password,
#         'HOST':host,
#         'PORT':'3306',
#     }
# }



# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'



# OAuth2 Setting Configuration
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "oauth2_provider.contrib.rest_framework.OAuth2Authentication",
        "rest_framework.authentication.TokenAuthentication",
    )
}

# Token Expire Time
OAUTH2_PROVIDER = {"ACCESS_TOKEN_EXPIRE_SECONDS": 8500}

CORS_ALLOW_METHODS = [ 'GET', 'POST', 'OPTIONS', 'PATCH','PUT', 'DELETE' ] 
# CORS_ALLOW_HEADERS = [ 'Content-Type', 'Content-Disposition',] 
# Add 'Content-Disposition' to allow this header # Add other custom headers here ]

CORS_ORIGIN_ALLOW_ALL = True

BASE_URL = "http://127.0.0.1:8000"

# Email Configuration
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_USE_TLS = True
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = "testerp053@gmail.com"
MAIL_SENDING_USER = "ERP 3.0 <testerp053@gmail.com>"
# EMAIL_HOST_PASSWORD = env("GMAIL_PASSWORD")
EMAIL_HOST_PASSWORD = "lrdo afqo wbby kfog"
EMAIL_PORT = 587

MEDIA_ROOT = os.path.join( "media")
MEDIA_URL = "/media/"