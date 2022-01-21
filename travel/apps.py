from django.apps import AppConfig


class PermitConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'travel'
    verbose_name = "Travel Models"

    def ready(self):
        import travel.signals
