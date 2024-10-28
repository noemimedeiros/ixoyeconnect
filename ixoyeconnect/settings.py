
import os
from pathlib import Path
import sys
import environ

env = environ.Env()
root_path = environ.Path(__file__) - 2

env.read_env(env_file=root_path(".env"))

BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("DJ_SECRET_KEY", default="")

DEBUG = True

ALLOWED_HOSTS = ['*']
CSRF_TRUSTED_ORIGINS = ["https://*.ngrok-free.app"]

sys.path.append(
    os.path.join(BASE_DIR, "apps")
)

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # Third party
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'crispy_forms',
    'crispy_bootstrap5',
    'django_ckeditor_5',
    'extra_views',
    'django_filters',
    'pwa_webpush',

    # Local,
    'core',
    'agenda',
    'contribuicao',
    'escala',
    'evento',
    'usuario',
    'posts',
    'notificacao',
    'relatorios'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "allauth.account.middleware.AccountMiddleware",
]

SITE_ID = 1

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend"
)

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env("EMAIL_HOST", default="")
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="")

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_LOGOUT_ON_GET = True
# ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_USERNAME_REQUIRED = False

SESSION_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = 'Lax'

ACCOUNT_FORMS = {
    'login': 'core.forms.MyLoginForm',
    'signup': 'core.forms.MySignUpForm',
    'change_password': 'core.forms.MyChangePasswordForm',
    'set_password': 'core.forms.MySetPasswordForm',
    'reset_password': 'core.forms.MyResetPasswordForm',
    'add_email': 'core.forms.MyAddEmailForm',
    'reset_password_from_key': 'core.forms.MyResetPasswordKeyForm'
}

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': '123',
            'secret': '456',
            'key': ''
        }
    }
}

LOGIN_URL = '/login/'

AUTH_USER_MODEL = "usuario.User" 

SILENCED_SYSTEM_CHECKS = ['models.W036']

ROOT_URLCONF = 'ixoyeconnect.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [root_path("templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                "django.template.context_processors.static",
                'django.contrib.messages.context_processors.messages',
            ],
            "libraries":{
                "icons_arquivos": "posts.filters",
                "file_ext": "posts.filters",
                "curtido": "posts.filters",
                "salvo": "posts.filters",
                "get_tipo_display": "contribuicao.filters",
                "evento_passado": "evento.filters",
                "icone_notificacao": "notificacao.filters",
                "get_atividade": "relatorios.filters",
                "instance_name": "core.filters",
                "culto_com_escalas": "relatorios.filters"
            }
        },
    },
]

WSGI_APPLICATION = 'ixoyeconnect.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

MYSQL_USER = env("MYSQL_USER", default="")
MYSQL_PASSWORD = env("MYSQL_PASSWORD", default="")
MYSQL_DATABASE = env("MYSQL_DATABASE", default="")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': MYSQL_DATABASE,
        'USER': MYSQL_USER,
        'PASSWORD': MYSQL_PASSWORD,
        'HOST': 'localhost',
        'PORT': '3306',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'pt-BR'
TIME_ZONE = "America/Recife"
USE_I18N = True
USE_TZ = True
USE_THOUSAND_SEPARATOR = True

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# -----------------------------------------------------------------------------
# Static & Media Files
# -----------------------------------------------------------------------------
STATIC_URL = env("DJ_STATIC_URL", default="/static/")
STATIC_ROOT = env("DJ_STATIC_ROOT", default=root_path("static"))
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

MEDIA_URL = env("DJ_MEDIA_URL", default="/media/")
MEDIA_ROOT = env("DJ_MEDIA_ROOT", default=root_path("media"))

# -----------------------------------------------------------------------------
# CRISPY
# -----------------------------------------------------------------------------
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# -----------------------------------------------------------------------------
# CKEDITOR
# -----------------------------------------------------------------------------
CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': {
            'items': [
                'undo',
                'redo',
                '|',
                'bold',
                'italic',
                'underline',
                'removeFormat',
                '|',
                'link',
                '|',
                'alignment',
                '|',
                'bulletedList',
                'numberedList'
            ],
            'shouldNotGroupWhenFull': False
        },
        'language': 'pt-br',
        'link': {
            'addTargetToExternalLinks': True,
            'defaultProtocol': 'https://',
            'decorators': {
                'toggleDownloadable': {
                    'mode': 'manual',
                    'label': 'Downloadable',
                    'attributes': {
                        'download': 'file'
                    }
                }
            }
        },
        'width': 'full',
        'removePlugins': ['WordCount', 'CharCount'],
    }
}
CKEDITOR_UPLOAD_PATH = 'uploads/'

# -----------------------------------------------------------------------------
# WEBPUSH
# -----------------------------------------------------------------------------
WEBPUSH_SETTINGS = {
   "VAPID_PUBLIC_KEY": env("VAPID_PUBLIC_KEY", default=""),
   "VAPID_PRIVATE_KEY": env("VAPID_PRIVATE_KEY", default=""),
   "VAPID_ADMIN_EMAIL": env("VAPID_ADMIN_EMAIL", default="")
}