from django.apps import AppConfig


class EShopConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "e_shop"

    def ready(self):
        from e_shop import signals
