from django.apps import AppConfig


class PartnersConfig(AppConfig):
    name = 'rotv_apps.partners'

    def ready(self):
        from . import signals
