from config.settings.base import *
# from .base import env

# DEBUG = env.bool("DJANGO_DEBUG", default=True)

# SECRET_KEY = env.str("DJANGO_SECRET_KEY")
# ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS")
# CSRF_TRUSTED_ORIGINS = env.list("DJANGO_CSRF_TRUSTED_ORIGINS")
# SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# CSRF_COOKIE_SECURE = True

# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": env.str("DJANGO_REDIS_URL"),
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#         },
#     }
# }

# # LOGGING
# # ------------------------------------------------------------------------------
# # https://docs.djangoproject.com/en/dev/ref/settings/#logging
# # See https://docs.djangoproject.com/en/dev/topics/logging for
# # more details on how to customize your logging configuration.
# LOGGING = {
#     "version": 1,
#     "disable_existing_loggers": False,
#     "filters": {
#         "require_debug_true": {
#             "()": "django.utils.log.RequireDebugTrue",
#         },
#     },
#     "formatters": {
#         "verbose": {
#             "format": "{name} {levelname} {asctime} {module} {process:d} {thread:d} {message}",
#             "style": "{",
#         },
#     },
#     "handlers": {
#         "console": {
#             "class": "logging.StreamHandler",
#             "level": "INFO",
#         },
#         "error": {
#             "class": "logging.FileHandler",
#             "filename": "/var/log/inter_hm/error.log",
#             "formatter": "verbose",
#             "level": "ERROR",
#         },
#         "info": {
#             "class": "logging.FileHandler",
#             "filename": "/var/log/inter_hm/info.log",
#             "formatter": "verbose",
#             "level": "INFO",
#         },
#     },
# }

# if SENTRY_DSN := env.str("DJANGO_SENTRY_DSN", None):
#     import sentry_sdk
#     from sentry_sdk.integrations.django import DjangoIntegration

#     sentry_sdk.init(
#         dsn=SENTRY_DSN,
#         integrations=[
#             DjangoIntegration(),
#         ],
#         # Set traces_sample_rate to 1.0 to capture 100%
#         # of transactions for performance monitoring.
#         # We recommend adjusting this value in production.
#         traces_sample_rate=1.0,
#         # If you wish to associate users to errors (assuming you are using
#         # django.contrib.auth) you may enable sending PII data.
#         send_default_pii=True,
#     )
