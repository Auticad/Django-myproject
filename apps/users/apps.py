"""Configurazione app users — apps/users/apps.py"""
from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name               = 'apps.users'
    verbose_name       = 'Utenti'

    def ready(self):
        import apps.users.signals  # noqa: F401
