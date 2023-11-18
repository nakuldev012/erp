from django.apps import AppConfig
from django.conf import settings

class ProfileConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "employee.profile"

    def ready(self):
        import employee.profile.signals
 