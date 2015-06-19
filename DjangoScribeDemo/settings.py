"""
Django settings for DjangoScribeDemo project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '%))jp0l@^2vcq-$4$(=6xvd+=7$(-_!7yj81jru12794q1zpiq'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    # %JFE+1 added to demo djangosuit
    'demo_djangosuit',
    'demo_django_fsm_admin',
    # %JFE+1 added for djangosuit
    'suit',
    # %JFE+1 added for djangosuit_redactor  extention
    'suit_redactor',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # %JFE+1 added for django_debug_toolbar
    'debug_toolbar',
    # %JFE+1 added for mptt
    'mptt',
    # %JFE+1 added for django-select2
    'django_select2',
    # %JFE+1 added for django-reversion
    'reversion',
    # %JFE+1 added for django-import-export
    'import_export',
    # %JFE+1 added for django-filer
    'filer',
    # %JFE+1 added for easy_thumbnails, required by django-filer
    'easy_thumbnails',
    # %JFE+1 added for django-fsm-admin
    'fsm_admin',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'DjangoScribeDemo.urls'

WSGI_APPLICATION = 'DjangoScribeDemo.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'



# %JFE+[ added for djangosuit and for django-fsm-admin
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
)
# %JFE+]



# %JFE+[ added for djangosuit
# see http://django-suit.readthedocs.org/en/develop/configuration.html
SUIT_CONFIG = {
    'ADMIN_NAME' : 'DjangoScribeDemo',
    'SHOW_REQUIRED_ASTERISK': True,
    'CONFIRM_UNSAVED_CHANGES': True,
    'SEARCH_URL': '',   # hide search form in menu
    'MENU_OPEN_FIRST_CHILD': False,
    'MENU_ICONS': {
        'sites': 'icon-leaf',
        'auth': 'icon-lock',
    },
    # 'MENU_EXCLUDE': ('auth.group', 'auth'),
    # 'MENU': (
    #
    #     # Keep original label and models
    #     'sites',
    #
    #     # Rename app and set icon
    #     {'app': 'auth', 'label': 'Authorization', 'icon': 'icon-lock'},
    #
    #     # Reorder app models
    #     {'app': 'auth', 'models': ('user', 'group')},
    #
    #     # Custom app, with models
    #     {'label': 'Settings', 'icon': 'icon-cog',
    #      'models': ('auth.user', 'auth.group')},
    #
    #     # Cross-linked models with custom name; Hide default icon
    #     {'label': 'Custom', 'icon': None, 'models': (
    #         'auth.group',
    #         {'model': 'auth.user', 'label': 'Staff'}
    #     )},
    #
    #     # Custom app, no models (child links)
    #     {'label': 'Users', 'url': 'auth.user', 'icon': 'icon-user'},
    #
    #     # Separator
    #     '-',
    #
    #     # Custom app and model with permissions
    #     {'label': 'Secure', 'permissions': 'auth.add_user', 'models': [
    #         {'label': 'custom-child',
    #          'permissions': ('auth.add_user', 'auth.add_group')}
    #     ]},
    # )
    'LIST_PER_PAGE': 20,
}
# %JFE+]
