"""Middleware personalizzati — config/middleware.py"""
import time
import logging

logger = logging.getLogger('apps')


class RequestTimingMiddleware:
    """Logga i tempi di risposta e aggiunge l'header X-Response-Time."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = time.monotonic()
        response = self.get_response(request)
        duration = time.monotonic() - start

        logger.debug(
            f"{request.method} {request.path} "
            f"— {duration * 1000:.1f}ms [{response.status_code}]"
        )
        response['X-Response-Time'] = f"{duration * 1000:.1f}ms"
        return response
