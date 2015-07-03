# coding=utf-8
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
    # %JFE+2
    'companies101rdb',
    ''
    # %JFE+5 added demos
    'demo_scrapy',
    'demo_django_guardian',
    'demo_djangosuit',
    'demo_django_fsm_admin',
    'demo_django_taggit',
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
    # %JFE+1 added to enable django' admindocs optional app
    'django.contrib.admindocs',
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
    # %JFE+1 added for django-fsm-log
    'django_fsm_log',
    # %JFE+1 added for django-extensions
    'django_extensions',
    # %JFE+1 added for django_filters, required by rest_framework
    'django_filters',
    # %JFE+1 added for rest_framework
    'rest_framework',
    # %JFE+1 added for rest_framework_swagger
    'rest_framework_swagger',
    # %JFE+1 added for django-guardian, could be used with rest_framework
    'guardian',
    # %JFE+1 added for django-explorer
    'explorer',
    # %JFE+1 added for django-taggit
    'taggit',
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

# %JFE+[ example of usage of rest_framework.
# see http://www.django-rest-framework.org/#example
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}
# %JFE+]


# %JFE+[ example of usage of rest_framework.
# see http://django-guardian.readthedocs.org/en/v1.2/configuration.html
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',  # this is default
    'guardian.backends.ObjectPermissionBackend',
)

ANONYMOUS_USER_ID = -1
# %JFE+]

# %JFE+1 added so that all sql tables (including auth, etc) are visible
EXPLORER_SCHEMA_EXCLUDE_APPS = ()

# %JFE+[ added to make it possible to use custom ''
# see
import django.db.models.options as options
options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('computed_fields',)
# %JFE+]


# %JFE+[ suppress some warnings
# see http://stackoverflow.com/questions/28424420/cant-silence-warnings-that-django-cms-produces
WARNINGS_TO_IGNORE = {
    'RemovedInDjango18Warning: `SuitAdminUser.queryset` '
         'method should be renamed `get_queryset`.',

}

def filter_some_warnings(record):
    for warning in WARNINGS_TO_IGNORE:
        # print '***', record.args[0]
        # print '   ', ignored in record.args[0]
        if warning in record.args[0]:
            return False
    return True


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'filters': {
        'ignore_some_warnings': {
            '()': 'django.utils.log.CallbackFilter',
            'callback': filter_some_warnings,
        },
    },
    'loggers': {
        'py.warnings': {
            'handlers': ['console', ],
            'filters': ['ignore_some_warnings', ],
        }
    },
}
# %JFE+]
