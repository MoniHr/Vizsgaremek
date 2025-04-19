from django.apps import AppConfig


class ImportConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.core"

    def ready(self):
        import apps.profile.translation
