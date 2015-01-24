# -*- coding: utf-8 -*-
# Django settings for sopler project.

import os.path
PROJECT_DIR = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))

DEBUG = True
TEMPLATE_DEBUG = DEBUG
SESSION_SAVE_EVERY_REQUEST = True
#Set "True" if all non-SSL requests should be permanently redirected to SSL.
SECURE_SSL_REDIRECT = False
# Setting to an integer number of seconds
#It is recommended to set the max-age to a big value like 31536000 (12 months) or 63072000 (24 months).
SECURE_HSTS_SECONDS = 31536000
# HTTP Strict Transport Security.
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# Prevent framing of your pages and protect them from clickjacking.
SECURE_FRAME_DENY = True
# Prevent the browser from guessing asset content types.
SECURE_CONTENT_TYPE_NOSNIFF = True
# Enable the browser’s XSS filtering protections.
SECURE_BROWSER_XSS_FILTER = True

SOCIAL_FRIENDS_USING_ALLAUTH = True

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.join(PROJECT_DIR, "../database.db"),                      # Or path to database file if using sqlite3.
        #'NAME': '',
        # The following settings are not used with sqlite3:
        #'USER': '',
        #'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}



# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['*']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_DIR, "../static/"),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
# Ensure that you’re using a long, random and unique "SECRET_KEY"
SECRET_KEY = 'Enter_Here_A_Long_Random_And_Unique_Key_&^%$&!!'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    "django.core.context_processors.request",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.contrib.messages.context_processors.messages",
    #"allauth.account.context_processors.account",
    "allauth.socialaccount.context_processors.socialaccount",
    'django.core.context_processors.request',
)

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'djangosecure.middleware.SecurityMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    #'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'sopler.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'sopler.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_DIR, "../templates/"),

)

INSTALLED_APPS = (

    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    #'django_admin_bootstrapped',
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # Available Social Account Providers
    'allauth.socialaccount.providers.twitter',
    'allauth.socialaccount.providers.persona',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
     #'allauth.socialaccount.providers.openid',
    'core',
    # Extra Security Features.
    'djangosecure',
    # Data migration.
    'south',
    # Faving and unfaving lists.
    'favit',
    # Webservice API framework for Django.
    #'tastypie',
    # Fetches your friends from different social-networks.
    'social_friends_finder',
    'embed_video',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
try:
    from local_settings import *
except ImportError:
    pass
