 # Django settings for scserver project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    #('me', ' ') ,('Your Name', 'your_email@domain.com'),
)

LOGIN_URL = '/'

MANAGERS = ADMINS
SERVER_NAME = 'btcserver'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': SERVER_NAME,                      # Or path to database file if using sqlite3.
        'USER': SERVER_NAME,                      # Not used with sqlite3.
        'PASSWORD': SERVER_NAME,                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True


import sys
import os
MEDIA_ROOT = os.path.join(sys.path[0], 'static')
MEDIA_URL = '/static/' 

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/static/admin-media/' 


# Make this unique, and don't share it with anybody.
SECRET_KEY = '0ve^l0fva883+*%@95oga5fmjj!&gn#3#938pc0=v+z5hrj5rf'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'webservice_tools.middleware.exception.WebServiceException',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'webservice_tools.middleware.response.ProvideResponse',
    'webservice_tools.logging.middleware.LoggingMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
 
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'backend.context_processors.base',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = ()
PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))    
for root, dirs, files in os.walk(PROJECT_PATH):
        if 'templates' in dirs:
            TEMPLATE_DIRS += (os.path.join(root, 'templates'),)


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'webservice_tools',
    'webservice_tools.apps.user',
    'south',
    'backend',
    'piston',
    'blackjack',
)


PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))
AUTH_PROFILE_MODULE = 'backend.Player' 
import logging.handlers
LOG_FILE = '%s/logs/log' % PROJECT_PATH
GLOBAL_LOG_LEVEL = logging.DEBUG
GLOBAL_LOG_HANDLERS = [logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=200000, backupCount=2)]


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}