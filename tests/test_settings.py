import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'fake-key'

INSTALLED_APPS = [
    'grappelli.dashboard',
    'grappelli',
    'adminactions',
    'filebrowser',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tagging',
    'tinymce',

    'rotv_apps.blog',
    'rotv_apps.heros',
    'rotv_apps.navigations',
    'rotv_apps.partners',
    'rotv_apps.program',
    'rotv_apps.tag_search',
    'rotv_apps.shortener',
]

ROOT_URLCONF = 'tests.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
    },
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

STATIC_URL = '/static/' # this is required for django-tinymce module

PATRONAGE_MANAGERS = ['some@email.com', ]
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
