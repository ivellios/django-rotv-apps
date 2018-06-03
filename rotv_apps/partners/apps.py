# coding: utf-8
from django.apps import AppConfig


class PartnersConfig(AppConfig):
    name = 'rotv_apps.partners'
    verbose_name = u'Współpraca'

    def ready(self):
        from . import signals
