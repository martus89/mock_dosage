from django.apps import AppConfig
from django.core.signals import setting_changed
from django.core.signals import request_finished


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        from . import signals
