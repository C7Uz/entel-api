from pathlib import Path
from dotenv import load_dotenv
from datetime import timedelta
import os
from datetime import timedelta
load_dotenv()

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.celery import CeleryIntegration


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-lfxu#bttb1r5oyz4e3-_9zw9=5k2xb1de62b2qh9!j=jly4ksk'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(int(os.getenv('DEBUG', 0)))
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(',')
CSRF_TRUSTED_ORIGINS = os.getenv('CSRF_TRUSTED_ORIGINS').split(',')
CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS').split(',')

# Rest framework
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_PERMISSION_CLASSES': [
        #'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.AllowAny',  # ← Cambiar a AllowAny por defecto
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=1440),
    'REFRESH_TOKEN_LIFETIME': timedelta(minutes=1400)
}

CORS_ORIGIN_ALLOW_ALL = True

# Application definition
INSTALLED_APPS = [
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "unfold.contrib.import_export",
    "django.contrib.admin",
    
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django.contrib.postgres',

    # Modules
    'modules.users',
    'modules.content',

    # Packages
    'adminsortable2',
    'corsheaders',
    'ckeditor',
    'import_export'
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'csp.middleware.CSPMiddleware',
    'django_permissions_policy.PermissionsPolicyMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware'
]

ROOT_URLCONF = 'wapp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages'
            ],
        },
    },
]

WSGI_APPLICATION = 'wapp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': os.getenv('DATABASE_ENGINE'),
        'HOST': os.getenv('DATABASE_HOST'),
        'NAME': os.getenv('DATABASE_NAME'),
        'USER': os.getenv('DATABASE_USER'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD'),
        'PORT': os.getenv('DATABASE_PORT'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        'OPTIONS': {
            'max_similarity': 0.5,
            'user_attributes': ('username', 'first_name', 'last_name')
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 6,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    }
]
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend'
]

AUTH_USER_MODEL = 'users.User'

CKEDITOR_BASEPATH = "/static/ckeditor/ckeditor/"
CKEDITOR_UPLOAD_PATH = "/media/uploads/"
CKEDITOR_FILENAME_GENERATOR = 'utils.get_filename'
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'height': 200,
        'width': 700,
        'toolbar_Custom': [
            {'name': 'clipboard', 'items': ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo']},
            ['Bold', 'Italic', 'Underline'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            
        ]
    },
}

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'es-ES'

TIME_ZONE = 'America/Lima'

USE_I18N = True

USE_L10N = True

USE_TZ = True


CSP_DEFAULT_SRC = ("'self'", "'unsafe-inline'", "https://fonts.googleapis.com")
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'", "https://entel-cdn.s3.amazonaws.com", "https://fonts.googleapis.com")
CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'", "'unsafe-eval'", "www.google.com", "www.gstatic.com")
CSP_FRAME_SRC = ("'self'", "'unsafe-inline'", "'unsafe-eval'", "www.google.com", "www.gstatic.com")
CSP_FONT_SRC = ("'self'", "'unsafe-inline'", "'unsafe-eval'", "https://fonts.gstatic.com", "https://fonts.googleapis.com")
CSP_IMG_SRC = ("'self'", "'unsafe-inline'")

if not DEBUG:
    SESSION_COOKIE_AGE = 28800
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_HTTPONLY = True
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_NAME = '__Secure-sessionid'
    CSRF_COOKIE_NAME = '__Secure-csrftoken'

PERMISSIONS_POLICY = {
    "accelerometer": [],
    "ambient-light-sensor": [],
    "autoplay": ['self'],
    "camera": [],
    "display-capture": [],
    "document-domain": [],
    "encrypted-media": [],
    "fullscreen": ['self'],
    "geolocation": [],
    "gyroscope": [],
    "magnetometer": [],
    "microphone": [],
    "midi": [],
    "payment": [],
    "usb": [],
}

LOGIN_URL = '/admin/login/'
LOGIN_REDIRECT_URL = '/admin'
PASSWORD_RESET_TIMEOUT_DAYS = 2

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]
STATIC_ROOT = os.getenv('STATIC_ROOT')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_URL = "/static/"
MEDIA_URL = "/media/"

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_USE_TLS = True
EMAIL_PORT = os.getenv('EMAIL_PORT', 25)
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Sentry
if not DEBUG:
    sentry_sdk.init(
        dsn=os.getenv('SENTRY_DSN'),
        integrations=[DjangoIntegration(), CeleryIntegration()],
        send_default_pii=True
    )

API_DOMAIN = os.getenv('API_DOMAIN')
APP_DOMAIN_WEB = os.getenv('APP_DOMAIN_WEB')
JWT_ENCODE_KEY = os.getenv('JWT_ENCODE_KEY')


from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


UNFOLD = {
    "SITE_TITLE": "Entel",
    "SITE_HEADER":"Backoffice",
    "SITE_URL": "/",
    "SITE_ICON": lambda request: static("assets/logo-entel.png"),
    "SITE_SYMBOL": "speed",
    "LOGIN": {
        "image": lambda r: static("assets/login-entel.png"),
        "redirect_after": lambda r: reverse_lazy("admin:users_user_changelist"),
    },
    "STYLES": [
        lambda request: static("css/admin.css"),
    ],
    "SCRIPTS": [
        lambda request: static("js/script.js"),
    ],
    "COLORS": {
        "primary": {
            "50": "250 245 255",
            "100": "243 232 255",
            "200": "233 213 255",
            "300": "216 180 254",
            "400": "192 132 252",
            "500": "168 85 247",
            "600": "147 51 234",
            "700": "126 34 206",
            "800": "107 33 168",
            "900": "88 28 135",
        },
    },
    "EXTENSIONS": {
        "modeltranslation": {
            "flags": {
                "en": "🇬🇧",
                "fr": "🇫🇷",
                "nl": "🇧🇪",
            },
        },
    },
    "SIDEBAR": {
        "show_search": False,  # Search in applications and models names
        "show_all_applications": False,  # Dropdown with all applications and models
        "navigation": [
            {
                "title": _("Usuarios"),
                "separator": True,  # Top border
                "items": [
                    {
                        "title": _("Users"),
                        "icon": "people",
                        "link": reverse_lazy("admin:users_user_changelist"),
                    },
                    {
                        "title": _("Inscritos"),
                        "icon": "assignment_ind",
                        "link": reverse_lazy("admin:users_inscriptions_changelist"),
                    }
                    
                ],
            },
            {
                "title": _("Páginas"),
                "separator": True,  # Top border
                "items": [
                    
                    {
                        "title": _("Home"),
                        "icon": "edit_document",
                        "link": reverse_lazy("admin:content_home_changelist"),
                    },
                    {
                        "title": _("P. gracias"),
                        "icon": "folded_hands",
                        "link": reverse_lazy("admin:content_page_changelist"),
                    },
                ],
            },
            {
                "title": _("Eventos"),
                "separator": True,  # Top border
                "items": [
                    {
                        "title": _("Eventos"),
                        "icon": "event",
                        "link": reverse_lazy("admin:content_event_changelist"),
                    },
                    {
                        "title": _("Expositores"),
                        "icon": "record_voice_over",
                        "link": reverse_lazy("admin:content_teacher_changelist"),
                    },
                    {
                        "title": _("Topicos"),
                        "icon": "topic",
                        "link": reverse_lazy("admin:content_topic_changelist"),
                    }
                ],
            },
            {
                "title": _("Configuración"),
                "separator": True,  # Top border
                "items": [
                    {
                        "title": _("Redes sociales"),
                        "icon": "public",
                        "link": reverse_lazy("admin:content_socialnetwork_changelist"),
                    },
                    {
                        "title": _("Países"),
                        "icon": "flag",
                        "link": reverse_lazy("admin:content_country_changelist"),
                    }
                ],
            },
            
            
        ],
    },
    "TABS": [
        {
            "models": [
                "users.user_in_lowercase",
            ],
            "items": [
                {
                    "title": _("Usuarios"),
                    "link": "#",
                },
            ],
        },
    ],
}
# Asegurar que reverse_lazy funcione (si usas la navegación personalizada)
from django.urls import reverse_lazy
from django.templatetags.static import static