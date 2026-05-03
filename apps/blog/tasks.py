"""Task Celery blog — apps/blog/tasks.py"""
import logging
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger('apps.blog')


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_post_notification(self, post_id):
    """Invia notifica email agli iscritti quando un post viene pubblicato."""
    try:
        from .models import Post
        from django.contrib.auth import get_user_model
        User = get_user_model()

        post = Post.objects.get(pk=post_id)
        subscribers = User.objects.filter(
            subscribe_newsletter=True,
            is_active=True,
        ).values_list('email', flat=True)

        if subscribers:
            send_mail(
                subject=f'Nuovo post: {post.title}',
                message=post.excerpt or post.body[:200],
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=list(subscribers),
                fail_silently=False,
            )
            logger.info(f'Notifica inviata per post #{post_id} a {len(subscribers)} utenti')

    except Exception as exc:
        logger.error(f'Errore invio notifica post #{post_id}: {exc}')
        raise self.retry(exc=exc)
