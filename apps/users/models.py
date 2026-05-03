"""Modello utente personalizzato — apps/users/models.py"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Utente personalizzato con email come campo di login.
    Da impostare PRIMA della prima migrazione (AUTH_USER_MODEL).
    """
    email = models.EmailField(unique=True)
    bio   = models.TextField(blank=True, verbose_name='Biografia')
    avatar = models.ImageField(
        upload_to='avatars/%Y/%m/',
        blank=True,
        verbose_name='Avatar',
    )
    is_verified = models.BooleanField(default=False, verbose_name='Email verificata')
    subscribe_newsletter = models.BooleanField(
        default=False, verbose_name='Iscritto alla newsletter'
    )

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name        = 'Utente'
        verbose_name_plural = 'Utenti'

    def __str__(self):
        return self.email

    def get_full_name(self):
        full = f"{self.first_name} {self.last_name}".strip()
        return full or self.username
