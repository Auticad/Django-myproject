"""Signal utenti — apps/users/signals.py"""
import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

logger = logging.getLogger('apps.users')


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def log_new_user(sender, instance, created, **kwargs):
    if created:
        logger.info(f"Nuovo utente registrato: {instance.email}")
