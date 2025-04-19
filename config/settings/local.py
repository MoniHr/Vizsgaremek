from .base import *
# from .base import env

# DEBUG = True

# # django-debug-toolbar
# # ------------------------------------------------------------------------------
# # https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#prerequisites
# INSTALLED_APPS += [
#     "debug_toolbar",
#     "django_extensions",
# ]
# # https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#middleware
# MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
# # https://django-debug-toolbar.readthedocs.io/en/latest/configuration.html#debug-toolbar-config
# DEBUG_TOOLBAR_CONFIG = {
#     "DISABLE_PANELS": ["debug_toolbar.panels.redirects.RedirectsPanel"],
#     "SHOW_TEMPLATE_CONTEXT": True,
# }
# ALLOWED_HOSTS = ["*"]
# # https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#internal-ips
# INTERNAL_IPS = ["127.0.0.1"]
# if env.bool("DJANGO_USE_DOCKER", default=False):
#     import socket

#     hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
#     INTERNAL_IPS += [".".join(ip.split(".")[:-1] + ["1"]) for ip in ips]

# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": env.str("DJANGO_REDIS_URL", "redis://redis:6379/0"),
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#         },
#     }
# }

# EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
