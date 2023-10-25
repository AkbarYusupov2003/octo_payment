import os
import environ
from pathlib import Path


env = environ.Env(
    HOST=(str, "http://127.0.0.1:8000"),
    SECRET_KEY=(str, "django-insecure-sh9_9vtf(=)62yk7dv9ewv8f#x4!3lx8_i&aormj$$--&l77n!"),
    DEBUG=(bool, True),
    ALLOWED_HOSTS=(list, ("*", )),
    OCTO_SHOP_ID=(int, 5806),
    OCTO_SECRET_KEY=(str, "c86f22ed-17ca-46aa-86c6-a45c402fde3f"),
)

BASE_DIR = Path(__file__).resolve().parent.parent

HOST = env("HOST")

SECRET_KEY = env("SECRET_KEY")

DEBUG = env("DEBUG")

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # custom apps
    # my apps
    "payment",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
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

WSGI_APPLICATION = 'config.wsgi.application'

# DATABASES = {
#     "default": {
#         "ENGINE": env("DB__ENGINE", default="django.db.backends.sqlite3"),
#         "NAME": env("DB__NAME", default=os.path.join(BASE_DIR, "db.sqlite3")),
#         "USER": env("DB__USER", default=None),
#         "PASSWORD": env("DB__PASSWORD", default=None),
#         "HOST": env("DB__HOST", default=None),
#         "PORT": env("DB__PORT", default=None),
#     }
# }

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "octo_payment",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "localhost",
        "PORT": "5432",
    }
}

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

TIME_ZONE = 'Asia/Tashkent'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'
# STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)
# STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

OCTO_SHOP_ID = env("OCTO_SHOP_ID")
OCTO_SECRET_KEY = env("OCTO_SECRET_KEY")

