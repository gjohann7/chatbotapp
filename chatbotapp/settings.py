import os
import django_heroku
from decouple import config, Csv
import dj_database_url
import whitenoise

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Activate Django-Heroku.
# django_heroku.settings(locals())

SECRET_KEY = config('SECRET_KEY')

DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'chatbotapp.accounts',
    'chatbotapp.chatbot',
    'chatbotapp.core'
]

MIDDLEWARE_CLASSES = ('whitenoise.middleware.WhiteNoiseMiddleware',)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'chatbotapp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR + "/chatbotapp/templates"],
        # 'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'loaders': [
                ('django.template.loaders.cached.Loader', [
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                ]),
            ],
        },
    },
]

WSGI_APPLICATION = 'chatbotapp.wsgi.application'

# Database
DATABASES = {
    'default': dj_database_url.config(default=config('DATABASE_URL'))
}
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': config('DB_NAME'),
#         'USER': config('DB_USER'),
#         'PASSWORD': config('DB_PASSWORD'),
#         'HOST': config('DB_HOST'),
#         'PORT': config('DB_PORT'),
#     }
# }

# Static files (CSS, JavaScript, Images)
#STATIC_TMP = os.path.join(BASE_DIR, 'static')
FORCE_SCRIPT_NAME = ''
STATIC_URL = FORCE_SCRIPT_NAME + '/static/'
STATICFILES_DIRS = [BASE_DIR + "/chatbotapp/static/"]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_STORAGE = 'whitenoise.django.CompressedManifestStaticFilesStorage'
#STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

#os.makedirs(STATIC_TMP, exist_ok=True)

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'chatbotapp.core.utils.CustomMinimumLengthValidator',
    },
    {
        'NAME': 'chatbotapp.core.utils.CustomNumericPasswordValidator',
    }
]

# Internationalization
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# EMAIL
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'chatbot.app.contact@gmail.com'
EMAIL_FROM = 'chatbot.app.contact@gmail.com'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'chatbot.app.contact@gmail.com'
EMAIL_HOST_PASSWORD = config('EMAIL_PASSWORD')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
CONTACT_EMAIL = 'chatbot.app.contact@gmail.com'

# Auth
LOGIN_URL = 'core:login'
LOGIN_REDIRECT_URL = 'chatbot:conversation'
LOGOUT_URL = 'core:logout'
AUTH_USER_MODEL = 'accounts.User'
