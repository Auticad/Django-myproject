"""ASGI config con Django Channels — config/asgi.py"""
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Nota: decommentare quando si installa channels
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
# import apps.chat.routing
#
# application = ProtocolTypeRouter({
#     'http': get_asgi_application(),
#     'websocket': AuthMiddlewareStack(
#         URLRouter(apps.chat.routing.websocket_urlpatterns)
#     ),
# })

application = get_asgi_application()
