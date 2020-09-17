# RENAME THIS FILE TO "local.py"

import os
from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '&q*=4+71zl5_e*i$+t+)a$8)49s$4^7l9mi60w@wu9bow$!$b8'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = os.path.join(BASE_DIR, "sent_emails")
