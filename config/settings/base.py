import os
from pathlib import Path
import environ
# ------------------------------------------------------------------------------
# ✅ Environment setup
# ------------------------------------------------------------------------------
env = environ.Env()

BASE_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = BASE_DIR.parent

# Load .env file if needed
READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=False)
if READ_DOT_ENV_FILE:
    env.read_env(str(ROOT_DIR / ".env"))

# ------------------------------------------------------------------------------
# ✅ Security Settings
# ------------------------------------------------------------------------------
SECRET_KEY = env.str("DJANGO_SECRET_KEY", default="django-insecure-sxv&8&(sax(v2nv&ohq3g0p@6*s@a0!b7(l@^1*+k3lte^_ix)")

DEFAULT_CHARSET = "utf-8"

ROOT_URLCONF = "config.urls"

DEBUG = env.bool("DJANGO_DEBUG", default=True)



# ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["localhost", "127.0.0.1", "0.0.0.0"])

ALLOWED_HOSTS = ["*"]

# ------------------------------------------------------------------------------
# ✅ Installed Apps
# ------------------------------------------------------------------------------
INSTALLED_APPS = [
    # Core Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "django.contrib.postgres",

    # Custom apps
    "apps.core",
    "apps.accounts",
    "apps.profile",
    "apps.job_post",
    "apps.pages",
    "apps.search",
    "apps.chat",

    # Third-party apps
    "crispy_forms",
    "crispy_bootstrap5",
    "django_filters",
    "email_log",
    "modeltranslation",
    "django_cleanup",
    "django_celery_results",
    "import_export",
]

# ------------------------------------------------------------------------------
# ✅ Middleware Configuration
# ------------------------------------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ------------------------------------------------------------------------------
# ✅ Authentication & Authorization
# ------------------------------------------------------------------------------
AUTH_USER_MODEL = "accounts.User"

LOGIN_REDIRECT_URL = "edit_profile"
LOGOUT_REDIRECT_URL = "login"
LOGIN_URL = "login"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

# ------------------------------------------------------------------------------
# ✅ Database Configuration
# ------------------------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": env.str("POSTGRES_DB"),
        "USER": env.str("POSTGRES_USER"),
        "PASSWORD": env.str("POSTGRES_PASSWORD"),
        "HOST": env.str("POSTGRES_HOST", default="postgres"),
        "PORT": env.int("POSTGRES_PORT", default=5432),
    }
}


CELERY_BROKER_URL = 'redis://redis:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_RESULT_BACKEND = 'django-db'

# ------------------------------------------------------------------------------
# ✅ Templating Configuration
# ------------------------------------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "apps.chat.context_processors.unread_messages_count",
                "apps.job_post.context_processors.unread_applications_count",
                "apps.job_post.context_processors.active_job_posts_count",
            ],
        },
    },
]

# ------------------------------------------------------------------------------
# ✅ Internationalization & Localization
# ------------------------------------------------------------------------------
LANGUAGE_CODE = env.str("DJANGO_DEFAULT_LANGUAGE", default="en-us")
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

CSRF_TRUSTED_ORIGINS = ["https://interhrm.com", "https://www.interhrm.com"]


LANGUAGES = [
    ('en', 'English'),
    ('hu', 'Hungary'),
]

MODELTRANSLATION_LANGUAGES = ("en", "hu")
MODELTRANSLATION_DEFAULT_LANGUAGE = "hu"
MODELTRANSLATION_FALLBACK_LANGUAGES = ('hu', 'en')
LOCALE_PATHS = [os.path.join(ROOT_DIR, "translations")]

# ------------------------------------------------------------------------------
# ✅ Static & Media Files
# ------------------------------------------------------------------------------
STATIC_URL = "static/"
STATIC_ROOT = os.path.join(ROOT_DIR, "static")

MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(ROOT_DIR, "media")

STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

# ------------------------------------------------------------------------------
# ✅ Email Configuration
# ------------------------------------------------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_USE_TLS = env.bool("DJANGO_EMAIL_USE_TLS", default=True)
EMAIL_HOST = env.str("DJANGO_EMAIL_HOST")
EMAIL_PORT = env.int("DJANGO_EMAIL_PORT", default=587)
EMAIL_HOST_USER = env.str("DJANGO_EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env.str("DJANGO_EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = env.str("DEFAULT_FROM_EMAIL")

# ------------------------------------------------------------------------------
# ✅ Payment - Stripe
# ------------------------------------------------------------------------------

# Keys from environment
STRIPE_TEST_SECRET_KEY = env.str("STRIPE_TEST_SECRET_KEY", default=None)
STRIPE_LIVE_SECRET_KEY = env.str("STRIPE_LIVE_SECRET_KEY", default=None)
STRIPE_PUBLIC_KEY = env.str("STRIPE_PUBLIC_KEY", default=None)
STRIPE_WEBHOOK_SECRET = env.str("STRIPE_WEBHOOK_SECRET", default=None)

# Mode switch
STRIPE_LIVE_MODE = env.bool("STRIPE_LIVE_MODE", default=False)

# Active key selection based on mode
STRIPE_SECRET_KEY = STRIPE_LIVE_SECRET_KEY if STRIPE_LIVE_MODE else STRIPE_TEST_SECRET_KEY


# ------------------------------------------------------------------------------
# ✅ Django Debug Toolbar (only for development)
# ------------------------------------------------------------------------------
if DEBUG:
    INSTALLED_APPS += [
        "debug_toolbar",
        "django_extensions",
    ]
    MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

    DEBUG_TOOLBAR_CONFIG = {
        "DISABLE_PANELS": ["debug_toolbar.panels.redirects.RedirectsPanel"],
        "SHOW_TEMPLATE_CONTEXT": True,
    }

    INTERNAL_IPS = ["127.0.0.1"]
    if env.bool("DJANGO_USE_DOCKER", default=False):
        import socket

        hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
        INTERNAL_IPS += [".".join(ip.split(".")[:-1] + ["1"]) for ip in ips]

# ------------------------------------------------------------------------------
# ✅ Miscellaneous
# ------------------------------------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

APPEND_TRAILING_SLASH = True


WEBSOCKET_SERVER_URL = os.getenv("WEBSOCKET_SERVER_URL", "http://localhost:3001")
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

CHAT_BASE_URL = "/chat/"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "apps": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}
